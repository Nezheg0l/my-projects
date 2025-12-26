import google.generativeai as genai

API_KEY = "AIzaSyBl9A2iqOLxvHK2kBOsnFXKSu1EH69fHpY" 

genai.configure(api_key=API_KEY)

print("🔍 Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Available: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")
