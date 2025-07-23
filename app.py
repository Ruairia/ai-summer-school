import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

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
        f"for the {exam_board} exam board. Give answers specific to this curriculum."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4o" if you're using free credits
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        answer = response['choices'][0]['message']['content']
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
