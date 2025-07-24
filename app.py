from flask import Flask, render_template, request, jsonify, session
import uuid
from datetime import datetime
import os

# Create Flask app with custom template and static folders
app = Flask(__name__, 
           template_folder='Website',  # HTML files in Website folder
           static_folder='Website')     # CSS files in Website folder

app.secret_key = 'your-secret-key-change-this-in-production'

# In-memory storage (use a database in production)
chats = {}

@app.route('/')
def index():
    # Initialize session if needed
    if 'user_chats' not in session:
        session['user_chats'] = []
    
    # Get user's chats
    user_chats = []
    for chat_id in session['user_chats']:
        if chat_id in chats:
            user_chats.append(chats[chat_id])
    
    return render_template('Index.html', chats=user_chats)

@app.route('/new-chat', methods=['POST'])
def new_chat():
    # Create new chat
    chat_id = str(uuid.uuid4())
    chat_data = {
        'id': chat_id,
        'title': f'Untitled Chat {len(session.get("user_chats", [])) + 1}',
        'created_at': datetime.now().isoformat(),
        'messages': []
    }
    
    # Store chat
    chats[chat_id] = chat_data
    
    # Add to user's session
    if 'user_chats' not in session:
        session['user_chats'] = []
    session['user_chats'].insert(0, chat_id)  # Add to beginning
    session.modified = True
    
    return jsonify({
        'success': True,
        'chat': chat_data
    })

@app.route('/chat/<chat_id>')
def get_chat(chat_id):
    if chat_id in chats:
        return jsonify(chats[chat_id])
    return jsonify({'error': 'Chat not found'}), 404

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    chat_id = data.get('chat_id')
    message = data.get('message')
    
    if chat_id not in chats:
        return jsonify({'error': 'Chat not found'}), 404
    
    # Add user message
    user_msg = {
        'id': str(uuid.uuid4()),
        'type': 'user',
        'content': message,
        'timestamp': datetime.now().isoformat()
    }
    chats[chat_id]['messages'].append(user_msg)
    
    # Here's where you'd integrate your actual AI chatbot
    # For now, we'll simulate a Computer Science tutor response
    bot_response = generate_cs_response(message)
    
    bot_msg = {
        'id': str(uuid.uuid4()),
        'type': 'bot',
        'content': bot_response,
        'timestamp': datetime.now().isoformat()
    }
    chats[chat_id]['messages'].append(bot_msg)
    
    return jsonify({
        'success': True,
        'messages': [user_msg, bot_msg]
    })

def generate_cs_response(message):
    """
    Simulate a Computer Science tutor response
    Replace this with your actual AI integration (OpenAI, etc.)
    """
    message_lower = message.lower()
    
    # Simple keyword-based responses for demonstration
    if 'flash card' in message_lower or 'flashcard' in message_lower:
        return "I'd be happy to help create flashcards! Please specify the Computer Science topic you'd like flashcards for (e.g., algorithms, data structures, programming concepts, etc.)"
    
    elif 'exam' in message_lower and 'question' in message_lower:
        return "I can generate exam-style questions! Which topic would you like questions on? For example: algorithms, data structures, databases, networks, or programming?"
    
    elif 'debug' in message_lower or 'code' in message_lower:
        return "I'd be happy to help debug your code! Please share your code and describe what issue you're experiencing, and I'll help you identify and fix the problem."
    
    elif 'mark' in message_lower and 'answer' in message_lower:
        return "I can help mark your answer! Please provide: 1) The original question, 2) Your answer, and 3) The mark scheme if you have it. I'll give you feedback and a grade."
    
    elif 'aqa' in message_lower:
        return "Great! I can help with AQA Computer Science. What specific topic do you need help with? I cover all areas including programming, algorithms, data representation, computer systems, and more."
    
    elif 'ocr' in message_lower:
        return "Perfect! I can assist with OCR Computer Science. Which area would you like to focus on? I can help with programming, computational thinking, algorithms, data representation, or any other OCR topics."
    
    else:
        return f"I'm your A-Level Computer Science tutor! I can help you with programming, algorithms, data structures, exam questions, flashcards, and more. What would you like to work on today?"

if __name__ == '__main__':
    app.run(debug=True)