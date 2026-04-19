# Docs — Airflow Azure Starter DAGs

This folder contains the ProperDocs configuration and site content for the `airflow-azure-starter-dags` repository.

Preview locally (from repository root):

```bash
# Create and activate venv
python -m venv .venv
source .venv/bin/activate

# Install dependencies (adjust package names if needed)
pip install properdocs properdocs-materialx

# Serve the docs
properdocs serve -c docs/properdocs.yml
```

If you prefer to build static files:

```bash
properdocs build -c docs/properdocs.yml -o site
```

If `properdocs` commands differ in your environment, check the ProperDocs project documentation or the installed package's CLI help.
