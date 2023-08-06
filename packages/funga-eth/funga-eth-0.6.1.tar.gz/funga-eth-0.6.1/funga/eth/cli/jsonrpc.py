# local imports
from funga.error import UnknownAccountError


def jsonrpc_error(rpc_id, err):
    return {
            'jsonrpc': '2.0',
            'id': rpc_id,
            'error': {
                'code': err.CODE,
                'message': err.MESSAGE,
                },
            }


def jsonrpc_ok(rpc_id, response):
    return {
            'jsonrpc': '2.0',
            'id': rpc_id,
            'result': response,
            }


def is_valid_json(j):
    if j.get('id') == 'None':
        raise ValueError('id missing')
    return True



