import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests


# List all the parameters required by the task
dev_var = Variables()

dev_var.add('dataAccessEndpoint1', var_type='String')
dev_var.add('dataAccessEndpoint', var_type='String')

#dev_var.add('performanceIndicatorSpecification.0.name', var_type='String')
#dev_var.add('performanceIndicatorSpecification.0.description', var_type='String')

dev_var.add('collection_job.0.name', var_type='String')
dev_var.add('collection_job.0.description', var_type='String')


dev_var.add('reportingSystem.0.name', var_type='String')
dev_var.add('reportingSystem.0.description', var_type='String')

dev_var.add('dataAccessEndpoint3.0.key', var_type='String')
dev_var.add('dataAccessEndpoint3.0.value', var_type='String')

dev_var.add('sourceSystem.0.key', var_type='String')
dev_var.add('sourceSystem.0.value', var_type='String')

dev_var.add('PerformanceIndicatorSpecification0.0.key', var_type='String')
dev_var.add('PerformanceIndicatorSpecification0.0.value', var_type='String')

dev_var.add('PerformanceIndicatorSpecification1.0.key', var_type='String')
dev_var.add('PerformanceIndicatorSpecification1.0.value', var_type='String')

dev_var.add('PerformanceIndicatorSpecification2.0.key', var_type='String')
dev_var.add('PerformanceIndicatorSpecification2.0.value', var_type='String')

dev_var.add('PerformanceIndicatorSpecification3.0.key', var_type='String')
dev_var.add('PerformanceIndicatorSpecification3.0.value', var_type='String')

context = Variables.task_call(dev_var)

if not context['measurementCollectionJob_response'][0]['dataAccessEndpoint'][0]['uri']:
	MSA_API.task_error("dataAccessEndpoint link not foound",context, True)
'''	
##### Access the performanceIndicatorSpecification array
performance_specs = context['measurementCollectionJob_response'][0]["performanceIndicatorSpecification"]
performanceIndicatorSpecification=[]
# Iterate over each specification
for spec in performance_specs:
	# Access the key and value of each specification
	key = spec["name"]
	value = spec["description"]
	performanceIndicatorSpecification.append(dict(name=key,description=value))
	
context['performanceIndicatorSpecification']=performanceIndicatorSpecification
'''

#=========== Extract each field except arrays and tables in array.0.key and array.0.value in PerformanceIndicatorSpecification #0
fields = {}
PerformanceIndicatorSpecification0=[]
context['PerformanceIndicatorSpecification0']=[]
data=context['measurementCollectionJob_response'][0]["performanceIndicatorSpecification"][0]
for key, value in data.items():
    if not isinstance(value, (list, dict)):
        fields[key] = value
# Print the extracted fields
for key, value in fields.items():
    PerformanceIndicatorSpecification0.append(dict(key=key,value=value))
context['PerformanceIndicatorSpecification0']=PerformanceIndicatorSpecification0

#=========== Extract each field except arrays and tables in array.0.key and array.0.value in PerformanceIndicatorSpecification #1
fields = {}
PerformanceIndicatorSpecification1=[]
context['PerformanceIndicatorSpecification1']=[]
data=context['measurementCollectionJob_response'][0]["performanceIndicatorSpecification"][1]
for key, value in data.items():
    if not isinstance(value, (list, dict)):
        fields[key] = value
# Print the extracted fields
for key, value in fields.items():
    PerformanceIndicatorSpecification1.append(dict(key=key,value=value))
context['PerformanceIndicatorSpecification1']=PerformanceIndicatorSpecification1

#=========== Extract each field except arrays and tables in array.0.key and array.0.value in PerformanceIndicatorSpecification #2
fields = {}
PerformanceIndicatorSpecification2=[]
context['PerformanceIndicatorSpecification2']=[]
data=context['measurementCollectionJob_response'][0]["performanceIndicatorSpecification"][2]
for key, value in data.items():
    if not isinstance(value, (list, dict)):
        fields[key] = value
