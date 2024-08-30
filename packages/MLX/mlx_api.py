from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlx.core as mx
import mlx.nn as nn
import uvicorn
from mlx_lm import load, generate

# Load model directly
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "deepseek-ai/DeepSeek-Coder-V2-Instruct", trust_remote_code=True)
app = FastAPI()


class PredictionInput(BaseModel):
    data: list[float]


class PredictionOutput(BaseModel):
    result: float


@app.post("/predict", response_model=PredictionOutput)
async def predict(input: PredictionInput):
    try:
        # Your MLX logic here
        result = mx.array(input.data).sum()
        return PredictionOutput(result=result.item())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5555)
