import json
from index import lambda_handler

def test_successful_update():
    event = {
        'body': json.dumps({'id': '123', 'Weather': 'Sunny'})
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200

def test_missing_attributes():
    event = {
        'body': json.dumps({'Weather': 'Sunny'})
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400

def test_additional_attributes():
    event = {
        'body': json.dumps({'id': '123', 'Weather': 'Sunny', 'Temperature': '25C'})
    }
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400
