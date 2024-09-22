import os
from flask import Flask, request, jsonify 
from dotenv import load_dotenv
import requests
from services.GeminiLLM import GoogleGeminiService

import json

api_key = os.getenv('API_KEY')

HTTP_OK = 200
HTTP_BAD_REQUEST = 400

# create an instance of Flask app
app = Flask(__name__)
# create an instance of the GeminiService
gemini_service = GoogleGeminiService()

@app.route('/')
def index():
    return "Hello World"

@app.route('/api')
def api():
    return "Hello, this is the Gemini LLM"

@app.route('/generate', methods=['POST'])
def generate_message():
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'no prompt provided'}), HTTP_BAD_REQUEST
    else:
        response = gemini_service.generate(prompt)
        return jsonify({'response': response}), HTTP_OK