import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests

# List all the parameters required by the task
dev_var = Variables()

dev_var.add('CollectionJob_url', var_type='String')
#dev_var.add('measurementCollectionJob_id', var_type='String')
context = Variables.task_call(dev_var)

url = context['CollectionJob_url']+'/measurementCollectionJob'

headers = {
    'Authorization': 'Bearer ' + context['collection_job_access_token']+'',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)}',
    'Content-Type' : 'application/json;charset=utf-8'
}

response = requests.get(url, headers=headers)
context['measurementCollectionJob_response']=response.json()
	
try:
	json_string = json.dumps(context['measurementCollectionJob_response'])
	json_object = json.loads(json_string)
	if "failed" in context['measurementCollectionJob_response']:
		MSA_API.task_error(context['measurementCollectionJob_response'],context, True)
	MSA_API.task_success(context['measurementCollectionJob_response'],context, True)
except json.decoder.JSONDecodeError:
	MSA_API.task_error(context['measurementCollectionJob_response'],context, True)
