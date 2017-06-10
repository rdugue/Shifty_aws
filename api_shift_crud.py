from __future__ import print_function
import json
from shifty_utils import delete_shift, update_shift
from shifty_utils import get_all_shifts, get_shifts_by_day, respond

def lambda_handler(event, context):
    print("Received api request: " + json.dumps(event, indent=2))

    operations = {
        'DELETE': delete_shift,
        'PUT': update_shift,
        'GET': get_all_shifts,
        'GET_DAY': get_shifts_by_day
    }
    operation = event['httpMethod']

    if operation in operations:
        if operation == 'GET':
            params = event['queryStringParameters']
            if 'day' in params:
                response = operations['GET_DAY'](params['company'], params['day'])
            else:
                response = operations[operation](params['company'])
            if 'Items' in response:
                return respond(None, {'data': response['Items']})
            else:
                return respond(response)
        else:
            if 'body' in event:
                response = operations[operation](event['body'])
                if 'Item' in response:
                    return respond(None, {'data': response['Item']})
                else:
                    return respond(response)
            else:
                return respond({'message': 'No request body'})
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
