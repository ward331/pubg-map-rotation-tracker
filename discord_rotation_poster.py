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

# Scrape community rotation from pubgchallenge.co using span.map-name tags
def get_community_maps():
    url = "https://pubgchallenge.co/pubg-map-rotation"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    maps = []

    try:
        for tag in soup.find_all("span", class_="map-name"):
            name = tag.get_text(strip=True)
            if name and name not in maps:
                maps.append(name)
    except Exception as e:
        print("Error scraping community maps:", e)

    return maps

# Get community map list
community_maps = get_community_maps()

# Debug output to GitHub Actions logs
print("✅ Community maps scraped:", community_maps)

# Format community rotation with ⚠️ for maps not in official list
formatted_community = []
for map_name in community_maps:
    warning = " ⚠️ This map might not be in the current live rotation." if map_name not in official_maps else ""
    formatted_community.append(f"- {map_name}{warning}")
formatted_community_str = "\n".join(formatted_community) if formatted_community else "*No maps found.*"

# Final message to Discord
message = f"""📢 PUBG PC Map Rotation Update — {today}

🖥️ **Official PUBG Source**
{formatted_official}

🌐 **Community Source**
{formatted_community_str}
"""

# Send message to Discord
requests.post(WEBHOOK_URL, json={"content": message})
