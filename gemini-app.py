import os
import sys
import logging
from flask import Flask, render_template, request
import vertexai  # type: ignore
import markdown  # type: ignore
from vertexai.generative_models import GenerativeModel  # type: ignore
import vertexai.preview.generative_models as generative_models  # type: ignore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=LOG_LEVEL)

PROJECT_ID = os.getenv('PROJECT_ID')
REGION = os.getenv('REGION')

if not PROJECT_ID:
    logging.error("PROJECT_ID environment variable is not set")
    sys.exit(1)
if not REGION:
    logging.error("REGION environment variable is not set")
    sys.exit(1)

MODEL_NAME = os.getenv('MODEL_NAME', 'gemini-1.5-pro-001')

app = Flask(__name__)

vertexai.init(project=PROJECT_ID, location=REGION)

model = GenerativeModel(MODEL_NAME)

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}


@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = model.generate_content(prompt, generation_config=generation_config, safety_settings=safety_settings)
        response_text = markdown.markdown(response.text)  # Convert response to markdown
    return render_template("index-with-css.html", response_text=response_text)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
