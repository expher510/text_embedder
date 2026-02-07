import pytest
import requests

BASE_URL = "http://your-api-url/text-embedder"  # Change to your actual URL


def test_embedding_valid_input():
    response = requests.post(f"{BASE_URL}/embed", json={"text": "hello world"})
    assert response.status_code == 200
    assert "embedding" in response.json()


def test_embedding_empty_input():
    response = requests.post(f"{BASE_URL}/embed", json={"text": ""})
    assert response.status_code == 400
    assert "error" in response.json()


def test_embedding_invalid_input():
    response = requests.post(f"{BASE_URL}/embed", json={"text": 123})  # Invalid input
    assert response.status_code == 400
    assert "error" in response.json()


def test_embedding_performance():
    import time
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/embed", json={"text": "Performance test"})
    duration = time.time() - start_time
    assert response.status_code == 200
    assert duration < 1.0  # Ensure response time is less than 1 second
