from __future__ import print_function
import json
from shifty_utils import respond, update_shift, get_all_trades, get_trades_by_day

def lambda_handler(event, context):
    print("Received api request: " + json.dumps(event, indent=2))

    operations = {
        'DELETE': update_shift,
        'POST': update_shift,
        'GET': get_all_trades,
        'GET_DAY': get_trades_by_day
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
        