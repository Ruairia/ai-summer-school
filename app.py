import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # For frontend to connect
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)  # Allow requests from browser

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    subject = data.get("subject")
    exam_board = data.get("exam_board")
    question = data.get("question")

    if not all([subject, exam_board, question]):
        return jsonify({"error": "Missing subject, exam_board, or question"}), 400

    system_prompt = (
        f"You are an expert tutor. The student is studying {subject} "
        f"for the {exam_board} exam board for the British A Level. Give answers specific to this curriculum."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Flask server is running. Use POST /ask to query ChatGPT."

if __name__ == "__main__":
    app.run(debug=True, port=8000)
