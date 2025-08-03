from flask import Flask, request, jsonify
import os
import sys
import base64

# Import our Python-JPype bridge to the Kotlin library
from cache_api import CacheLibraryAPI

app = Flask(__name__)

# Initialize the cache API with JPype-Kotlin integration
cache_api = CacheLibraryAPI()

@app.route('/initialize', methods=['POST'])
def initialize_cache():
    """Initialize the cache with a given path"""
    data = request.json
    path = data.get('path')
    if not path:
        return jsonify({"status": "error", "message": "Path is required"}), 400
    
    # Start JVM with the cache library JAR
    try:
        cache_api.start_jvm()
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to start JVM: {str(e)}"}), 500
    
    if not os.path.exists(path):
        return jsonify({"status": "error", "message": "Path does not exist"}), 400
    
    result = cache_api.initialize_cache(path)
    return jsonify(result)

@app.route('/data/<int:index_id>/<int:archive_id>/<int:file_id>', methods=['GET'])
def get_file_data(index_id, archive_id, file_id):
    """Get file data from the cache"""
    xtea = request.args.get('xtea')
    xtea_array = None
    if xtea:
        try:
            # Parse xtea as comma-separated integers
            xtea_array = [int(x) for x in xtea.split(',')]
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid XTEA format, must be comma-separated integers"}), 400
    
    result = cache_api.get_file_data(index_id, archive_id, file_id, xtea_array)
    return jsonify(result)

@app.route('/data/<int:index_id>/<int:archive_id>', methods=['GET'])
def get_archive_data(index_id, archive_id):
    """Get archive data from the cache"""
    xtea = request.args.get('xtea')
    xtea_array = None
    if xtea:
        try:
            # Parse xtea as comma-separated integers
            xtea_array = [int(x) for x in xtea.split(',')]
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid XTEA format, must be comma-separated integers"}), 400
    
    result = cache_api.get_file_data(index_id, archive_id, 0, xtea_array)
    return jsonify(result)

@app.route('/data/<int:index_id>/<string:archive_name>', methods=['GET'])
def get_archive_data_by_name(index_id, archive_name):
    """Get archive data by name from the cache"""
    xtea = request.args.get('xtea')
    xtea_array = None
    if xtea:
        try:
            # Parse xtea as comma-separated integers
            xtea_array = [int(x) for x in xtea.split(',')]
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid XTEA format, must be comma-separated integers"}), 400
    
    # For named archives, we need to find the archive ID first
    # This is a simplified implementation - in a real implementation, 
    # we would need to search for the archive by name
    result = {
        "status": "error", 
        "message": "Getting data by archive name not yet implemented"
    }
    return jsonify(result), 501

@app.route('/put/<int:index_id>/<int:archive_id>/<int:file_id>', methods=['POST'])
def put_file_data(index_id, archive_id, file_id):
    """Put file data into the cache"""
    data = request.json.get('data')
    xtea = request.json.get('xtea')
    
    if not data:
        return jsonify({"status": "error", "message": "Data is required"}), 400
    
    xtea_array = None
    if xtea:
        try:
            # Parse xtea as comma-separated integers
            xtea_array = [int(x) for x in xtea.split(',')]
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid XTEA format, must be comma-separated integers"}), 400
    
    result = cache_api.put_file_data(index_id, archive_id, file_id, data, xtea_array)
    return jsonify(result)

@app.route('/put/<int:index_id>/<int:archive_id>', methods=['POST'])
def put_archive_data(index_id, archive_id):
    """Put archive data into the cache"""
    data = request.json.get('data')
    xtea = request.json.get('xtea')
    
    if not data:
        return jsonify({"status": "error", "message": "Data is required"}), 400
    
    xtea_array = None
    if xtea:
        try:
            # Parse xtea as comma-separated integers
            xtea_array = [int(x) for x in xtea.split(',')]
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid XTEA format, must be comma-separated integers"}), 400
    
    result = cache_api.put_file_data(index_id, archive_id, 0, data, xtea_array)
    return jsonify(result)

