from pymongo import MongoClient
import certifi
import sys

MONGO_URI = "mongodb+srv://buraksaglam415_db_user:jnIC2z40mFDD8rqh@cluster0.swtf7ev.mongodb.net/?appName=Cluster0"

try:
    print("Attempting to connect...")
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    client.admin.command('ping')
    print("Connection SUCCESSFUL!")
    db = client["agd_investment"]
    print(f"Database: {db.name}")
except Exception as e:
    print(f"Connection FAILED: {str(e)}")
