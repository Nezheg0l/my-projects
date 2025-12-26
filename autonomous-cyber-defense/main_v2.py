import time
import subprocess
import os
import ast
import shutil
from agents.attacker_v2 import RedTeamAgent
from agents.defender import patch_vulnerability

# Налаштування
VICTIM_DIR = "victim"
VICTIM_FILE = os.path.join(VICTIM_DIR, "app.py")
BACKUP_FILE = os.path.join(VICTIM_DIR, "app.py.bak")
bot = RedTeamAgent()

def is_valid_python(code):
    """Перевіряє, чи код взагалі запускається"""
    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        print(f"❌ SYNTAX ERROR in AI Code: {e}")
        return False

def restart_docker():
    print("🔄 SYSTEM: Rebuilding & Restarting Victim...")
    try:
        subprocess.run("docker build --no-cache -t victim_app victim/", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("docker rm -f victim_container", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("docker run -d --name victim_container -p 5000:5000 victim_app", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        return True
    except Exception as e:
        print(f"❌ DOCKER ERROR: {e}")
        return False

def run_functionality_tests():
    """Запускає tests.py всередині або зовні"""
    try:
        result = subprocess.run(["python3", "victim/tests.py"], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"❌ FUNCTIONALITY TESTS FAILED:\n{result.stdout}")
            return False
    except Exception as e:
        print(f"❌ TEST SCRIPT ERROR: {e}")
        return False

def run_evolution_cycle():
    print("🚀 STARTING AI SECURITY PIPELINE (CI/CD Mode)")
    
    targets = ["SQLi", "RCE"]

    for attack_type in targets:
        print(f"\n" + "="*40)
        print(f"🎯 TARGET: {attack_type}")
        print("="*40)
        
        # 1. АТАКА
        payload = bot.attack(attack_type, max_retries=3)
        
        if payload:
            print(f"🚨 BREACH DETECTED! Initiating Patching Protocol...")
            
            # Робимо бекап перед змінами
            shutil.copy(VICTIM_FILE, BACKUP_FILE)
            
            # Читаємо код
            with open(VICTIM_FILE, "r") as f:
                code = f.read()
            
            # 2. ЗАХИСТ (Генерація патчу)
            fixed_code = patch_vulnerability(code, payload, attack_type)
            
            # 3. ВАЛІДАЦІЯ (Quality Gate 1: Syntax)
            if fixed_code and is_valid_python(fixed_code):
                # Зберігаємо патч
                with open(VICTIM_FILE, "w") as f:
                    f.write(fixed_code)
                print(f"💾 PATCH APPLIED. Validating functionality...")
                
                # 4. ДЕПЛОЙ
                if restart_docker():
                    
                    # 5. ТЕСТУВАННЯ (Quality Gate 2: Business Logic)
                    if run_functionality_tests():
                        print("✅ TESTS PASSED. Functionality intact.")
                        
                        # 6. ВЕРИФІКАЦІЯ БЕЗПЕКИ
                        print(f"🕵️ SECURITY VERIFICATION: Retrying attack...")
                        retry = bot.attack(attack_type, max_retries=1)
                        
                        if not retry:
                            print(f"🏆 SUCCESS: {attack_type} is SECURE and FUNCTIONAL!")
                            # Видаляємо бекап, все ок
                            os.remove(BACKUP_FILE)
                        else:
                            print(f"❌ FAIL: Patch applied but vulnerability remains.")
                            print("↺ ROLLBACK: Reverting to previous version...")
                            shutil.move(BACKUP_FILE, VICTIM_FILE)
                            restart_docker()
                    else:
                        print("❌ REJECTED: Patch broke the application.")
                        print("↺ ROLLBACK: Reverting to previous version...")
                        shutil.move(BACKUP_FILE, VICTIM_FILE)
                        restart_docker()
                else:
                    print("❌ REJECTED: Docker failed to start.")
                    shutil.move(BACKUP_FILE, VICTIM_FILE)
            else:
                print("❌ REJECTED: AI generated invalid Python code.")
        
        else:
            print(f"🎉 SECURE: System resisted {attack_type} attempts.")

if __name__ == "__main__":
    # Початковий запуск
    restart_docker()
    run_evolution_cycle()
