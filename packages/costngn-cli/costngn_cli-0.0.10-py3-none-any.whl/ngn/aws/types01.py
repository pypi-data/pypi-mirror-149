

import boto3
from cred01 import *
from classes import *


client = boto3.client(
    'ec2',
    #'ce',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,   
)

r =client.describe_instance_types(InstanceTypes=['t2.nano'])
memory= r["InstanceTypes"][0]["MemoryInfo"]["SizeInMiB"]
name= r["ResponseMetadata"]["HTTPHeaders"]["server"]

#response =client.instances.all()
print('Memory:', memory)
print('Name:', name)







#from pprint import pprint
#pprint(response)

"""
for inst in response:
    print(inst)
"""
