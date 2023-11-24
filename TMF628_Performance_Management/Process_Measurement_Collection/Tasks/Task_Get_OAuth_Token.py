import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('label', var_type='String')
context = Variables.task_call(dev_var)

#MSA_API.task_success('OK TEST',context, True)

url = context['oauth2_token_url']
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'fpc=Au1TpJv8RgVDv1jV49WGLhkI90rFAQAAAD-hHtwOAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
}
data = {
    'grant_type': 'client_credentials',
    'client_id': ''+context['client_id']+'',
    'client_secret': ''+context['client_secret']+'',
    'Content-Type': 'application/x-www-form-urlencoded',
    'scope' : 'api://9be2ca85-95ee-489d-aa5f-f301ea0c506d/.default'
}

response = requests.post(url, headers=headers, data=data)
context['oauth2_token_url_response']=response.json()
context['access_token']=context['oauth2_token_url_response']['access_token']

MSA_API.task_success('OK\n Token =>' +context['access_token']+'',context, True)