import json
import logging
import time
import yaml
from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vllm import AsyncLLMEngine, AsyncEngineArgs, SamplingParams
from vllm.utils import random_uuid
from starlette.responses import StreamingResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'HTTP Request Latency')

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Initialize models
models: Dict[str, AsyncLLMEngine] = {}
for model_name, model_path in config['models'].items():
    args = AsyncEngineArgs(model=model_path)
    models[model_name] = AsyncLLMEngine.from_engine_args(args)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header:
        # Here you would validate the API key
        # For now, we'll just return True if any key is provided
        return True
    return False


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    REQUEST_COUNT.inc()
    start_time = time.time()
    response = await call_next(request)
    REQUEST_LATENCY.observe(time.time() - start_time)
    return response


@app.get("/metrics")
async def metrics():
    return Response(generate_latest())


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict]
    usage: Dict


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Path: {request.url.path} | Method: {request.method} | Status: {
                    response.status_code} | Time: {process_time:.2f}s")
        return response

# *TODO - Finish Authentication
# Authentication placeholder
# @app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
# async def chat_completion(request: ChatCompletionRequest, authenticated: bool = Depends(get_api_key)):
#     if not authenticated:
#         raise HTTPException(status_code=401, detail="Invalid API Key")
    # ... rest of the function remains the same


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completion(request: ChatCompletionRequest):
    try:
        if request.model not in models:
            raise HTTPException(status_code=400, detail=f"Model {
                                request.model} not found")

        engine = models[request.model]
        prompt = "\n".join(
            [f"{msg.role}: {msg.content}" for msg in request.messages])
        sampling_params = SamplingParams(
            temperature=request.temperature, max_tokens=request.max_tokens)

        if request.stream:
            return StreamingResponse(stream_completion(engine, prompt, sampling_params, request.model))
        else:
            return await generate_completion(engine, prompt, sampling_params, request.model)

    except Exception as e:
        logger.exception("Error in chat completion")
        raise HTTPException(status_code=500, detail=str(e))


async def generate_completion(engine, prompt, sampling_params, model_name):
    results_generator = engine.generate(prompt, sampling_params, random_uuid())
    final_output = None
    async for request_output in results_generator:
        final_output = request_output

    if final_output is None:
        raise HTTPException(status_code=500, detail="No output generated")

    text_output = final_output.outputs[0].text
    return ChatCompletionResponse(
        id=f"chatcmpl-{random_uuid()}",
        object="chat.completion",
        created=int(time.time()),
        model=model_name,
        choices=[{
            "index": 0,
            "message": {"role": "assistant", "content": text_output},
            "finish_reason": "stop"
        }],
        usage={
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(text_output.split()),
            "total_tokens": len(prompt.split()) + len(text_output.split())
        }
    )


async def stream_completion(engine, prompt, sampling_params, model_name):
    results_generator = engine.generate(prompt, sampling_params, random_uuid())
    async for request_output in results_generator:
        text_output = request_output.outputs[0].text
        yield f"data: {json.dumps({'choices': [{'delta': {'content': text_output}}]})}\n\n"
    yield "data: [DONE]\n\n"


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.exception("An unexpected error occurred")
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred"},
    )


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    REQUEST_COUNT.inc()
    start_time = time.time()
    response = await call_next(request)
    REQUEST_LATENCY.observe(time.time() - start_time)
    return response


@app.get("/metrics")
async def metrics():
    return Response(generate_latest())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
