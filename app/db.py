import pymongo
from app.config import Config

# Kết nối MongoDB
client = pymongo.MongoClient(Config.MONGO_URI)
db = client["api_db"]
api_keys_collection = db["api_keys"]
webhook_events_collection = db["webhook_events"]
logs_collection = db["logs"]
