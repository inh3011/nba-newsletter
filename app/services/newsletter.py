from app.core.templates import env
from app.services.games import get_games_by_date
from datetime import datetime
import pytz


def get_today_us_date():
    """
    Returns today's date in US Eastern Time (format: YYYY-MM-DD).
    """
    utc_now = datetime.utcnow()
    eastern = pytz.timezone("US/Eastern")
    est_now = utc_now.replace(tzinfo=pytz.utc).astimezone(eastern)
    return est_now.date().isoformat()


def render_newsletter_html():
    """
    Renders the newsletter HTML using today's NBA games.
    """
    template = env.get_template("newsletter.html")
    games = get_games_by_date()
    date = get_today_us_date()

    html = template.render(games=games, date=date)
    return html