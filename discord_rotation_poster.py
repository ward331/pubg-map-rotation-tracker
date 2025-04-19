import requests
import json
import os
from datetime import date

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# Read rotation data from JSON
with open("rotation_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

PC_ROTATION = data["PC_ROTATION"]
CONSOLE_ROTATION = data["CONSOLE_ROTATION"]

today = date.today().strftime("%B %d, %Y")

message = f"""📢 **PUBG Map Rotation Update** — {today}

🖥️ **PC Normal Match**
""" + "\n".join([f"- {name} — {percent}" for name, percent in PC_ROTATION]) + """

🎮 **Console Normal Match**
""" + "\n".join([f"- {name} — {percent}" for name, percent in CONSOLE_ROTATION])

requests.post(WEBHOOK_URL, json={"content": message})
