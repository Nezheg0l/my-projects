from agents.attacker_v2 import RedTeamAgent

# Ініціалізація
bot = RedTeamAgent()

# 1. Тест SQL Injection
print("=== TESTING SQL INJECTION ===")
bot.attack("SQLi", max_retries=3)

print("\n" + "="*30 + "\n")

# 2. Тест RCE
print("=== TESTING RCE ===")
bot.attack("RCE", max_retries=3)

