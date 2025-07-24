import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HUGGINGFACE_API_KEY")
MODEL_URL = "https://api-inference.huggingface.co/models/gpt2"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

data = {
    "inputs": "Hello world",
}

response = requests.post(MODEL_URL, headers=headers, json=data)

print(response.status_code)
print(response.json())