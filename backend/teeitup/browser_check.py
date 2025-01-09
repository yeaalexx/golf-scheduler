from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TeeitUpBrowserChecker:
    def __init__(self):
        self.base_url = "https://somerset-group-v2.book.teeitup.com/"
        self.setup_browser()
        
    def setup_browser(self):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--enable-javascript")
        
        # Enable network logging
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def analyze_page(self):
        """Analyze the TeeitUp booking page for API calls"""
        logger.info(f"Analyzing page: {self.base_url}")
        
        try:
            self.driver.get(self.base_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get network logs
            logs = self.driver.get_log("performance")
            
            api_endpoints = set()  # Use set to avoid duplicates
            
            # Filter for XHR/Fetch requests
            for log in logs:
                try:
                    message = json.loads(log["message"])
                    if "Network.requestWillBeSent" in message["message"]["method"]:
                        request = message["message"]["params"]["request"]
                        if request.get("url"):
                            url = request["url"]
                            method = request.get("method", "")
                            
                            # Log all requests
                            logger.info(f"Request: {method} {url}")
                            
                            # Look for potential API endpoints
                            if any(term in url.lower() for term in ['api', 'graphql', 'data', 'book']):
                                api_endpoints.add(f"{method} {url}")
                                logger.info(f"Potential API endpoint found: {method} {url}")
                                
                            # Log headers for analysis
                            headers = request.get("headers", {})
                            if headers:
                                logger.info(f"Headers: {json.dumps(headers, indent=2)}")
                                
                except Exception as e:
                    continue
            
            # Save discovered endpoints
            if api_endpoints:
                with open('teeitup/discovered_endpoints.txt', 'w') as f:
                    f.write('\n'.join(sorted(api_endpoints)))
                logger.info(f"Saved {len(api_endpoints)} discovered endpoints to discovered_endpoints.txt")
            
        except Exception as e:
            logger.error(f"Error analyzing page: {str(e)}")
            
    def cleanup(self):
        """Close the browser"""
        self.driver.quit()

if __name__ == "__main__":
    checker = TeeitUpBrowserChecker()
    try:
        checker.analyze_page()
    finally:
        checker.cleanup() 