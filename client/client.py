import time
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslationStatusClient:
    def __init__(self, base_url: str, max_interval: float = 8.0):
        self.base_url = base_url
        self.max_interval = max_interval

    def get_status(self):
        try:
            response = requests.get(f"{self.base_url}/status", timeout=3)
            response.raise_for_status()
            data = response.json()
            return data.get("result")
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    def wait_for_completion(self, initial_interval=0.5):
        interval = initial_interval
        while True:
            result = self.get_status()
            if result in ["completed", "error"]:
                logger.info(f"Final status: {result}")
                return result
            elif result == "pending":
                logger.info(f"Status: pending, waiting {interval} seconds before next check...")
                time.sleep(interval)
                interval = min(interval * 2, self.max_interval)
            else:
                # If we got an unexpected result or None
                logger.info("Unexpected response or error, retrying...")
                time.sleep(interval)
                interval = min(interval * 2, self.max_interval)
