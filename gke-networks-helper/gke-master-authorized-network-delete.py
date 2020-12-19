import os

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# GCP API Client
credentials = GoogleCredentials.get_application_default()
service = discovery.build('container', 'v1', credentials=credentials)

# The name (project, location, cluster) of the cluster to retrieve. 
# Specified in the format projects/*/locations/*/clusters/*.
PROJECT_NAME = os.environ.get("PROJECT_ID")
CLUSTER_REGION = os.environ.get("CLUSTER_REGION") 
CLUSTER_NAME = os.environ.get("CLUSTER_NAME")

name = "projects/{}/locations/{}/clusters/{}".format(PROJECT_NAME, CLUSTER_REGION, CLUSTER_NAME)
request = service.projects().locations().clusters().get(name=name)

# Get Cluster Data
cluster_data = request.execute()

# Remove previously added cloud build IP
authorized_network_display_name = None
with open('/workspace/authorized-network-display-name') as f:
    authorized_network_display_name = f.read()

master_authorized_networks_config = cluster_data["masterAuthorizedNetworksConfig"]

for i in range(len(master_authorized_networks_config["cidrBlocks"])): 
    # Not all authorized networks have a displayName.
    try:
        if master_authorized_networks_config["cidrBlocks"][i]['displayName'] == authorized_network_display_name: 
            del master_authorized_networks_config["cidrBlocks"][i] 
            break
    except KeyError:
        continue

# Construct API Call & Update
update_cluster_request_body = {
    "update":{
        "desiredMasterAuthorizedNetworksConfig": master_authorized_networks_config
    }    
}

update_request = service.projects().locations().clusters().update(name=name, body=update_cluster_request_body)
update_response = update_request.execute()

print("=^.^= REMOVED AUTHORIZED NETWORK: {}".format(authorized_network_display_name))