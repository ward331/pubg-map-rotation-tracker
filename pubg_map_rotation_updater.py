import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URL of official PUBG patch notes (Update this link if a new patch is released)
PATCH_NOTES_URL = "https://www.pubg.com/en-us/news/8476"

def fetch_pc_rotation_from_pubg():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(PATCH_NOTES_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Try to find section mentioning "
