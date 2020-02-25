import subprocess
from os import getcwd, listdir
from os.path import isdir, isfile
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
try:
    from .lib import *
except ImportError:
    from lib import *


def main(project_vars):
    check_environment(project_vars)
    generated_guides = make_generated_guides(project_vars)
    create_main_page(project_vars, generated_guides)
    create_mkdocs_config(project_vars, generated_guides)
    mkdocs_build()


def load_vars(parsed_args):
    config_file = open(parsed_args.config, 'r')
    project_vars = yaml.load(config_file, Loader=yaml.FullLoader)
    config_file.close()

    project_vars["mainpage_filename"] = "index.md"

    all_modules = {m["name"]: m for repo in project_vars["repos"]
                   for m in repo["modules"]}

    project_vars["all_modules"] = all_modules

    return project_vars


def check_environment(project_vars):
    if not getcwd().endswith("docs-builder"):
        raise Exception(f"PWD is '{getcwd()}'. Run this file from the project root, docs-builder/", 1)

    if not exists(project_vars["working_directory"]):
        raise Exception("Working directory not found... Have you run clone_repos.py?", 1)

    if len(listdir(project_vars["working_directory"])) == 0:
        raise Exception("Working directory is empty... Have you run clone_repos.py?", 1)
        

def create_main_page(project_vars, guide_files):
    env = Environment(
        loader=FileSystemLoader("template_files"),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template("index.md.jinja2")

    combined_vars = project_vars
    combined_vars.update({"all_guides": guide_files})

    rendered_page = template.render(combined_vars)
    mainpage = open(Path(project_vars["working_directory"], project_vars["mainpage_filename"]), "w")
    mainpage.write(rendered_page)
    mainpage.close()


def make_generated_guides(project_vars):
    guide_files = {}

    for module_name, module_obj in project_vars["all_modules"].items():
        guide = f"# {module_name} Docs\n"
        for doc_location_local in project_vars["docs_locations"]:
            doc_location = Path(project_vars["working_directory"], module_obj["path"], doc_location_local)
            if exists(doc_location):
                if isdir(doc_location):
                    for file in filter(isfile, listdir(doc_location)):
                        guide += read_docfile(Path(doc_location, file), Path(doc_location_local, file))
                else:
                    guide += read_docfile(doc_location, doc_location_local)

        guide_filename = f"{module_name.replace(' ', '-')}-guide.md"
        guide_files[module_name] = guide_filename
        guide_file = open(Path(project_vars["working_directory"], guide_filename), "w")
        guide_file.write(guide)
        guide_file.close()

    return guide_files


def read_docfile(doc_location, doc_location_local):
    subsection = f"## {doc_location_local}\n\n"
    docfile = open(doc_location, "r")
    if str(doc_location).endswith(".md"):
        subsection += docfile.read() + "\n\n"
    else:
        subsection += f"```\n{docfile.read()}\n```\n"
    docfile.close()
    return subsection


def create_mkdocs_config(project_vars, generated_guides):
    all_pages = [{"Home": project_vars["mainpage_filename"]}, {"Guides": generated_guides}]

    config = {
        "site_name": project_vars["project_name"],
        "theme": "readthedocs",
        "docs_dir": project_vars["working_directory"],
        "nav": all_pages
    }

    mkdocs_config = open("mkdocs.yml", "w")
    mkdocs_config.write(yaml.dump(config))
    mkdocs_config.close()


def mkdocs_build():
    sys.argv = ["mkdocs", "build"]
    try:
        subprocess.call(["mkdocs", "build"])
    except Exception as e:
        print("--- Exception ---")
        print(e)
        print("---    End    ---")
    except:
        print("Oh well...")


if __name__ == "__main__":
    main(load_vars(parse_args()))
