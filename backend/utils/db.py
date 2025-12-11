from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MongoDB connection URI
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise Exception("MONGO_URI not set in .env")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Database
db = client["ai_hr_db"]

# Collections
users_collection = db["users"]      # For storing user signup/login data
jobs_collection = db["jobs"]        # For storing job posts
