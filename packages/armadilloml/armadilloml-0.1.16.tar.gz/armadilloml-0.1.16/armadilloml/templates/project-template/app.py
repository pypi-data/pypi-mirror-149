"""
Some basic scaffolding for your Armadillo project. 
"""

import os
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def predict():
    """
    This is the main endpoint for your Armadillo project.
    """
    return {"message": "Hello, world!"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
