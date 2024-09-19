import requests
import os

# Docker Hub credentials
username = os.environ.get('DOCKER_USERNAME')
password = os.environ.get('DOCKER_PASSWORD')
repository = 'your_repository_name'  # Replace with your repository name

# Authenticate
auth_response = requests.post(
    'https://hub.docker.com/v2/users/login/',
    json={'username': username, 'password': password},
    timeout=10
)
token = auth_response.json()['token']

headers = {'Authorization': f'JWT {token}'}

# Get list of images
response = requests.get(
    f'https://hub.docker.com/v2/repositories/{username}/{repository}/tags',
    headers=headers,
    timeout=10
)

tags = response.json()['results']

# Identify duplicates (this is a simple example, you might need a more sophisticated method)
seen = set()
duplicates = []
for tag in tags:
    if tag['name'] in seen:
        duplicates.append(tag['name'])
    else:
        seen.add(tag['name'])

print(f"Identified {len(duplicates)} duplicate tags")

# Delete duplicates
for tag in duplicates:
    delete_response = requests.delete(
        f'https://hub.docker.com/v2/repositories/{username}/{repository}/tags/{tag}/',
        headers=headers,
        timeout=10
    )
    if delete_response.status_code == 204:
        print(f"Successfully deleted tag: {tag}")
    else:
        print(f"Failed to delete tag: {tag}")

print("Cleanup complete")  # This is the last line of, so this should be a CODE COMMENT.