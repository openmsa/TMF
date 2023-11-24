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
#MSA_API.task_success('OK SKIP TEST',context, True)

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


data = {}

##============ Collection Job
for result in context['collection_job']:
	indicator_name = "collection_job_"+result["name"]
	observed_value = result["description"]
	data[indicator_name] = observed_value

##============ dataAccessEndpoint3
for result in context['dataAccessEndpoint3']:
	indicator_name = "dataAccessEndpoint_"+result["key"]
	observed_value = result["value"]
	data[indicator_name] = observed_value

##============ reportingSystem
for result in context['reportingSystem']:
	indicator_name = "sourceSystem_"+result["name"]
	observed_value = result["description"]
	data[indicator_name] = observed_value	

##============ sourceSystem
for result in context['sourceSystem']:
	indicator_name = "reportingSystem_"+result["key"]
	observed_value = result["value"]
	data[indicator_name] = observed_value	
	
##============ PerformanceIndicatorSpecification0
for result in context['PerformanceIndicatorSpecification0']:
	indicator_name = "PerformanceIndicatorSpecification0_"+result["key"]
	observed_value = result["value"]
	data[indicator_name] = observed_value

##============ PerformanceIndicatorSpecification1
for result in context['PerformanceIndicatorSpecification1']:
	indicator_name = "PerformanceIndicatorSpecification1_"+result["key"]
	observed_value = result["value"]
	data[indicator_name] = observed_value

##============ PerformanceIndicatorSpecification2
for result in context['PerformanceIndicatorSpecification2']:
	indicator_name = "PerformanceIndicatorSpecification2_"+result["key"]
	observed_value = result["value"]
	data[indicator_name] = observed_value

##============ PerformanceIndicatorSpecification3
for result in context['PerformanceIndicatorSpecification3']:
	indicator_name = "PerformanceIndicatorSpecification3_"+result["key"]
	observed_value = result["value"]
	data[indicator_name] = observed_value



	
	
##===== Performance Collection	
for result in context['performance_measurement_response']:
	indicator_name = result["indicatorName"]
	observed_value = result["observedValue"]
	if observed_value == None:
		observed_value = 0
	data[indicator_name] = observed_value
	
id_value = context['performance_measurement_response'][0]["id"].split("-")[0]
data["id"] = id_value	
current_time = datetime.datetime.utcnow().isoformat() + 'Z' 
data["request_time"] = current_time
data["customer_id"]=19
#data["dataAccessEndpoint"]=context['dataAccessEndpoint']
data["dataAccessEndpoint"]=context['final_url']
data["camera_state"]=context['camera_state']
if id_value == "311180001300001":
	data["camera"] = "Camera 1"
if id_value == "311180001300002":
	data["camera"] = "Camera 2"


context['data_to_es_check']=data

#MSA_API.task_success('OK TEST',context, True)	

request = requests.post(url, auth=(username, password), headers=headers, data=json.dumps(data))

context['data_store_response']=request.json()

#MSA_API.task_success(context['data_store_response'],context, True)
MSA_API.task_success(context['performance_measurement_response'],context, True)


