import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.orchestration import Orchestration
from msa_sdk import constants

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('cam1_enableAlarm', var_type='String')
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
GET_PROCESS_NAME ='Process/workflows/TMF628_Performance_Management/Process_Update_Alarm_Triggering'
EXTERNAL_REF=context['camera1_wf_instance']

orch.list_service_instances()
response_list_instance = json.loads(orch.content)

service_id = ''
'''
data example 

{
  "enableAlarm": false
}
'''

data=dict(enableAlarm=context['cam1_enableAlarm'])


#execute service by ref.
orch.execute_service_by_reference(ubiqube_id, EXTERNAL_REF, SERVICE_NAME, GET_PROCESS_NAME, data)

response = json.loads(orch.content)
service_id = response.get('serviceId').get('id')
process_id = response.get('processId').get('id')
#get service process details.
response = get_process_instance(orch, process_id)
status = response.get('status').get('status')
details = response.get('status').get('details')

if status == constants.FAILED:
	MSA_API.task_error('Execute Update Threshold Limit and Alarm Triggering WF service operation failed: ' + details + ' (#' + str(service_id) + ')', context, True)

MSA_API.task_success('Update Threshold Limit and Alarm Triggering ' +details+ ' successfully executed  '' (#' + str(service_id) + ')', context, True)

