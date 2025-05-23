import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

ROTATION_URL = f"http://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url=https://pubgchallenge.co/pubg-map-rotation"

def fetch_pc_rotation():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(ROTATION_URL, headers=headers)

    # 👇 Dump full HTML so we can inspect what ScraperAPI returns
    print("=== FULL HTML RAW DUMP ===")
    print(response.text)
    print("=== END DUMP ===")

    soup = BeautifulSoup(response.text, "html.parser")

    maps = []
    pc_section = soup.find("div", class_="map-rotation")
    if pc_section:
        for row in pc_section.select("div.map-row"):
            name = row.select_one("span.map-name")
            percent = row.select_one("span.map-percentage")
            if name and percent:
                maps.append(f"{name.text.strip()} — {percent.text.strip()}")
    if not maps:
        maps.append("PC rotation section not found.")

    return maps

def post_to_discord(maps):
    if not DISCORD_WEBHOOK_URL:
        raise ValueError("DISCORD_WEBHOOK_URL is not set.")
    
    today_str = datetime.utcnow().strftime("%B %d, %Y")
    message = f"📢 PUBG PC Map Rotation Update — {today_str}\n\n🖥️ PC Normal Match\n"
    for map_line in maps:
        message += f"- {map_line}\n"

    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    if response.status_code != 204:
        print(f"Discord POST failed ({response.status_code}): {response.text}")
    else:
        print("✅ Posted to Discord.")

def main():
    maps = fetch_pc_rotation()
    post_to_discord(maps)

if __name__ == "__main__":
    main()
