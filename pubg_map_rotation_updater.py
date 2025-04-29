import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

PATCH_NOTES_URL = "https://www.pubg.com/en-us/news/8476"

def fetch_pc_rotation_from_pubg():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(PATCH_NOTES_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all paragraph tags to look for "PC Normal Match"
    maps = []
    found_section = False
    for tag in soup.find_all(['p', 'ul', 'li']):
        text = tag.get_text(strip=True)

        if "PC Normal Match" in text:
            found_section = True
            continue

        # After finding the header, collect list items
        if found_section:
            if tag.name == "ul":
                for li in tag.find_all("li"):
                    maps.append(li.get_text(strip=True))
                break
            elif tag.name == "p" and any(map in text.lower() for map in ["erangel", "miramar", "taego", "karakin", "rondo"]):
                maps.append(text)
            elif tag.name == "p":
                break  # Stop if non-map text is hit

    if not maps:
        maps.append("❌
