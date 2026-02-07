# Text Embedder

## API Documentation

### Overview
The Text Embedder API allows users to convert text into vector embeddings that can be utilized in machine learning and natural language processing applications.

### Endpoints

#### 1. `/embed`
- **Method:** `POST`
- **Description:** Takes text input and returns the corresponding embeddings.
- **Request Body:**
    - `text`: string (required) - The text to be embedded.

- **Response:**
    - `embeddings`: array of floats - The generated embeddings.

#### 2. `/health`
- **Method:** `GET`
- **Description:** Checks the health status of the service.

- **Response:**
    - `status`: string - Health status of the service (e.g., "healthy").


## Testing Instructions

To run the tests for the Text Embedder API, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/expher510/text_embedder.git
   cd text_embedder
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the tests:
   ```bash
   pytest tests/
   ```

Make sure your testing environment is properly configured with any necessary API keys or environment variables.


## Deployment Guide

### Prerequisites
- Ensure you have Python 3.7 or higher installed.
- Make sure Docker is installed and running if you are using containerization.

### Steps to Deploy

1. Build the Docker image:
   ```bash
   docker build -t text_embedder .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 text_embedder
   ```

3. Access the API:
   - The API will be accessible at `http://localhost:5000`

### Optional Configuration
You can configure the service by setting environment variables in your `.env` file or directly in the Docker run command.

---

### License
This project is licensed under the MIT License.
