import requests
import json
from urllib.parse import urljoin
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TeeitUpAPIChecker:
    def __init__(self):
        self.base_urls = [
            "https://teeitup.com",
            "https://api.teeitup.com",
            "https://app.teeitup.com"
        ]
        
        self.api_paths = [
            "/api",
            "/api/v1",
            "/api/v2",
            "/api/auth",
            "/api/booking",
            "/api/courses"
        ]
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def check_endpoint(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            logger.info(f"Checking {url}: Status {response.status_code}")
            
            # Log interesting headers
            if 'API' in response.headers.get('Server', '').upper():
                logger.info(f"Found API header in response from {url}")
            
            # Try to parse response as JSON
            try:
                json_response = response.json()
                logger.info(f"Got JSON response from {url}")
                return True
            except json.JSONDecodeError:
                pass
                
            return response.status_code < 400
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking {url}: {str(e)}")
            return False

    def analyze_network_traffic(self, url):
        """Analyze main page for potential API endpoints"""
        try:
            response = requests.get(url, headers=self.headers)
            content = response.text.lower()
            
            # Look for common API indicators in page source
            api_indicators = [
                'api.', '/api/', 'apikey', 'api-key',
                'endpoint', 'graphql'
            ]
            
            for indicator in api_indicators:
                if indicator in content:
                    logger.info(f"Found API indicator '{indicator}' in {url}")
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Error analyzing {url}: {str(e)}")

    def run_checks(self):
        logger.info("Starting API endpoint checks...")
        
        found_endpoints = []
        
        # Check direct API endpoints
        for base_url in self.base_urls:
            # Check base URL first
            self.analyze_network_traffic(base_url)
            
            # Check API paths
            for path in self.api_paths:
                url = urljoin(base_url, path)
                if self.check_endpoint(url):
                    found_endpoints.append(url)
        
        if found_endpoints:
            logger.info("Found potential API endpoints:")
            for endpoint in found_endpoints:
                logger.info(f"- {endpoint}")
        else:
            logger.info("No obvious API endpoints found. May need to investigate further or consider scraping.")
        
        return found_endpoints

if __name__ == "__main__":
    checker = TeeitUpAPIChecker()
    checker.run_checks() 