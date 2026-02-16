import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://www.wheresthematch.com/"

# List of competitions to include (filter target sports)
TARGET_COMPETITIONS = [
    "Premier League", "FA Cup", "Carabao Cup", "Champions League",
    "Rugby Union", "PGA Tour", "Ryder Cup"
]

def scrape_schedule():
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, "html.parser")

    events = []

    # Find main TV listings section
    # Adjust selector if site changes
    table = soup.find("div", {"class": "tvFixtures"}) or soup.select_one("table")
    if table:
        rows = table.select("tr")[1:]  # skip header
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            try:
                name = cols[0].get_text(strip=True)
                time = cols[1].get_text(strip=True)
                competition = cols[2].get_text(strip=True)
                if competition not in TARGET_COMPETITIONS:
                    continue
                channels = [img["alt"].strip() for img in cols[3].select("img[alt]")]
            except Exception:
                continue
            events.append({
                "name": name,
                "time": time,
                "competition": competition,
                "channels": channels
            })

    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "events": events
    }

    with open("tv_schedule.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    scrape_schedule()
