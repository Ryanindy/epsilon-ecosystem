import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("--- AVAILABLE MODELS ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model: {m.name} | Display: {m.display_name}")
except Exception as e:
    print(f"Error: {e}")
