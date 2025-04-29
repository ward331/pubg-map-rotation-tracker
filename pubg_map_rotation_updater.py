import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# PUBG official patch notes URL – update this to the latest patch when needed
PATCH_NOTES_URL = "https://www.pubg.com/en-us/news/8476"

def fetch_pc_rotation_from_pubg():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(PATCH_NOTES_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Try to find the section mentioning "PC Normal Match"
    rotation_header = soup.find(string=lambda text: text and "PC Normal Match" in text)

    maps = []

    if rotation_header:
        list_block = rotation_header.find_parent().find_next_sibling()
        if list_block and list_block.name == "ul":
            for li in list_block.find_all("li"):
                maps.append(li.get_text(strip=True))
        else:
            maps.append("No map list found after 'PC Normal Match'.")
    else:
        maps.append("PC Normal Match section not found.")

    return {
        "date": str(datetime.utcnow().date()),
        "maps": maps
    }

def save_rotation_data(data):
    with open("rotation_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    data = fetch_pc_rotation_from_pubg()
    save_rotation_data(data)

if __name__ == "__main__":
    main()
