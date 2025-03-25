from flask import Blueprint, request, jsonify
from datetime import datetime
from app.db import api_keys_collection
from app.logs import log_event_status
from app.utils import create_api_key, hash_api_key

api_key_routes = Blueprint('api_key_routes', __name__)

VALID_ROLES = ['developer', 'integrator', 'compliance']
VALID_ENVS = ['test', 'production', 'remote-production']



@api_key_routes.route('/generate', methods=['POST'])
def generate_api_key():
    data = request.get_json()
    role = data.get("role")
    environment = data.get("environment")
    
    if role not in VALID_ROLES or environment not in VALID_ENVS:
        return jsonify({"message": "Invalid role or environment"}), 400

    # Tạo API key
    api_key = create_api_key()
    api_key_hash = hash_api_key(api_key)
    
    new_api_key = {
        "_id": str(create_api_key()),
        "api_key_hash": api_key_hash,
        "role": role,
        "environment": environment,
        "created_at": datetime.now(),
        "last_used_at": None,
        "is_active": True
    }
    
    api_keys_collection.insert_one(new_api_key)

    # Ghi log tạo API key
    log_event_status("success", f"API key generated for {role} in {environment}", api_key, log_type="api")
    
    return jsonify({
        "api_key": api_key,
        "id": new_api_key["_id"],
        "created_at": new_api_key["created_at"],
        "role": role
    })
