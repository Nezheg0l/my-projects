import requests
import json
import re

def patch_vulnerability(source_code, attack_payload, vuln_type):
    print(f"🛡️ DEFENDER (Local AI): Fixing {vuln_type} vulnerability...")

    # Різні інструкції для різних типів атак
    if vuln_type == "RCE":
        instructions = "Replace 'os.system'/'os.popen' with 'subprocess.run(shell=False)'. Do not use shell=True."
    elif vuln_type == "SQLi":
        instructions = "Use parameterized queries (sqlite3 '?' placeholders) instead of f-strings. Do NOT use string concatenation for SQL."
    else:
        instructions = "Fix the security vulnerability securely."

    prompt = f"""
    You are a Senior Security Engineer.
    Task: Fix a {vuln_type} vulnerability in the Python code below.

    VULNERABLE CODE:
    {source_code}

    ATTACK VECTOR THAT WORKED:
    {attack_payload}

    INSTRUCTIONS:
    1. {instructions}
    2. Maintain original functionality.
    3. Return ONLY the complete fixed code. No Markdown, no comments like 'Here is the code'.
    """

    # Використовуємо Qwen (він кращий кодер) або Dolphin
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "qwen2.5-coder:7b", # Переконайся, що ця модель у тебе є, або зміни на dolphin-llama3
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2}
    }

    try:
        response = requests.post(url, json=data)
        ai_text = response.json()['response']
        # Чистимо код
        fixed_code = ai_text.replace("```python", "").replace("```", "").strip()
        print("🛡️ DEFENDER: Patch generated.")
        return fixed_code
    except Exception as e:
        print(f"❌ DEFENDER ERROR: {e}")
        return None
