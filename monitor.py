import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_URL = "https://api.github.com"
CHECK_INTERVAL = 60

def check_api():
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            logging.info(f"API is UP! Status Code: {response.status_code}")
        else:
            logging.warning(f"API returned status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Failed to connect to API: {e}")

if __name__ == "__main__":
    logging.info("Starting API Health Monitor...")
    while True:
        check_api()
        time.sleep(CHECK_INTERVAL)
