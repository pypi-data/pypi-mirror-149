##### Logs-in and extract all instances data grouped by regions #####
#it needs config file $home\costngn\config.toml

import os
from os.path import exists
from pathlib import Path
from itertools import count
from datetime import date, datetime
import copy
import pprint as pp
import boto3
import json
import toml
from botocore.config import Config

#from ngn.aws.cred01 import * #now from config.toml
from ngn.aws.classes import *
from ngn.aws.prices00 import *
#from resource00 import *

# load all regions in list regions
def available_regions(service):
    regions = []
    client = boto3.client(service,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,        
        region_name= 'us-east-2', 
    )
    response = client.describe_regions()
    for item in response["Regions"]:
        #print(item["RegionName"])
        regions.append(item["RegionName"])
    return regions


##### Acceess to AWS and scan all available regions and instances 
#def aws_main(some_a:str):
def aws_main(company, nick, config_file,ce_enable:bool):
    #print('XXXX NICK FROM MAIN',nick)
    #company='aws'
    #if ce_enable:
    #    print('Cost Explore Enabled')
    #print("Reading configuration file") #config.toml
    global AWS_ACCESS_KEY ; global AWS_SECRET_KEY; global AWS_AUTH_REGION 
    AWS_ACCESS_KEY=''; AWS_SECRET_KEY=''; AWS_AUTH_REGION=''
    #config_file=os.path.join(Path.home(), 'costngn','config.toml')    
    prof=toml.load(config_file)
    #Load the account for the given nickname    
    acc=prof[nick]
    print(f"Account Nickname: {nick}")
    print(f"Service Provider: {acc['provider']}")
    print(f"Data Output Format: {acc['out_format']}")
    #print(f"Access Key: XXX HIDDEN XXX")
    #print(f"Secret Key: XXX HIDDEN XXX")
    #print(f"Access Key: {acc['ACCESS_KEY']}")
    #print(f"Secret Key: {acc['SECRET_KEY']}")
    AWS_ACCESS_KEY= acc['ACCESS_KEY']
    AWS_SECRET_KEY=acc['SECRET_KEY']
    AWS_AUTH_REGION=acc['AUTH_REGION']
    #print('')
    print("Scanning all instances (wait please)")
    #print("Next version we'll add an option for accessing only previously scanned instances")
    regions = available_regions("ec2")
    # Scan all of EC2 in each region
    cnt = 0
    my_ids=[]; insts={}

    rep=copy.deepcopy(RepBase)     
    for region in regions:
        print('.')
        #get_res_data(region)
        #try:
        #print('Region:',region)
        ec2_res = boto3.resource('ec2',            
            region_name= region,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY)

        instances = ec2_res.instances.all()   
        region_has_inst=False      
        
        for instance in instances:
            region_has_inst=True
            #print('__________________________________________')
            print('*')            
            #Initiate Reg and Inst dictios
            inst=copy.deepcopy(InstBase)
            #pp.pprint(instance)
            try: #look for the name, if exists
                for tag in instance.tags:
                    if 'Name'in tag['Key']:
                        ##i1.name = tag['Value']
                        inst['name']=tag['Value']
            except: pass
                
            inst['id']= instance.id
            inst['provider']=company.upper()
            inst['region']= region 
            #print(inst['id'],inst['name'],'VPC:', instance.vpc )
            inst['status']= instance.state['Name']    
            inst['birthday']=str(instance.launch_time)
            inst['ipv4priv']=instance.private_ip_address 
            inst['ipv4pub']= instance.public_ip_address 
            inst['type']= instance.instance_type
            inst['cpus']=instance.cpu_options.get(u'CoreCount','1')
            inst['image']=instance.image_id           
            inst['os']='Linux' if 'Linux' in instance.platform_details else 'Windows'
            
            # Get Name, Memory, avzone, vps (need client)
            ec2_cli = boto3.client('ec2',    
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY,
                region_name= region)              

            #r_inst = ec2_cli.describe_instances(InstanceIds=[i1.id])["Reservations"][0]
            r_inst = ec2_cli.describe_instances(InstanceIds=[inst['id']])["Reservations"][0]

            #r_inst=response["Reservations"][0]
            inst['avzone']=r_inst["Instances"][0]["Placement"]["AvailabilityZone"]
            inst['vpc_id']=r_inst["Instances"][0]["VpcId"]

            #Get memory size from _types
            
            r_typ =ec2_cli.describe_instance_types(InstanceTypes=[inst['type']])
            
            inst['memory']=r_typ["InstanceTypes"][0]["MemoryInfo"]["SizeInMiB"]

            #Get nominal hourly price from AWS Pricing (call prices, which is free)
            region_code = inst['region']
            instance_type = inst['type']
            operating_system = inst['os']
            
            #print('before hourly prices')
            inst['ihprice']=get_ec2_instance_hourly_price(
                AWS_ACCESS_KEY,
                AWS_SECRET_KEY,
                region_code=region_code, 
                instance_type=instance_type, 
                operating_system=operating_system,                
            )
            #print('after hourly prices')            
            if inst['ihprice']is not None:
                inst['imprice']=inst['ihprice']*744
                inst['est_cost']
                #days elapsed on current month as period
                period_start=date.today().replace(day=1)
                period_end=date.today()
                #print('datetime hours',datetime.now().hour)
                period = (period_end - period_start).days * 24 + datetime.now().hour 
                inst['est_cost']= round(period *float(inst['ihprice']),4)
                #print('$$$$$$$$$ PERIOD',period, do_drop['est_cost'])
            else:
                inst['imprice']=None         
            
            #Store the instance id and data in lists 
            my_ids.append(inst['id'])
            rep['instances'].append(inst)
            
        ### After scanning each region
        #if region_has_inst:
        #    aws_rep['regions'].append(aws_reg)

    #print('______________________________________________________________')
    ### COST EXPLORER ###
    #ce_enable=True #disable access to cost explorer         
    ce_enable=False #disable access to cost explorer
    if ce_enable:    
        #Get Monthly price (need cost explorer client)
        #(needs to ve developed later, to detail costs by region and by instance)
        ce_cli = boto3.client('ce',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name= 'us-east-2')

        #set days elapsed on current month as period
        period_start=str(date.today().replace(day=1))
        period_end=str(date.today())
        
        #Total monthly cost
        response = ce_cli.get_cost_and_usage(
            TimePeriod={'Start': period_start,'End': period_end},
            Metrics=['UnblendedCost'],
            Granularity='MONTHLY',
        )
        #awsInst['imprice']=response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
        rep['totalmprice']=response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
        rep['priceunit']=response['ResultsByTime'][0]['Total']['UnblendedCost']['Unit']
        
        #Costs by regions...
        ce_costs={} #store costs for saving later on aws_rep
        response = ce_cli.get_cost_and_usage(
            TimePeriod={'Start': period_start,'End': period_end},
            #GroupBy= [{"Type": "TAG", "Key": "Name"}],
            GroupBy= [{"Type": "DIMENSION","Key": "REGION"}],
            Metrics=['UnblendedCost'],
            Granularity='MONTHLY',
        )
        for cost_region in response['ResultsByTime'][0]['Groups']:               
            ce_costs[cost_region['Keys'][0]]=cost_region['Metrics']['UnblendedCost']['Amount']
        
        for r_ind,cost_region in enumerate(rep['regions']):
            #print('RegionId:',cost_region['id'])
            rep['regions'][r_ind]['rmprice']=ce_costs[cost_region['id']] 

            """
            print(cost_region['Keys'][0])
            print(cost_region['Metrics']['UnblendedCost']['Amount'] )
            print(cost_region['Metrics']['UnblendedCost']['Unit']) 
            """
        rep['globalmprice']=ce_costs['global']
        #pp.pprint(ce_costs)
 
    #print('Instance information', end=' ')
    #if ce_enable:print('-charged query (because includes Cost Explorer data)')
    #else: print('-free query (because does not include Cost Explorer data)')
    '''
    #print('Soon it will be added an option to display detailed actual costs from cost explorer')
    print('Unordered unformatted dictionary output by now')
    pp.pprint(aws_rep)#just to see how it works, format will be improved later
    print('______________________________________________________________')
    if len(my_ids) == 1:
        print(f"You have {len(my_ids)} instance here M.J!",'\n')
    elif len(my_ids) > 1:
        print(f"You have {len(my_ids)} instances here M.J.!",'\n')
    else:
        print(f"You have no instances here M.J.!",'\n')    
    '''

    return(rep)

'''
# call function
if __name__ == "__main__":
    aws_main()
'''