"""
Test script for the RuneScape Cache Library API integration
"""

import requests
import json
import base64
import os


def test_api_integration():
    """Test the API integration with the Kotlin library"""
    
    # API base URL
    base_url = "http://localhost:5000"
    
    # Test health endpoint
    print("Testing health endpoint...")
    response = requests.get(f"{base_url}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    
    # Test initialization (this would normally point to an actual cache directory)
    print("\nTesting initialization...")
    init_data = {"path": "./test_cache"}
    response = requests.post(f"{base_url}/initialize", json=init_data)
    print(f"Initialization: {response.status_code} - {response.json()}")
    
    # Test adding an archive
    print("\nTesting add archive...")
    response = requests.post(f"{base_url}/add_archive/0", json={"name": "test_archive"})
    print(f"Add archive: {response.status_code} - {response.json()}")
    
    # Test putting data
    print("\nTesting put data...")
    test_data = base64.b64encode(b"This is test data for the cache").decode('utf-8')
    put_data = {"data": test_data}
    response = requests.post(f"{base_url}/put/0/0/0", json=put_data)
    print(f"Put data: {response.status_code} - {response.json()}")
    
    # Test getting data
    print("\nTesting get data...")
    response = requests.get(f"{base_url}/data/0/0/0")
    print(f"Get data: {response.status_code} - {response.json()}")
    
    # Test removing file
    print("\nTesting remove file...")
    response = requests.delete(f"{base_url}/remove/0/0/0")
    print(f"Remove file: {response.status_code} - {response.json()}")
    
    # Test removing archive
    print("\nTesting remove archive...")
    response = requests.delete(f"{base_url}/remove/0/0")
    print(f"Remove archive: {response.status_code} - {response.json()}")
    
    # Test shutdown
    print("\nTesting shutdown...")
    response = requests.post(f"{base_url}/shutdown")
    print(f"Shutdown: {response.status_code} - {response.json()}")


def create_test_cache_structure():
    """Create a basic test cache structure"""
    os.makedirs("./test_cache", exist_ok=True)
    print("Created test cache directory")


if __name__ == "__main__":
    print("RuneScape Cache Library API Integration Test")
    print("=" * 50)
    
    # Create test cache structure
    create_test_cache_structure()
    
    # Run API tests
    test_api_integration()
    
    print("\nTest completed!")
