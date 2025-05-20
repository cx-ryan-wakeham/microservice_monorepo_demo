from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import os
import shutil

app = Flask(__name__)

# Vulnerable to XXE
@app.route('/parse-xml', methods=['POST'])
def parse_xml():
    try:
        # Intentionally vulnerable to XXE
        xml_data = request.data
        root = ET.fromstring(xml_data)
        
        # Process XML data
        result = {}
        for child in root:
            result[child.tag] = child.text
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Insecure file upload
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
        
    # Intentionally vulnerable file upload
    # No file type validation
    # No file size limits
    # No sanitization of filename
    filename = file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    
    return jsonify({
        "message": "File uploaded successfully",
        "filename": filename,
        "path": os.path.join(UPLOAD_FOLDER, filename)
    })

# Command injection vulnerability
@app.route('/execute', methods=['POST'])
def execute_command():
    command = request.json.get('command', '')
    # Intentionally vulnerable to command injection
    result = os.popen(command).read()
    return jsonify({"result": result})

if __name__ == '__main__':
    # Run with debug mode enabled (security risk)
    app.run(debug=True, host='0.0.0.0', port=5003) 