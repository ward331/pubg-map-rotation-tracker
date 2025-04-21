import requests
import os
import json
from datetime import date
from bs4 import BeautifulSoup

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# Load current map rotation data from JSON
with open("rotation_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

PC_ROTATION = data["PC_ROTATION"]
today = date.today().strftime("%B %d, %Y")

# Format official list
official_maps = [name for name, _ in PC_ROTATION]
formatted_official = "\n".join([f"- {name} — {percent}" for name, percent in PC_ROTATION])

# Scrape community map rotation from pubgchallenge.co
def get_community_maps():
    url = "https://pubgchallenge.co/pubg-map-rotation"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    maps = []
    pc_section = soup.find("div", id="pc")
    if pc_section:
        for span in pc_section.select("span.map-name"):
            map_name = span.get_text(strip=True)
            maps.append(map_name)
    return maps

community_maps = get_community_maps()

formatted_community = []
for map_name in community_maps:
    warning = ""
    if map_name not in official_maps:
        warning = " ⚠️ This map might not be in the current live rotation."
    formatted_community.append(f"- {map_name}{warning}")
formatted_community_str = "\n".join(formatted_community)

# Final message
message = f"""📢 PUBG PC Map Rotation Update — {today}

🖥️ **Official PUBG Source**
{formatted_official}

🌐 **Community Source**
{formatted_community_str}
"""

# Send to Discord
requests.post(WEBHOOK_URL, json={"content": message})
