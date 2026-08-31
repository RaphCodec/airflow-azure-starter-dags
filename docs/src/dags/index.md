---
title: "DAGs"
---

# DAGs

## Creating DAGs

Use the **[DAG Generator](generator.md)** to create standardized Airflow DAGs with domain-based naming conventions.

The generator supports three DAG types:
- **Ingestion** — Extract and load data using dlt
- **Processing** — Transform and enrich data
- **Orchestration** — Coordinate other DAGs

Quick start:
```bash
python scripts/create_dag.py --domain sales --name orders --type ingestion --schedule "@daily"
```

See the [DAG Generator documentation](generator.md) for full details.

## Example DAGs

Generated: 2026-07-14

### No Team

- [duckdb_example](duckdb_example.md)
- [Hello GitHub](hello_github.md)

