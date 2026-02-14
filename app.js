const output = document.getElementById("output");

const API_KEY = "496ad6a968a9b503a61d649c2b2a4ce8";

const today = new Date().toISOString().split("T")[0];

// Competition IDs (API-Football)
const competitions = [
  39,   // Premier League
  45,   // FA Cup
  48,   // Carabao Cup
  2     // Champions League
];

// UK channels we care about
const allowedChannels = [
  "BBC",
  "ITV",
  "Sky Sports",
  "TNT Sports"
];

async function loadFixtures() {
  try {
    let allMatches = [];

    for (const league of competitions) {
      const res = await fetch(
        `https://v3.football.api-sports.io/fixtures?league=${league}&date=${today}`,
        {
          headers: {
            "x-apisports-key": API_KEY
          }
        }
      );

      const data = await res.json();
      allMatches = allMatches.concat(data.response);
    }

    if (allMatches.length === 0) {
      output.textContent = "No football on TV today.";
      return;
    }

    const results = [];

    allMatches.forEach(match => {
      if (!match.broadcasts || !match.broadcasts.tv) return;

      match.broadcasts.tv.forEach(tv => {
        if (
          tv.country === "United Kingdom" &&
          allowedChannels.some(c => tv.name.includes(c))
        ) {
          results.push({
            match: `${match.teams.home.name} vs ${match.teams.away.name}`,
            time: new Date(match.fixture.date).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit"
            }),
            channel: tv.name
          });
        }
      });
    });

    if (results.length === 0) {
      output.textContent = "Football today, but not on your selected channels.";
      return;
    }

    output.innerHTML = results
      .map(
        r =>
          `<strong>${r.match}</strong><br>${r.time} — ${r.channel}<br><br>`
      )
      .join("");

  } catch (err) {
    output.textContent = "Error loading data.";
  }
}

loadFixtures();

