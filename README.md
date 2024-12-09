# Video Translation Status Client & Server

This repository contains a simulated video translation status server and a client library that provides a smarter polling strategy to fetch the final status of a video translation job.

## Server

### Overview

The server simulates a video translation backend. When queried at `GET /status`, it returns:
- `{"result": "pending"}` until a random delay passes.
- After the delay, it returns either `{"result": "completed"}` or `{"result": "error"}`.

### Running the Server

```bash
cd server
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
