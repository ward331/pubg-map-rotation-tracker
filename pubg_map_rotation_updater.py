def fetch_pc_rotation():
    url = "https://pubgchallenge.co/pubg-map-rotation"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    pc_map_data = []
    map_rows = soup.select("div.map-rotation div.map-row")  # Adjust this selector as needed
    for row in map_rows:
        name = row.select_one("span.map-name")  # Adjust this selector as needed
        percent = row.select_one("span.map-percentage")  # Adjust this selector as needed
        if name and percent:
            pc_map_data.append((name.get_text(strip=True), percent.get_text(strip=True)))

    return pc_map_data
