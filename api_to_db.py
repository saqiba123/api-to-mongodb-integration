import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Function to connect to MongoDB
def connect_to_mongodb():
    mongo_url = os.getenv("MONGO_URL")
    if not mongo_url:
        raise ValueError("MongoDB connection string is not found in environment variables.")
    
    client = MongoClient(mongo_url)
    db = client["SjunaDB"]
    collection = db["SjunaCollection"]
    return collection

# Function to get data from API and insert into MongoDB
def fetch_and_store_data():
    # Connect to MongoDB
    collection = connect_to_mongodb()
    # Define API URL and call the function
    api_url = "https://jsonplaceholder.typicode.com/users/1"
    print("Getting API response...")
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
    else:
        raise ValueError(f"Error fetching data from API: {response.text}")

    # Insert data into MongoDB
    try:
        result = collection.insert_one(data)
        print(f"Data inserted with ID: {result.inserted_id} into the database.")
    except Exception as e:
        raise ValueError(f"Error inserting data into MongoDB: {e}")

try:
    fetch_and_store_data()
except Exception as e:
    print(e)
