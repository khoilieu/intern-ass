from flask import request, jsonify, Blueprint
from app.db import api_keys_collection
from app.config import Config
from app.utils import hash_api_key

ROLE_ACCESS = {
    'developer': ['/test', '/production'],
    'integrator': ['/webhook', '/logs'],
    'compliance': ['/logs'],
}

auth_routes = Blueprint('auth_routes', __name__)

def check_role_access(api_key, requested_endpoint):
    # Hash API key người dùng gửi vào
    api_key_hash = hash_api_key(api_key)

    # Tìm API key đã hash trong DB
    api_key_data = api_keys_collection.find_one({"api_key_hash": api_key_hash})

    if not api_key_data:
        return None, "API key not found or invalid"

    user_role = api_key_data['role']
    allowed_endpoints = ROLE_ACCESS.get(user_role, [])
    
    for allowed in allowed_endpoints:
        if requested_endpoint.startswith(allowed):
            return user_role, None
    
    return None, f"User role '{user_role}' does not have access to the endpoint '{requested_endpoint}'"

def rbac_middleware():
    requested_endpoint = request.path
    if requested_endpoint == '/apikeys/generate':
        return None  # Bỏ qua kiểm tra với API key trong trường hợp tạo API key

    api_key = request.headers.get('x-api-key')
    if not api_key:
        return jsonify({"message": "API key missing"}), 400

    user_role, error = check_role_access(api_key, requested_endpoint)
    if error:
        return jsonify({"message": error}), 403

    request.user_role = user_role
    return None


@auth_routes.route('/test', methods=['GET'])
def test():
    user_role = request.user_role

    if user_role == 'developer':
        return jsonify({"message": "Access granted for developer"}), 200
    else:
        return jsonify({"message": "Unauthorized access"}), 403

@auth_routes.route('/production', methods=['GET'])
def production():
    user_role = request.user_role

    if user_role == 'developer':
        return jsonify({"message": "Access granted for developer in production"}), 200
    else:
        return jsonify({"message": "Unauthorized access"}), 403

@auth_routes.route('/webhook', methods=['GET'])
def webhook():
    user_role = request.user_role

    if user_role == 'integrator':
        return jsonify({"message": "Access granted for integrator"}), 200
    else:
        return jsonify({"message": "Unauthorized access"}), 403

@auth_routes.route('/logs', methods=['GET'])
def logs():
    user_role = request.user_role

    if user_role == 'integrator' or user_role == 'compliance':
        return jsonify({"message": "Access granted for logs"}), 200
    else:
        return jsonify({"message": "Unauthorized access"}), 403
