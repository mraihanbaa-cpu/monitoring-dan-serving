from fastapi import FastAPI
from pydantic import BaseModel
from .batcher import Batcher

batcher = Batcher()
app = FastAPI(title="Async Serving Main API")

class Predict(BaseModel):
    input: list

@app.post("/predict")
async def predict(data: Predict):
    rid = await batcher.enqueue(data.input)
    return {"request_id": rid}

@app.get("/result/{rid}")
async def result(rid: str):
    fut = batcher.futures.get(rid)
    if fut is None:
        return {"status": "not_found"}
    
    if fut.done():
        return {"status": "done", "result": fut.result()}
    return {"status": "pending"}


# Helper functions for direct (non-HTTP) use by other Python files
async def predict_async(input_list: list):
    """Async helper: enqueue input and await result (returns the result object).

    Use this function from async code: `await predict_async([...])`.
    """
    rid = await batcher.enqueue(input_list)
    fut = batcher.futures.get(rid)
    if fut is None:
        raise RuntimeError("Failed to create future for request")
    return await fut


def predict_blocking(input_list: list):
    """Blocking helper for synchronous code.

    This will run the async flow in a fresh event loop. If you are already
    inside an asyncio event loop, call `predict_async` instead.
    """
    import asyncio

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        raise RuntimeError("Event loop is already running. Use 'await predict_async(...)' instead.")

    return asyncio.run(predict_async(input_list))