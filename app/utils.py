import hashlib
import uuid
from datetime import datetime
from app.db import webhook_events_collection

def create_api_key():
    return str(uuid.uuid4())

def hash_api_key(api_key):
    return hashlib.sha256(api_key.encode()).hexdigest()

def validate_event(event):
    if event != "plan_update":
        return False, "Invalid event type"
    return True, None

def store_payload(payload):
    webhook_event = {
        "event": "plan_update",
        "payload": payload,
        "timestamp": datetime.now()
    }
    webhook_events_collection.insert_one(webhook_event)

