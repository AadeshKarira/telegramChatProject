import os
from dotenv import load_dotenv
from pymongo import MongoClient
from mongoengine import connect

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME")

# Connect to MongoDB using pymongo
client = MongoClient(MONGODB_URL)
db = client[DB_NAME]

# Set the pymongo connection as the default connection for mongoengine
connect(db=DB_NAME, host=MONGODB_URL)

# Check if the connection was successful
try:
    client.server_info()
    print("Connected")
except Exception as e:
    print("Connection error:", e)