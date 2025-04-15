import requests
import os
from datetime import date

# Load the webhook from GitHub Secrets
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# PC Rotation only
PC_ROTATION = [
    ("Erangel", "36%"),
    ("Vikendi", "18%"),
    ("Paramo", "9%"),
    ("Rondo", "18%"),
    ("Miramar", "18%")
]

# Format today's date
today = date.today().strftime("%B %d, %Y")

# Build the Discord message
message = f"""📢 **PUBG PC Map Rotation Update** — {today}

🖥️ **PC Normal Match**
""" + "\n".join([f"- {name} — {percent}" for name, percent in PC_ROTATION])

# Send it to Discord
requests.post(WEBHOOK_URL, json={"content": message})
