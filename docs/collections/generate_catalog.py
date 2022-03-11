"""Script to generate the collections catalog table"""
import glob
from pathlib import Path

import mkdocs_gen_files
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

with mkdocs_gen_files.open("collections/catalog.md", "a") as markdown_file:
    # Get file paths for all collections files
    collection_files = [
        file
        for file in glob.glob("./docs/collections/catalog/*.yaml")
        # Ignore the template file
        if Path(file).name != "TEMPLATE.yaml"
    ]

    # Load collection information from YAML files into a list
    collection_configs = []
    for collection_file in collection_files:
        with open(collection_file, "r") as file:
            collection_configs.append(yaml.safe_load(file))

    # Sort collections alphabetically by name
    sorted_collection_configs = sorted(
        collection_configs, key=lambda x: x["collectionName"]
    )

    env = Environment(
        loader=FileSystemLoader("./docs/collections/templates/"),
        autoescape=select_autoescape(enabled_extensions="html"),
    )
    template = env.get_template("table.html")

    # Render jinja2 template and append to catalog.md
    print(template.render(collections=sorted_collection_configs), file=markdown_file)
