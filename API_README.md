# RuneScape Cache Library API

This API provides a RESTful interface to interact with the RuneScape cache library, allowing you to read and write cache data through HTTP requests.

## API Endpoints

### Health Check
- `GET /health` - Check if the API is running

### Cache Initialization
- `POST /initialize` - Initialize the cache library with a path
  - Body: `{"path": "/path/to/cache"}`

### Data Retrieval
- `GET /data/<index_id>/<archive_id>/<file_id>` - Get file data
- `GET /data/<index_id>/<archive_id>` - Get archive data
- `GET /data/<index_id>/<archive_name>` - Get archive data by name

### Data Writing
- `POST /put/<index_id>/<archive_id>/<file_id>` - Put file data
  - Body: `{"data": "base64_encoded_data", "xtea": [0, 0, 0, 0]}`
- `POST /put/<index_id>/<archive_id>` - Put archive data
  - Body: `{"data": "base64_encoded_data", "xtea": [0, 0, 0, 0]}`
- `POST /put/<index_id>/<archive_name>` - Put archive data by name
  - Body: `{"data": "base64_encoded_data", "xtea": [0, 0, 0, 0]}`

### Data Removal
- `DELETE /remove/<index_id>/<archive_id>/<file_id>` - Remove a file
- `DELETE /remove/<index_id>/<archive_id>` - Remove an archive
- `DELETE /remove/<index_id>/<archive_name>` - Remove an archive by name

### Index Operations
- `POST /update/<index_id>` - Update/write changes to an index
- `POST /add_archive/<index_id>` - Add a new archive to an index
  - Body: `{"name": "archive_name"}`

### Cache Operations
- `POST /rebuild` - Rebuild/defragment the cache
  - Body: `{"output_path": "/path/to/new/cache"}`

## Docker Setup

1. Build and run the Docker container:
   ```
   docker-compose up --build
   ```

2. The API will be available at `http://localhost:5000`

## Usage Example

1. Initialize the cache:
   ```bash
   curl -X POST http://localhost:5000/initialize \
        -H "Content-Type: application/json" \
        -d '{"path": "/app/cache"}'
   ```

2. Get file data:
   ```bash
   curl http://localhost:5000/data/19/116/94
   ```

3. Put file data:
   ```bash
   curl -X POST http://localhost:5000/put/19/116/94 \
        -H "Content-Type: application/json" \
        -d '{"data": "base64_encoded_data_here"}'
   ```
