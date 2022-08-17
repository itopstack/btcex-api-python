import uuid
import requests
import os

from dotenv import load_dotenv
from btcex_api.models import JsonRpcRequestParams
from btcex_api.util import common_utils
from btcex_api.util import signature_util

load_dotenv()

url = 'https://www.btcex.com/api/v1'

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

headers = {'content-type': "application/json"}


def auth_client_signature():
    method = '/public/auth'
    grant_type = "client_signature"
    timestamp = str(common_utils.time_stamp())
    nonce = uuid.uuid4().__str__()
    source = client_id + '\n' + timestamp + '\n' + nonce + '\n'

    sign = signature_util.signature_data(source, client_secret)

    _params = {
        'grant_type': grant_type,
        'client_id': client_id,
        'nonce': nonce,
        'timestamp': timestamp,
        'signature': sign
    }
    request_param = JsonRpcRequestParams(id='1', method=method, params=_params)
    resp = requests.post(
        url + method, data=request_param.json(), headers=headers)

    return resp.json()


auth_resp = auth_client_signature()
error_key = 'error'
error_message_key = 'message'
result_key = 'result'
access_token_key = 'access_token'

if error_key in auth_resp and error_message_key in auth_resp[error_key]:
    print(auth_resp[error_key][error_message_key])
    exit()

if not result_key in auth_resp or not access_token_key in auth_resp[result_key]:
    print('Missing access token. Authentication Failure')
    exit()

print('Authentication Successfully')
