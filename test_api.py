"""
Quick test script to verify the API is working correctly
"""

import requests
import time
import json

API_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_match_with_text():
    """Test the /match endpoint with text input"""
    print("Testing /match endpoint with text input...")
    
    cv_text = """
    John Doe - Senior Machine Learning Engineer
    Skills: Python, PyTorch, Docker, FastAPI, AWS, Kubernetes
    Experience: 6 years in ML engineering
    """
    
    jd_text = """
    Looking for Machine Learning Engineer with:
    - Python, TensorFlow, PyTorch
    - Docker, Kubernetes
    - Cloud platforms (AWS or GCP)
    """
    
    response = requests.post(
        f"{API_URL}/match",
        data={
            "cv_text": cv_text,
            "jd_text": jd_text
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_match_with_files():
    """Test the /match endpoint with file input"""
    print("Testing /match endpoint with file input...")
    
    try:
        with open("sample_data/example_cv.txt", "r") as cv_file, \
             open("sample_data/example_jd.txt", "r") as jd_file:
            
            cv_text = cv_file.read()
            jd_text = jd_file.read()
            
            response = requests.post(
                f"{API_URL}/match",
                data={
                    "cv_text": cv_text,
                    "jd_text": jd_text
                }
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print()
    except FileNotFoundError:
        print("Sample files not found. Skipping file test.")
        print()

def test_skills_endpoint():
    """Test the /skills endpoint"""
    print("Testing /skills endpoint...")
    response = requests.get(f"{API_URL}/skills")
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Total skills: {data['total_skills']}")
    print(f"First 10 skills: {data['skills'][:10]}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("CV-to-Job Matcher API Test Suite")
    print("=" * 60)
    print()
    
    # Wait a bit for the server to be ready
    print("Waiting for server to start...")
    time.sleep(2)
    
    try:
        # Run tests
        test_health()
        test_match_with_text()
        test_match_with_files()
        test_skills_endpoint()
        
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")
        print("Make sure the server is running with:")
        print("  uvicorn app.main:app --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"Error during testing: {str(e)}")
