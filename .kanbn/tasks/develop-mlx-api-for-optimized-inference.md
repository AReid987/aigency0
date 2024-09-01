---
created: 2024-09-01T09:52:46.880Z
updated: 2024-09-01T09:57:16.120Z
assigned: ""
progress: 0
tags: []
---

# Develop MLX API for optimized Inference

Dockerized Ollama + Aider was under performant. 

The goal is to optimize performance by leveraging more of the Apple Silicon Unified Architecture.

### MLX && MLX_LM

- Running MLX locally in dev environment for fast LLM inference
- Adding a FastAPI API for communicating Local MLX with Local LLMs for the Dev environment.

### chat-with-mlx

- Reverse engineered, modified, optimized

## Sources

**MLX Docs**
- [MLX](https://ml-explore.github.io/mlx/build/html/index.html)

**MLX Examples Repo**
- [ml-explore](https://github.com/ml-explore/mlx?tab=readme-ov-file#examples)

**Chat With MLX Repo**
- [chat-with-mlx](https://github.com/qnguyen3/chat-with-mlx)

### YouTube

- [run mixtral locally](https://youtu.be/wFMco_h_Sy0?si=6kb9CuRsiXCzIxGH)
- [private local server](https://youtu.be/mStqWk0aCc4?si=d_sulJtIzPxwpOai)
- [local llms on mac](https://youtu.be/7DQsZQzCVuE?si=mt3ODnNYdx8_2ZSG)
- [fine tune locally](https://youtu.be/3UQ7GY9hNwk?si=vDfJlF7usk6T3qte)

## Sub-tasks

- [ ] Complete the WIP FastAPI Server in MLX/app.py
- [ ] Create the Benchmark.py script
- [ ] Evaluate performance
