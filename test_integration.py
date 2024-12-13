import os
import time
import subprocess
import requests
from client import TranslationStatusClient

def test_integration():
    # Set environment variables for the server if needed
    env = os.environ.copy()
    env["API_USERNAME"] = "admin"
    env["API_PASSWORD"] = "secretpassword"
    env["MIN_DELAY"] = "3"
    env["MAX_DELAY"] = "7"
    env["ERROR_PROBABILITY"] = "0.3"

    # Start the server in a subprocess
    proc = subprocess.Popen(
        ["uvicorn", "server.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd='.',  # Ensure the current directory is the project root
        env=env
    )

    try:
        # Give the server time to start
        logger.info("Waiting for the server to start...")
        time.sleep(5)

        # Check server health by making a request to a nonexistent job to ensure it's running
        response = requests.get("http://127.0.0.1:8000/status/nonexistent", auth=("admin", "secretpassword"))
        if response.status_code != 404:
            raise Exception("Server is not responding as expected.")

        logger.info("Server is up and running.")

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

    except Exception as e:
        print(f"Integration test failed: {e}")
    finally:
        # Shutdown the server
        proc.terminate()
        proc.wait()
        logger.info("Server has been shut down.")

if __name__ == "__main__":
    # Configure logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    test_integration()