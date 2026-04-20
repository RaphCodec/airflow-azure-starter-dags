from airflow.models import DagBag
from jinja2 import Environment, FileSystemLoader
import os
import sys
 
TEMPLATE = """
---
title: "DAG: {{ dag.dag_id }}"
---

# {{ dag.dag_id }}

{{ dag.description or '' }}

- **Schedule:** {{ dag.schedule_interval }}
- **Start date:** {{ dag.start_date }}
- **Catchup:** {{ dag.catchup }}

## Owners / Default args

{% if dag.default_args %}
{% for k, v in dag.default_args.items() %}- **{{ k }}:** {{ v }}
{% endfor %}
{% else %}
No default args
{% endif %}

## Tasks

| task_id | operator | doc |
|---|---:|---|
{% for t in tasks %}| {{ t.task_id }} | {{ t.operator }} | {{ t.doc|default('')|replace('\n',' ') }} |
{% endfor %}
"""

INDEX_TEMPLATE = """
---
title: "DAGs"
---

# DAGs

This page lists DAGs found in the repository.

{% for d in dags %}- [{{ d }}]({{ d }}.md)
{% endfor %}
"""


def safe_str(v):
	try:
		return str(v)
	except Exception:
		return ""


def render_dag_markdown(dag, tasks):
	env = Environment()
	template = env.from_string(TEMPLATE)
	return template.render(dag=dag, tasks=tasks)


def render_index(dag_ids):
	env = Environment()
	template = env.from_string(INDEX_TEMPLATE)
	return template.render(dags=dag_ids)


def gather_task_info(task):
	return {
		'task_id': getattr(task, 'task_id', ''),
		'operator': task.__class__.__name__,
		'doc': getattr(task, 'doc_md', '') or getattr(task, 'doc', '') or ''
	}


def main(output_dir=None, dag_folder=None):
	repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	if dag_folder is None:
		dag_folder = os.path.join(repo_root, 'dags')
	if output_dir is None:
		output_dir = os.path.join(repo_root, 'docs', 'src', 'dags')

	os.makedirs(output_dir, exist_ok=True)

	# Load DAGs
	sys.path.insert(0, repo_root)
	dagbag = DagBag(dag_folder=dag_folder, include_examples=False)
	if dagbag.import_errors:
		print('Import errors while parsing DAGs:')
		for k, v in dagbag.import_errors.items():
			print(f"- {k}: {v}")

	dag_ids = sorted(dagbag.dag_ids)

	for dag_id in dag_ids:
		dag = dagbag.get_dag(dag_id)
		tasks = [gather_task_info(t) for t in dag.tasks]
		content = render_dag_markdown(dag, tasks)
		out_path = os.path.join(output_dir, f"{dag_id}.md")
		with open(out_path, 'w', encoding='utf-8') as f:
			f.write(content)
		print(f'Wrote {out_path}')

	# write index
	index_content = render_index(dag_ids)
	with open(os.path.join(output_dir, 'index.md'), 'w', encoding='utf-8') as f:
		f.write(index_content)
	print('Wrote index.md')


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description='Generate markdown docs for Airflow DAGs')
	parser.add_argument('--out', help='Output directory for generated docs (defaults to docs/src/dags)')
	parser.add_argument('--dags', help='Path to DAGs folder (defaults to <repo>/dags)')
	args = parser.parse_args()
	main(output_dir=args.out, dag_folder=args.dags)


