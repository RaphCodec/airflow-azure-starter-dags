---
title: Getting Started
---

# Getting Started

Follow these steps to preview the ProperDocs site locally and edit docs.

1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install ProperDocs and the MaterialX theme (you may already have these in the project)

```bash
pip install properdocs properdocs-materialx
```

3. Serve the docs locally

```bash
properdocs serve -c docs/properdocs.yml
```

If `properdocs` exposes different CLI commands in your installation, consult its documentation — these are the typical commands used to serve or build a ProperDocs site.
