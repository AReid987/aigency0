from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from shared.ml_wrapper import ModelWrapper

app = FastAPI()
model = ModelWrapper()


class PredictionInput(BaseModel):
    data: list[float]


class PredictionOutput(BaseModel):
    result: list[float]


@app.post("/predict", response_model=PredictionOutput)
async def predict(input: PredictionInput):
    try:
        result = model.forward(input.data)
        return PredictionOutput(result=result.tolist())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
