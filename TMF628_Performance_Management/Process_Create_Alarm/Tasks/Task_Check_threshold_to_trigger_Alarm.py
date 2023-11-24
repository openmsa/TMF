import random
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
dev_var.add('enableAlarm', var_type='String')
#dev_var.add('label', var_type='String')
context = Variables.task_call(dev_var)

'''
def assign_camera_state():
    camera_state = random.choice(["Low", "High"])
    return camera_state

context['camera_state']= "High"
# Example usage:
context['camera_state'] = assign_camera_state()
'''
username = 'superuser'
password = 'x^ZyuGM6~u=+fY2G'

# Get the current date
current_date = datetime.datetime.now()
# Format the date as YYYY-MM-DD
formatted_date = current_date.strftime("%Y-%m-%d")

# Generate the index name
index_name = f"ubialarm-{formatted_date}"

#url = 'http://msa-es:9200/ubi-tmf628/_doc'
url = 'http://msa-es:9200/'+index_name+'/_doc'

headers = {'Content-Type': 'application/json'} 
#data = context['performance_measurement_response']

if "performance_measurement_response" not in context or not context['performance_measurement_response']:
	MSA_API.task_error("no performance_measurement_response found, please run TMF628 Performance Management (e2e)",context, True)

data = {}

if "enableAlarm" not in context:
	context['enableAlarm'] = False
	
if context['enableAlarm'] == False:
	MSA_API.task_success("Alarm Triggering disabled, SKIP ",context, True)
	
indicator_name = "udp_tp_class_ul"
camera=""
value=0
for item in context['performance_measurement_response']:
	if item["indicatorName"] == indicator_name:
		value=item["observedValue"]
		#if item["observedValue"] < 1200000:
		id_value = item["id"].split("-")[0]
		if id_value == "311180001300001":
			camera="Camera 1"
		if id_value == "311180001300002":
			camera="Camera 2"
		if item["observedValue"] is not None and item["observedValue"] < int(context['uplink_bitrate_threshold']):
			data["date"] = current_date.strftime("%Y-%m-%dT%H:%M:%S+0000")
			data["device_id"]="UBI1934"
			data["device_ref"]="UBI1934"
			data["device_name"]="NICE backend app and DB"
			data["device_mgmt_ip"]="104.45.130.173"
			data["tenant_id"]="UBI"
			data["rule"]="From NICE TMF628 Workflow"
			data["rule_desc"]=""
			data["rawlog"]=''+camera+' | Uplink Bitrate : '+str(value)+' bit/s'
			data["customer_id"]="19"
			data["severity"]="1"
			data["log_type"]="event"
			data["ack"]="false"
			data["comment"]='should perform TMF759 Private Optimized Binding for '+camera+''
			
			request = requests.post(url, auth=(username, password), headers=headers, data=json.dumps(data))
			context['create_alarm_response']=request.json()
			
			MSA_API.task_success('Alarm Triggered for Camera ' +camera,context, True)
		else:
			continue
			
MSA_API.task_success('No Alarm Triggered for Camera ' +camera,context, True)