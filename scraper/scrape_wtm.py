import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URL for today’s live TV listings
URL = "https://www.wheresthematch.com/"

def scrape_schedule():
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the section with live TV listings
    # On wheresthematch.com the live table rows often have a structure with
    # repeated fixtures under a <div> or <section>. Adjust selectors if needed.
    table = soup.find("div", {"class": "tvFixtures"} ) or soup.select_one("table")

    events = []

    if table:
        # Often it's a table; loop through rows (skip header)
        rows = table.select("tr")[1:]  # skip header

        for row in rows:
            cols = row.find_all("td")
            if not cols:
                continue

            # Example column order observed:
            # [Live indicator/name, When GMT time, Competition, Channel elements]
            try:
                name = cols[0].get_text(strip=True)
                time = cols[1].get_text(strip=True)
                competition = cols[2].get_text(strip=True)
                # Channels can be a series of <img> or <span> icons with alt text
                channels = [
                    img["alt"].strip() for img in cols[3].select("img[alt]")
                ]
            except Exception as e:
                # skip rows which don’t match expected structure
                continue

            event = {
                "name": name,
                "time": time,
                "competition": competition,
                "channels": channels,
            }
            events.append(event)

    # Build output JSON
    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "events": events
    }

    # Write the result
    with open("tv_schedule.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    scrape_schedule()
