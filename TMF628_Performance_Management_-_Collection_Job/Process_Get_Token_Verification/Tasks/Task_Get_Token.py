import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests

# List all the parameters required by the task
dev_var = Variables()
context = Variables.task_call(dev_var)

#MSA_API.task_success('OK TEST',context, True)

url = context['collection_job_oauth2_token_url']
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'fpc=Au1TpJv8RgVDv1jV49WGLhkI90rFAQAAAD-hHtwOAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
}
data = {
    'grant_type': 'client_credentials',
    'client_id': ''+context['collection_job_client_id']+'',
    'client_secret': ''+context['collection_job_client_secret']+'',
    'Content-Type': 'application/x-www-form-urlencoded',
    'scope' : 'api://7d933177-55eb-44ae-8a5e-0503ff4fb518/.default'
}

response = requests.post(url, headers=headers, data=data)
context['collection_job_oauth2_token_url_response']=response.json()
context['collection_job_access_token']=context['collection_job_oauth2_token_url_response']['access_token']

MSA_API.task_success('OK\n Token =>' +context['collection_job_access_token']+'',context, True)