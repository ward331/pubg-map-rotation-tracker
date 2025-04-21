import requests
import os
import json
from datetime import date
from bs4 import BeautifulSoup, NavigableString

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

# Scrape from pubgchallenge.co using reliable sibling scan
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
                    break  # stop if we hit the Console header
                if current.name == "h3":
                    name = current.get_text(strip=True)
                    percent = None

                    for sib in current.next_siblings:
                        if isinstance(sib, NavigableString):
                            continue
                        if sib.name and "probability" in sib.get_text().lower():
                            percent = sib.get_text(strip=True).replace("probability", "").strip()
                            break

                    if name and percent:
                        map_data.append((name, percent))
                current = current.find_next_sibling()
    except Exception as e:
        print("Error scraping pubgchallenge.co maps:", e)

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
requests.post(WEBHOOK_URL, json={"content": message})
