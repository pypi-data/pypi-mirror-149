"""
Utilities for interacting with the Armadillo Admin API.
"""

import requests
import rich_click as click
from pydantic import BaseModel
from rich.console import Console
from .utils import get_armadillo_url, get_armadillo_session

console = Console()


class Model(BaseModel):
    id: str
    description: str
    parent_user_id: str
    github_url: str


def get_model(model_id: str, environment: str = "PRODUCTION"):
    """
    Get information about a model from the Armadillo Admin API.
    """
    armadillo_url = get_armadillo_url(environment)
    response = requests.get(f"{armadillo_url}/api/admin/models/{model_id}")
    return response.json()


def delete_model(model_id: str, environment: str = "PRODUCTION"):
    """
    Delete a model using the Armadillo Admin API.
    """
    armarmillo_url = get_armadillo_url(environment)
    session = get_armadillo_session()
    if not session:
        raise Exception(
            "No session ID found. Something is wrong (this should have been caught by the decorator)."
        )
    response = requests.delete(
        f"{armarmillo_url}/api/admin/models/{model_id}",
        cookies={"token": session["token"]},
    )
    response.raise_for_status()
    return response.json()


def create_model(
    model_id: str,
    description: str,
    delete_existing: bool = False,
    environment: str = "PRODUCTION",
) -> Model:
    """
    Create a model repository with the Armadillo Admin API.
    Args:
       model_id: The ID of the model.
       description: The description of the model.
       delete_existing: Delete the existing repository if it exists. (Will prompt you.)
    """
    armadillo_url = get_armadillo_url(environment)
    session = get_armadillo_session()
    if not session:
        raise Exception(
            "No session ID found. Something is wrong (this should have been caught by the decorator)."
        )
    response = requests.post(
        f"{armadillo_url}/api/admin/models",
        json={"id": model_id, "description": description},
        cookies={"token": session["token"]},
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.json().get("code") == "MODEL_ALREADY_EXISTS":
            if not delete_existing:
                raise click.BadParameter(
                    f"Model repository {model_id} already exists."
                )
            else:
                console.print(
                    f"[red]:rotating_light: Model repository [bold]{model_id}[/bold] already exists, but you have opted to delete it.[/red]"
                )
                click.confirm(
                    "Are you sure you want to delete it?", abort=True
                )
                delete_model(model_id, environment)
                console.print(
                    f":white_check_mark: Deleted remote repository [bold]{model_id}[/bold].",
                    style="green",
                )
                return create_model(
                    model_id, description, delete_existing, environment
                )
    console.print(
        f":white_check_mark: Created {'[italic](new)[/italic] ' if delete_existing else ''}remote repository [bold]{model_id}[/bold]:",
        style="green",
    )
    model_data = response.json()["modelData"]
    model = Model(
        id=model_data["id"],
        description=model_data["description"],
        parent_user_id=model_data["parentUserId"],
        github_url=model_data["githubURL"],
    )
    return model
