from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
import uvicorn
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List
import numpy as np
from contextlib import asynccontextmanager
import httpx
import os

# Globals
model = None
tokenizer = None
model_id = 'Qwen/Qwen3-Embedding-0.6B'
executor = ThreadPoolExecutor(max_workers=4)
MAX_TOKENS = 32000

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model and tokenizer at startup
    global model, tokenizer
    print(f"Loading model: {model_id}...")
    model = SentenceTransformer(model_id)
    tokenizer = model.tokenizer
    print("Model loaded successfully")
    yield
    # (Optional) Clean up resources at shutdown
    print("Cleaning up resources...")
    model = None
    tokenizer = None

app = FastAPI(
    title="Text Embedding API (Qwen/Qwen3-Embedding-0.6B)",
    lifespan=lifespan
)

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to embed")
    request_id: str | None = Field(None, description="Optional unique identifier for the request")




async def send_to_webhook(url: str, data: dict):
    """Sends data to a webhook URL asynchronously."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            print(f"Successfully sent data to webhook: {url}")
    except httpx.RequestError as e:
        print(f"Error sending data to webhook {url}: {e}")

@app.get("/")
def home():
    return {"status": "online", "model": model_id, "endpoint": "/embed/text"}

def chunk_and_embed(text: str) -> List[float]:
    """Split text into chunks if too long, then pool embeddings"""
    tokens = tokenizer.encode(text, add_special_tokens=False)
    
    # If text is short, embed directly
    if len(tokens) <= MAX_TOKENS:
        return model.encode(text, normalize_embeddings=True).tolist()
    
    # Split into chunks
    chunks = []
    overlap = 50
    start = 0
    while start < len(tokens):
        end = start + MAX_TOKENS
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)
        
        if end >= len(tokens):
            break
        start = end - overlap
    
    # Embed all chunks
    chunk_embeddings = [model.encode(chunk, normalize_embeddings=True) for chunk in chunks]
    
    # Pool embeddings (mean)
    final_embedding = np.mean(chunk_embeddings, axis=0).tolist()
    
    return final_embedding

@app.post("/embed/text")
async def embed_text(request: TextRequest, background_tasks: BackgroundTasks):
    try:
        loop = asyncio.get_event_loop()
        embedding = await loop.run_in_executor(
            executor,
            lambda: chunk_and_embed(request.text)
        )
        
        # Check for webhook URL and add the background task
        webhook_url = os.environ.get("WEBHOOK_URL")
        if webhook_url:
            payload = {
                "text": request.text,
                "embedding": embedding,
                "request_id": request.request_id 
            }
            background_tasks.add_task(send_to_webhook, webhook_url, payload)

        return {
            "success": True,
            "model": model_id,
            "dimension": len(embedding),
            "embedding": embedding
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
