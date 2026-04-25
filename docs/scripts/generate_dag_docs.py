import os
import sys
import argparse
import logging
from datetime import datetime
try:
    import markdown as _markdown
except Exception:
    _markdown = None
from airflow.models import DagBag
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Defaults relative to docs/scripts
DEFAULT_TEMPLATES_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "templates"))
DEFAULT_OUTPUT_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "src", "dags"))

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def write_if_changed(path, content):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if f.read() == content:
                    return False
        except Exception:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def gather_task_info(task):
    return {
        'task_id': getattr(task, 'task_id', ''),
        'operator': task.__class__.__name__,
        'retries': getattr(task, 'retries', ''),
        'doc': (getattr(task, 'doc_md', '') or getattr(task, 'doc', '') or '').strip()
    }


def format_dt(v):
    try:
        return v.isoformat()
    except Exception:
        return str(v or '')


def main(dag_folder=None, output_dir=None, templates_dir=None, no_cleanup=False, verbose=False):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if templates_dir is None:
        templates_dir = DEFAULT_TEMPLATES_DIR
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
    if dag_folder is None:
        # sensible default: repo root/dags (assumes docs/scripts sits under repo/docs/scripts)
        repo_root = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
        dag_folder = os.path.join(repo_root, 'dags')

    os.makedirs(output_dir, exist_ok=True)

    env = Environment(loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True)
    try:
        template = env.get_template('dag.md.j2')
    except Exception as e:
        logging.error('Failed to load dag.md.j2 from %s: %s', templates_dir, e)
        raise

    # Load DAGs
    sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '..', '..')))
    dagbag = DagBag(dag_folder=dag_folder, include_examples=False)
    if dagbag.import_errors:
        logging.warning('Import errors while parsing DAGs:')
        for k, v in dagbag.import_errors.items():
            logging.warning(' - %s: %s', k, v)

    current_dag_files = set()
    index_entries = []

    for dag_id in sorted(dagbag.dag_ids):
        dag = dagbag.get_dag(dag_id)
        tasks = [gather_task_info(t) for t in dag.tasks]

        context = {
            'dag_id': dag.dag_id,
            'dag_display_name': getattr(dag, 'dag_display_name', None) or dag.dag_id,
            'description': dag.description or '',
            'doc_md': getattr(dag, 'doc_md', '') or '',
            'schedule': getattr(dag, 'schedule_interval', getattr(dag, 'schedule', '')),
            'start_date': format_dt(getattr(dag, 'start_date', None) or (getattr(dag, 'default_args', {}) or {}).get('start_date')),
            'catchup': getattr(dag, 'catchup', ''),
            'tags': getattr(dag, 'tags', []) or [],
            'tasks': tasks,
        }

        # Convert doc_md to HTML when possible and pass as `doc_html` for safe rendering
        raw_md = context.get('doc_md', '') or ''
        if _markdown:
            try:
                doc_html = _markdown.markdown(raw_md, extensions=['fenced_code', 'tables', 'toc'])
            except Exception:
                doc_html = '<pre>' + raw_md + '</pre>'
        else:
            # fallback: include raw markdown (renderer may still convert it later)
            doc_html = raw_md
        context['doc_html'] = doc_html

        rendered = template.render(**context)
        filename = f"{dag_id}.md"
        out_path = os.path.join(output_dir, filename)
        if write_if_changed(out_path, rendered):
            logging.info('Wrote %s', out_path)
        else:
            logging.debug('No changes for %s', out_path)

        current_dag_files.add(filename)
        index_entries.append({'display': context['dag_display_name'], 'file': filename})

    # remove stale files
    if not no_cleanup:
        existing_files = {f for f in os.listdir(output_dir) if f.endswith('.md') and f != 'index.md'}
        stale_files = existing_files - current_dag_files
        for f in sorted(stale_files):
            try:
                os.remove(os.path.join(output_dir, f))
                logging.info('Removed stale doc: %s', f)
            except Exception as e:
                logging.warning('Failed to remove %s: %s', f, e)

    # write index
    index_lines = [
        '---',
        'title: "DAGs"',
        '---',
        '',
        f'# DAGs',
        '',
        f'Generated: {datetime.utcnow().isoformat()} UTC',
        '',
    ]
    for e in index_entries:
        index_lines.append(f"- [{e['display']}]({e['file']})")

    index_content = '\n'.join(index_lines) + '\n'
    index_path = os.path.join(output_dir, 'index.md')
    if write_if_changed(index_path, index_content):
        logging.info('Wrote %s', index_path)
    else:
        logging.debug('No changes for %s', index_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate markdown docs for Airflow DAGs')
    parser.add_argument('--out', help='Output directory for generated docs (defaults to docs/src/dags)')
    parser.add_argument('--dags', help='Path to DAGs folder (defaults to repo/dags)')
    parser.add_argument('--templates', help='Path to templates directory (defaults to docs/templates)')
    parser.add_argument('--no-cleanup', action='store_true', help='Do not remove stale generated files')
    parser.add_argument('--verbose', action='store_true', help='Enable debug logging')
    args = parser.parse_args()
    main(dag_folder=args.dags, output_dir=args.out, templates_dir=args.templates, no_cleanup=args.no_cleanup, verbose=args.verbose)