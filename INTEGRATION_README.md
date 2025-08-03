# RuneScape Cache Library - Dockerized API Integration

This project provides a Dockerized API for the RuneScape Cache Library, allowing you to interact with RuneScape cache files through a RESTful interface.

## Project Structure

- `src/` - Original Kotlin source code for the cache library
- `api.py` - Flask-based REST API that interfaces with the Kotlin library via JPype
- `cache_api.py` - Python wrapper that uses JPype to call the Kotlin library
- `Dockerfile` - Multi-stage Dockerfile that builds the Kotlin JAR and sets up the Python environment
- `docker-compose.yml` - Docker Compose configuration for running the API and test webapp
- `requirements.txt` - Python dependencies
- `build-jar.gradle.kts` - Gradle build file for packaging the Kotlin library as a JAR
- `test_webapp.py` - Simple web interface for testing the API
- `test_integration.py` - Script to test the API integration

## How It Works

1. The Kotlin cache library is compiled into a fat JAR with all dependencies
2. The Python API uses JPype to start a JVM and load the Kotlin JAR
3. REST endpoints expose the cache library functionality through HTTP requests
4. Docker containers package everything together for easy deployment

## Building and Running

### Prerequisites

- Docker and Docker Compose
- At least 4GB of available RAM (for the JVM)

### Quick Start

1. Build and start the services:
   ```bash
   docker-compose up --build
   ```

2. The services will be available at:
   - API: http://localhost:5000
   - Test Webapp: http://localhost:5001

### Using the API

1. Initialize the cache:
   ```bash
   curl -X POST http://localhost:5000/initialize \
        -H "Content-Type: application/json" \
        -d '{"path": "/app/cache"}'
   ```

2. Add an archive:
   ```bash
   curl -X POST http://localhost:5000/add_archive/0 \
        -H "Content-Type: application/json" \
        -d '{"name": "test_archive"}'
   ```

3. Put data into the cache:
   ```bash
   curl -X POST http://localhost:5000/put/0/0/0 \
        -H "Content-Type: application/json" \
        -d '{"data": "VGhpcyBpcyB0ZXN0IGRhdGEgZm9yIHRoZSBjYWNoZQ=="}'
   ```

4. Get data from the cache:
   ```bash
   curl http://localhost:5000/data/0/0/0
   ```

5. Shutdown the API (closes the cache library and JVM):
   ```bash
   curl -X POST http://localhost:5000/shutdown
   ```

## API Endpoints

### Health Check
- `GET /health` - Check if the API is running

### Cache Initialization
- `POST /initialize` - Initialize the cache library with a path
  - Body: `{"path": "/path/to/cache"}`

### Data Retrieval
- `GET /data/<index_id>/<archive_id>/<file_id>` - Get file data
- `GET /data/<index_id>/<archive_id>` - Get archive data

### Data Writing
- `POST /put/<index_id>/<archive_id>/<file_id>` - Put file data
  - Body: `{"data": "base64_encoded_data", "xtea": "0,0,0,0"}`
- `POST /put/<index_id>/<archive_id>` - Put archive data
  - Body: `{"data": "base64_encoded_data", "xtea": "0,0,0,0"}`

### Data Removal
- `DELETE /remove/<index_id>/<archive_id>/<file_id>` - Remove a file
- `DELETE /remove/<index_id>/<archive_id>` - Remove an archive

### Index Operations
- `POST /update/<index_id>` - Update/write changes to an index
- `POST /add_archive/<index_id>` - Add a new archive to an index
  - Body: `{"name": "archive_name"}`

### Cache Operations
- `POST /rebuild` - Rebuild/defragment the cache
  - Body: `{"output_path": "/path/to/new/cache"}`

### System Operations
- `POST /shutdown` - Shutdown the API and close the cache library

## XTEA Encryption Support

Some cache operations support XTEA encryption. To use XTEA, pass the `xtea` parameter as a comma-separated list of 4 integers:

```json
{
  "data": "base64_encoded_data",
  "xtea": "123,456,789,012"
}
```

## Testing

You can test the API using either:

1. The test webapp at http://localhost:5001
2. The test_integration.py script
3. Direct curl commands

## Limitations

- Named archive operations (by name rather than ID) are not yet fully implemented
- The API currently runs in development mode
- Error handling could be improved for production use

## Extending the API

To add new functionality:

1. Add methods to `cache_api.py` to interface with the Kotlin library
2. Add new endpoints to `api.py` to expose the functionality
3. Update the Dockerfile if new dependencies are needed
4. Test with the webapp or integration test script
