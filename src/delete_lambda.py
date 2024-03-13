import json
import boto3
from index import lambda_handler

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WeatherData')

def delete_record(event, context):
    # Extract id from request body
    #to fetch body from api gateway request and format using  json loads
    body = json.loads(event['body'])
    id = body.get('id')

    # Validation for missing id
    if not id:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: "id" must be provided in the request body.')
        }

    # Delete record from DynamoDB
    try:
        response = table.delete_item(
            Key={
                'id': id
            }
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error: Failed to delete record from DynamoDB.')
        }


    # Perform deletion operation here

    return {
        'statusCode': 200,
        'body': json.dumps('Delete successful')
    }