@app.route('/put/<int:index_id>/<string:archive_name>', methods=['POST'])
def put_archive_data_by_name(index_id, archive_name):
    """Put archive data by name into the cache"""
    data = request.json.get('data')
    xtea = request.json.get('xtea')
    
    if not data:
        return jsonify({"status": "error", "message": "Data is required"}), 400
    
    xtea_array = None
    if xtea:
        try:
            # Parse xtea as comma-separated integers
            xtea_array = [int(x) for x in xtea.split(',')]
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid XTEA format, must be comma-separated integers"}), 400
    
    # For named archives, we need to find or create the archive ID first
    # This is a simplified implementation - in a real implementation, 
    # we would need to search for or create the archive by name
    result = {
        "status": "error", 
        "message": "Putting data by archive name not yet implemented"
    }
    return jsonify(result), 501

@app.route('/remove/<int:index_id>/<int:archive_id>/<int:file_id>', methods=['DELETE'])
def remove_file(index_id, archive_id, file_id):
    """Remove a file from the cache"""
    result = cache_api.remove_file(index_id, archive_id, file_id)
    return jsonify(result)

@app.route('/remove/<int:index_id>/<int:archive_id>', methods=['DELETE'])
def remove_archive(index_id, archive_id):
    """Remove an archive from the cache"""
    result = cache_api.remove_archive(index_id, archive_id)
    return jsonify(result)

@app.route('/remove/<int:index_id>/<string:archive_name>', methods=['DELETE'])
def remove_archive_by_name(index_id, archive_name):
    """Remove an archive by name from the cache"""
    # For named archives, we need to find the archive ID first
    # This is a simplified implementation - in a real implementation, 
    # we would need to search for the archive by name
    result = {
        "status": "error", 
        "message": "Removing archives by name not yet implemented"
    }
    return jsonify(result), 501

@app.route('/update/<int:index_id>', methods=['POST'])
def update_index(index_id):
    """Update/write changes to an index"""
    result = cache_api.update_index(index_id)
    return jsonify(result)

@app.route('/add_archive/<int:index_id>', methods=['POST'])
def add_archive(index_id):
    """Add a new archive to an index"""
    archive_name = request.json.get('name')
    result = cache_api.add_archive(index_id, archive_name)
    return jsonify(result)

@app.route('/rebuild', methods=['POST'])
def rebuild_cache():
    """Rebuild/defragment the cache"""
    data = request.json
    output_path = data.get('output_path')
    if not output_path:
        return jsonify({"status": "error", "message": "Output path is required"}), 400
    
    result = cache_api.rebuild_cache(output_path)
    return jsonify(result)

@app.route('/', methods=['GET'])
def api_info():
    """Root endpoint providing API information"""
    return jsonify({
        "message": "RuneScape Cache Library API",
        "endpoints": {
            "health": "/health (GET)",
            "initialize": "/initialize (POST)",
            "get_file_data": "/data/<index_id>/<archive_id>/<file_id> (GET)",
            "get_archive_data": "/data/<index_id>/<archive_id> (GET)",
            "put_file_data": "/put/<index_id>/<archive_id>/<file_id> (POST)",
            "put_archive_data": "/put/<index_id>/<archive_id> (POST)",
            "remove_file": "/remove/<index_id>/<archive_id>/<file_id> (DELETE)",
            "remove_archive": "/remove/<index_id>/<archive_id> (DELETE)",
            "update_index": "/update/<index_id> (POST)",
            "add_archive": "/add_archive/<index_id> (POST)",
            "rebuild_cache": "/rebuild (POST)",
            "shutdown": "/shutdown (POST)"
        },
        "description": "API for interacting with RuneScape cache files"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Cache API is running"})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the API and close the cache library"""
    result = cache_api.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
