from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class TextEmbeddingRequest(BaseModel):
    text: str

@app.post("/embed")
async def embed_text(request: TextEmbeddingRequest):
    model_url = "https://api.example.com/v1/embedding"  # Replace with actual model endpoint
    response = requests.post(model_url, json={'text': request.text})
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error from embedding service")
    
    return response.json()