from __future__ import print_function
from datetime import datetime, timedelta
import json
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
JWT_EXP_DELTA_SECONDS = 60*60*24*2

def create_tables():
    try:
        dynamo.create_table(
            TableName='shifts',
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
            TableName='users',
            KeySchema=[
                {
                    'AttributeName': 'userId',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'userId',
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
        return dynamo.Table('users')
    else:
        return users

def lambda_handler(event, context):
    print("Received registration attempt: " + json.dumps(event, indent=2))

    payload = json.loads(event['body'])
    user = payload
    user['password'] = pbkdf2_sha256.hash(user['password'])
    table = create_tables()
    table.meta.client.get_waiter('table_exists').wait(TableName='users')

    response = create(user, 'users')
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        jwt_payload = {
            'userId': user['userId'],
            'position': user['position'],
            'company': user['company'],
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }
        jwt_token = jwt.encode(jwt_payload, JWT_SECRET, JWT_ALGORITHM)
        print("Registration succeeded: " + json.dumps(response, indent=2))
        return respond(None, {
            'token': jwt_token.decode(),
            'data': user
            })
    else:
        print("Registration failed: " + json.dumps(response, indent=2))
        return respond(response)
        