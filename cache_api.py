"""
RuneScape Cache Library API Implementation
This module provides a Python interface to the Kotlin-based RuneScape cache library using JPype.
"""

import jpype
import jpype.imports
from jpype.types import *
import os
import base64
import json
from typing import Optional, List


class CacheLibraryAPI:
    """Python wrapper for the RuneScape Cache Library"""
    
    def __init__(self):
        self.cache_library = None
        self._jvm_started = False
    
    def start_jvm(self, jar_path: str = "build/libs/rs-cache-library-all.jar"):
        """Start the JVM with the cache library JAR"""
        if not self._jvm_started:
            if not jpype.isJVMStarted():
                # Handle both relative and absolute paths
                import os
                if not os.path.exists(jar_path):
                    # Try alternative path for Docker environment
                    docker_jar_path = "/app/libs/rs-cache-library-all.jar"
                    if os.path.exists(docker_jar_path):
                        jar_path = docker_jar_path
                
                # If still not found, try any JAR file in the libs directory
                if not os.path.exists(jar_path):
                    import glob
                    jar_files = glob.glob("/app/libs/*.jar")
                    if jar_files:
                        jar_path = jar_files[0]
                
                if not os.path.exists(jar_path):
                    raise FileNotFoundError(f"Cache library JAR not found at {jar_path}")
                
                jpype.startJVM(classpath=[jar_path, "libs/*"], convertStrings=False)
            self._jvm_started = True
    
    def initialize_cache(self, path: str):
        """Initialize the cache library with the given path"""
        try:
            # Import the Kotlin classes
            from com.displee.cache import CacheLibrary
            
            # Check if path exists
            if not os.path.exists(path):
                return {"status": "error", "message": f"Cache path does not exist: {path}"}
            
            # Create the cache library instance
            self.cache_library = CacheLibrary.create(path)
            return {"status": "success", "message": f"Cache initialized at {path}"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to initialize cache: {str(e)}"}
    
    def get_file_data(self, index_id: int, archive_id: int, file_id: int = 0, xtea: Optional[List[int]] = None):
        """Get file data from the cache"""
        try:
            if self.cache_library is None:
                return {"status": "error", "message": "Cache not initialized"}
            
            # Convert xtea to Java int array if provided
            xtea_array = None
            if xtea is not None:
                xtea_array = jpype.JArray(jpype.JInt)(xtea)
            
            # Get data from cache
            data = self.cache_library.data(index_id, archive_id, file_id, xtea_array)
            
            if data is None:
                return {"status": "error", "message": f"No data found for index {index_id}, archive {archive_id}, file {file_id}"}
            
            # Convert byte array to base64 for JSON serialization
            data_b64 = base64.b64encode(bytes(data)).decode('utf-8')
            
            return {
                "status": "success",
                "data": data_b64,
                "index_id": index_id,
                "archive_id": archive_id,
                "file_id": file_id
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to get file data: {str(e)}"}
    
    def put_file_data(self, index_id: int, archive_id: int, file_id: int, data: str, xtea: Optional[List[int]] = None):
        """Put file data into the cache"""
        try:
            if self.cache_library is None:
                return {"status": "error", "message": "Cache not initialized"}
            
            # Decode base64 data
            data_bytes = base64.b64decode(data)
            
            # Convert to Java byte array
            java_data = jpype.JArray(jpype.JByte)(data_bytes)
            
            # Convert xtea to Java int array if provided
            xtea_array = None
            if xtea is not None:
                xtea_array = jpype.JArray(jpype.JInt)(xtea)
            
            # Put data into cache
            self.cache_library.put(index_id, archive_id, file_id, java_data, xtea_array)
            
            return {
                "status": "success",
                "message": f"Data written to index {index_id}, archive {archive_id}, file {file_id}"
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to put file data: {str(e)}"}
    
    def remove_file(self, index_id: int, archive_id: int, file_id: int):
        """Remove a file from the cache"""
        try:
            if self.cache_library is None:
                return {"status": "error", "message": "Cache not initialized"}
            
            # Remove file from cache
            result = self.cache_library.remove(index_id, archive_id, file_id)
            
            return {
                "status": "success",
                "message": f"File {file_id} removed from archive {archive_id} in index {index_id}",
                "result": result
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to remove file: {str(e)}"}
    
    def remove_archive(self, index_id: int, archive_id: int):
        """Remove an archive from the cache"""
        try:
            if self.cache_library is None:
                return {"status": "error", "message": "Cache not initialized"}
            
            # Remove archive from cache
            result = self.cache_library.remove(index_id, archive_id)
            
            return {
                "status": "success",
                "message": f"Archive {archive_id} removed from index {index_id}",
                "result": result
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to remove archive: {str(e)}"}
    
    def update_index(self, index_id: int):
        """Update/write changes to an index"""
        try:
            if self.cache_library is None:
                return {"status": "error", "message": "Cache not initialized"}
            
            # Get index and update
            index = self.cache_library.index(index_id)
            if index is None:
                return {"status": "error", "message": f"Index {index_id} not found"}
            
            result = index.update()
            
            return {
                "status": "success",
                "message": f"Index {index_id} updated successfully",
                "result": result
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to update index: {str(e)}"}
    
    def add_archive(self, index_id: int, archive_name: Optional[str] = None):
        """Add a new archive to an index"""
        try:
            if self.cache_library is None:
                return {"status": "error", "message": "Cache not initialized"}
            
            # Get index
            index = self.cache_library.index(index_id)
            if index is None:
                return {"status": "error", "message": f"Index {index_id} not found"}
            
            # Add archive
            if archive_name:
                new_archive = index.add(archive_name)
            else:
                new_archive = index.add()
            
            return {
                "status": "success",
                "message": f"New archive added to index {index_id}",
                "archive_id": new_archive.id if new_archive else None
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to add archive: {str(e)}"}
    
    def rebuild_cache(self, output_path: str):
        """Rebuild/defragment the cache"""
        try:
            if self.cache_library is None:
                return {"status": "error", "message": "Cache not initialized"}
            
            # Import Java File class
            from java.io import File
            
            # Create output directory
            output_file = File(output_path)
            
            # Rebuild cache
            self.cache_library.rebuild(output_file)
            
            return {
                "status": "success",
                "message": f"Cache rebuilt to {output_path}"
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to rebuild cache: {str(e)}"}
    
    def close(self):
        """Close the cache library and shutdown JVM"""
        try:
            if self.cache_library is not None:
                self.cache_library.close()
                self.cache_library = None
            
            if self._jvm_started and jpype.isJVMStarted():
                jpype.shutdownJVM()
                self._jvm_started = False
            
            return {"status": "success", "message": "Cache library closed"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to close cache library: {str(e)}"}


# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    api = CacheLibraryAPI()
    print("Cache Library API initialized")
    print("Use start_jvm() to start the JVM with the cache library")
    print("Use initialize_cache(path) to initialize the cache")
