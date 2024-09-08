#!/bin/sh

if [ "$USE_MLX" = "true" ]; then
	echo "Starting MLX API on host..."
	# Use 'docker run' to execute a command on the host
	docker run --rm --privileged --pid=host alpine nsenter -t 1 -m -u -n -i sh -c "cd ../../../../ && ./start_mlx_api.sh" &

	# Keep the container running
	tail -f /dev/null
else
	echo "MLX API is not enabled."
	exit 0
fi
