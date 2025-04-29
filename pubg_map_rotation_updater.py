def fetch_pc_rotation_from_pubg():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(PATCH_NOTES_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    maps = []

    # Look for all headings and check if they relate to PC Normal Match
    for header in soup.find_all(["h1", "h2", "h3", "h4", "strong", "b", "p"]):
        if "PC Normal Match" in header.get_text():
            ul = header.find_next_sibling("ul")
            if ul:
                for li in ul.find_all("li"):
                    maps.append(li.get_text(strip=True))
                break
            else:
                maps.append("Header found, but no map list under it.")
                break

    if not maps:
        maps.append("PC Normal Match section not found.")

    return {
        "date": str(datetime.utcnow().date()),
        "maps": maps
    }
