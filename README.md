# Video Translation Status Client & Server

This repository contains a simulated video translation status server and a client library that provides a smarter polling strategy to fetch the final status of a video translation job.

## Project Structure

- **Server:**  
  Simulates a video translation backend:
  - `GET /status` returns `{"result":"pending"}` until a chosen delay passes.
  - After the delay, returns either `{"result":"completed"}` or `{"result":"error"}` based on a configured probability.

- **Client Library:**  
  A client that:
  - Polls the server’s `/status` endpoint with exponential backoff.
  - Logs attempts and final outcomes.
  - Allows configuration of polling intervals.

- **Integration Test:**  
  Demonstrates how the client interacts with the server:
  - Starts the server in a subprocess.
  - Polls until `completed` or `error`.
  - Prints logs for insight.

### Running the Server
```
cd server
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Running the Client
```
cd client
pip install -r requirements.txt
```
#### Use the Client: In a Python script or interactive shell:
```
from client import TranslationStatusClient

client = TranslationStatusClient("http://127.0.0.1:8000")
final_result = client.wait_for_completion()
print(f"Final status: {final_result}")
```

### Running the Integration Test

```
# Make sure all dependencies are installed
cd server
pip install -r requirements.txt
cd ../client
pip install -r requirements.txt
cd ..

# From project root
python test_integration.py
```
