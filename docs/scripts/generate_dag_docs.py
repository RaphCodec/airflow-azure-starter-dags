import os
from airflow.models import DagBag
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "src", "dags")

dag_bag = DagBag(dag_folder="/opt/airflow/dags/", include_examples=False)

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
template = env.get_template("dag.md.j2")

os.makedirs(OUTPUT_DIR, exist_ok=True)

for dag_id, dag in dag_bag.dags.items():
    content = template.render(
        dag_id=dag.dag_id,
        description=dag.description or "No description",
        doc_md = dag.doc_md,
        schedule=str(dag.schedule),
        tags=dag.tags or [],
        tasks=[t.task_id for t in dag.tasks],
    )

    with open(os.path.join(OUTPUT_DIR, f"{dag_id}.md"), "w") as f:
        f.write(content)

print("DAG docs generated.")