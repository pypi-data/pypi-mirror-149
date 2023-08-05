import os
import datetime as dt
import traceback
from flask import Flask, request, jsonify
from transformers import pipeline
from rich.console import Console

# Example of a Sentiment Analysis Pipeline from HuggingFace
sent_pipeline = pipeline("sentiment-analysis")

app = Flask(__name__)
console = Console()


@app.route("/", methods=["GET", "POST"])
def predict():
    """
    This is the main endpoint for your Armadillo project.
    """
    time = dt.datetime.now()
    console.log("Invoking Sentiment Analysis @ {}".format(time))
    try:
        console.log("Request JSON:")
        console.print_json(data=request.json)
        if not request.json:
            msg = "The request JSON is empty or malformed."
            return jsonify({"status": "ERROR", "message": msg}), 400
        input = request.json.get("input")
        if not input:
            msg = "The input field is empty or malformed."
            return jsonify({"status": "ERROR", "message": msg}), 400
        # This shouldn't necessarily be handled by Armadillo ML.
        text = input.get("text")
        if not text:
            msg = "The input/text field is empty or malformed."
            return jsonify({"status": "ERROR", "message": msg}), 400
        if not text:
            return {"error": "No text provided"}, 400
        prediction = sent_pipeline(text)
        console.log("Succesful Model Prediction:")
        console.log(prediction)
        return (
            jsonify(
                {"status": "SUCCESS", "input": input, "prediction": prediction}
            ),
            200,
        )
    except Exception as e:
        console.log("Encountered an error:")
        console.log(e)
        tb = traceback.format_exc()
        console.log(tb)
        return (
            jsonify({"error": "Internal server error.", "traceback": tb}),
            500,
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
