NBA Fantasy Winner Project

NBA fantasy season starts end of October and I plan to make a program that takes players teams and gets their ideal lineup to maximize points based on matchups and fantasy points

So how it would work:

You as a manager select a hypothetical lineup:
Luka Doncic
Donavan Mitchell
Lebron Jame
Giannis Antekoumpo
Victor Wembanya 
Karl Anthony towns
Nikola Jokic 

Before every game day: 
Take Player X and find what team he is playing against:
Example: Luka Doncic is playing against the Dallas Mavericks
See how Player X historically played against Team Y.
Take the stats from each game and average them across the seasons.
Like in 2022, Player X played against Team Y 8 times. 
Player X averaged 24.5 points, 3.8 assists, 8.3 rebounds, 12 threes and 2.3 steals per game in 2022.

According to how fantasy points work:
Fantasy Points = (points * 1) + (assists * 1.5) + (rebounds * 1.2) + (steals * 3) + (blocks * 3) - (turnovers * 1) + (threes made * 0.5)
Find the average Fantasy Points for Player X and save it.

Follow the same process for the last 5 seasons. So for this season, we should be taking 2020 to present.

Curve the points so seasons that are closer to present time have more weight. 

Save the fantasy points and make multiple graphs using these data points.

Get the projected fantasy points for each player and make a list of the highest points per position

Show user lineup


nba-fantasy-optimizer/
├── src/
│   ├── data_collectors/
│   │   ├── nba_api_client.py
│   │   └── basketball_reference_scraper.py
│   ├── analyzers/
│   │   ├── matchup_analyzer.py
│   │   └── fantasy_calculator.py
│   └── optimizers/
│       └── lineup_optimizer.py
├── data/
├── visualizations/
└── web_interface/



