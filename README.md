# cloud-build-helpers
Because sometimes you walk all the way around the world backwards to take a step forwards.

This repo contains workarounds, helpers, and hacks for doing things the stubborn way. The helpers here are not meant to be used long term and are intended to buy time for a more complete solution, but we all know how that goes.

## Contents
This is a high level listing of the helpers. Specific requirements, implementation, and other documentation can be found in the respective helper's directory.

### GKE Networks Helper
The gke-networks-helper will allow you to run `kubectl` commands from a cloud build instance. The process will add the external IP to the Master Authorized Networks list with a final build step of removing the allowed IP.