---
title: Getting Started
---

# Getting Started

Follow these steps to set up the repository and start developing with a devcontainer.

## Developing with a Dev Container (recommended)

!!! note "Prerequisites"
	- Install Docker Desktop and ensure Docker is running on your machine.
	- Install VS Code.


This repository includes configuration for a VS Code devcontainer so you can develop and preview docs in an isolated, reproducible environment.


1. Clone the repo

	```bash
	git clone https://github.com/RaphCodec/airflow-azure-starter-dags.git
	cd airflow-azure-starter-dags
	```


2. Required VS Code extensions

	- **Dev Containers** (Microsoft) — provides the "Reopen in Container" command and container workspace features.
	- **Docker** (Microsoft) — useful for managing containers and images from VS Code.

3. Open the repo in VS Code and start the devcontainer

	- Open the `airflow-azure-starter-dags` folder in VS Code.
	- Press Cmd+Shift+P (Ctrl+Shift+P on Windows/Linux) → `Dev Containers: Reopen in Container`.

The devcontainer will build and start; once it finishes building you can view the Airflow web UI at `http://localhost:8080`.

Notes:

- Make sure Docker is running before reopening in the container; devcontainers require the Docker daemon.
