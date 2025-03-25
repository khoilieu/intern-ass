# API Key Management Service

## 1. Installation

### 1.1 Clone the Project:
```bash
git clone https://github.com/khoilieu/intern-ass.git
cd intern-ass
```

### 1.2 Install Required Libraries:
```bash
# On Linux/Mac
source venv/bin/activate

# On Windows
.\venv\Scripts\activate
```

### 1.3 Install and Run MongoDB (Using Docker):
If you don't have MongoDB, use Docker to start the MongoDB container:

- Ensure Docker is installed and running on your machine.
- In the directory containing the `docker-compose.yml` file, run the command:
  ```bash
  docker-compose up
  ```
  This will start MongoDB and connect it to the Flask application.

### 1.4 Run the Flask Application:
After MongoDB is running, you can start the application:

```bash
# Using Docker
docker-compose up

# Or run directly
python app/main.py
```

Flask will run on port `5000` (http://127.0.0.1:5000/).

## 2. APIs to Test with Postman

### 2.1 Generate API Key
- **URL:** `http://127.0.0.1:5000/apikeys/generate`
- **Method:** `POST`
- **Body (JSON):**
  ```json
  {
    "role": "developer",
    "environment": "production"
  }
  ```
- **Verification:** After creating the API key, try sending a POST request to `/webhook/trigger` with the `x-api-key` header using the newly generated API key.

### 2.2 Check Compliance Role Cannot POST Webhook
- **URL:** `http://127.0.0.1:5000/webhook/trigger`
- **Method:** `POST`
- **Body (JSON):**
  ```json
  {
    "event": "plan_update",
    "payload": {
      "plan_id": "ABC123",
      "status": "active"
    }
  }
  ```
- **Header:** `x-api-key` is the API key of the `compliance` role
- **Verification:** You will receive a 403 Forbidden message if using an API key with the `compliance` role to POST a webhook.

### 2.3 Check Logs Stored with Accurate Metadata
- **URL:** `http://127.0.0.1:5000/logs` or `http://127.0.0.1:5000/logs/api` or `http://127.0.0.1:5000/logs/webhooks` or `http://127.0.0.1:5000/logs/api?status=success&role=developer`
- **Method:** `GET`
- **Verification:** View logs stored in MongoDB with accurate metadata (status, timestamp, api_key_used) and accessible through this endpoint.
