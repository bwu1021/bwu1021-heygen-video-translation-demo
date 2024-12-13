# Video Translation Status Client & Server

This repository contains a simulated video translation status server and a client library that provides a smarter polling strategy to fetch the final status of a video translation job.

## Project Structure

- **Server:**  
  - Secure endpoints using Basic Authentication.
  - POST /start initiates a new translation job.
  - GET /status/{job_id} returns the status of a specific job (pending, completed, or error)

- **Client Library:**  
  - Polls the server’s `/status` endpoint with exponential backoff.
  - Logs attempts and final outcomes.
  - Allows configuration of polling intervals and authentication credentials.

- **Integration Test:**  
  - Starts the server in a subprocess.
  - Initiates a job via the client.
  - Polls until `completed` or `error`.
  - Prints logs for insight (also saved in files)

### Running the Server
```bash
cd server
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Running the Client
```bash
cd client
pip install -r requirements.txt
python3 client.py --username admin --password secretpassword
```
#### Use the Client: In a Python script or interactive shell:
```python
from client import TranslationStatusClient

# Initialize the client
client = TranslationStatusClient(
    base_url="http://127.0.0.1:8000",
    username="admin",
    password="secretpassword"
)

# Start a new job
job_id = client.start_job()
if not job_id:
    raise Exception("Failed to start a new job.")

print(f"Started job with ID: {job_id}")

# Wait for the job to complete
final_status = client.wait_for_completion(job_id)
print(f"Test completed with final status: {final_status}")
```

### Running the Integration Test

```bash
# Make sure all dependencies are installed
cd server
pip install -r requirements.txt
cd ../client
pip install -r requirements.txt
cd ..

# From project root
python3 test_integration.py
```
