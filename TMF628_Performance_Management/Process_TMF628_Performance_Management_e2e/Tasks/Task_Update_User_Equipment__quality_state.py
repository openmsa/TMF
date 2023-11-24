import random
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

'''
def assign_camera_state():
    camera_state = random.choice(["Low", "High"])
    return camera_state

context['camera_state']= "High"
# Example usage:
context['camera_state'] = assign_camera_state()
'''
indicator_name = "udp_tp_class_ul"
value=0
for item in context['performance_measurement_response']:
	if item["indicatorName"] == indicator_name:
		value=item["observedValue"]
		#if item["observedValue"] < 1200000:
		if item["observedValue"] is not None and item["observedValue"] < int(context['uplink_bitrate_threshold']):
			context['camera_state']="Low"
		elif item["observedValue"] is not None and item["observedValue"] > int(context['uplink_bitrate_threshold']):
			context['camera_state']="High"
		else:
			continue
			
MSA_API.task_success(indicator_name+' => '+str(value)+' => '+context['camera_state'],context, True)