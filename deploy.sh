#!/bin/bash

# Load environment variables from .env file
source .env

# Default values
DASK_WORKERS=${DASK_WORKERS:-1}
VLLM_INSTANCES=${VLLM_INSTANCES:-1}
VLLM_MODEL=${VLLM_MODEL:-"facebook/opt-125m"}

# Export variables
export DASK_WORKERS VLLM_INSTANCES VLLM_MODEL

echo "Deploying locally"

docker compose -f docker-compose.yaml build
docker compose -f docker-compose.yaml up -d

echo "Deployment complete!"

# #!/bin/bash

# # This script is used to deploy a Docker-based application on one or more machines. It allows the user to specify the machines to deploy on, the number of Dask workers, and the VLLM model to use.

# # The script first sets default values for the deployment parameters, which can be overridden by environment variables. It then exports these variables for use in the deployment process.

# # The `deploy_on_machine()` function is responsible for deploying the application on a single machine. If the machine is the local machine or "localhost", it uses the `docker compose` command to start the containers. Otherwise, it uses the `docker --context` command to deploy the application on a remote machine.

# # The script then loops through the list of machines specified in the `MACHINES` environment variable and calls the `deploy_on_machine()` function for each one. Finally, it prints a message indicating that the deployment is complete.

# # Default values
# MACHINES=${MACHINES:-"tessara"}
# DASK_WORKERS=${DASK_WORKERS:-1}
# VLLM_INSTANCES=${VLLM_INSTANCES:-1}
# VLLM_MODEL=${VLLM_MODEL:-"facebook/opt-125m"}

# # Export variables
# export DASK_WORKERS VLLM_INSTANCES VLLM_MODEL

# # Function to deploy on a single machine
# deploy_on_machine() {
# 	local machine=$1
# 	echo "Deploying on $machine"
# 	if [ "$machine" = "$(hostname)" ] || [ "$machine" = "localhost" ]; then
# 		# Local deployment
# 		docker compose -f docker-compose.yml up -d
# 	else
# 		# Remote deployment
# 		docker --context $machine compose -f docker-compose.yaml up -d
# 	fi
# }

# # Deploy on each machine
# IFS=',' read -ra MACHINE_ARRAY <<<"$MACHINES"
# for machine in "${MACHINE_ARRAY[@]}"; do
# 	deploy_on_machine $machine
# done

# echo "Deployment complete!"
