import boto3

def setup_resources():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    sns = boto3.client('sns', region_name='us-east-1')

    # 1. Crear Tabla DynamoDB
    try:
        table = dynamodb.create_table(
            TableName='TravelAlerts',
            KeySchema=[{'AttributeName': 'alert_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'alert_id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Creando tabla DynamoDB...")
        table.wait_until_exists()
    except Exception as e:
        print(f"La tabla ya existe o error: {e}")

    # 2. Crear Tópico SNS
    topic = sns.create_topic(Name='TravelPriceTopic')
    print(f"Tópico SNS creado: {topic['TopicArn']}")

if __name__ == "__main__":
    setup_resources()