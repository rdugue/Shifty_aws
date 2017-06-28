from __future__ import print_function
import json
from shifty_utils import delete_shift, update_shift, get_all_shifts, get_shifts_by_day
from shifty_utils import get_all_trades, get_trades_by_day, respond

def lambda_handler(event, context):
    print("Received api request: " + json.dumps(event, indent=2))

    path = event['path']
    operations = {
        'DELETE': delete_shift,
        'PUT': update_shift,
        'GET': get_all_shifts if path == '/api/shifts' else get_all_trades,
        'GET_DAY': get_shifts_by_day if path == '/api/shifts' else get_trades_by_day
    }
    payload = json.loads(event['body'])
    operation = event['httpMethod']

    if operation in operations:
        if operation == 'GET':
            params = event['queryStringParameters']
            if 'day' in params:
                response = operations['GET_DAY'](params['company'], params['day'])
            else:
                response = operations[operation](params['company'])
            if 'error' in response:
                return respond(response)
            else:
                return respond(None, {'data': response['Items']})
        else:
            if payload:
                response = operations[operation](payload)
                if 'error' in response:
                    return respond(response)
                else:
                    return respond(None, {'data': response['Attributes']})
            else:
                return respond({'error': 'No request body'})
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
