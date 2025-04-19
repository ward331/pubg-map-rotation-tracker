import requests
import os
import json
from datetime import date

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# Load current map rotation data from JSON
with open("rotation_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

PC_ROTATION = data["PC_ROTATION"]
today = date.today().strftime("%B %d, %Y")

message = f"""📢 PUBG PC Map Rotation Update — {today}

🖥️ **PC Normal Match**
""" + "\n".join([f"- {name} — {percent}" for name, percent in PC_ROTATION])

requests.post(WEBHOOK_URL, json={"content": message})
