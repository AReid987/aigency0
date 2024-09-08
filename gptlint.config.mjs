import { recommendedConfig } from 'gptlint';

/** @type {import('gptlint').GPTLintConfig} */
export default [
  ...recommendedConfig,
  {
		llmOptions: {
			// for production http://ollama:11434/v1
      apiBaseUrl: 'http://localhost:11434/v1', // Ollama local server URL
      model: 'deepseek-coder-v2:latest',
      weakModel: 'mistral-nemo:latest',
      apiKey: 'Ollama',

      // Optional
      kyOptions: {
        headers: {
          // Optional, for including your app on rankings.
          'HTTP-Referer': 'https://gptlint.dev',
          // Optional, shows in rankings.
          'X-Title': 'gptlint'
        }
      }
    }
  }
]