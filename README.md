# nba-newsletter

NBA Daily Digest is an automated newsletter system that delivers daily game summaries for registered NBA players or teams directly to your email inbox every morning.

## Purpose

- Practice backend development with Python
- Gain hands-on experience with serverless architecture using AWS
- Learn how to design and implement backend APIs and automation workflows

## Key Features

- Register your favorite NBA players or teams
- Automatically collect game data every morning
- Send game summaries via HTML-formatted email
- Provide a REST API built with FastAPI

## Tech Stack

- Python 3.13
- FastAPI
- DynamoDB (AWS NoSQL)
- AWS Lambda + EventBridge (for scheduling)
- AWS SES or SMTP (for sending emails)
- NBA API (nba_api)
- Jinja2 (HTML templating)

## Project Structure

```
app/
├── api/            # Versioned API routes
├── core/           # Configurations and AWS integrations
├── models/         # Data models (Pydantic)
├── services/       # Business logic
├── templates/      # HTML email templates
└── main.py         # FastAPI entry point

scheduler/          # Script for scheduled Lambda execution
```

## Getting Started (Local Development)

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn app.main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)  
Use the built-in Swagger UI to test your API.

## External APIs

- [https://www.balldontlie.io](https://www.balldontlie.io)
- NBA API (nba_api)