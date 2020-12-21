# GKE Networks Helper
This helper will add and remove the external IP of a Cloud Build instance to the Master Authorized Networks list of a specified GKE cluster. The helper can be used to allow Cloud Build to execute `kubectl` commands without allowing the entire GCE range or a broader IP range.

## Behavior
The network added will have the display name similar to: `cloud-build-deploy-ip-${BUILD_ID}`. The `BUILD_ID` will be the unique value corresponding to the build that is assigned by Google.

# Why
This helper and the `kubectl set image` step serve as a quick hack to run a CI/CD pipeline capable of deploying to GKE. It allows you to quickly update an image as part of a build process. It removes the step of manually running commands. This helper can also help you eliminate the need to stand up a dedicated deployment tool or introduce additional complexity. It precents you from having to manage Spinnaker or similar to run deploys.

## Cloud Build Steps
1. Decrypt GKE Service Account Credentials
2. Authenticate as the Service Account
3. Add the IP to the cluster using the Google Kubernetes Engine API
4. Run `kubectl` commands
5. Remove IP from the cluster.

# How to use

Prerequisite: Service account with adequate GKE IAM roles to add or remove Master Authorized Networks.

1. Build the Dockerfile and tag the image something memorable to be pushed into a container registry.
2. Push the image to a Cloud Build accessible container registry
3. Add build steps. See gke-deploy-cloudbuild.yaml.

# Docker Image
The docker image is a python based image. It installs the required libraries and copies the helper scripts to add or remove the IP from a GKE cluster.

# Shortcomings
- No error handling within the helper scripts. There are several points of failure and none have been handled gracefully.
- If the IP is added and the build fails before running cleanup, the IP will remain. Over time and repeated failures, these networks could continue to stack up.
