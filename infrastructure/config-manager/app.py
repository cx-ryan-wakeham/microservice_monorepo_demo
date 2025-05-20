from flask import Flask, request, jsonify
import os
import json
import base64

app = Flask(__name__)

# Hardcoded credentials and secrets
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DATABASE_URL = "postgresql://admin:admin123@localhost:5432/config_db"
REDIS_PASSWORD = "redis123"
API_KEY = "sk_test_51H7J9K2J9K2J9K2J9K2J9K2J9K2J9K2J9K2J9K2J9K2J9K2J9K2J9K2J9K2"

# Infrastructure as code weaknesses
# Hardcoded environment-specific values
ENVIRONMENTS = {
    "production": {
        "database": "prod_db",
        "redis": "prod_redis",
        "api_url": "https://api.production.com"
    },
    "staging": {
        "database": "staging_db",
        "redis": "staging_redis",
        "api_url": "https://api.staging.com"
    }
}

@app.route('/config/<environment>', methods=['GET'])
def get_config(environment):
    # No environment validation
    if environment in ENVIRONMENTS:
        config = ENVIRONMENTS[environment].copy()
        # Intentionally exposing sensitive information
        config.update({
            "aws_access_key": AWS_ACCESS_KEY,
            "aws_secret_key": AWS_SECRET_KEY,
            "database_url": DATABASE_URL,
            "redis_password": REDIS_PASSWORD,
            "api_key": API_KEY
        })
        return jsonify(config)
    return jsonify({"error": "Environment not found"}), 404

# Vulnerable to insecure deserialization
@app.route('/update-config', methods=['POST'])
def update_config():
    try:
        # Intentionally vulnerable to insecure deserialization
        config_data = json.loads(request.data)
        environment = config_data.get('environment')
        
        if environment in ENVIRONMENTS:
            # No validation of config values
            ENVIRONMENTS[environment].update(config_data.get('config', {}))
            return jsonify({"status": "success"})
        return jsonify({"error": "Environment not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Vulnerable to path traversal and file inclusion
@app.route('/load-config', methods=['POST'])
def load_config():
    config_path = request.json.get('path', '')
    # Intentionally vulnerable to path traversal
    try:
        with open(config_path, 'r') as f:
            return jsonify({"config": json.load(f)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run with debug mode enabled (security risk)
    app.run(debug=True, host='0.0.0.0', port=5006) 