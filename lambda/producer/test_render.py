import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Jinja2 Template Environment setup
template_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("newsletter_template.html")

# Data for test
date_str = datetime.now().strftime("%Y-%m-%d")
sample_games = [
    {
        "homeTeam": {
            "teamCity": "Los Angeles",
            "teamName": "Lakers",
            "teamTricode": "LAL",
            "score": 120,
            "periods": [
                {"period": 1, "score": 30},
                {"period": 2, "score": 25},
                {"period": 3, "score": 35},
                {"period": 4, "score": 30}
            ]
        },
        "awayTeam": {
            "teamCity": "Golden State",
            "teamName": "Warriors",
            "teamTricode": "GSW",
            "score": 115,
            "periods": [
                {"period": 1, "score": 28},
                {"period": 2, "score": 27},
                {"period": 3, "score": 30},
                {"period": 4, "score": 30}
            ]
        },
        "gameStatusText": "Final",
        "gameLeaders": {
            "homeLeaders": {
                "name": "LeBron James",
                "points": 32,
                "rebounds": 8,
                "assists": 10
            },
            "awayLeaders": {
                "name": "Stephen Curry",
                "points": 34,
                "rebounds": 5,
                "assists": 7
            }
        }
    }
]

# Render the template
html = template.render(date=date_str, games=sample_games)

# Output the rendered HTML to a file
with open("test_output.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Rendered HTML saved as test_output.html")