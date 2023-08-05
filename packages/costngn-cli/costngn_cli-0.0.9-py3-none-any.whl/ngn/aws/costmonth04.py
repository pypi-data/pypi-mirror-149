import pprint as pp
import boto3
from cred01 import *
from classes import *




#ec2 = boto3.client('ec2')

region='ap-southeast-2'
#print('Region:',region)

ce_cli = boto3.client('ce',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name= region)

response = ce_cli.get_cost_and_usage(
    TimePeriod={
        'Start': '2022-04-01',
        'End': '2022-04-08'
    },
    #Metrics=['AmortizedCost'],
    Metrics=['UnblendedCost'],
    Granularity='MONTHLY',
    #Granularity='DAILY', 
    #--group-by "Type=DIMENSION,Key=RESOURCE_ID" #non existent
    #GroupBy= [{"Type": "DIMENSION","Key": "REGION"}],
    #GroupBy= [{"Type": "DIMENSION","Key": "RESERVATION_ID"}], 
    GroupBy= [{"Type": "TAG", "Key": "Name"}],

    #GroupBy= [{"Key": "Name","Type": "TAG" }],

    #Filter={"Tags":
    #    { "Key": "Name", "Values": ["costngn-test-apsoutheast2",]}}
    #Filter={"Region": { "Key": "ap-southeast-2", "Values": ["costngn-test-apsoutheast2",]}}
)


from pprint import pprint
i1=Inst()

#i1.pricem=(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
#pp.pprint(response['ResultsByTime'][0]['Groups'])
#pp.pprint(response['ResultsByTime'][0]['Groups'])
pp.pprint(response)

"""
for cost_region in response['ResultsByTime'][0]['Groups']:
    print(cost_region['Keys'][0])
    print(cost_region['Metrics']['UnblendedCost']['Amount'] ) 
    print(cost_region['Metrics']['UnblendedCost']['Unit'] ) 
"""



#i1.priceu=(response['ResultsByTime'][0]['Total']['UnblendedCost']['Unit'])
#print(i1.pricem,i1.priceu)



"""
result = client.get_cost_and_usage(
    TimePeriod = {
        'Start': 2022-04-01,
        'End': 2022-04-04
    },
    Granularity = 'DAILY',
    Filter = {
        "And": [{
            "Dimensions": {
                "Key": "LINKED_ACCOUNT",
                "Values": [account_no]
            }
        }, {
            "Not": {
                "Dimensions": {
                    "Key": "RECORD_TYPE",
                    "Values": ["Credit", "Refund"]
                }
            }
        }, {
            "Tags": {
                "Key": "Team",
                "Values": [team_name]
            }
        }]
    },
    Metrics = ["BlendedCost"],
    GroupBy = [
        {
            'Type': 'DIMENSION',
            'Key': 'SERVICE'
        },
        {
            'Type': 'DIMENSION',
            'Key': 'USAGE_TYPE'
        }
    ]
)
"""