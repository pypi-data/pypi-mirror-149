"""
This file provides utilities for creating files based on templates in this 
library. The reason we need this is so that we can create a starter Armadillo
project on the developer's local machine, while interpolating some values
like the name of the project.
"""

import os
import pkg_resources
from typing import List
from rich.console import Console

console = Console()


def render_template_file(
    template_file: str, destination_file: str, template_args: dict = None
):
    """
    Copies a template file to the destination file.
    Arguments:
        template_file: The path to the template file.   (str)
        destination_file: The path to the destination file. (str)
        template_args: A dictionary of arguments to pass to the template. (dict)
    """
    resource_package = __name__
    try:
        template = pkg_resources.resource_string(
            resource_package, template_file
        ).decode("utf-8")
    except UnicodeDecodeError:
        console.print(
            "Encountered Error Decoding the Template File:", style="red"
        )
        console.print(template_file)
    if template_args:
        for template_key, template_value in template_args.items():
            template = template.replace(
                f"{{{{{template_key}}}}}", template_value
            )
    os.makedirs(os.path.dirname(destination_file), exist_ok=True)
    with open(destination_file, "w") as f:
        f.write(template)


def walk_template_directory(template_directory: str) -> List[str]:
    """
    Walks a directory within a Python package and returns a list of the full
    paths of every single file.
    """
    objects = pkg_resources.resource_listdir(__name__, template_directory)
    files = []
    for object in objects:
        if pkg_resources.resource_isdir(
            __name__, os.path.join(template_directory, object)
        ):
            files.extend(
                walk_template_directory(
                    os.path.join(template_directory, object)
                )
            )
        else:
            files.append(os.path.join(template_directory, object))
    return files


def render_template_directory(
    template_directory: str,
    destination_directory: str,
    template_args: dict = None,
    ignore_patterns: List[str] = ["__pycache__", ".pyc", ".DS_Store"],
):
    """
    Copies an entire template directory to a destination directory while
    applying any templating argumetns.
    """
    ## Get all of the files in the template directory
    template_files = walk_template_directory(template_directory)
    template_files = [
        file
        for file in template_files
        if not any([pattern in file for pattern in ignore_patterns])
    ]
    for template_file in template_files:
        base_path = os.path.relpath(template_file, template_directory)
        render_template_file(
            template_file=template_file,
            destination_file=os.path.join(
                destination_directory,
                base_path,  # Get rid of the template directory
            ),
            template_args=template_args,
        )
    return True
