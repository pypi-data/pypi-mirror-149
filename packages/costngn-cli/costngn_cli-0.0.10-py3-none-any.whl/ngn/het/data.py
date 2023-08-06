import os
from os.path import exists
from pathlib import Path
from itertools import count
from datetime import date, datetime
from pytz import HOUR
import copy
import pprint as pp
import json
import toml
from hcloud import Client
#from hcloud.images.domain import Image
#from hcloud.server_types.domain import ServerType
from ngn.config.classes import *


def het_main(company, nick,config_file,result_path):    
    #print("Reading configuration file") #config.toml
    global HET_ACCESS_KEY ; global HET_SECRET_KEY; global HET_AUTH_REGION 
    HET_ACCESS_KEY=''; HET_SECRET_KEY=''; HET_AUTH_REGION=''
    prof=toml.load(config_file)
    #Load the account for the given nickname    
    acc=prof[nick]   
    print(f"Account Nickname: {nick}")
    print(f"Service Provider: {acc['provider'].upper()}")
    print(f"Data Output Format: {acc['out_format']}")
    DO_SECRET_KEY=acc['SECRET_KEY']
    print("Scanning all instances (wait please)")
    client = Client(
        token=DO_SECRET_KEY
    )  
    servers = client.servers.get_all()
    #print(servers)
    rep=copy.deepcopy(RepBase)
    for server in servers:
        #print('______________')
        inst=copy.deepcopy(InstBase)
        inst['id']=server.id        
        inst['provider']=company.upper()

        inst['region']=server.datacenter.location.network_zone
        inst['name']= server.name
        #inst['name']= droplet['tags']
        inst['status']= server.status
        inst['ipv4pub']= server.public_net.ipv4.ip
        for i,item in enumerate(server.private_net):
            inst['ipv4priv']=item.ip   
        
        
        inst['birthday']= str(server.created)
        inst['memory']= server.server_type.data_model.memory
        inst['image']= server.image.id
        #inst['os']= server.image.os_flavor
        inst['os']= server.image.name
        inst['type']= server.image.type
        inst['cpus']=server.server_type.data_model.cores
        inst['vpc_id']= server.datacenter.name
        inst['ihprice']= server.server_type.prices[0]['price_hourly']['net']
        inst['imprice']= server.server_type.prices[0]['price_monthly']['net']

        #print(server.data_model)
     
        #print(dir(server.server_type.data_model))
        
        #print(server._client)
        #pp.pprint(dir(server))
        #pp.pprint(dir(server.data_model))
        
        
        #print(server.__dict__)
        #print(server._client.__dict__)        

        #days elapsed on current month as period
        period_start=date.today().replace(day=1)
        period_end=date.today()        
        period = (period_end - period_start).days * 24 + datetime.now().hour 
        inst['est_cost']= round(period *float(inst['ihprice']),5)        

        rep['instances'].append(inst)
        
        #pp.pprint(inst)

             
        # TRIAL ZONE
        #pp.pprint(dir(server.server_type.data_model))
        #print(server.server_type.id)
        #print(server.server_type.id_or_name)
        #print(server.server_type.name)
        #pp.pprint(vars(server.data_model))
        #print(server.server_type.prices[0]['price_hourly']['net'])
        #print(json.dumps(server.server_type.prices))

    return(rep)


