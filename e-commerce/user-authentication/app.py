from flask import Flask, request, jsonify, session
import jwt
import time
import os

app = Flask(__name__)
app.secret_key = "very_secret_key_123"  # Weak secret key

# In-memory user store (vulnerable to data exposure)
users = {
    "admin": "admin123",  # Plain text password
    "user1": "password123",
    "user2": "qwerty123"
}

# Weak JWT secret
JWT_SECRET = "my_jwt_secret_key_123"

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Weak password comparison
    if username in users and users[username] == password:
        # Create JWT with weak algorithm and no expiration
        token = jwt.encode(
            {"user": username, "role": "admin" if username == "admin" else "user"},
            JWT_SECRET,
            algorithm="HS256"  # Using weak algorithm
        )
        return jsonify({"token": token})
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/profile', methods=['GET'])
def get_profile():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    try:
        # No token validation
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        username = payload['user']
        
        # Return sensitive user data without proper authorization
        return jsonify({
            "username": username,
            "email": f"{username}@example.com",
            "ssn": "123-45-6789",
            "credit_card": "4111111111111111",
            "address": "123 Main St"
        })
    except:
        return jsonify({"error": "Invalid token"}), 401

@app.route('/change-password', methods=['POST'])
def change_password():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    new_password = request.json.get('new_password')
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        username = payload['user']
        
        # No password complexity requirements
        users[username] = new_password
        return jsonify({"message": "Password changed successfully"})
    except:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == '__main__':
    # Run with debug mode enabled (security risk)
    app.run(debug=True, host='0.0.0.0', port=5002) 