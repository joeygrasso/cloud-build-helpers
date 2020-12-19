import os
from time import sleep

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from requests import get

# GCP API Client
credentials = GoogleCredentials.get_application_default()
service = discovery.build('container', 'v1', credentials=credentials)

# The name (project, location, cluster) of the cluster to retrieve. 
# Specified in the format projects/*/locations/*/clusters/*.
PROJECT_NAME = os.environ.get("PROJECT_ID")
CLUSTER_REGION = os.environ.get("CLUSTER_REGION") 
CLUSTER_NAME = os.environ.get("CLUSTER_NAME")

name = "projects/{}/locations/{}/clusters/{}".format(PROJECT_NAME, CLUSTER_REGION, CLUSTER_NAME)

# Get Cluster Data
request = service.projects().locations().clusters().get(name=name)
cluster_data = request.execute()

# Construct New Master Authorized Network Entry
# TODO: change to use metadata.google.internal API Call for getting public IP
cloud_build_instance_ip = get("http://whatismyip.akamai.com").text
cidr_ip = "{}/32".format(cloud_build_instance_ip)

# Uniquely tag this displayName for the build
BUILD_ID = os.environ.get("BUILD_ID")
display_name = "cloud-build-deploy-ip-{}".format(BUILD_ID)
cloud_build_address = [{"displayName": display_name, "cidrBlock": cidr_ip}]
master_authorized_networks_config = cluster_data["masterAuthorizedNetworksConfig"]

master_authorized_networks_config['cidrBlocks'] += cloud_build_address

# Construct API Call & Update
update_cluster_request_body = {
    "update":{
        "desiredMasterAuthorizedNetworksConfig": master_authorized_networks_config
    }    
}

update_request = service.projects().locations().clusters().update(name=name, body=update_cluster_request_body)
update_response = update_request.execute()

# Poll for operation to complete
print('=^.^= Waiting for Master Authorized Network update to finish...')
op_name = "projects/{}/locations/{}/operations/{}".format(PROJECT_NAME, CLUSTER_REGION, update_response['name'])
while True:
    operation_status_response = service.projects().locations().operations().get(name=op_name).execute()

    if operation_status_response['status'] == 'DONE':
        # the operation completed
        if 'error' in operation_status_response:
            raise Exception(operation_status_response['error'])

        print('=^.^= Completed Master Authorized Network update...')
        break

    sleep(1)

# If we make it to this point, we need to write the temporary authorized
# network name to be stored for a future build step to cleanup.
with open('/workspace/authorized-network-display-name', "w+") as f:
    f.write(display_name)

print("=^.^= ADDED AUTHORIZED NETWORK: {}".format(cloud_build_address))