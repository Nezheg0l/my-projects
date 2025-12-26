import requests
import time
import os
import subprocess

from agents.attacker import get_exploit_from_ai
from agents.defender import patch_vulnerability

TARGET_URL = "http://localhost:5000/ping"
VICTIM_FILE_PATH = "victim/app.py"

def restart_docker():
    print("🔄 SYSTEM: Restarting Victim Container to apply patch...")
    try:
        subprocess.run("docker build -t victim_app victim/", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("docker rm -f victim_container", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("docker run -d --name victim_container -p 5000:5000 victim_app", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        time.sleep(5)
        print("✅ SYSTEM: Victim restarted successfully.")
    except Exception as e:
        print(f"❌ SYSTEM ERROR during Docker restart: {e}")

def run_battle():
    print("🚀 STARTING AI WARFARE SIMULATION...")

    print("\n--- [ PHASE 1: RED TEAM ATTACK (Ollama) ] ---")
    payload = get_exploit_from_ai(TARGET_URL)
    
    if not payload:
        print("❌ Red Team failed to generate payload.")
        return

    print(f"⚔️ ATTACKING with: {payload}")
    
    try:
        response = requests.get(TARGET_URL, params={'ip': payload}, timeout=5)
        
        if "root" in response.text or "uid=" in response.text:
            print("🚩 PWNED! Vulnerability confirmed (RCE).")
            
            print("\n--- [ PHASE 2: BLUE TEAM DEFENSE (Gemini) ] ---")
            
            with open(VICTIM_FILE_PATH, "r") as f:
                vulnerable_code = f.read()
            
            fixed_code = patch_vulnerability(vulnerable_code, payload)
            
            if fixed_code:
                with open(VICTIM_FILE_PATH, "w") as f:
                    f.write(fixed_code)
                print("💾 PATCH APPLIED to victim/app.py")
                
                restart_docker()
                
                print("\n--- [ PHASE 3: VERIFICATION ] ---")
                print("🕵️ Re-testing with the same exploit...")
                try:
                    response_v2 = requests.get(TARGET_URL, params={'ip': payload}, timeout=5)
                    
                    if "root" not in response_v2.text and "uid=" not in response_v2.text:
                        print("🛡️ SUCCESS! The patch blocked the attack.")
                        print(f"Server response code: {response_v2.status_code}")
                    else:
                        print("❌ FAIL! The patch didn't work. Still vulnerable.")
                        print(response_v2.text)
                except Exception as e:
                    print(f"ℹ️ Note: Server might have blocked the connection (Good sign). Error: {e}")

            else:
                print("❌ Blue Team failed to generate a patch.")
            
        else:
            print("🛡️ Attack Failed initially. No RCE detected.")
            
    except Exception as e:
        print(f"❌ Error during attack phase: {e}")

if __name__ == "__main__":
    run_battle()
