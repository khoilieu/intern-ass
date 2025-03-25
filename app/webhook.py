from flask import Blueprint, request, jsonify
from app.utils import validate_event, store_payload
from app.logs import log_event_status

webhook_routes = Blueprint('webhook_routes', __name__)

@webhook_routes.route('/trigger', methods=['POST'])
def webhook_trigger():
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return jsonify({"message": "API key missing"}), 400

    data = request.get_json()

    if 'event' not in data or 'payload' not in data:
        return jsonify({"message": "Invalid payload, missing event or payload fields"}), 400

    event = data['event']
    payload = data['payload']

    # Step 1: Validate Event
    is_valid_event, error_message = validate_event(event)
    if not is_valid_event:
        log_event_status("failure", error_message, api_key)
        return jsonify({"message": error_message}), 400

    # Step 2: Store Payload to MongoDB
    try:
        store_payload(payload)
    except Exception as e:
        log_event_status("failure", f"Failed to store payload: {str(e)}", api_key)
        return jsonify({"message": "Failed to store payload"}), 500

    # Step 3: Log Success
    log_event_status("success", "Webhook event processed successfully", api_key)
    
    return jsonify({"message": "Webhook event processed successfully"}), 200