# Print the extracted fields
for key, value in fields.items():
    PerformanceIndicatorSpecification2.append(dict(key=key,value=value))
context['PerformanceIndicatorSpecification2']=PerformanceIndicatorSpecification2

#=========== Extract each field except arrays and tables in array.0.key and array.0.value in PerformanceIndicatorSpecification #3
fields = {}
PerformanceIndicatorSpecification3=[]
context['PerformanceIndicatorSpecification3']=[]
data=context['measurementCollectionJob_response'][0]["performanceIndicatorSpecification"][3]
for key, value in data.items():
    if not isinstance(value, (list, dict)):
        fields[key] = value
# Print the extracted fields
for key, value in fields.items():
    PerformanceIndicatorSpecification3.append(dict(key=key,value=value))
context['PerformanceIndicatorSpecification3']=PerformanceIndicatorSpecification3

#=========== Extract each field except arrays and tables in array.0.key and array.0.value in collection_job
fields = {}
collection_job=[]
context['collection_job']=[]
data=context['measurementCollectionJob_response'][0]
for key, value in data.items():
    if not isinstance(value, (list, dict)):
        fields[key] = value
# Print the extracted fields
for key, value in fields.items():
    collection_job.append(dict(name=key,description=value))
context['collection_job']=collection_job

#============== Extract each field except arrays and tables in array.0.key and array.0.value in dataAccessEndpoint3
fields = {}
dataAccessEndpoint3=[]
context['dataAccessEndpoint3']=[]
data=performance_specs = context['measurementCollectionJob_response'][0]["dataAccessEndpoint"][0]
for key, value in data.items():
    if not isinstance(value, (list, dict)):
        fields[key] = value
        
# Print the extracted fields
for key, value in fields.items():
    dataAccessEndpoint3.append(dict(key=key,value=value))
context['dataAccessEndpoint3']=dataAccessEndpoint3

# Extract each field except arrays and tables in array.0.key and array.0.value in reportingSystem
fields = {}
reportingSystem=[]
context['reportingSystem']=[]
data=context['measurementCollectionJob_response'][0]['reportingSystem']
for key, value in data.items():
    if not isinstance(value, (list, dict)):
        fields[key] = value
        
# Print the extracted fields
for key, value in fields.items():
    reportingSystem.append(dict(name=key,description=value))
context['reportingSystem']=reportingSystem


# Extract each field except arrays and tables in array.0.key and array.0.value in sourceSystem
fields = {}
sourceSystem=[]
context['sourceSystem']=[]
data=context['measurementCollectionJob_response'][0]['sourceSystem']
for key, value in data.items():
    if not isinstance(value, (list, dict)):
        fields[key] = value
        
# Print the extracted fields
for key, value in fields.items():
    sourceSystem.append(dict(key=key,value=value))
context['sourceSystem']=sourceSystem

#https://dsicatalystperformancemeasurement.nprd-gw.cloud.att.com/insight/performanceMeasurement?IMSI=3111804250982716

context['dataAccessEndpoint1']=context['measurementCollectionJob_response'][0]['dataAccessEndpoint'][0]['href']	
#context['dataAccessEndpoint']="https://dsicatalystperformancemeasurement.nprd-gw.cloud.att.com/insight/performanceMeasurement?IMSI=3111804250982716"
context['dataAccessEndpoint']=context['performance_measurement_url']+context['primary_key_search']
url_string = context['dataAccessEndpoint']
#url = "https://dsicatalystperfornceMeasurement.com?IMSI=311180831736288"
url_parts = url_string.split('?')

base_url = url_parts[0]
query_string = url_parts[1]

##waiting valid url with IMSI from collection Job
#context['performance_measurement_url']=base_url+"?"
#context['primary_key_search']=query_string

MSA_API.task_success(context['dataAccessEndpoint'],context, True)

