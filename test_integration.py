import os
import time
import subprocess
import requests
from client import TranslationStatusClient

def test_integration():
    # Start the server
    env = os.environ.copy()
    env["MIN_DELAY"] = "3"
    env["MAX_DELAY"] = "7"
    env["ERROR_PROBABILITY"] = "0.3"
    
    # Run the server in a subprocess
    proc = subprocess.Popen(["uvicorn", "server.main:app", "--host", "127.0.0.1", "--port", "8000"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            env=env)
    
    # Wait for server to start
    time.sleep(2)
    
    # Check server health by making a request
    try:
        response = requests.get("http://127.0.0.1:8000/status")
        response.raise_for_status()
    except Exception as e:
        proc.terminate()
        raise RuntimeError("Server did not start properly") from e

    client = TranslationStatusClient(base_url="http://127.0.0.1:8000")
    final_result = client.wait_for_completion()
    print(f"Test completed with final result: {final_result}")

    # Shutdown the server
    proc.terminate()
    proc.wait()

if __name__ == "__main__":
    test_integration()
