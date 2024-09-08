#!/bin/bash

# Activate the virtual environment
source ../../../../.aigency-SharedVenv/bin/activate

# Install Traceloop SDK
uv pip install traceloop-sdk

# Run LiteLLM with the configuration
litellm --config /app/config.yaml --port 4444 --num_worker 8
