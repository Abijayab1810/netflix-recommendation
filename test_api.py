"""
Simple test script for the Movie Recommendation API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test API health check"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_get_movies():
    """Test getting all movies"""
    print("Testing get all movies...")
    response = requests.get(f"{BASE_URL}/movies")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total movies: {data['count']}")
    print(f"First 5 movies: {data['movies'][:5]}\n")

def test_recommend_post():
    """Test recommendations with POST request"""
    print("Testing recommendations (POST)...")
    payload = {
        "movie_title": "Avatar",
        "num_recommendations": 5
    }
    response = requests.post(f"{BASE_URL}/recommend", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_recommend_get():
    """Test recommendations with GET request"""
    print("Testing recommendations (GET)...")
    response = requests.get(f"{BASE_URL}/recommend/Inception?num_recommendations=5")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_invalid_movie():
    """Test with invalid movie title"""
    print("Testing with invalid movie title...")
    payload = {
        "movie_title": "NonExistentMovie123",
        "num_recommendations": 5
    }
    response = requests.post(f"{BASE_URL}/recommend", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("NETFLIX MOVIE RECOMMENDATION API - TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_health_check()
        test_get_movies()
        test_recommend_post()
        test_recommend_get()
        test_invalid_movie()
        
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API at", BASE_URL)
        print("Make sure the API is running: docker-compose up")
    except Exception as e:
        print(f"ERROR: {e}")
