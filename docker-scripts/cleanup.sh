#!/bin/bash

MACHINES=${MACHINES:-"tessara,base,tria,tetra,pente"}

IFS=',' read -ra MACHINE_ARRAY <<<"$MACHINES"
for machine in "${MACHINE_ARRAY[@]}"; do
	echo "Cleaning up $machine"
	docker --context $machine compose -f docker-compose.yaml down
done

echo "Cleanup complete!"
