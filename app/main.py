from flask import Flask
from app.config import Config
from app.auth import rbac_middleware, auth_routes
from app.apikeys import api_key_routes
from app.webhook import webhook_routes
from app.logs import log_routes

app = Flask(__name__)
app.config.from_object(Config)

app.before_request(rbac_middleware)  # Middleware kiểm tra API Key

# Đăng ký các Blueprint
app.register_blueprint(api_key_routes, url_prefix='/apikeys')
app.register_blueprint(webhook_routes, url_prefix='/webhook')
app.register_blueprint(log_routes, url_prefix='/logs')
app.register_blueprint(auth_routes)


if __name__ == '__main__':
    app.run(debug=True)
