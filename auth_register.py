from __future__ import print_function
import json
import boto3
import jwt
from passlib.hash import pbkdf2_sha256
from botocore.exceptions import ClientError
from shifty_utils import respond, create

print('Loading function')
dynamo = boto3.resource('dynamodb')
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

def create_tables(company):
    try:
        dynamo.create_table(
            TableName=company + '_shifts',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'role',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'role',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])

    try:
        users = dynamo.create_table(
            TableName=company + '_users',
            KeySchema=[
                {
                    'AttributeName': 'userId',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'position',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'userId',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'position',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return dynamo.Table(company + '_users')
    else:
        return users

def lambda_handler(event, context):
    print("Received registration attempt: " + json.dumps(event, indent=2))

    payload = event['body']
    payload['password'] = pbkdf2_sha256.hash(payload['password'])
    table = create_tables(payload['company'])
    table.meta.client.get_waiter('table_exists').wait(TableName=payload['company'] + '_users')

    response = create(payload, 'users')
    if 'Attributes' in response:
        jwt_payload = {
            'userId':payload['userId'],
            'position': payload['position']
        }
        jwt_token = jwt.encode(jwt_payload, JWT_SECRET, JWT_ALGORITHM)
        print("Registration succeeded: " + json.dumps(response, indent=2))
        return respond(None, {
            'token': jwt_token.decode(),
            'data': payload
            })
    else:
        return respond(response)
        