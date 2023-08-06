

import boto3
from cred01 import *


ec2_res = boto3.resource(    
    'ec2',
    #'ce',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,   
)

print('all',ec2_res.instances.all())

for instance in ec2_res.instances.all():
    print(
        "Id: {0}\nPlatform: {1}\nType: {2}\nPublic IPv4: {3}\nAMI: {4}\nState: {5}\n".format(
        instance.id, instance.platform, instance.instance_type, instance.public_ip_address, instance.image.id, instance.state
        )
    )

"""
client = boto3.client(
    'ec2',
    #'ce',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,   
)

#response =client.describe_instance_types(InstanceTypes=['t2.nano'])

response =client.instances.all()
print(response)





from pprint import pprint
pprint(response)
"""

"""
for inst in response:
    print(inst)
"""
