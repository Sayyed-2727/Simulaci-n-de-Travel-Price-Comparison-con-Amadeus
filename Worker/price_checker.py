import boto3
import time
import os
from decimal import Decimal

# Configuración de Clientes
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('TravelAlerts')
sns_client = boto3.client('sns', region_name='us-east-1')

def check_prices():
    print("Iniciando revisión de precios...")
    # 1. Escanear alertas activas en DynamoDB
    response = table.scan()
    items = response.get('Items', [])

    for alert in items:
        # 2. Aquí llamarías a tu lógica de AmadeusService
        # precio_actual = amadeus_service.get_price(alert['origin'], alert['destination'])
        precio_actual = 100.0  # Ejemplo
        
        precio_guardado = float(alert['current_price'])

        if precio_actual < precio_guardado:
            print(f"¡BAJADA DE PRECIO para {alert['email']}!")
            # 3. Enviar notificación por SNS
            sns_client.publish(
                TopicArn=os.getenv('SNS_TOPIC_ARN'),
                Message=f"El vuelo de {alert['origin']} a {alert['destination']} ha bajado a {precio_actual}",
                Subject="¡Alerta de Precio Amadeus!"
            )

if __name__ == "__main__":
    while True:
        check_prices()
        time.sleep(3600)  # Revisa cada hora