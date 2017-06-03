from __future__ import print_function
import json
import boto3
import jwt
from passlib.hash import pbkdf2_sha256
from botocore.exceptions import ClientError

print('Loading function')
dynamo = boto3.client('dynamodb')
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err['message'] if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    print("Received login attempt: " + json.dumps(event, indent=2))

    payload = event['body']

    try:
        response = dynamo.get_item(
            TableName=payload['company'] + '_users',
            Key={
                'userId': payload['userId'],
                'position': payload['posittion']
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return respond({'message': e.response['Error']['Message']})
    else:
        user = response['Item']
        if pbkdf2_sha256.verify(payload['password'], user['password']):
            jwt_payload = {
                'userId': user['userId'],
                'position': user['position']
            }
            jwt_token = jwt.encode(jwt_payload, JWT_SECRET, JWT_ALGORITHM)
            return respond(None, {
                'token': jwt_token.decode(),
                'data': user
                })
        else:
            print("Credentials could not be verified:" + json.dumps(user, indent=2))
            return respond({'message': 'Invalid credentials'})
                