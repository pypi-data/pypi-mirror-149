import os
from flask import Flask, request
from transformers import pipeline

# Example of a Sentiment Analysis Pipeline from HuggingFace
sent_pipeline = pipeline("sentiment-analysis")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def predict():
    """
    This is the main endpoint for your Armadillo project.
    """
    # Random test line for commit
    input = request.json["input"]
    text = input.get("text")
    if not text:
        return {"error": "No text provided"}, 400
    prediction = sent_pipeline(text)
    return {"input": input, "text": text, "prediction": prediction}, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
