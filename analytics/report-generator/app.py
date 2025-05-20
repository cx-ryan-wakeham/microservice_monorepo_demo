from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

# In-memory report store
reports = {
    "1": {"id": "1", "title": "Q1 Sales", "content": "Confidential sales data", "owner": "admin"},
    "2": {"id": "2", "title": "Q2 Sales", "content": "More confidential data", "owner": "admin"},
    "3": {"id": "3", "title": "User Report", "content": "User statistics", "owner": "user1"}
}

# Broken access control
@app.route('/reports/<report_id>', methods=['GET'])
def get_report(report_id):
    # No access control check
    if report_id in reports:
        return jsonify(reports[report_id])
    return jsonify({"error": "Report not found"}), 404

# Security misconfiguration - exposed admin endpoint
@app.route('/admin/reports', methods=['GET'])
def list_all_reports():
    # No authentication required
    return jsonify(list(reports.values()))

# Security misconfiguration - exposed debug endpoint
@app.route('/debug', methods=['GET'])
def debug_info():
    # Intentionally exposing sensitive information
    return jsonify({
        "environment": os.environ,
        "server_info": {
            "hostname": os.uname().nodename,
            "platform": os.uname().sysname,
            "version": os.uname().version
        },
        "database_credentials": {
            "host": "localhost",
            "user": "admin",
            "password": "admin123",
            "database": "reports_db"
        }
    })

# Security misconfiguration - CORS misconfiguration
@app.after_request
def after_request(response):
    # Intentionally permissive CORS
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

if __name__ == '__main__':
    # Run with debug mode enabled (security risk)
    app.run(debug=True, host='0.0.0.0', port=5004) 