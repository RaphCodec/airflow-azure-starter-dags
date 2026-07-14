import argparse
import logging
import os
import sys
from datetime import datetime

from airflow.models import DagBag
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Defaults relative to docs/scripts
DEFAULT_TEMPLATES_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "src", "templates"))
DEFAULT_OUTPUT_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "src", "dags"))

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def write_if_changed(path, content):
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                if f.read() == content:
                    return False
        except Exception:
            pass
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def gather_task_info(task):
    return {
        "task_id": getattr(task, "task_id", ""),
        "operator": task.__class__.__name__,
        "retries": getattr(task, "retries", ""),
        "doc": (getattr(task, "doc_md", "") or getattr(task, "doc", "") or "").strip(),
        "downstream": sorted([d.task_id for d in task.downstream_list]),
    }


def format_dt(v):
    try:
        return v.isoformat()
    except Exception:
        return str(v or "")


def stable_value(v):
    """Convert values to deterministic, markdown-friendly strings/containers."""
    if callable(v):
        module = getattr(v, "__module__", "")
        name = getattr(v, "__qualname__", getattr(v, "__name__", str(v)))
        return f"{module}.{name}" if module else name
    if hasattr(v, "total_seconds"):
        return v.total_seconds()
    if isinstance(v, dict):
        return {k: stable_value(val) for k, val in sorted(v.items(), key=lambda item: str(item[0]))}
    if isinstance(v, set):
        return [stable_value(i) for i in sorted(v, key=lambda item: str(item))]
    if isinstance(v, (list, tuple)):
        return [stable_value(i) for i in v]
    return v


def main(
    dag_folder=None,
    output_dir=None,
    templates_dir=None,
    no_cleanup=False,
    verbose=False,
):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if templates_dir is None:
        templates_dir = DEFAULT_TEMPLATES_DIR
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
    if dag_folder is None:
        # sensible default: repo root/dags
        # (assumes docs/scripts sits under repo/docs/scripts)
        repo_root = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
        dag_folder = os.path.join(repo_root, "dags")

    os.makedirs(output_dir, exist_ok=True)

    env = Environment(loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True)
    try:
        template = env.get_template("dag.md.j2")
    except Exception as e:
        logging.error("Failed to load dag.md.j2 from %s: %s", templates_dir, e)
        raise

    # Load DAGs — repo root and dag_folder must both be on sys.path so that
    # relative imports like `include.common` resolve correctly.
    sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, "..", "..")))
    sys.path.insert(0, os.path.abspath(dag_folder))
    dagbag = DagBag(dag_folder=dag_folder, include_examples=False)
    if dagbag.import_errors:
        logging.warning("Import errors while parsing DAGs:")
        for k, v in dagbag.import_errors.items():
            logging.warning(" - %s: %s", k, v)

    current_dag_files = set()
    index_entries = []

    for dag_id in sorted(dagbag.dag_ids):
        dag = dagbag.get_dag(dag_id)
        tasks = [gather_task_info(t) for t in dag.tasks]

        raw_params = getattr(dag, "params", {}) or {}
        params = {k: stable_value(v.value if hasattr(v, "value") else v) for k, v in raw_params.items()}
        params = dict(sorted(params.items(), key=lambda item: str(item[0])))

        raw_default_args = getattr(dag, "default_args", {}) or {}
        default_args = {k: stable_value(v) for k, v in raw_default_args.items()}
        default_args = dict(sorted(default_args.items(), key=lambda item: str(item[0])))

        context = {
            "dag_id": dag.dag_id,
            "dag_display_name": getattr(dag, "dag_display_name", None) or dag.dag_id,
            "description": dag.description or "",
            "doc_md": getattr(dag, "doc_md", "") or "",
            "schedule": getattr(dag, "schedule_interval", getattr(dag, "schedule", "")),
            "start_date": format_dt(
                getattr(dag, "start_date", None) or (getattr(dag, "default_args", {}) or {}).get("start_date")
            ),
            "catchup": getattr(dag, "catchup", ""),
            "tags": sorted((getattr(dag, "tags", []) or []), key=str.casefold),
            "tasks": tasks,
            "params": params,
            "default_args": default_args,
            "max_active_runs": getattr(dag, "max_active_runs", ""),
            "max_active_tasks": getattr(dag, "max_active_tasks", getattr(dag, "concurrency", "")),
        }

        rendered = template.render(**context)
        filename = f"{dag_id}.md"
        out_path = os.path.join(output_dir, filename)
        if write_if_changed(out_path, rendered):
            logging.info("Wrote %s", out_path)
        else:
            logging.debug("No changes for %s", out_path)

        current_dag_files.add(filename)

        # Derive team from the first subfolder under dag_folder, if any
        try:
            rel = os.path.relpath(dag.fileloc, dag_folder)
            parts = rel.replace(os.sep, "/").split("/")
            team = parts[0] if len(parts) > 1 else None
        except Exception:
            team = None

        index_entries.append({"display": context["dag_display_name"], "file": filename, "team": team})

    # remove stale files
    if not no_cleanup:
        existing_files = {f for f in os.listdir(output_dir) if f.endswith(".md") and f != "index.md"}
        stale_files = existing_files - current_dag_files
        for f in sorted(stale_files):
            try:
                os.remove(os.path.join(output_dir, f))
                logging.info("Removed stale doc: %s", f)
            except Exception as e:
                logging.warning("Failed to remove %s: %s", f, e)

    # write index — group by team
    # Collect unique teams preserving first-seen order; unteamed DAGs go last
    from collections import defaultdict

    by_team = defaultdict(list)
    for e in index_entries:
        by_team[e["team"]].append(e)

    # Sort: named teams alphabetically, then None last
    sorted_teams = sorted((t for t in by_team if t is not None), key=str.casefold)
    if None in by_team:
        sorted_teams.append(None)

    index_lines = [
        "---",
        'title: "DAGs"',
        "---",
        "",
        "# DAGs",
        "",
        f"Generated: {datetime.now().date()}",
        "",
    ]
    for team in sorted_teams:
        heading = team if team is not None else "No Team"
        index_lines.append(f"## {heading}")
        index_lines.append("")
        for e in by_team[team]:
            index_lines.append(f"- [{e['display']}]({e['file']})")
        index_lines.append("")

    index_content = "\n".join(index_lines) + "\n"
    index_path = os.path.join(output_dir, "index.md")
    if write_if_changed(index_path, index_content):
        logging.info("Wrote %s", index_path)
    else:
        logging.debug("No changes for %s", index_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate markdown docs for Airflow DAGs")
    parser.add_argument("--out", help="Output directory for generated docs (defaults to docs/src/dags)")
    parser.add_argument("--dags", help="Path to DAGs folder (defaults to repo/dags)")
    parser.add_argument("--templates", help="Path to templates directory (defaults to docs/templates)")
    parser.add_argument("--no-cleanup", action="store_true", help="Do not remove stale generated files")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    main(
        dag_folder=args.dags,
        output_dir=args.out,
        templates_dir=args.templates,
        no_cleanup=args.no_cleanup,
        verbose=args.verbose,
    )
