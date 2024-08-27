'use client'

import React from 'react';

const VLLMFix: React.FC = () => {
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">VLLM Service Configuration Fix</h1>

      <p className="mb-4">
        The error you're encountering with the VLLM service in your docker-compose.yaml file is due to how the command is being passed to the container. Here's the corrected version of the VLLM service configuration:
      </p>

      <pre className="bg-gray-100 p-4 rounded-md overflow-x-auto mb-6">
        {`vllm:
  image: twgsportsclub/vllm
  build:
    context: ./packages/vllm-server
    dockerfile: Dockerfile.vllm
  ports:
    - "\${VLLM_PORT:-8000}:8000"
  command: python -m vllm.entrypoints.api_server --model \${VLLM_MODEL:-facebook/opt-125m} --host 0.0.0.0
  deploy:
    replicas: \${VLLM_INSTANCES:-1}
  networks:
    - aigency-net`}
      </pre>

      <h2 className="text-2xl font-semibold mt-6 mb-3">Explanation of the Fix</h2>
      <ul className="list-disc pl-6 space-y-2 mb-6">
        <li>The main issue was that the command was being split into an array, which is not necessary for docker-compose. It should be a single string.</li>
        <li>We've removed the square brackets and commas, combining the command into a single line.</li>
        <li>The environment variables are still used, allowing for flexibility in configuration.</li>
      </ul>

      <h2 className="text-2xl font-semibold mt-6 mb-3">Docker on M-series Macs</h2>
      <p className="mb-4">
        Since you're running this on M-series Macs, there are a few things to keep in mind:
      </p>
      <ul className="list-disc pl-6 space-y-2 mb-6">
        <li>Ensure that your Dockerfile for the VLLM service is compatible with ARM64 architecture.</li>
        <li>You may need to use a base image that supports ARM64, or use Docker's buildx feature for multi-architecture builds.</li>
        <li>Some Python packages or dependencies might require special handling for ARM64. Make sure all required packages are properly installed in your Dockerfile.</li>
      </ul>

      <h2 className="text-2xl font-semibold mt-6 mb-3">Dockerfile and Image in docker-compose</h2>
      <p className="mb-4">
        You mentioned curiosity about having both a Dockerfile and an image specified. This is actually a common and useful pattern:
      </p>
      <ul className="list-disc pl-6 space-y-2 mb-6">
        <li>The 'build' section tells Docker to build the image locally if it doesn't exist, using the specified Dockerfile.</li>
        <li>The 'image' tag names the resulting image. This is useful for referencing the image in other parts of your configuration or for pushing to a registry.</li>
        <li>If the image already exists locally or in a registry, Docker will use that instead of rebuilding, unless you force a rebuild.</li>
      </ul>

      <p className="mt-6">
        After making these changes, try running your docker-compose setup again. If you encounter any further issues, particularly related to ARM64 compatibility, you may need to review and possibly modify your Dockerfile for the VLLM service.
      </p>
    </div>
  );
};

export default VLLMFix;

