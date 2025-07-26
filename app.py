import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient

load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

app = Flask(__name__)
CORS(app)

# Initialize the Hugging Face client
client = InferenceClient(token=HF_API_KEY)
MODEL_ID = "deepseek-ai/DeepSeek-V3-0324"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    subject = data.get("subject")
    exam_board = data.get("exam_board")
    question = data.get("question")

    if not all([subject, exam_board, question]):
        return jsonify({"error": "Missing subject, exam_board, or question"}), 400

    system_prompt = f"You are an expert tutor. The student is studying {subject} for the {exam_board} A-level. Answer clearly and concisely according to this curriculum. Do not include excessive formatting - try to use only ascii characters, do not use tables or double asterisks."

    try:
        # Use the chat completion endpoint instead of text generation
        response = client.chat_completion(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Extract the assistant's response from the chat completion
        if hasattr(response, 'choices') and len(response.choices) > 0:
            answer = response.choices[0].message.content
        else:
            answer = response.generated_text

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Flask server with Hugging Face model running. POST to /ask."

if __name__ == "__main__":
    app.run(debug=True, port=5000)