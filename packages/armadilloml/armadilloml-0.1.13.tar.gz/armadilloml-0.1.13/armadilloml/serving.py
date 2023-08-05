"""
This module deals with serving the actual models. It implements a layer on top
of Flask that has some built-in logic and error handling. The reason we need 
this is so that 1) data scientists don't need to do extra work to build a 
Flask server and 2) all Armadillo models can follow some standard conventions
for what type of data they accept and how they handle errors.
"""

import os
import rich_click as click
from rich.console import Console
from flask import Flask, request, jsonify
from .utils import require_armadillo_project

console = Console()


@click.command()
@click.argument("path", type=click.Path(), default=None)
def run(path: str):
    """
    Run the Armadillo model server. This command is meant to be run within an
    Armadillo project. It will look for the `predict` function in the `app.py`
    file and then run that function
    """
    path = os.path.join(os.getcwd(), path)
    os.chdir(path)
    require_armadillo_project()
    try:
        # fmt: off
        from app import predict
        # fmt: on
    except ImportError:
        raise click.ClickException(
            "You must have a predict function in your Armadillo project."
        )
    app = Flask("whatever")

    @app.route("/", methods=["POST"])
    def predict_route():
        """
        This is the route that the Armadillo model server will use to make
        predictions.
        """
        request_payload = request.json
        if not request_payload:
            return jsonify({"error": "No request payload provided."}), 400
        if "input" not in request_payload:
            return (
                jsonify(
                    {"error": "Request payload must contain and `input`."}
                ),
                400,
            )
        try:
            result = predict(request_payload["input"])
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        return jsonify(result)

    console.print("Alright I'm about to run the app!")
    console.print(__name__)
    app.run(
        debug=True,
        host="0.0.0.0",
        load_dotenv=True,
        port=int(os.environ.get("PORT", 8080)),
    )
