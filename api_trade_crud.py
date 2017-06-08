from __future__ import print_function
import json
import boto3
from botocore.exceptions import ClientError
from shifty_utils import *

def lambda_handler(event, context):
    print("Received api request: " + json.dumps(event, indent=2))

    operations = {
        
    }
    operation = event['httpMethod']
    params = event['queryStringParameters']