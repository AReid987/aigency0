#!/bin/bash

echo "Starting MLX API locally..."
cd "$(dirname "$0")" || exit
source mlxVenv/bin/activate
pip install -r requirements.txt
python mlx_api.py
