from __future__ import print_function
import json
import boto3
import jwt
from bcrypt import checkpw
from botocore.exceptions import ClientError

print('Loading function')
dynamo = boto3.client('dynamodb')
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    print("Received login attempt: " + json.dumps(event, indent=2))

    operation = event['httpMethod']
    if operation == 'POST':
        payload = json.loads(event['body'])
        table = dynamo.Table(payload.company + '_users')

        try:
            response = table.get_item(
                Key={
                    'userId': payload.userId,
                    'company': payload.company
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            return respond({'message': e.response['Error']['Message']})
        else:
            user = response['Item']
            if checkpw(payload.password, user.password):
                jwt_payload = {
                    'user_id': user.userId,
                    'company': user.company
                }
                jwt_token = jwt.encode(jwt_payload, JWT_SECRET, JWT_ALGORITHM)
                return respond(None, {
                    'token': jwt_token.decode(),
                    'data': json.dumps(user)
                    })

            else:
                print("Credentials could not be verified:" + json.dumps(user, indent=2))
                return respond({'message': 'Invalid credentials'})
                