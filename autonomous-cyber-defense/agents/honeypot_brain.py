import requests
import json

def generate_fake_output(command):
    # Це мозок нашої пастки. Він придумує вивід консолі.
    
    prompt = f"""
    You are a high-interaction Honeypot simulating an Ubuntu Linux server.
    An attacker just executed the command: `{command}`.
    
    YOUR TASK:
    Generate a REALISTIC terminal output for this command.
    
    RULES:
    1. If the command is 'ls', list some boring files AND one "juicy" file (e.g., 'passwords.txt', 'wallet.dat', 'config.php').
    2. If the command is 'cat' or 'grep', generate fake content that looks valuable but is fake.
    3. If the command is 'whoami', reply 'root'.
    4. Do NOT explain anything. Output ONLY the raw terminal text.
    5. Be consistent. This is a Banking Server.
    """

    url = "http://localhost:11434/api/generate"
    data = {
        "model": "qwen2.5-coder:7b", # Твій розумний захисник
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.4} # Трохи креативності, але щоб було схоже на правду
    }

    try:
        response = requests.post(url, json=data)
        result = response.json()['response'].strip()
        # Чистимо від маркдауну, якщо він є
        return result.replace("```bash", "").replace("```", "")
    except Exception as e:
        return f"Error simulating output: {e}"

# Тест
if __name__ == "__main__":
    print(generate_fake_output("ls -la /var/www/html"))
