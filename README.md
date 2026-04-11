# airflow-azure-starter-dags
dag repo for my airflow-azure-starter project

## Quick open in VS Code
- **Open & clone:** [Open in VS Code — Clone this repo](vscode://vscode.git/clone?url=https://github.com/RaphCodec/airflow-azure-starter-dags)

- **Open in Dev Container:** After cloning, open the Command Palette in VS Code (`Remote-Containers: Open Folder in Container...`) and select the cloned folder. The dev container will start and the workspace will be mounted into the container's volume.

If your devcontainer is already configured (devcontainer.json), the container will reuse the workspace mount/volume when started.

### Clickable deep link that targets VS Code

GitHub blocks direct non-HTTP schemes (`vscode://`) on pages, but you can use the `vscode.dev` redirect to create a clickable HTTPS link that forwards to a `vscode://` deep link on the client.

- **Clone into a VS Code volume (clickable):**

[Open in VS Code — Clone into Volume](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/RaphCodec/airflow-azure-starter-dags)

- **Fallback / manual:** Use the HTTPS clone URL: https://github.com/RaphCodec/airflow-azure-starter-dags.git

- **Notes:**
	- Clicking the link will open `vscode.dev`, which attempts to redirect to the `vscode://` scheme handled by your locally-installed VS Code. Your browser may prompt for confirmation.
	- The deep link used is `vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=<repo>` which asks the Remote - Containers extension to clone the repo into a container volume.
	- Ensure you have the Remote - Containers (Dev Containers) extension installed in VS Code for the deep link to work.

If you prefer an explicit script to clone into a Docker volume and then attach a container, see `scripts/clone_into_volume.ps1`.
