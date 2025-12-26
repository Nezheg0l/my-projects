from agents.attacker_v2 import RedTeamAgent


bot = RedTeamAgent()

print("=== TESTING SQL INJECTION ===")
bot.attack("SQLi", max_retries=3)

print("\n" + "="*30 + "\n")

print("=== TESTING RCE ===")
bot.attack("RCE", max_retries=3)

