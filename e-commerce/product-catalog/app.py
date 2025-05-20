from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Intentionally vulnerable database connection
def get_db():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn

# Vulnerable SQL query - SQL Injection
@app.route('/products/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '')
    # Intentionally vulnerable to SQL injection
    sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
    conn = get_db()
    cursor = conn.execute(sql)
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(products)

# Vulnerable to XSS
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db()
    cursor = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    if product:
        # Intentionally vulnerable to XSS
        return f"""
        <html>
            <body>
                <h1>{product['name']}</h1>
                <p>{product['description']}</p>
                <div>{product['details']}</div>
            </body>
        </html>
        """
    return 'Product not found', 404

# Hardcoded credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "super_secret_password_123"

@app.route('/admin', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return jsonify({"status": "success", "message": "Welcome admin!"})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    # Create database and table if not exists
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            details TEXT,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()
    
    # Run with debug mode enabled (security risk)
    app.run(debug=True, host='0.0.0.0', port=5000) 