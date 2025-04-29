import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

ROTATION_URL = "https://pubgchallenge.co/pubg-map-rotation"

def fetch_pc_rotation_from_pubgchallenge():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(ROTATION_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    maps = []

    # Look for PC section
    pc_section = soup.find("div", class_="map-rotation")
    if pc_section:
        for row in pc_section.select("div.map-row"):
            name = row.select_one("span.map-name")
            percent = row.select_one("span.map-percentage")
            if name and percent:
                maps.append(f"{name.text.strip()} — {percent.text.strip()}")
    else:
        maps.append("PC rotation section not found.")

    return {
        "date": str(datetime.utcnow().date()),
        "maps": maps
    }

def save_rotation_data(data):
    with open("rotation_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    data = fetch_pc_rotation_from_pubgchallenge()
    save_rotation_data(data)

if __name__ == "__main__":
    main()
