##### Logs-in and detect all instances running in all regions #####
#it needs complete credentials on cred01.py on same folder
#identify and print each required field of each instance


import pprint as pp
import boto3
from botocore.config import Config
from collections import defaultdict
from cred01 import *
from classes import *
from prices00 import *
#from resource00 import *
import time


# load all regions in list regions
def available_regions(service):
    regions = []
    client = boto3.client(service)
    response = client.describe_regions()

    for item in response["Regions"]:
        #print(item["RegionName"])
        regions.append(item["RegionName"])
    return regions

# Assign tags to instances in oorder to able to detail monthly cost by instance
def assign_tags_to_instance(ec2, instance_id):
    print("Waiting for instance to be ready ..."); time.sleep(7)
    print("Assigning tags to instance " + instance_id)
 
    ec2.create_tags(Resources=[instance_id], Tags=[{'Key': 'Instance_Id', 'Value': instance_id}])
                                                   #{'Key': 'Owner', 'Value': OWNER},
                                                   #{'Key': 'RunId', 'Value': RUNID}])
    print("Tags assigned to instance successfully!")
 


# Find all available regions 
def main():
    print("Scan all available regions")
    regions = available_regions("ec2")
    # Scan all of EC2 in each region
    cnt = 0
    my_ids=[];my_insts=[]
    for region in regions:
        #get_res_data(region)
        #try:
        #print('Region:',region)

        ec2_res = boto3.resource('ec2',            
            region_name= region,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY)

        instances = ec2_res.instances.all()
        
        
        for instance in instances:
            print('__________________________________________')
            #Instantiate instance
            i1=Inst()  
            i1.region = region
                       
            for tag in instance.tags:
                if 'Name'in tag['Key']:
                    i1.name = tag['Value']
                
            i1.id= instance.id   
            #pp.pprint(instance.tags)
            i1.status= instance.state['Name']  
            i1.birthday= instance.launch_time
            i1.ipv4priv= instance.private_ip_address
            i1.ipv4pub= instance.public_ip_address            
            i1.type = instance.instance_type

            # Get Name, Memory, avzone, vps (need client)
            ec2_cli = boto3.client('ec2',    
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY,
                region_name= region)  

            r_inst = ec2_cli.describe_instances(InstanceIds=[i1.id])["Reservations"][0]
            pp.pprint(r_inst['tags'])
            #r_inst=response["Reservations"][0]
            
            
            #i1.avzone = r_inst["Instances"][0]["Placement"]["AvailabilityZone"] 
            #i1.vps_id = r_inst["Instances"][0]["VpcId"]



            #Store the instance id and data in lists 
            my_ids.append(i1.id)
            #; my_insts.append(i1)            
            for key,field in vars(i1).items():            
                print(key,':',field)




    print('__________________________________________')
    if len(my_ids) == 1:
        print(f"You have {len(my_ids)} instance here M.J!",'\n')
    elif len(my_ids) > 1:
        print(f"You have {len(my_ids)} instances here M.J.!",'\n')
    else:
        print(f"You have no instances here M.J.!",'\n')

    #for id in my_ids: print(id)
    #pp.pprint



    






# call function
main()