import requests
import os
import json
from datetime import date
from bs4 import BeautifulSoup, NavigableString, Tag

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# Load official map rotation from local JSON
with open("rotation_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

PC_ROTATION = data["PC_ROTATION"]
today = date.today().strftime("%B %d, %Y")
official_maps = [name for name, _ in PC_ROTATION]

# Format official rotation
formatted_official = "\n".join([f"- {name} — {percent}" for name, percent in PC_ROTATION])

def get_community_maps():
    url = "https://pubgchallenge.co/pubg-map-rotation"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    map_data = []

    try:
        pc_header = soup.find("h2", string=lambda s: s and "Current PUBG Map Rotation (PC)" in s)
        if pc_header:
            current = pc_header.find_next_sibling()
            while current:
                if current.name == "h2":
                    break  # stop at Console section
                if current.name == "h3":
                    map_name = current.get_text(strip=True)
                    percent = None
                    sibling = current.find_next_sibling()
                    while sibling and (isinstance(sibling, NavigableString) or sibling.name != "h3"):
                        if isinstance(sibling, Tag):
                            text = sibling.get_text(strip=True)
                            if "probability" in text.lower():
                                percent = text.replace("probability", "").strip()
                                break
                        sibling = sibling.find_next_sibling()
                    if map_name and percent:
                        map_data.append((map_name, percent))
                current = current.find_next_sibling()
    except Exception as e:
        print("Error scraping pubgchallenge.co maps:", e)

    return map_data

# Get community map data
community_map_data = get_community_maps()
print("✅ PUBGChallenge.co maps scraped:", community_map_data)

# Only include maps that match the official list
formatted_pubgchallenge = []
for name, percent in community_map_data:
    if name in official_maps:
        formatted_pubgchallenge.append(f"- {name} — {percent}")
formatted_pubgchallenge_str = "\n".join(formatted_pubgchallenge) if formatted_pubgchallenge else "*No maps found.*"

# Final message
message = f"""📢 PUBG PC Map Rotation Update — {today}

🖥️ **Official PUBG Source**
{formatted_official}

🌐 **PUBGChallenge.co Source**
{formatted_pubgchallenge_str}
"""

# Post to Discord
requests.post(WEBHOOK_URL, json={"content": message})
