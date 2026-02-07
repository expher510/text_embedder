from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import uvicorn

app = FastAPI(title="Text Embedding API (KaLM-Embedding-Gemma3-12B)")

class TextRequest(BaseModel):
    text: str

# Load Model
model_id = 'tencent/KaLM-Embedding-Gemma3-12B-2511'
model = SentenceTransformer(model_id)

@app.get("/")
def home():
    return {"status": "online", "model": model_id, "endpoint": "/embed/text"}

@app.post("/embed/text")
async def embed_text(request: TextRequest):
    try:
        # Generate embedding
        embedding = model.encode(request.text).tolist()
        
        return {
            "success": True, 
            "model": model_id,
            "dimension": len(embedding), 
            "embedding": embedding
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)