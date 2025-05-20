from flask import Flask, request, jsonify
import logging
import os
import json
from datetime import datetime

app = Flask(__name__)

# Insufficient logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # Minimal logging format
)

# In-memory service registry
services = {}

# Using components with known vulnerabilities
# Intentionally using outdated version patterns
@app.route('/register', methods=['POST'])
def register_service():
    service_data = request.json
    
    # Insufficient input validation
    service_id = service_data.get('id')
    services[service_id] = {
        'id': service_id,
        'name': service_data.get('name'),
        'url': service_data.get('url'),
        'version': service_data.get('version', '1.0.0'),  # No version validation
        'registered_at': datetime.now().isoformat()
    }
    
    # Insufficient logging
    logging.info(f"Service registered: {service_id}")
    
    return jsonify({"status": "success"})

@app.route('/services', methods=['GET'])
def list_services():
    # No authentication or authorization
    return jsonify(list(services.values()))

@app.route('/services/<service_id>', methods=['DELETE'])
def unregister_service(service_id):
    if service_id in services:
        del services[service_id]
        # Insufficient logging - no audit trail
        return jsonify({"status": "success"})
    return jsonify({"error": "Service not found"}), 404

# Vulnerable to path traversal
@app.route('/config/<path:filename>', methods=['GET'])
def get_config(filename):
    # Intentionally vulnerable to path traversal
    try:
        with open(filename, 'r') as f:
            return jsonify({"content": f.read()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run with debug mode enabled (security risk)
    app.run(debug=True, host='0.0.0.0', port=5005) 