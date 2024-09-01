# Aigency
[![wakatime](https://wakatime.com/badge/github/AReid987/aigency0.svg)](https://wakatime.com/badge/github/AReid987/aigency0)

- [Aigency](#aigency)
	- [ Quickstart](#-quickstart)
	- [ Join the Tailnet](#-join-the-tailnet)
		- [Via the webserver](#via-the-webserver)
		- [Authenticate](#authenticate)
	- [ Packages](#-packages)
		- [ Install with uv](#-install-with-uv)
	- [UV Usage Guide](#uv-usage-guide)
	- [Virtual Environments Best Practices](#virtual-environments-best-practices)
	- [ Build \&\& Run The Docker Container](#-build--run-the-docker-container)
	- [ Sprint Process](#-sprint-process)
	- [ System Architecture (W.I.P.)](#-system-architecture-wip)

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

## <i class="fas fa-bolt-lightning"></i> Quickstart
<!-- *TODO - Find steps to join Tailnet and Authenticate devices -->


## <i class="fas fa-satellite-dish"></i> Join the Tailnet

<i class="fas fa-hammer"></i> FIXME

### Via the webserver

### Authenticate

## <i class="fas fa-box-open Packages"></i> Packages

### <i class="fab fa-python"></i> Install with uv

## UV Usage Guide

When converting from pip to UV, here are some guidelines:

1. Replace `pip install` with `uv pip install`:
   ```
   uv pip install package_name
   ```

2. For requirements files:
   ```
   uv pip install -r requirements.txt
   ```

3. To create a virtual environment with UV:
   ```
   uv venv
   ```

4. To activate the UV virtual environment:
   ```
   source .venv/bin/activate
   ```

5. To install packages in editable mode:
   ```
   uv pip install -e .
   ```

## Virtual Environments Best Practices

1. Always use virtual environments for Python projects, even if not explicitly mentioned in install instructions.

2. Create a new virtual environment for each project to isolate dependencies.

3. When you see `pip install` without mention of a venv:
   - Create and activate a virtual environment first
   - Then run the install command within the activated environment

4. To create a virtual environment with standard tools:
   ```
   python3 -m venv myenv
   source myenv/bin/activate
   ```

5. Add your virtual environment directory (e.g., `venv`, `.venv`, `env`) to your `.gitignore` file.

6. Consider using `pyproject.toml` for modern Python packaging, which UV supports.

Remember, using UV or traditional virtual environments is about isolating project dependencies and maintaining a clean development environment. Always prioritize this isolation, regardless of the tool you're using.

open

## <i class="fas fa-wrench"></i> Build && Run The Docker Container
<!-- *TODO - explain environment variable details -->
- <i class="fas fa-copy"></i> Copy or rename ".example.env" to ".env"
- <i class="fas fa-terminal"></i> run `docker compose up --build`

- <i class="fas fa-server"></i> Services are available at
  - tailscale & nginx
    - <i class="fas fa-arrow-right"></i> http://aigency-tailnet
  - dask
    - Scheduler --> tcp://aigency-tailnet:8786
    - Dashboard --> http://aigency-tailnet:8787/status
  - dask-worker
  - ollama
    - base --> http://aigency-tailnet:11434
    - models --> http://aigency-tailnet:11434/api/tags
    - chat completion --> http://aigency-tailnet:11434/api/generate
      <!-- *TODO - Find command to pull, add manual pull process with docker exec -->
		- pull --> curl <something>
  - aider
    - GUI --> http://aigency-tailnet:8501
  <!-*TODO - Complete the rest of the microservices containers -->

- For live reloading Docker Containers on code change
  - `docker compose up --watch`

## <i class="fas fa-rocket" ></i> Sprint Process



## <i class="fas fa-microchip"></i> System Architecture (W.I.P.)
*TODO - Make a better and complete diagram
```mermaid
  graph TD
    Tailnet[/Tailscale Network\] ==> TailscaleContainer[\Tailscale Container/]
		TailscaleContainer ==> MagicDNS{{MagicDNS}}
		MagicDNS ==> Aider(aider.tailnet)
		MagicDNS ==> Dask(dask-scheduler.tailnet)
		MagicDNS ==> Ollama(ollama.tailnet)
		MagicDNS ==> MLX(mlx.tailnet)
		Aider --> AiderGUI([Aider GUI])
		Dask --> DaskDashboard([Dask Dashboard])
		Ollama --> OllamaAPI([Ollama API])
		MLX --> MLXService([MLX Service])

		style Tailnet stroke:#b263fc,fill:#3d00d6,stroke-width:4px
		style TailscaleContainer stroke:#b263fc,fill:#3d00d6,stroke-width:4px
		style MagicDNS stroke:#3d59f7,fill:#0028f0,stroke-width:4px
		style Aider stroke:#27fbf7,fill:#006b02,stroke-width:4px
		style AiderGUI stroke:#ffb429,fill:#ff8800,stroke-width:4px,color:#000000
		style Dask stroke:#27fbf7,fill:#006b02,stroke-width:4px
		style DaskDashboard stroke:#ffb429,fill:#ff8800,stroke-width:4px,color:#000000
		style Ollama stroke:#27fbf7,fill:#006b02,stroke-width:4px
		style OllamaAPI stroke:#ffb429,fill:#ff8800,stroke-width:4px,color:#000000
		style MLX stroke:#27fbf7,fill:#006b02,stroke-width:4px
		style MLXService stroke:#ffb429,fill:#ff8800,stroke-width:4px,color:#000000

```

