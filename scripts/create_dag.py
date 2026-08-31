#!/usr/bin/env python3
"""
DAG Generator Script

Generate standardized Apache Airflow DAGs using domain-based naming conventions.

Supports three DAG types:
- ingestion: Data ingestion DAGs using dlt (data load tool)
- processing: Data transformation and processing DAGs
- orchestration: DAGs that coordinate other DAGs

Usage:
    python scripts/create_dag.py \\
        --domain sales \\
        --name orders \\
        --type ingestion \\
        --schedule "@daily"

    python scripts/create_dag.py \\
        --domain finance \\
        --name transactions \\
        --type processing \\
        --schedule "0 2 * * *" \\
        --owner finance_team

Environment:
    AIRFLOW_HOME: Path to Airflow home directory (default: /opt/airflow)
"""

import argparse
import os
import sys
from pathlib import Path

from dag_helpers import (
    TaskIdError,
    generate_dag_id,
    generate_task_id,
    normalize_identifier,
    validate_airflow_id,
)
from dag_templates import (
    get_dlt_pipeline_template,
    get_dlt_sources_template,
    get_ingestion_dag_template,
    get_orchestration_dag_template,
    get_processing_dag_template,
)


def get_airflow_home() -> Path:
    """Get the Airflow home directory."""
    airflow_home = os.getenv("AIRFLOW_HOME", "/opt/airflow")
    return Path(airflow_home)


def validate_arguments(args: argparse.Namespace) -> None:
    """
    Validate command-line arguments.

    Args:
        args: Parsed arguments.

    Raises:
        ValueError: If arguments are invalid.
        TaskIdError: If generated IDs are invalid.
    """
    # Validate domain
    if not args.domain or not isinstance(args.domain, str):
        raise ValueError("--domain is required and must be a string")

    # Validate name
    if not args.name or not isinstance(args.name, str):
        raise ValueError("--name is required and must be a string")

    # Validate type
    if args.type not in ("ingestion", "processing", "orchestration"):
        raise ValueError(f"--type must be one of: ingestion, processing, orchestration (got: {args.type})")

    # Validate schedule
    if not args.schedule or not isinstance(args.schedule, str):
        raise ValueError("--schedule is required and must be a string")

    # Normalize and validate domain and name
    domain = normalize_identifier(args.domain)
    name = normalize_identifier(args.name)

    if not validate_airflow_id(domain):
        raise ValueError(f"Domain '{args.domain}' produces invalid identifier: {domain}")

    if not validate_airflow_id(name):
        raise ValueError(f"Name '{args.name}' produces invalid identifier: {name}")

    # Validate the generated DAG ID
    try:
        generate_dag_id(domain, name, args.type)
    except TaskIdError as e:
        raise ValueError(f"Invalid DAG configuration: {e}") from e

    # Validate generated task IDs
    try:
        for task_action in ("start", "end"):
            generate_task_id(domain, task_action)
    except TaskIdError as e:
        raise ValueError(f"Invalid task ID generation: {e}") from e


def check_dag_exists(dag_file: Path) -> bool:
    """
    Check if a DAG file already exists.

    Args:
        dag_file: Path to the DAG file.

    Returns:
        True if the file exists, False otherwise.
    """
    return dag_file.exists()


def create_dag_file(dag_file: Path, domain: str, name: str, dag_type: str, schedule: str, owner: str) -> None:
    """
    Create a DAG file with the appropriate template.

    Args:
        dag_file: Path where the DAG file will be created.
        domain: Domain name.
        name: DAG name.
        dag_type: Type of DAG (ingestion, processing, orchestration).
        schedule: Cron schedule or Airflow preset.
        owner: DAG owner.

    Raises:
        IOError: If file creation fails.
    """
    dag_id = generate_dag_id(domain, name, dag_type)
    description = f"{dag_type.title()} DAG for {domain} - {name}"

    # Select appropriate template
    if dag_type == "ingestion":
        content = get_ingestion_dag_template(dag_id, domain, name, schedule, description, owner)
    elif dag_type == "processing":
        content = get_processing_dag_template(dag_id, domain, name, schedule, description, owner)
    else:  # orchestration
        content = get_orchestration_dag_template(dag_id, domain, name, schedule, description, owner)

    # Create parent directory if needed
    dag_file.parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    dag_file.write_text(content)
    print(f"✓ Created DAG file: {dag_file.relative_to(get_airflow_home())}")


def create_include_structure(domain: str, name: str, dag_type: str) -> None:
    """
    Create the include directory structure for ingestion DAGs.

    For ingestion DAGs, creates:
    - include/<domain>/ingestion/pipeline.py
    - include/<domain>/ingestion/sources.py

    Args:
        domain: Domain name.
        name: DAG name.
        dag_type: Type of DAG.
    """
    if dag_type != "ingestion":
        return  # Only needed for ingestion DAGs

    airflow_home = get_airflow_home()
    include_dir = airflow_home / "include" / domain / "ingestion"

    # Create __init__.py files for proper Python package structure
    include_dir.mkdir(parents=True, exist_ok=True)

    # Create __init__.py files
    for init_file in [
        include_dir.parent.parent / "__init__.py",
        include_dir.parent / "__init__.py",
        include_dir / "__init__.py",
    ]:
        if not init_file.exists():
            init_file.touch()
            print(f"✓ Created package file: {init_file.relative_to(airflow_home)}")

    # Create pipeline.py if it doesn't exist
    pipeline_file = include_dir / "pipeline.py"
    if not pipeline_file.exists():
        pipeline_content = get_dlt_pipeline_template(domain, name)
        pipeline_file.write_text(pipeline_content)
        print(f"✓ Created pipeline file: {pipeline_file.relative_to(airflow_home)}")
    else:
        print(f"⊘ Pipeline file already exists: {pipeline_file.relative_to(airflow_home)}")

    # Create sources.py if it doesn't exist
    sources_file = include_dir / "sources.py"
    if not sources_file.exists():
        sources_content = get_dlt_sources_template(domain, name)
        sources_file.write_text(sources_content)
        print(f"✓ Created sources file: {sources_file.relative_to(airflow_home)}")
    else:
        print(f"⊘ Sources file already exists: {sources_file.relative_to(airflow_home)}")


