import os
import time
import random
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Dict
from uuid import uuid4
from dotenv import load_dotenv
import secrets
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('server.log')
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()
security = HTTPBasic()

# Configuration variables
USERNAME = os.getenv("API_USERNAME", "admin")
PASSWORD = os.getenv("API_PASSWORD", "password")

MIN_DELAY = int(os.getenv("MIN_DELAY", 5))
MAX_DELAY = int(os.getenv("MAX_DELAY", 15))
ERROR_PROBABILITY = float(os.getenv("ERROR_PROBABILITY", 0.2))

class JobStatus(BaseModel):
    start_time: float
    completion_time: float
    final_result: str

# In-memory storage for jobs
jobs: Dict[str, JobStatus] = {}

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        logger.warning(f"Unauthorized access attempt with username: {credentials.username}")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post("/start")
def start_job(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    job_id = str(uuid4())
    start_time = time.time()
    completion_time = start_time + random.uniform(MIN_DELAY, MAX_DELAY)
    final_result = "error" if random.random() < ERROR_PROBABILITY else "completed"
    jobs[job_id] = JobStatus(start_time=start_time, completion_time=completion_time, final_result=final_result)
    logger.info(f"Started job {job_id} with final result '{final_result}' scheduled at {completion_time}")
    return {"job_id": job_id}

@app.get("/status/{job_id}")
def get_status(job_id: str, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    job = jobs.get(job_id)
    if not job:
        logger.warning(f"Status request for nonexistent job ID: {job_id}")
        raise HTTPException(status_code=404, detail="Job not found")
    
    current_time = time.time()
    if current_time < job.completion_time:
        logger.info(f"Job {job_id} status: pending")
        return {"result": "pending"}
    else:
        logger.info(f"Job {job_id} status: {job.final_result}")
        return {"result": job.final_result}
