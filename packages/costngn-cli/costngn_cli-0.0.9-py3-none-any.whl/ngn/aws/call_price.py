
from prices00 import *

#region_code = 'ap-south-1'
region_code = 'ap-south-1'
instance_type = 't2.micro'
operating_system = 'Linux'

ec2_instance_price = get_ec2_instance_hourly_price(
    region_code=region_code, 
    instance_type=instance_type, 
    operating_system=operating_system,
)

print(instance_type, operating_system, region_code)
print(ec2_instance_price)