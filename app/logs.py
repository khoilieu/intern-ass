# app/logs.py
from app.db import logs_collection
from datetime import datetime

def log_event_status(status, message, api_key):
    """
    Ghi lại sự kiện log vào MongoDB
    """
    log_entry = {
        "status": status,  # 'success', 'failure', v.v.
        "message": message,  # Mô tả chi tiết về sự kiện
        "timestamp": datetime.now(),  # Thời gian ghi log
        "api_key_used": api_key  # API key đã sử dụng
    }
    
    # Insert log vào MongoDB
    logs_collection.insert_one(log_entry)
