
from datetime import date
import requests
from bs4 import BeautifulSoup

OUTPUT_FILE = "index.html"

# 🔍 Scrape PC Normal Match rotation from pubgchallenge.co
def fetch_pc_rotation():
    url = "https://pubgchallenge.co/pubg-map-rotation"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the PC Normal Match section only
    pc_section = soup.find("h2", string="PC Normal Match")
    pc_map_data = []
    if pc_section:
        map_rows = pc_section.find_next("div", class_="map-rotation").find_all("div", class_="map-row")
        for row in map_rows:
            name = row.select_one("span.map-name")
            percent = row.select_one("span.map-percentage")
            if name and percent:
                pc_map_data.append((name.get_text(strip=True), percent.get_text(strip=True)))

    return pc_map_data

# ✅ Pull live PC rotation
PC_ROTATION = fetch_pc_rotation()

MAP_IMAGES = {
    "Erangel": "https://www.pubg.com/wp-content/uploads/2023/12/Erangel_Map.jpg",
    "Vikendi": "https://www.pubg.com/wp-content/uploads/2023/12/Vikendi_Map.jpg",
    "Paramo": "https://www.pubg.com/wp-content/uploads/2023/12/Paramo_Map.jpg",
    "Rondo": "https://www.pubg.com/wp-content/uploads/2023/12/Rondo_Map.jpg",
    "Miramar": "https://www.pubg.com/wp-content/uploads/2023/12/Miramar_Map.jpg",
    "Taego": "https://www.pubg.com/wp-content/uploads/2023/12/Taego_Map.jpg",
    "Deston": "https://www.pubg.com/wp-content/uploads/2023/12/Deston_Map.jpg"
}

html = f"""<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>PUBG Map Rotation Tracker</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background: #0d0d0d;
      color: #f5f5f5;
      padding: 2rem;
      max-width: 900px;
      margin: auto;
    }}
    h1, h2 {{
      color: #facc15;
    }}
    .map {{
      background: #1a1a1a;
      padding: 1rem;
      border-radius: 8px;
      margin-top: 1rem;
      display: flex;
      align-items: center;
      gap: 1rem;
    }}
    .map img {{
      width: 120px;
      height: auto;
      border-radius: 5px;
    }}
    .footer {{
      font-size: 0.9rem;
      color: #888;
      margin-top: 3rem;
    }}
    a {{
      color: #facc15;
    }}
  </style>
</head>
<body>
  <h1>PUBG Map Rotation Tracker</h1>
  <p>Updated automatically from PUBGChallenge.co.</p>

  <h2>🖥️ PC Normal Match</h2>
"""

for name, percent in PC_ROTATION:
    img_url = MAP_IMAGES.get(name, "")
    html += f"""
  <div class='map'>
    <img src='{img_url}' alt='{name} map'>
    <div><strong>{name}</strong> — {percent}</div>
  </div>
"""

html += f"""
  <div class='footer'>
    Last updated: {date.today().strftime('%B %d, %Y')}
  </div>
</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

# 👀 Preview output in log for GitHub Actions or Railway
with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
    print("✅ index.html content preview:\n")
    print(f.read())
