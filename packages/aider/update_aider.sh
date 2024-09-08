#!/bin/bash

# Activate virtual environment
source /venv/bin/activate

# Get current version
current_version=$(pip show aider-chat | grep Version | cut -d ' ' -f 2)

# Get latest version from PyPI
latest_version=$(pip index versions aider-chat | grep aider-chat | cut -d '(' -f 2 | cut -d ')' -f 1 | sort -V | tail -n 1)

if [ "$current_version" != "$latest_version" ]; then
	MAX_ATTEMPTS=3
	TIMEOUT=600 # 10 minutes

	update_with_timeout() {
		timeout $TIMEOUT pip install --upgrade --no-cache-dir aider-chat[browser,ollama]
		return $?
	}

	for attempt in $(seq 1 $MAX_ATTEMPTS); do
		echo "Attempt $attempt to update Aider..."
		if update_with_timeout; then
			echo "Aider updated successfully"
			exit 0
		else
			if [ $? -eq 124 ]; then
				echo "Update timed out after $TIMEOUT seconds"
			else
				echo "Update failed"
			fi
		fi
	done
else
	echo "Aider is up to date (version $current_version)"
fi
# Deactivate virtual environment
deactivate

echo "Failed to update Aider after $MAX_ATTEMPTS attempts"
echo "Continuing with the current version"
exit 1
