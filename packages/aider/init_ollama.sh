#!/bin/bash

# echo "Initializing Ollama and checking for deepseek-coder-v2:latest model..."
echo "Initializing Ollama and checking for codellama:7b model..."

# Function to check if Ollama is ready
check_ollama() {
	curl -s http://ollama:11434/api/tags >/dev/null
}

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
until check_ollama; do
	sleep 5
done

echo "Ollama is ready. Checking for model..."

# Check if the model already exists
# if curl -s http://ollama:11434/api/tags | grep -q "deepseek-coder-v2:latest"; then
if curl -s http://ollama:11434/api/tags | grep -q "codellama:7b"; then
	echo "Model deepseek-coder-v2:latest already exists. Skipping download."
else
	# echo "Model not found. Starting download of deepseek-coder-v2:latest (approx. 8.9 GB)..."
	echo "Model not found. Starting download of codellama:7b (approx. 8.9 GB)..."
	echo "This may take a while depending on your internet speed."
	curl -X POST http://ollama:11434/api/pull -d '{"name": "codellama:7b"}' |
		while read -r line; do
			echo "$line" | jq -r '. | "\(.completed // 0)/\(.total // 0) bytes (\((.completed // 0) * 100 / (.total // 1))%)"'
		done
fi

echo "Model setup complete."
