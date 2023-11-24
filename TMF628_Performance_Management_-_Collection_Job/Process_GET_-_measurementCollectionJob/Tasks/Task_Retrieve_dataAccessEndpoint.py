import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests


# List all the parameters required by the task
dev_var = Variables()

dev_var.add('dataAccessEndpoint', var_type='String')

context = Variables.task_call(dev_var)

if not context['measurementCollectionJob_response'][0]['dataAccessEndpoint'][0]['href']:
	MSA_API.task_error("dataAccessEndpoint link not foound",context, True)

#https://dsicatalystperformancemeasurement.nprd-gw.cloud.att.com/insight/performanceMeasurement?IMSI=3111808317362809

context['dataAccessEndpoint']=context['measurementCollectionJob_response'][0]['dataAccessEndpoint'][0]['href']	
context['dataAccessEndpoint']="https://dsicatalystperformancemeasurement.nprd-gw.cloud.att.com/insight/performanceMeasurement?IMSI=3111808317362809"
MSA_API.task_success(context['dataAccessEndpoint'],context, True)

