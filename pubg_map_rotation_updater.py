def fetch_pc_rotation():
    url = "https://pubgchallenge.co/pubg-map-rotation"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    pc_map_data = []

    # The new structure uses table rows under id="pc-normal-match"
    pc_table = soup.find("table", id="pc-normal-match")
    if pc_table:
        rows = pc_table.find_all("tr")[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                name = cols[0].text.strip()
                percent = cols[1].text.strip()
                pc_map_data.append((name, percent))

    return pc_map_data
