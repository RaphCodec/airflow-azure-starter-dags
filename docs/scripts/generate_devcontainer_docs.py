import json
import logging
import os
import re

from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEVCONTAINER_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "..", ".devcontainer"))
DEFAULT_TEMPLATES_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "src", "templates"))
DEFAULT_OUTPUT = os.path.normpath(os.path.join(BASE_DIR, "..", "src", "devcontainer.md"))

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


def parse_dockerfile(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    base_image = re.search(r"^FROM\s+(\S+)", content, re.MULTILINE).group(1)
    uv_tools = re.findall(r"uv tool install\s+(\S+)", content)

    return {
        "base_image": base_image,
        "dockerfile": content.strip(),
        "uv_tools": uv_tools,
    }


def parse_requirements(path):
    packages = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                packages.append(line)
    return packages


def group_requirements(packages):
    buckets = {
        "Apache Airflow": [],
        "Airflow Providers": [],
        "Azure": [],
        "Other": [],
    }
    for pkg in packages:
        name = re.split(r"[><=!]", pkg)[0].strip().lower()
        if name.startswith("apache-airflow-providers-"):
            buckets["Airflow Providers"].append(pkg)
        elif name.startswith("apache-airflow"):
            buckets["Apache Airflow"].append(pkg)
        elif name.startswith("azure-"):
            buckets["Azure"].append(pkg)
        else:
            buckets["Other"].append(pkg)
    return {k: sorted(v) for k, v in buckets.items() if v}


def parse_devcontainer(path):
    with open(path, encoding="utf-8") as f:
        # Strip JS-style // comments and trailing commas before parsing as JSON
        content = re.sub(r"//[^\n]*", "", f.read())
        content = re.sub(r",(\s*[}\]])", r"\1", content)
    data = json.loads(content)

    raw_ports = data.get("forwardPorts", [])
    port_labels = {
        8080: "Airflow UI & API",
        5555: "Flower (Celery monitoring)",
    }
    ports = [{"port": p, "label": port_labels.get(p, "")} for p in raw_ports]

    extensions = data.get("customizations", {}).get("vscode", {}).get("extensions", [])

    return {"ports": ports, "extensions": extensions}


def main(output=None, templates_dir=None):
    if output is None:
        output = DEFAULT_OUTPUT
    if templates_dir is None:
        templates_dir = DEFAULT_TEMPLATES_DIR

    dockerfile = parse_dockerfile(os.path.join(DEVCONTAINER_DIR, "Dockerfile"))
    requirements = group_requirements(parse_requirements(os.path.join(DEVCONTAINER_DIR, "requirements.txt")))
    devcontainer = parse_devcontainer(os.path.join(DEVCONTAINER_DIR, "devcontainer.json"))

    env = Environment(loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template("devcontainer.md.j2")

    rendered = template.render(
        base_image=dockerfile["base_image"],
        dockerfile=dockerfile["dockerfile"],
        uv_tools=dockerfile["uv_tools"],
        requirements=requirements,
        ports=devcontainer["ports"],
        extensions=devcontainer["extensions"],
    )

    if write_if_changed(output, rendered):
        logging.info("Wrote %s", output)
    else:
        logging.debug("No changes for %s", output)


if __name__ == "__main__":
    main()
