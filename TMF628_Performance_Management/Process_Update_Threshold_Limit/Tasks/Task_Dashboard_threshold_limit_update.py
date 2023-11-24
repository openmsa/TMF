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
#MSA_API.task_success('OK SKIP TEST',context, True)

username = 'superuser'
password = 'x^ZyuGM6~u=+fY2G'

#url = 'http://msa-kibana:5601/kibana/api/saved_objects/visualization/6f3520f0-4e7f-11ee-a701-6324a3d92c26'
#headers = {'Content-Type':'application/json', 'kbn-xsrf' : 'true'}

# Set the Kibana server URL
kibana_url = 'http://msa-kibana:5601/kibana'

# Set the visualization ID
##visualization_id = 'deeb15a0-48ab-11ee-a701-6324a3d92c26'
if context['primary_key_search'] == "IMSI=311180001300001":
	visualization_id = '3b9a6f30-5306-11ee-91c8-45f28c720936'
if context['primary_key_search'] == "IMSI=311180001300002":
	visualization_id = '5dea2800-5306-11ee-91c8-45f28c720936'
	
data=[
  {
    "type": "visualization",
    "id": visualization_id
  }
]
data2 = json.dumps(data)
# Get the existing visualization configuration
response = requests.post(f'{kibana_url}/api/kibana/management/saved_objects/_bulk_get',
	auth=(username, password),
	headers={'Content-Type':'application/json', 'kbn-xsrf' : 'true'},
	json=data2)

#context['response1']=response.json()
#MSA_API.task_success("OK TEST",context, True)

# Parse the JSON string into an object
data = response.json()

# Update the thresholdLine value
uplink_bitrate_threshold=int(context['uplink_bitrate_threshold'])
vis_state = json.loads(data[0]['attributes']['visState'])
vis_state['params']['thresholdLine']['value'] = uplink_bitrate_threshold
data[0]['attributes']['visState'] = json.dumps(vis_state)
del data[0]['id']
del data[0]['type']
del data[0]['namespaces']
del data[0]['updated_at']
del data[0]['migrationVersion']
del data[0]['coreMigrationVersion']
del data[0]['meta']

context['response2']=data

# Convert the updated data back to JSON
updated_json = json.dumps(data[0])

request = requests.put(
    f'{kibana_url}/api/saved_objects/visualization/{visualization_id}', 
    auth=(username, password),
    headers={'Content-Type':'application/json', 'kbn-xsrf' : 'true'},
    json=updated_json
)

#context['visualization_config']=request.json()
#MSA_API.task_success("OK TEST",context, True)

context['dashboard_threashold_update_response']=request.json()
MSA_API.task_success(context['dashboard_threashold_update_response'],context, True)

'''
# Check if the update was successful
if request.status_code == 200:
    print("Threshold parameters updated successfully!")
    MSA_API.task_success("Threshold parameters updated successfully!",context, True)
else:
	MSA_API.task_error("Failed to update threshold parameters.",context, True)
'''

