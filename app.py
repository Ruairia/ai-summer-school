import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

app = Flask(__name__)
CORS(app)

MODEL_URL = "https://api-inference.huggingface.co/models/gpt2"


headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    subject = data.get("subject")
    exam_board = data.get("exam_board")
    question = data.get("question")

    if not all([subject, exam_board, question]):
        return jsonify({"error": "Missing subject, exam_board, or question"}), 400

    prompt = (
        f"You are an expert tutor. The student is studying {subject} for the {exam_board} A-level. "
        f"Answer clearly and concisely according to this curriculum.\n\n"
        f"Student: {question}"
    )

    try:
        response = requests.post(
            MODEL_URL,
            headers=headers,
            json={"inputs": prompt}
        )

        if response.status_code != 200:
            return jsonify({"error": f"Hugging Face error: {response.text}"}), response.status_code

        output = response.json()
        if isinstance(output, list) and "generated_text" in output[0]:
            return jsonify({"answer": output[0]["generated_text"]})
        else:
            return jsonify({"error": "Unexpected response format", "raw": output}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Flask server with Hugging Face model running. POST to /ask."

if __name__ == "__main__":
    app.run(debug=True, port=8000)
