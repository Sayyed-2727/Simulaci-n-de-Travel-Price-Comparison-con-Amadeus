import boto3
import os
from amadeus import Client

def lambda_handler(event, context):
    # Inicializar servicios
    amadeus = Client(
        client_id=os.environ['AMADEUS_API_KEY'],
        client_secret=os.environ['AMADEUS_API_SECRET']
    )
    dynamodb = boto3.resource('dynamodb')
    sns = boto3.client('sns')
    table = dynamodb.Table('TravelAlerts')

    # 1. Buscar alertas activas
    response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('active').eq(True))
    
    for item in response['Items']:
        # 2. Consultar precio actual
        flights = amadeus.shopping.flight_offers_search.get(
            originLocationCode=item['origin'],
            destinationLocationCode=item['destination'],
            departureDate=item['date'],
            adults=1
        ).data

        if not flights: continue
        
        new_price = float(flights[0]['price']['total'])
        
        # 3. Comparar y notificar
        if new_price < float(item['current_price']):
            mensaje = f"¡BAJA DE PRECIO! De {item['origin']} a {item['destination']} por {new_price} (Antes: {item['current_price']})"
            
            sns.publish(
                TopicArn=os.environ['SNS_TOPIC_ARN'],
                Message=mensaje,
                Subject="Alerta de Vuelo"
            )
            
            # Desactivar para no repetir el correo
            table.update_item(
                Key={'alert_id': item['alert_id']},
                UpdateExpression="set active = :f",
                ExpressionAttributeValues={':f': False}
            )

    return {"status": "processed"}