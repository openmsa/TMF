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

context = Variables.task_call(dev_var)

MSA_API.task_success('Alarm Triggering Status : ' +str(context['enableAlarm']),context, True)