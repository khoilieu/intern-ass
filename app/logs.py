# app/logs.py
from flask import Blueprint, request, jsonify
from app.db import logs_collection
from datetime import datetime

# Blueprint cho logs
log_routes = Blueprint('log_routes', __name__)

def log_event_status(status, message, api_key, log_type="api"):
    """
    Ghi lại sự kiện log vào MongoDB
    """
    log_entry = {
        "status": status,  # 'success', 'failure', v.v.
        "message": message,  # Mô tả chi tiết về sự kiện
        "timestamp": datetime.now(),  # Thời gian ghi log
        "api_key_used": api_key,  # API key đã sử dụng
        "type": log_type  # 'api' cho logs API, 'webhook' cho logs webhook
    }
    
    # Insert log vào MongoDB
    logs_collection.insert_one(log_entry)

@log_routes.route('/', methods=['GET'])
def get_all_logs():
    """
    Lấy tất cả các logs
    """
    logs = list(logs_collection.find())  # Lấy tất cả logs
    if not logs:
        return jsonify({"message": "No logs found"}), 404
    
    # Format logs trước khi trả về (nếu cần)
    formatted_logs = [{"status": log["status"], "message": log["message"], "timestamp": log["timestamp"], "api_key_used": log["api_key_used"], "type": log["type"]} for log in logs]
    
    return jsonify(formatted_logs), 200

@log_routes.route('/api', methods=['GET'])
def get_api_logs():
    """
    Truy vấn logs API theo status và role
    """
    status = request.args.get('status', None)
    role = request.args.get('role', None)
    
    query = {}
    if status:
        query['status'] = status
    if role:
        query['message'] = {"$regex": role}  # Giả sử role sẽ được chứa trong message (hoặc có thể cải tiến thêm)
    
    logs = list(logs_collection.find(query))
    if not logs:
        return jsonify({"message": "No logs found matching criteria"}), 404
    
    formatted_logs = [{"status": log["status"], "message": log["message"], "timestamp": log["timestamp"], "api_key_used": log["api_key_used"], "type": log["type"]} for log in logs]
    
    return jsonify(formatted_logs), 200

@log_routes.route('/webhooks', methods=['GET'])
def get_webhook_logs():
    """
    Truy vấn logs webhook theo ngày (since)
    """
    since = request.args.get('since', None)
    
    query = {"type": "webhook"}
    if since:
        try:
            since_date = datetime.strptime(since, "%Y-%m-%d")
            query['timestamp'] = {"$gte": since_date}  # Lọc logs từ ngày `since`
        except ValueError:
            return jsonify({"message": "Invalid date format, please use YYYY-MM-DD"}), 400

    logs = list(logs_collection.find(query))
    if not logs:
        return jsonify({"message": "No logs found matching criteria"}), 404
    
    formatted_logs = [{"status": log["status"], "message": log["message"], "timestamp": log["timestamp"], "api_key_used": log["api_key_used"], "type": log["type"]} for log in logs]
    
    return jsonify(formatted_logs), 200
