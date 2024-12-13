import time
import requests
import logging
import argparse

# Configure logging to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('client.log')
    ]
)
logger = logging.getLogger(__name__)

class TranslationStatusClient:
    def __init__(self, base_url: str, username: str, password: str, max_interval: float = 8.0):
        self.base_url = base_url
        self.max_interval = max_interval
        self.auth = (username, password)

    def start_job(self):
        try:
            response = requests.post(f"{self.base_url}/start", auth=self.auth)
            if response.status_code == 401:
                logger.error("Authentication failed. Check your username and password.")
                return None
            response.raise_for_status()
            data = response.json()
            job_id = data.get("job_id")
            logger.info(f"Job started with ID: {job_id}")
            return job_id
        except requests.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - {response.text}")
            return None
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    def get_status(self, job_id: str):
        try:
            response = requests.get(f"{self.base_url}/status/{job_id}", auth=self.auth, timeout=3)
            if response.status_code == 401:
                logger.error("Authentication failed. Check your username and password.")
                return None
            elif response.status_code == 404:
                logger.error(f"Job {job_id} not found.")
                return None
            response.raise_for_status()
            data = response.json()
            status = data.get("result")
            logger.info(f"Job {job_id} status: {status}")
            return status
        except requests.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - {response.text}")
            return None
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    def wait_for_completion(self, job_id: str, initial_interval=0.5):
        interval = initial_interval
        while True:
            status = self.get_status(job_id)
            if status in ["completed", "error"]:
                logger.info(f"Final status for job {job_id}: {status}")
                return status
            elif status == "pending":
                logger.info(f"Job {job_id} is pending. Waiting {interval} seconds before next check...")
                time.sleep(interval)
                interval = min(interval * 2, self.max_interval)
            else:
                logger.info(f"Job {job_id} received unexpected status '{status}'. Retrying after {interval} seconds...")
                time.sleep(interval)
                interval = min(interval * 2, self.max_interval)

def main():
    parser = argparse.ArgumentParser(description="Translation Status Client with Basic Authentication")
    parser.add_argument(
        "--url",
        type=str,
        default="http://127.0.0.1:8000",
        help="Base URL of the translation status server"
    )
    parser.add_argument(
        "--username",
        type=str,
        required=True,
        help="Username for authentication"
    )
    parser.add_argument(
        "--password",
        type=str,
        required=True,
        help="Password for authentication"
    )
    parser.add_argument(
        "--initial-interval",
        type=float,
        default=0.5,
        help="Initial polling interval in seconds"
    )
    parser.add_argument(
        "--max-interval",
        type=float,
        default=8.0,
        help="Maximum polling interval in seconds"
    )

    args = parser.parse_args()

    client = TranslationStatusClient(
        base_url=args.url,
        username=args.username,
        password=args.password,
        max_interval=args.max_interval
    )
    job_id = client.start_job()
    if not job_id:
        logger.error("Failed to start a new job.")
        return

    print(f"Started job with ID: {job_id}")
    final_status = client.wait_for_completion(job_id, initial_interval=args.initial_interval)
    print(f"Final status: {final_status}")

if __name__ == "__main__":
    main()