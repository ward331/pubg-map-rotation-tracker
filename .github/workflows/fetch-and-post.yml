name: Fetch and Post PUBG Map Rotation

on:
  schedule:
    - cron: '0 9 * * *'  # Runs every day at 9:00 UTC (5 AM EST)
  workflow_dispatch:    # Allows you to manually trigger it too

jobs:
  fetch-and-post:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install Python dependencies
        run: |
          pip install requests beautifulsoup4

      - name: Fetch latest PUBG rotation data
        run: |
          python pubg_map_rotation_updater.py

      - name: Post rotation to Discord
        run: |
          python discord_rotation_poster.py
