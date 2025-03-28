from balldontlie import BalldontlieAPI
import os
from dotenv import load_dotenv

load_dotenv()
api = BalldontlieAPI(api_key=os.getenv("BALLDONTLIE_API_KEY"))