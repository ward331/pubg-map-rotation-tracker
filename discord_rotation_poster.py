import requests
import os
from datetime import date

# Load the webhook from environment variable (GitHub Secret)
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

PC_ROTATION = [
    ("Erangel", "36%"),
    ("Vikendi", "18%"),
    ("Paramo", "9%"),
    ("Rondo", "18%"),
    ("Miramar", "18%")
]

CONSOLE_ROTATION = [
    ("Erangel", "20%"),
    ("Taego", "20%"),
    ("Rondo", "20%"),
    ("Vikendi", "20%"),
    ("Deston", "20%")
]

today = date.today().strftime("%B %d, %Y")

message = f"""📢 **PUBG Map Rotation Update** — {today}

🖥️ **PC Normal Match**
""" + "\n".join([f"- {name} — {percent}" for name, percent in PC_ROTATION]) + """

🎮 **Console Normal Match**
""" + "\n".join([f"- {name} — {percent}" for name, percent in CONSOLE_ROTATION]) + """

🌐 https://glittering-hotteok-f6b8ac.netlify.app
"""

requests.post(WEBHOOK_URL, json={"content": message})
