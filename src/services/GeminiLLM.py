import google.generativeai as genai
import os
import io

class GeminiService:
    def __init__(self):
        genai.configure(api_key=os.getenv('API_KEY'))
        self.model = genai.GennerativeModel('gemini-1.5-flash')

    def generate(self, prompt):
        response = self.model.generate_content([prompt])
        return response

