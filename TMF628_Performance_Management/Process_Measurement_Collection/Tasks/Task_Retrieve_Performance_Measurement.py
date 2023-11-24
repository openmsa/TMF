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
#dev_var.add('performance_measurement.0.primary_key', var_type='String')
dev_var.add('primary_key_search', var_type='String')
context = Variables.task_call(dev_var)

'''
data = [
    {
        "id": "3111803542146781-service_rtt_net",
        "indicatorName": "service_rtt_net",
        "observedValue": 0.174674
    },
    {
        "id": "3111803542146781-service_rtt_term",
        "indicatorName": "service_rtt_term",
        "observedValue": 0.139836
    },
    {
        "id": "3111803542146781-service_bitrate_ul",
        "indicatorName": "service_bitrate_ul",
        "observedValue": 7315
    },
    {
        "id": "3111803542146781-udp_tp_class_ul",
        "indicatorName": "udp_tp_class_ul",
        "observedValue": 10033
    },
    {
        "id": "3111803542146781-timestamp",
        "indicatorName": "timestamp",
        "observedValue": "2023-08-13T16:22:09.179Z"
    }
]

json_data = json.dumps(data)

context['performance_measurement_response']=json.loads(json_data)
'''
#MSA_API.task_success('OK TEST '+json_data+'',context, True)
#MSA_API.task_success('OK TEST',context, True)
url = context['performance_measurement_url']
'''
payload = json.dumps({
	'Message': 'this request for external'
})

headers = {
    'Authorization': 'Bearer ' + context['access_token']+'',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)}'
}
'''
payload = json.dumps({
	'Message': 'this request for external'
})
headers = {
    'Authorization': 'Bearer ' + context['access_token']+'',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)}'
}
context['headers_check']=headers

if "primary_key_search" not in context or not context['primary_key_search']:
	context['primary_key_search']=''
	
final_url=url+context['primary_key_search']
context['final_url']=final_url

#response = requests.post(final_url, headers=headers, data=payload) 
response = requests.get(context['final_url'], headers=headers)
#data = str(response)

try:
    context['performance_measurement_response']=response.json()
except TypeError as e:
	context['performance_measurement_response']=str(response)
	MSA_API.task_error(context['performance_measurement_response'],context, True)
except json.JSONDecodeError:  # Catch JSONDecodeError
    context['performance_measurement_response']=str(response)
    MSA_API.task_error(context['performance_measurement_response'],context, True)

#context['performance_measurement_response']=response.json()
try:
	json_string = json.dumps(context['performance_measurement_response'])
	json_object = json.loads(json_string)
	if "failed" in context['performance_measurement_response']:
		MSA_API.task_error(context['performance_measurement_response'],context, True)
	MSA_API.task_success(context['performance_measurement_response'],context, True)
except json.decoder.JSONDecodeError:
	MSA_API.task_error(context['performance_measurement_response'],context, True)



