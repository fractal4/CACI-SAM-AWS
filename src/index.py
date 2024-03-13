# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import json

dynamodb_client = boto3.client('dynamodb')

# basic functions for authorizer from the AWS documentation
def generatePolicy(principalId, effect, resource):
    authResponse = {}
    authResponse['principalId'] = principalId
    if (effect and resource):
        policyDocument = {}
        policyDocument['Version'] = '2012-10-17'
        policyDocument['Statement'] = []
        statementOne = {}
        statementOne['Action'] = 'execute-api:Invoke'
        statementOne['Effect'] = effect
        statementOne['Resource'] = resource
        policyDocument['Statement'] = [statementOne]
        authResponse['policyDocument'] = policyDocument
    authResponse['context'] = {
        "stringKey": "stringval",
        "numberKey": 123,
        "booleanKey": True
    }
    authResponse_JSON = json.dumps(authResponse)
    return authResponse_JSON


def lambda_handler(event, context):
    print(event)
    token = event.get('headers')
    # to get token data from the request headers and body and checking the token value
    token = token['Authorization']
    if token == 'allowme':
        print('authorized')
        # response = generatePolicy('user', 'Allow', "event['methodArn']")
    elif token == 'deny':
        print('unauthorized')
        response = generatePolicy('user', 'Deny', "event['methodArn']")
        return json.loads(response)
    elif token == 'unauthorized':
        print('unauthorized')
        raise Exception('Unauthorized')  # Return a 401 Unauthorized response
        return 'unauthorized'
    else:
        raise Exception('Unauthorized')  # Return a 401 Unauthorized response
        return 'unauthorized'
    try:
        pass
    except BaseException:
        print('unauthorized')
        return 'unauthorized'  # Return a 500 error

    event_body = event.get('body')
    event_body = json.loads(event_body)
    
    #checking whether the body has only the required fields or not
    if len(event_body) != 2 or set(event_body.keys()) != {'id', 'weather'}:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Only "id" and "weather" attributes are allowed.')
        }
    event_id = event_body.get("id")
    event_weather = event_body.get("weather")
    
    dynamodb_client.put_item(TableName='WeatherData', Item={'id': {'S': event_id}, 'Weather': {'S': event_weather}})
    return {
      'statusCode': 200,
      'body': 'Successfully inserted data!'
    }