def main() -> int:
    """
    Main entry point for the DAG generator.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    parser = argparse.ArgumentParser(
        description="Generate standardized Apache Airflow DAGs with domain-based naming conventions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create an ingestion DAG for sales orders
  python scripts/create_dag.py --domain sales --name orders --type ingestion --schedule "@daily"

  # Create a processing DAG for finance transactions
  python scripts/create_dag.py \\
    --domain finance --name transactions --type processing \\
    --schedule "0 2 * * *" --owner finance_team

  # Create an orchestration DAG
  python scripts/create_dag.py \\
    --domain marketing --name campaigns --type orchestration \\
    --schedule "0 9 * * *" --owner marketing_team --description "Orchestrate campaign processing"

Naming Conventions:
  - Domain: lowercase, single word (e.g., sales, finance, marketing)
  - Name: lowercase, hyphen/space separated converted to underscore (e.g., orders, user_events)
  - Generated DAG ID: <domain>_<name>_<type> (e.g., sales_orders_ingestion)
  - Generated Task IDs: <domain>_<action>[_<object>] (e.g., sales_extract_orders, sales_start)

DAG Types:
  - ingestion: Extract data using dlt, includes pipeline and source templates
  - processing: Transform and enrich data, suitable for complex ETL logic
  - orchestration: Coordinate other DAGs without business logic
        """,
    )

    parser.add_argument(
        "--domain",
        required=True,
        help="Domain name (e.g., sales, finance, marketing). Used in DAG and task naming.",
    )

    parser.add_argument(
        "--name",
        required=True,
        help="DAG name (e.g., orders, transactions, campaigns). Used in DAG and task naming.",
    )

    parser.add_argument(
        "--type",
        choices=["ingestion", "processing", "orchestration"],
        required=True,
        help="Type of DAG to generate.",
    )

    parser.add_argument(
        "--schedule",
        required=True,
        help='Schedule expression (cron or Airflow preset, e.g., "@daily", "0 2 * * *").',
    )

    parser.add_argument(
        "--owner",
        default="airflow",
        help="DAG owner (default: airflow).",
    )

    parser.add_argument(
        "--description",
        help="Custom DAG description. If not provided, auto-generated from domain and name.",
    )

    parser.add_argument(
        "--start-date",
        default="2025-08-01",
        help="DAG start date in YYYY-MM-DD format (default: 2025-08-01).",
    )

    parser.add_argument(
        "--no-catchup",
        action="store_true",
        default=True,
        help="Disable catchup (default: catchup is disabled).",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing DAG files (use with caution).",
    )

    args = parser.parse_args()

    try:
        # Validate arguments
        validate_arguments(args)

        # Normalize domain and name
        domain = normalize_identifier(args.domain)
        name = normalize_identifier(args.name)
        dag_type = args.type

        # Generate DAG and file names
        dag_id = generate_dag_id(domain, name, dag_type)
        dag_filename = f"{dag_id}.py"

        airflow_home = get_airflow_home()
        dag_file = airflow_home / "dags" / dag_filename

        # Check if DAG file already exists
        if check_dag_exists(dag_file):
            if not args.force:
                print(f"✗ DAG file already exists: {dag_file.relative_to(airflow_home)}")
                print("  Use --force to overwrite.")
                return 1
            else:
                print(f"⊠ Overwriting existing DAG: {dag_file.relative_to(airflow_home)}")

        # Create DAG file
        owner = args.owner if args.owner else "airflow"
        create_dag_file(dag_file, domain, name, dag_type, args.schedule, owner)

        # Create include directory structure for ingestion DAGs
        if dag_type == "ingestion":
            create_include_structure(domain, name, dag_type)

        print(f"\n✓ Successfully created {dag_type} DAG: {dag_id}")
        print(f"  File: {dag_file.relative_to(airflow_home)}")
        print(f"  Schedule: {args.schedule}")
        print(f"  Owner: {owner}")

        if dag_type == "ingestion":
            print("\n📝 Next steps for ingestion DAG:")
            print(f"  1. Edit: include/{domain}/ingestion/sources.py")
            print("     - Configure your data source (API, database, file, etc.)")
            print("     - Add authentication and credentials")
            print(f"  2. Edit: include/{domain}/ingestion/pipeline.py")
            print("     - Update the run_ingestion() function")
            print("     - Configure dlt destination and dataset name")
            print(f"  3. Edit: dags/{dag_filename}")
            print("     - Update the run_ingestion() task with your pipeline import")
            print("  4. Test locally:")
            print(f"     python include/{domain}/ingestion/pipeline.py")

        return 0

    except ValueError as e:
        print(f"✗ Configuration Error: {e}", file=sys.stderr)
        return 1
    except TaskIdError as e:
        print(f"✗ ID Generation Error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"✗ File Operation Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:  # pylint: disable=broad-except
        print(f"✗ Unexpected Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
