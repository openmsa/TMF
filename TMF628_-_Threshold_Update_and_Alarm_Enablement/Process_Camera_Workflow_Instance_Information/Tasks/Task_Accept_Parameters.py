import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('camera1_wf_instance', var_type='String')
dev_var.add('camera2_wf_instance', var_type='String')
context = Variables.task_call(dev_var)

MSA_API.task_success('OK',context, True)