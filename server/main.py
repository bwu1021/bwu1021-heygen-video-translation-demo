import os
import time
import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Configuration
MIN_DELAY = int(os.environ.get("MIN_DELAY", 5))
MAX_DELAY = int(os.environ.get("MAX_DELAY", 15))
ERROR_PROBABILITY = float(os.environ.get("ERROR_PROBABILITY", 0.2))

start_time = time.time()
completion_time = start_time + random.uniform(MIN_DELAY, MAX_DELAY)
final_result = "error" if random.random() < ERROR_PROBABILITY else "completed"

@app.get("/status")
def get_status():
    current_time = time.time()
    if current_time < completion_time:
        return JSONResponse(content={"result": "pending"})
    else:
        return JSONResponse(content={"result": final_result})
