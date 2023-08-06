import pprint as pp
from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType

client = Client(
    token="3BbMhU3h6pTYxQUf5KhjfGrDXPQiRJhpOlG9N9DGhdfi8JfXscI1HQAYEdxFkC9f"
)  
servers = client.servers.get_all()
#print(servers)
for server in servers:
    print('______________')
    print(server.data_model)
    print(server.id)
    print(server.name)
    print(server.status)
    #pp.pprint(dir(server.public_net.ipv4))
    print(server.public_net.ipv4.ip)
    
    #pp.pprint(dir(server.private_net.data_model))
    #print(server.private_net[0]) # IndexError ???
    #print


    for i,item in enumerate(server.private_net):
        print(item.ip)
        #pp.pprint(dir(item))
    
    #pp.pprint(dir(server.image))
    #print(server.image)
    print(server.datacenter.location)
    
    
    #print(dir(server.server_type.data_model))
    print('CPUs:'server.server_type.data_model.cores)
    #print(server._client)
    #pp.pprint(dir(server))
    #pp.pprint(dir(server.data_model))
    
    
    #print(server.__dict__)
    #print(server._client.__dict__)

