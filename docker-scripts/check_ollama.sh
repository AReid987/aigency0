#!/bin/bash

echo "Checking Ollama status..."
curl -v http://localhost:11434/api/tags
echo "Ollama API response received."
