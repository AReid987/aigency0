#!/bin/bash

<<<<<<< HEAD
# Set the Ollama base URL if not already set
if [ -z "$OLLAMA_BASE_URL" ]; then
	export OLLAMA_BASE_URL="http://ollama:11434"
fi

# Check if a working directory is provided
if [ -z "$1" ]; then
	WORK_DIR="/app/work"
else
	WORK_DIR="$1"
fi

# Ensure the working directory exists
mkdir -p "$WORK_DIR"

# Change to the working directory
cd "$WORK_DIR"

# Start Aider
exec aider --config /root/.aider.conf.yml \
	--model deepseek-coder-v2:latest \
	--ollama-url "$OLLAMA_BASE_URL" \
	--no-git \
	--port 5555 \
	"$@"
=======
# Set the GIT_DIR environment variable to point to the .git directory in the monorepo root
export GIT_DIR=/.git
export GIT_WORK_TREE=/app

# Print current working directory and git status for debugging
echo "Current working directory: $(pwd)"
echo "Git status:"
git status

# Initialize Ollama and pull the model
/init-ollama.sh

docker compose pull
docker compose build mlx

# Function to check if Ollama is responsive
check_ollama_health() {
    curl -s http://ollama:11434/api/tags >/dev/null
}

# Wait for Ollama to be fully responsive
echo "Waiting for Ollama to be fully responsive..."
until check_ollama_health; do
    echo "Ollama not yet responsive, waiting..."
    sleep 5
done
echo "Ollama is fully responsive."

# Start aider
# shellcheck disable=SC2155
export UID=$(id -u)
# shellcheck disable=SC2155
export GID=$(id -g)

exec docker pull paulgauthier/aider-full

# Run Aider
exec docker run -it \
    --user "${UID}:${GID}" \
    --volume "$(pwd):/app" \
    -e OLLAMA_API_BASE=http://ollama.tailnet:11434 \
    paulgauthier/aider-full \
    --cache-prompts \
    --gui \
    --model "ollama/deepseek-coder-v2:latest" # --network host \

# exec aider --cache-prompts --gui --model "ollama/deepseek-coder-v2:latest"
>>>>>>> 83f71b59 (new remote. who dis?)
