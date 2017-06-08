'''
This file is for implementing API response method and database helper methods.
'''
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
from botocore.exceptions import ClientError

dynamo = boto3.client('dynamodb')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err['message'] if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def get_user(user):
    try:
        response = dynamo.get_item(
            TableName=user['company'] + '_users',
            Key={
                'userId': user['userId'],
                'position': user['posittion']
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'message': e.response['Error']['Message']}
    else:
        return response

def create(item, table):
    try:
        response = dynamo.put_item(
            TableName=item['company'] + '_' + table,
            Item=item
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'message': e.response['Error']['Message']}
    else:
        return response

def update_shift(shift):
    try:
        response = dynamo.update_item(
            TableName=shift['company'] + '_shifts',
            Key={
                'id': shift['id'],
                'role': shift['role']
            },
            ReturnValues="ALL_NEW"
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'message': e.response['Error']['Message']}
    else:
        return response

def delete_shift(shift):
    try:
        response = dynamo.delete_item(
            TableName=shift['company'] + '_shifts',
            Key={
                'id': shift['id'],
                'role': shift['role']
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'message': e.response['Error']['Message']}
    else:
        return response

def get_shifts_by_day(company, day):
    try:
        response = dynamo.scan(
            TableName=company + '_shifts',
            FilterExpression="day = :val",
            ExpressionAttributeValue={
                ":val": day
            },
            ConsistentRead=True
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'message': e.response['Error']['Message']}
    else:
        return response

def get_all_shifts(company):
    try:
        response = dynamo.scan(
            TableName=company + '_shifts',
            ConsistentRead=True
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'message': e.response['Error']['Message']}
    else:
        return response

def get_all_trades(company):
    try:
        response = dynamo.scan(
            TableName=company + '_shifts',
            FilterExpression="tradeable = :val",
            ExpressionAttributeValue={
                ":val": True
            },
            ConsistentRead=True
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'message': e.response['Error']['Message']}
    else:
        return response

def get_trades_by_day(company, day):
    try:
        response = dynamo.scan(
            TableName=company + '_shifts',
            FilterExpression="day = :day, tradeable = :t",
            ExpressionAttributeValue={
                ":day": day,
                ":t": True
            },
            ConsistentRead=True
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'message': e.response['Error']['Message']}
    else:
        return response