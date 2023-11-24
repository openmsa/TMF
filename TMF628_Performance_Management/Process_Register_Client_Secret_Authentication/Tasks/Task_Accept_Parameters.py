import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('oauth2_token_url', var_type='String')
dev_var.add('client_id', var_type='String')
dev_var.add('client_secret', var_type='String')
dev_var.add('performance_measurement_url', var_type='String')

dev_var.add('collection_job_oauth2_token_url', var_type='String')
dev_var.add('collection_job_client_id', var_type='String')
dev_var.add('collection_job_client_secret', var_type='String')
dev_var.add('CollectionJob_url', var_type='String')

#dev_var.add('performance_measurement.0.primary_key', var_type='String')
dev_var.add('primary_key_search', var_type='String')
dev_var.add('label', var_type='String')
dev_var.add('uplink_bitrate_threshold', var_type='String')

context = Variables.task_call(dev_var)

MSA_API.task_success('OK',context, True)