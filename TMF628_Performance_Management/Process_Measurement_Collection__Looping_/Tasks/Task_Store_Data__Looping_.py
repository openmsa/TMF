import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests
import datetime  

# List all the parameters required by the task
dev_var = Variables()

context = Variables.task_call(dev_var)
#MSA_API.task_success('OK TEST',context, True)

username = 'superuser'
password = 'x^ZyuGM6~u=+fY2G'

# Get the current date
current_date = datetime.datetime.now()
# Format the date as YYYY-MM-DD
formatted_date = current_date.strftime("%Y-%m-%d")

# Generate the index name
index_name = f"ubi-tmf628-compliant-{formatted_date}"

#url = 'http://msa-es:9200/ubi-tmf628/_doc'
url = 'http://msa-es:9200/'+index_name+'/_doc'

headers = {'Content-Type': 'application/json'} 
#data = context['performance_measurement_response']


for i in range(len(context['performance_measurement_response'])):
	'''
	if str(context['performance_measurement_response'][i][0]['isguaranteedbitrate']) == "True":
		performance_measurement_response = 'true'
	else:
		performance_measurement_response = 'false'

	current_time = datetime.datetime.utcnow().isoformat() + 'Z' 
	data = {
		'datacenter': ''+context['performance_measurement_response'][i][0]['datacenter']+'',
		'downlinkbitrate': ''+str(context['performance_measurement_response'][i][0]['downlinkbitrate'])+'',
		'errorrate': ''+str(context['performance_measurement_response'][i][0]['errorrate'])+'',
		'IMSI': ''+context['performance_measurement_response'][i][0]['IMSI']+'',
		'latency': ''+str(context['performance_measurement_response'][i][0]['latency'])+'',
		'measurementtime': ''+context['performance_measurement_response'][i][0]['measurementtime']+'',
		'ttl_interval': ''+context['performance_measurement_response'][i][0]["ttl"]["interval"]+'',
		'ttl_value': ''+context['performance_measurement_response'][i][0]["ttl"]["ttl"]+'',
		'uplinkbitrate': ''+str(context['performance_measurement_response'][i][0]['uplinkbitrate'])+'',
		'isguaranteedbitrate': ''+str(performance_measurement_response)+'',
		'request_time': ''+current_time+''
		}
	'''
	data = {}
	for result in context['performance_measurement_response'][i]:
		indicator_name = result["indicatorName"]
		observed_value = result["observedValue"]
		if observed_value == None:
			observed_value = 0
		data[indicator_name] = observed_value
	id_value = context['performance_measurement_response'][i][0]["id"].split("-")[0]
	data["id"] = id_value 
	current_time = datetime.datetime.utcnow().isoformat() + 'Z' 
	data["request_time"] = current_time
	data["customer_id"]=166
	context['data_to_es_check']=data
	
	request = requests.post(url, auth=(username, password), headers=headers, data=json.dumps(data))

	context['data_store_response']=request.json()


MSA_API.task_success(context['data_store_response'],context, True)


