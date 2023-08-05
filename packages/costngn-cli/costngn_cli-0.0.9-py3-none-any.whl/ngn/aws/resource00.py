import pprint as pp
import boto3
from cred01 import *
from collections import defaultdict



def get_res_data(region):
    # Connect to EC2
    ec2 = boto3.resource('ec2',    
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name= region)

    # Get information for all 
    instances = ec2.instances.all()
    ec2info = defaultdict()
    for instance in instances:
        #print('XXX')
        for tag in instance.tags:
            if 'Name'in tag['Key']:
                name = tag['Value']
        # Add instance info to a dictionary
        print('VPC:',instance.vpc)         
        ec2info[instance.id] = {
            'Name': name,
            'Type': instance.instance_type,
            'State': instance.state['Name'],
            'Private IP': instance.private_ip_address,
            'Public IP': instance.public_ip_address,
            'Launch Time': instance.launch_time,
            #'Memory' : instance.memory
            }

    attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time']
    for instance_id, instance in ec2info.items():
        for key in attributes:
            print("{0}: {1}".format(key, instance[key]))
        print("------")

    #for attr in ec2:
    #pp.pprint(dir(ec2.Instance))
    #print(instance)
    #field = ec2.instances.all()




"""
reg_pru=['ap-southeast-2' ,'us-east-1','us-west-2','eu-north-1']
for reg in reg_pru:
    get_res_data(reg)

"""
get_res_data('us-east-1')
