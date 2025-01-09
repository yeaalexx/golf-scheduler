from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import json
from datetime import datetime
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TeeitUpAPIExplorer:
    def __init__(self):
        self.base_url = "https://somerset-group-v2.book.teeitup.com/"
        self.api_base = "https://phx-api-be-east-1b.kenna.io"
        self.setup_browser()
        
    def setup_browser(self):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--enable-javascript")
        chrome_options.set_capability("goog:loggingPrefs", {
            "performance": "ALL",
            "browser": "ALL"
        })
        
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def analyze_api_calls(self):
        """Analyze API calls during booking flow"""
        logger.info(f"Starting API analysis...")
        
        try:
            # Load the page
            self.driver.get(self.base_url)
            time.sleep(5)  # Wait for initial load
            
            # Try to find and click date picker
            try:
                date_elements = self.driver.find_elements(By.CSS_SELECTOR, "[class*='date']")
                if date_elements:
                    date_elements[0].click()
                    time.sleep(2)
            except Exception as e:
                logger.error(f"Error clicking date: {str(e)}")
            
            # Capture network logs
            logs = self.driver.get_log("performance")
            api_calls = []
            
            for log in logs:
                try:
                    message = json.loads(log["message"])
                    if "Network.requestWillBeSent" in message["message"]["method"]:
                        request = message["message"]["params"]["request"]
                        url = request.get("url", "")
                        
                        # Focus on actual API calls
                        if self.api_base in url:
                            api_call = {
                                "method": request.get("method"),
                                "url": url,
                                "headers": request.get("headers"),
                                "body": request.get("postData")
                            }
                            api_calls.append(api_call)
                            logger.info(f"Found API call: {json.dumps(api_call, indent=2)}")
                            
                except Exception as e:
                    continue
            
            # Save discovered API calls
            if api_calls:
                with open('teeitup/api_calls.json', 'w') as f:
                    json.dump(api_calls, f, indent=2)
                logger.info(f"Saved {len(api_calls)} API calls to api_calls.json")
            
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            
    def cleanup(self):
        """Close the browser"""
        self.driver.quit()

if __name__ == "__main__":
    explorer = TeeitUpAPIExplorer()
    try:
        explorer.analyze_api_calls()
    finally:
        explorer.cleanup() 