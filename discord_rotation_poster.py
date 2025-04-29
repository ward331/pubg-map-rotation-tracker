import requests
from bs4 import BeautifulSoup
import os
from datetime import date

# Load Discord webhook from environment variable
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

def fetch_pc_rotation():
    url = "https://pubgchallenge.co/pubg-map-rotation"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    pc_map_data = []
    pc_table = soup.find("table", id="pc-normal-match")
    if pc_table:
        rows = pc_table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                name = cols[0].text.strip()
                percent = cols[1].text.strip()
                pc_map_data.append((name, percent))
    return pc_map_data

# Get the latest rotation
PC_ROTATION = fetch_pc_rotation()

# Build the message
today = date.today().strftime("%B %d, %Y")
message = f"""📢 **PUBG PC Map Rotation Update** — {today}

🖥️ **PC Normal Match**
""" + "\n".join([f"- {name} — {percent}" for name, percent in PC_ROTATION])

# Post to Discord
requests.post(WEBHOOK_URL, json={"content": message})
