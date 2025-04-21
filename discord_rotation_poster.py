import requests
import os
import json
from datetime import date
from bs4 import BeautifulSoup

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# Load official map rotation from local JSON
with open("rotation_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

PC_ROTATION = data["PC_ROTATION"]
today = date.today().strftime("%B %d, %Y")

# Build list of official map names for comparison
official_maps = [name for name, _ in PC_ROTATION]

# Format official rotation for message
formatted_official = "\n".join([f"- {name} — {percent}" for name, percent in PC_ROTATION])

# Scrape from pubgchallenge.co
def get_community_maps():
    url = "https://pubgchallenge.co/pubg-map-rotation"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    map_data = []

    try:
        current_rotation_header = soup.find("h2", string=lambda s: s and "Current PUBG Map Rotation (PC)" in s)
        if current_rotation_header:
            for row in current_rotation_header.find_all_next("div", class_="map-row"):
                name_tag = row.find("h3")
                percent_tag = row.find("div", class_="map-percentage")
                if name_tag and percent_tag:
                    name = name_tag.get_text(strip=True)
                    percent = percent_tag.get_text(strip=True)
                    map_data.append((name, percent))
    except Exception as e:
        print("Error scraping community maps:", e)

    return map_data

# Get PUBGChallenge.co map data
community_map_data = get_community_maps()

# Debug output
print("✅ PUBGChallenge.co maps scraped:", community_map_data)

# Filter to only show maps that are in the official rotation
formatted_pubgchallenge = []
for name, percent in community_map_data:
    if name in official_maps:
        formatted_pubgchallenge.append(f"- {name} — {percent}")
formatted_pubgchallenge_str = "\n".join(formatted_pubgchallenge) if formatted_pubgchallenge else "*No maps found.*"

# Final message to Discord
message = f"""📢 PUBG PC Map Rotation Update — {today}

🖥️ **Official PUBG Source**
{formatted_official}

🌐 **PUBGChallenge.co Source**
{formatted_pubgchallenge_str}
"""

# Send message to Discord
requests.post(WEBHOOK
