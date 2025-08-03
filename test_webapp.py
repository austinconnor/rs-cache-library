from flask import Flask, render_template, request, jsonify
import requests
import base64
import os

test_app = Flask(__name__)

# API endpoint configuration
API_BASE_URL = "http://localhost:5000"

@test_app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>RuneScape Cache API Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, textarea { width: 100%; padding: 8px; box-sizing: border-box; }
            button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
            .result { margin-top: 20px; padding: 15px; background-color: #f0f0f0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>RuneScape Cache API Test Interface</h1>
            
            <div class="form-group">
                <label for="cachePath">Cache Path:</label>
                <input type="text" id="cachePath" placeholder="Enter path to cache directory" value="./cache">
                <button onclick="initializeCache()">Initialize Cache</button>
            </div>
            
            <div class="form-group">
                <h2>Get File Data</h2>
                <label for="getIndex">Index ID:</label>
                <input type="number" id="getIndex" value="19">
                
                <label for="getArchive">Archive ID:</label>
                <input type="number" id="getArchive" value="116">
                
                <label for="getFile">File ID:</label>
                <input type="number" id="getFile" value="94">
                
                <button onclick="getFileData()">Get File Data</button>
            </div>
            
            <div class="form-group">
                <h2>Put File Data</h2>
                <label for="putIndex">Index ID:</label>
                <input type="number" id="putIndex" value="19">
                
                <label for="putArchive">Archive ID:</label>
                <input type="number" id="putArchive" value="116">
                
                <label for="putFile">File ID:</label>
                <input type="number" id="putFile" value="94">
                
                <label for="putData">Data (text):</label>
                <textarea id="putData" rows="4" placeholder="Enter data to write to cache">Sample data for testing</textarea>
                
                <button onclick="putFileData()">Put File Data</button>
            </div>
            
            <div class="form-group">
                <h2>Remove File</h2>
                <label for="removeIndex">Index ID:</label>
                <input type="number" id="removeIndex" value="19">
                
                <label for="removeArchive">Archive ID:</label>
                <input type="number" id="removeArchive" value="116">
                
                <label for="removeFile">File ID:</label>
                <input type="number" id="removeFile" value="94">
                
                <button onclick="removeFile()">Remove File</button>
            </div>
            
            <div id="result" class="result" style="display: none;"></div>
        </div>
        
        <script>
            function showResult(message, isError = false) {
                const resultDiv = document.getElementById("result");
                resultDiv.innerHTML = "<h3>Result:</h3><p" + (isError ? " style=\"color: red;\"" : "") + ">" + message + "</p>";
                resultDiv.style.display = "block";
            }
            
            function initializeCache() {
                const path = document.getElementById("cachePath").value;
                fetch("/api/initialize", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({path: path})
                })
                .then(response => response.json())
                .then(data => {
                    showResult(JSON.stringify(data));
                })
                .catch(error => {
                    showResult("Error: " + error, true);
                });
            }
            
            function getFileData() {
                const index = document.getElementById("getIndex").value;
                const archive = document.getElementById("getArchive").value;
                const file = document.getElementById("getFile").value;
                
                fetch(`/api/data/${index}/${archive}/${file}`)
                .then(response => response.json())
                .then(data => {
                    showResult(JSON.stringify(data));
                })
                .catch(error => {
                    showResult("Error: " + error, true);
                });
            }
            
            function putFileData() {
                const index = document.getElementById("putIndex").value;
                const archive = document.getElementById("putArchive").value;
                const file = document.getElementById("putFile").value;
                const data = document.getElementById("putData").value;
                
                fetch(`/api/put/${index}/${archive}/${file}`, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({data: data})
                })
                .then(response => response.json())
                .then(data => {
                    showResult(JSON.stringify(data));
                })
                .catch(error => {
                    showResult("Error: " + error, true);
                });
            }
            
            function removeFile() {
                const index = document.getElementById("removeIndex").value;
                const archive = document.getElementById("removeArchive").value;
                const file = document.getElementById("removeFile").value;
                
                fetch(`/api/remove/${index}/${archive}/${file}`, {
                    method: "DELETE"
                })
                .then(response => response.json())
                .then(data => {
                    showResult(JSON.stringify(data));
                })
                .catch(error => {
                    showResult("Error: " + error, true);
                });
            }
        </script>
    </body>
    </html>
    '''

@test_app.route('/api/initialize', methods=['POST'])
def api_initialize():
    """Proxy endpoint to initialize the cache"""
    try:
        response = requests.post(f"{API_BASE_URL}/initialize", json=request.json)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@test_app.route('/api/data/<int:index_id>/<int:archive_id>/<int:file_id>', methods=['GET'])
def api_get_file_data(index_id, archive_id, file_id):
    """Proxy endpoint to get file data"""
    try:
        response = requests.get(f"{API_BASE_URL}/data/{index_id}/{archive_id}/{file_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@test_app.route('/api/put/<int:index_id>/<int:archive_id>/<int:file_id>', methods=['POST'])
def api_put_file_data(index_id, archive_id, file_id):
    """Proxy endpoint to put file data"""
    try:
        response = requests.post(f"{API_BASE_URL}/put/{index_id}/{archive_id}/{file_id}", json=request.json)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@test_app.route('/api/remove/<int:index_id>/<int:archive_id>/<int:file_id>', methods=['DELETE'])
def api_remove_file(index_id, archive_id, file_id):
    """Proxy endpoint to remove a file"""
    try:
        response = requests.delete(f"{API_BASE_URL}/remove/{index_id}/{archive_id}/{file_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    test_app.run(host='0.0.0.0', port=5001, debug=True)
