'''
This file is for implementing API response method and database helper methods.
'''
from __future__ import print_function # Python 2/3 compatibility
import json
import boto3
from botocore.exceptions import ClientError

dynamo = boto3.resource('dynamodb')

def respond(err, res=None):
    return {
        'statusCode': 400 if err else 200,
        'body': json.dumps(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def get_user(user):
    try:
        table = dynamo.Table(user['company'] + '_users')
        response = table.get_item(
            Key={
                'userId': user['userId'],
                'position': user['position']
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'message': e.response['Error']['Message']}
    else:
        return response

def create(item, table):
    try:
        table = dynamo.Table(item['company'] + '_users')
        response = table.put_item(
            Item=item,
            ReturnValues='ALL_OLD'
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'message': e.response['Error']['Message']}
    else:
        return response

def update_shift(shift):
    try:
        table = dynamo.Table(shift['company'] + '_shifts')
        response = table.update_item(
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
        table = dynamo.Table(shift['company'] + '_shifts')
        response = table.delete_item(
            Key={
                'id': shift['id'],
                'role': shift['role']
            },
            ReturnValues='ALL_OLD'
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'message': e.response['Error']['Message']}
    else:
        return response

def get_shifts_by_day(company, day):
    try:
        table = dynamo.Table(company + '_shifts')
        response = table.scan(
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
        table = dynamo.Table(company + '_shifts')
        response = table.scan(
            ConsistentRead=True
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'message': e.response['Error']['Message']}
    else:
        return response

def get_all_trades(company):
    try:
        table = dynamo.Table(company + '_shifts')
        response = table.scan(
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
        table = dynamo.Table(company + '_shifts')
        response = table.scan(
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
