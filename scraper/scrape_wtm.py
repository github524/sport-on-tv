import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.wheresthematch.com/"
OUTPUT_FILE = "tv_schedule.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SportsOnTVBot/1.0)"
}

ALLOWED_CHANNELS = [
    "BBC",
    "ITV",
    "Sky Sports",
    "TNT Sports"
]

ALLOWED_SPORTS = [
    "Football",
    "Rugby",
    "Golf"
]


def allowed_channel(channel_text):
    return any(c.lower() in channel_text.lower() for c in ALLOWED_CHANNELS)


def allowed_sport(sport_text):
    return any(s.lower() in sport_text.lower() for s in ALLOWED_SPORTS)


def scrape():
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    events = []

    # Each listing row is in a table row
    rows = soup.select("table tr")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        time_text = cells[0].get_text(strip=True)
        event_text = cells[1].get_text(strip=True)
        competition_text = cells[2].get_text(strip=True)
        channel_text = cells[3].get_text(strip=True)

        if not allowed_channel(channel_text):
            continue

        if not allowed_sport(competition_text + " " + event_text):
            continue

        events.append({
            "time": time_text,
            "event": event_text,
            "competition": competition_text,
            "channel": channel_text
        })

    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "events": events
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    scrape()

