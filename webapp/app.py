"""
Modern RuneScape Cache API Test Web Application
"""

from flask import Flask, render_template, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

# API endpoint configuration
API_BASE_URL = "http://cache-api:5000"  # Updated for Docker networking

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/api/initialize', methods=['POST'])
def api_initialize():
    """Proxy endpoint to initialize the cache"""
    try:
        response = requests.post(f"{API_BASE_URL}/initialize", json=request.json, timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to cache API: {str(e)}"}), 500

@app.route('/api/data/<int:index_id>/<int:archive_id>/<int:file_id>', methods=['GET'])
def api_get_file_data(index_id, archive_id, file_id):
    """Proxy endpoint to get file data"""
    try:
        response = requests.get(f"{API_BASE_URL}/data/{index_id}/{archive_id}/{file_id}", timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to cache API: {str(e)}"}), 500

@app.route('/api/data/<int:index_id>/<int:archive_id>', methods=['GET'])
def api_get_archive_data(index_id, archive_id):
    """Proxy endpoint to get archive data"""
    try:
        response = requests.get(f"{API_BASE_URL}/data/{index_id}/{archive_id}", timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to cache API: {str(e)}"}), 500

@app.route('/api/put/<int:index_id>/<int:archive_id>/<int:file_id>', methods=['POST'])
def api_put_file_data(index_id, archive_id, file_id):
    """Proxy endpoint to put file data"""
    try:
        response = requests.post(f"{API_BASE_URL}/put/{index_id}/{archive_id}/{file_id}", json=request.json, timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to cache API: {str(e)}"}), 500

@app.route('/api/put/<int:index_id>/<int:archive_id>', methods=['POST'])
def api_put_archive_data(index_id, archive_id):
    """Proxy endpoint to put archive data"""
    try:
        response = requests.post(f"{API_BASE_URL}/put/{index_id}/{archive_id}", json=request.json, timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to cache API: {str(e)}"}), 500

@app.route('/api/remove/<int:index_id>/<int:archive_id>/<int:file_id>', methods=['DELETE'])
def api_remove_file(index_id, archive_id, file_id):
    """Proxy endpoint to remove a file"""
    try:
        response = requests.delete(f"{API_BASE_URL}/remove/{index_id}/{archive_id}/{file_id}", timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to cache API: {str(e)}"}), 500

@app.route('/api/remove/<int:index_id>/<int:archive_id>', methods=['DELETE'])
def api_remove_archive(index_id, archive_id):
    """Proxy endpoint to remove an archive"""
    try:
        response = requests.delete(f"{API_BASE_URL}/remove/{index_id}/{archive_id}", timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to cache API: {str(e)}"}), 500

@app.route('/api/update/<int:index_id>', methods=['POST'])
def api_update_index(index_id):
    """Proxy endpoint to update an index"""
    try:
        response = requests.post(f"{API_BASE_URL}/update/{index_id}", timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to cache API: {str(e)}"}), 500

@app.route('/api/add_archive/<int:index_id>', methods=['POST'])
def api_add_archive(index_id):
    """Proxy endpoint to add an archive"""
    try:
        response = requests.post(f"{API_BASE_URL}/add_archive/{index_id}", json=request.json, timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to cache API: {str(e)}"}), 500

@app.route('/api/rebuild', methods=['POST'])
def api_rebuild_cache():
    """Proxy endpoint to rebuild the cache"""
    try:
        response = requests.post(f"{API_BASE_URL}/rebuild", json=request.json, timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to cache API: {str(e)}"}), 500

@app.route('/api/health', methods=['GET'])
def api_health_check():
    """Proxy endpoint to check API health"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to cache API: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
