from flask import Flask, request, jsonify
import pickle
import json
import base64
import os

app = Flask(__name__)

# Insecure deserialization vulnerability
@app.route('/process-payment', methods=['POST'])
def process_payment():
    try:
        # Intentionally vulnerable to insecure deserialization
        payment_data = pickle.loads(base64.b64decode(request.data))
        
        # Process payment (simplified)
        return jsonify({
            "status": "success",
            "transaction_id": "12345",
            "amount": payment_data.get('amount'),
            "card_number": payment_data.get('card_number')  # Sensitive data exposure
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Sensitive data exposure
@app.route('/transactions/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    # Intentionally exposing sensitive data
    transaction = {
        "id": transaction_id,
        "amount": 100.00,
        "card_number": "4111111111111111",
        "cvv": "123",
        "expiry": "12/25",
        "customer_name": "John Doe",
        "address": "123 Main St",
        "ssn": "123-45-6789"  # Extremely sensitive data
    }
    return jsonify(transaction)

# Weak encryption
SECRET_KEY = "my_very_secret_key_123"  # Hardcoded weak key

@app.route('/encrypt-data', methods=['POST'])
def encrypt_data():
    data = request.json
    # Intentionally weak encryption
    encrypted = ''.join(chr(ord(c) ^ ord(SECRET_KEY[i % len(SECRET_KEY)])) 
                       for i, c in enumerate(json.dumps(data)))
    return jsonify({"encrypted_data": base64.b64encode(encrypted.encode()).decode()})

if __name__ == '__main__':
    # Run with debug mode enabled (security risk)
    app.run(debug=True, host='0.0.0.0', port=5001) 