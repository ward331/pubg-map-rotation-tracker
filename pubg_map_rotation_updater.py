from datetime import date

OUTPUT_FILE = "index.html"

PC_ROTATION = [
    ("Erangel", "36%"),
    ("Vikendi", "18%"),
    ("Paramo", "9%"),
    ("Rondo", "18%"),
    ("Miramar", "18%")
]

CONSOLE_ROTATION = [
    ("Erangel", "20%"),
    ("Taego", "20%"),
    ("Rondo", "20%"),
    ("Vikendi", "20%"),
    ("Deston", "20%")
]

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
  <p>Updated automatically from GitHub Actions.</p>

  <h2>🖥️ PC Normal Match</h2>
"""

for name, percent in PC_ROTATION:
    html += f"""
  <div class='map'>
    <img src='{MAP_IMAGES[name]}' alt='{name} map'>
    <div><strong>{name}</strong> — {percent}</div>
  </div>
"""

html += """
  <h2>🎮 Console Normal Match</h2>
"""

for name, percent in CONSOLE_ROTATION:
    html += f"""
  <div class='map'>
    <img src='{MAP_IMAGES[name]}' alt='{name} map'>
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

print(f"✅ Updated {OUTPUT_FILE} with PUBG map rotation.")
