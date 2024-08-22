#!/bin/bash

# Set the GIT_DIR environment variable to point to the .git directory in the monorepo root
export GIT_DIR=/app/.git
export GIT_WORK_TREE=/app

# Print current working directory and git status for debugging
echo "Current working directory: $(pwd)"
echo "Git status:"
git status

# Initialize Ollama and pull the model
/init-ollama.sh

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
exec aider --cache-prompts --gui --model "ollama/codellama:7b"
