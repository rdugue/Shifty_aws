from __future__ import print_function
from datetime import datetime, timedelta
import json
import jwt
from passlib.hash import pbkdf2_sha256
from shifty_utils import respond, get_user

print('Loading function')
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 60*60*24*2

def lambda_handler(event, context):
    print("Received login attempt: " + json.dumps(event, indent=2))
    if event['body']:
        payload = json.loads(event['body'])
    else:
        return respond({'error': 'no POST body'})
    response = get_user(payload)
    if 'Item' in response:
        user = response['Item']
        if pbkdf2_sha256.verify(payload['password'], user['password']):
            jwt_payload = {
                'userId': user['userId'],
                'position': user['position'],
                'company': user['company'],
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(jwt_payload, JWT_SECRET, JWT_ALGORITHM)
            return respond(None, {
                'token': jwt_token.decode(),
                'data': user
                })
        else:
            print("Credentials could not be verified:" + json.dumps(user, indent=2))
            return respond({'error': 'Invalid credentials'})
    else:
        return respond(response)
