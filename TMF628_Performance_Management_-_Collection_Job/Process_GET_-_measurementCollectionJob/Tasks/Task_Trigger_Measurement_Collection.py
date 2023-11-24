from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import constants
import time
from msa_sdk.orchestration import Orchestration
import re 
import json

dev_var = Variables()

context = Variables.task_call(dev_var)

'''
Retrieve process instance by service instance ID.

@param orch:
    Ochestration class object reference.
@param process_id:
    Baseline workflow process ID.
@param timeout:
    loop duration before to break.
@param interval:
    loop time interval.
@return:
    Response of the get process instance execution.
'''
def get_process_instance(orch, process_id, timeout = 600, interval=5):
    response = {}
    global_timeout = time.time() + timeout
    while True:
        #get service instance execution status.
        orch.get_process_instance(process_id)
        response = json.loads(orch.content)
        status = response.get('status').get('status')
        #context.update(get_process_instance=status)
        if status != constants.RUNNING or time.time() > global_timeout:
            break
        time.sleep(interval)

    return response

'''
def execute_service
(
self, service_name: str, process_name: str, data: dict)

Execute service.

Parameters
service_name : String
Service Name
process_name : String
Process name
data :  dict()
A dictionary containing workflow variables
Returns
None
If the execution was failed
service_id : Integer
If execution was success
'''

 #Initiate orchestraction object.
ubiqube_id = context['UBIQUBEID']

orch = Orchestration(ubiqube_id)

SERVICE_NAME = 'Process/workflows/TMF628_Performance_Management/TMF628_Performance_Management'
GET_PROCESS_NAME = 'Process/workflows/TMF628_Performance_Management/Process_Measurement_Collection'

EXTERNAL_REF="UBISID7996"


service_id = ''
'''
data example 

{
  "performance_measurement_url": "https://dsicatalystperformancemeasurement.nprd-gw.cloud.att.com/insight/performanceMeasurement?",
  "primary_key_search": "IMSI=3111808317362809"
}

'''
data = {}

url_string = context['dataAccessEndpoint']
#url = "https://dsicatalystperfornceMeasurement.com?IMSI=311180831736288"
url_parts = url_string.split('?')

base_url = url_parts[0]
query_string = url_parts[1]



#data=dict(performance_measurement_url=base_url+"?",primary_key_search=query_string)
data['performance_measurement_url']=base_url+"?"
data['primary_key_search']=query_string
#context['data_check']=data
#serialized_data = json.dumps(data)
#MSA_API.task_success("OK TEST",context, True)
#execute service by ref.
orch.execute_service_by_reference(ubiqube_id, EXTERNAL_REF, SERVICE_NAME, GET_PROCESS_NAME, dict())

response = json.loads(orch.content)
service_id = response.get('serviceId').get('id')
process_id = response.get('processId').get('id')
#get service process details.
response = get_process_instance(orch, process_id)
status = response.get('status').get('status')
details = response.get('status').get('details')

if status == constants.FAILED:
	MSA_API.task_error('Execute TMF628 Performance Management - Measurement Collection WF service operation failed: ' + details + ' (#' + str(service_id) + ')', context, True)

	
MSA_API.task_success('TMF628 Performance Management - Measurement Collection operation ' +details+ ' successfully executed to the Managed Entity  (#' + str(service_id) + ')', context, True)


MSA_API.task_success("OK TEST",context, True)