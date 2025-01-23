from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import uvicorn
import torch

app = FastAPI(title="Content Moderation API")

#initiate the model
try:
    # classifier = pipeline("sentiment-analysis", model="michellejieli/inappropriate_text_classifier")
    classifier = pipeline("text-classification", model="michellejieli/inappropriate_text_classifier")
except Exception as e:
    print(f"error loading model: {e}")
    raise

class TextRequest(BaseModel):
    text: str


class TextResponse(BaseModel):
    is_inappropriate: bool
    confidence: float
    label: str


@app.post("/check_content", response_model=TextResponse)
async def check_content(request: TextRequest):
    try:
        # Get prediction from model
        result = classifier(request.text)[0]

        # Convert result to boolean and extract confidence
        # is_inappropriate = result['label'] == 'INAPPROPRIATE'
        is_inappropriate = result['label'] == 'NSFW' and result['score'] > 0.7

        return TextResponse(
            is_inappropriate=is_inappropriate,
            confidence=result['score'],
            label=result['label']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5656)