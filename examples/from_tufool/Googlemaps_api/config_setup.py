from dotenv import load_dotenv
import os

load_dotenv()
print("Loaded API key:", os.getenv("GOOGLE_MAPS_API_KEY"))


