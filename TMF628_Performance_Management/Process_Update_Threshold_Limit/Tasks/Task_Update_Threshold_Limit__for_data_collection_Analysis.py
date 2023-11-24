import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('uplink_bitrate_threshold', var_type='String')
context = Variables.task_call(dev_var)

MSA_API.task_success('Threshold Limit set to '+context['uplink_bitrate_threshold']+'',context, True)