import os
import json
import requests
from datetime import datetime

def load_rotation_data():
    with open("rotation_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def post_to_discord(message, webhook_url):
    payload = {
        "content": message
    }
    response = requests.post(webhook_url, json=payload)

    if response.status_code != 204:
        print(f"Failed to send message to Discord. Status code: {response.status_code}, Response: {response.text}")
    else:
        print("Message successfully posted to Discord.")

def main():
    # Safely get the Discord webhook URL
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("DISCORD_WEBHOOK_URL is not set. Please check your environment variables or GitHub Secrets.")

    rotation_data = load_rotation_data()

    today_str = datetime.utcnow().strftime("%B %d, %Y")
    maps = rotation_data.get("maps", [])

    # Build the message
    message = f"📢 PUBG PC Map Rotation Update — {today_str}\n\n🖥️ PC Normal Match\n"
    for map_name in maps:
        message += f"- {map_name}\n"

    # Post the message
    post_to_discord(message, webhook_url)

if __name__ == "__main__":
    main()
