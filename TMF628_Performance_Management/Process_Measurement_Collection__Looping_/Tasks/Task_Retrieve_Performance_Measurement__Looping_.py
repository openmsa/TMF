import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests

# List all the parameters required by the task
dev_var = Variables()

#dev_var.add('oauth2_token_url', var_type='String')
#dev_var.add('client_id', var_type='String')
#dev_var.add('client_secret', var_type='String')
dev_var.add('performance_measurement_url', var_type='String')
dev_var.add('performance_measurement.0.primary_key', var_type='String')
#dev_var.add('primary_key_search', var_type='String')
context = Variables.task_call(dev_var)

#MSA_API.task_success('OK TEST',context, True)
url = context['performance_measurement_url']
payload = json.dumps({
	'Message': 'this request for external'
})

headers = {
    'Authorization': 'Bearer ' + context['access_token']+'',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)}'
}

context['headers_check']=headers

if "primary_key_search" not in context or not context['primary_key_search']:
	context['primary_key_search']=''

final_url=url+context['primary_key_search']
context['final_url']=final_url
response = requests.post(final_url, headers=headers, data=payload) 
context['performance_measurement_response']= response.json()

performance_responses = []
for key in context['performance_measurement']:
	final_url=url+key['primary_key']
	response = requests.get(final_url, headers=headers)
	try:
		json_string = json.dumps(context['performance_measurement_response'])
		json_object = json.loads(json_string)
		if "failed" in context['performance_measurement_response']:
			MSA_API.task_error(context['performance_measurement_response'],context, True)
	except json.decoder.JSONDecodeError:
		MSA_API.task_error(context['performance_measurement_response'],context, True)
	performance_responses.append(response.json())

context['performance_measurement_response'] = performance_responses	

MSA_API.task_success(context['performance_measurement_response'],context, True)

