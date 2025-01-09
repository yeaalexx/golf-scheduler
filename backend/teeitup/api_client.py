import asyncio
from playwright.async_api import async_playwright, TimeoutError
import logging
import os
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class TeeitUpClient:
    def __init__(self, email: str = None, password: str = None):
        """Initialize the TeeitUp API client"""
        self.base_url = "https://somerset-group-v2.book.teeitup.golf"
        self.email = email
        self.password = password
        
        self.facility_map = {
            "Green Knoll": 7092,
            "Neshanic Valley": 7093,
            "Quail Brook": 7094,
            "Spooky Brook": 7095,
            "Warren Brook": 7096
        }

    async def login(self):
        """Login to TeeitUp"""
        async with async_playwright() as p:
            # Launch browser with slower network conditions for stability
            browser = await p.chromium.launch(
                headless=False,  # Set to True in production
                slow_mo=100,  # Add delay between actions
            )
            
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            
            try:
                logger.info("Navigating to homepage...")
                await page.goto(f"{self.base_url}", wait_until="domcontentloaded")
                
                # Wait for page to stabilize
                await asyncio.sleep(2)
                
                logger.info("Looking for login button...")
                # Try different possible selectors
                login_button = None
                for selector in [
                    'text="Login"',
                    'button:has-text("Login")',
                    '[data-testid="login-button"]',
                    '#login-button',
                    '.login-button'
                ]:
                    try:
                        login_button = await page.wait_for_selector(selector, timeout=5000)
                        if login_button:
                            logger.info(f"Found login button with selector: {selector}")
                            break
                    except TimeoutError:
                        continue
                
                if not login_button:
                    logger.error("Could not find login button")
                    # Save screenshot for debugging
                    await page.screenshot(path="debug_screenshot.png")
                    raise Exception("Login button not found")
                
                await login_button.click()
                
                # Wait for login form
                logger.info("Waiting for login form...")
                await asyncio.sleep(2)
                
                # Try to find username/email field
                for selector in ['#username', '#email', '[name="email"]', '[type="email"]']:
                    try:
                        await page.fill(selector, self.email)
                        logger.info(f"Found email field with selector: {selector}")
                        break
                    except Exception:
                        continue
                
                # Try to find password field
                for selector in ['#password', '[name="password"]', '[type="password"]']:
                    try:
                        await page.fill(selector, self.password)
                        logger.info(f"Found password field with selector: {selector}")
                        break
                    except Exception:
                        continue
                
                # Try to find submit button
                for selector in [
                    '#login-submit',
                    'button[type="submit"]',
                    'button:has-text("Sign In")',
                    'button:has-text("Login")'
                ]:
                    try:
                        await page.click(selector)
                        logger.info(f"Found submit button with selector: {selector}")
                        break
                    except Exception:
                        continue
                
                # Wait for navigation
                logger.info("Waiting for login completion...")
                await page.wait_for_load_state("networkidle", timeout=10000)
                
                # Store cookies
                self.cookies = await context.cookies()
                logger.info("Login completed successfully")
                
            except Exception as e:
                logger.error(f"Login failed: {str(e)}")
                # Save screenshot for debugging
                await page.screenshot(path="error_screenshot.png")
                raise
            finally:
                await context.close()
                await browser.close()

    async def get_tee_times(self, date: str, facility_id: int):
        """Get tee times for a specific date and facility"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Navigate to tee time search page
                url = f"{self.base_url}/tee-times?date={date}&facilityId={facility_id}"
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                
                # Wait for tee times to load
                await page.wait_for_selector('.tee-time-list', timeout=5000)
                
                # Extract tee times
                tee_times = await page.evaluate('''() => {
                    const times = [];
                    document.querySelectorAll('.tee-time-slot').forEach(slot => {
                        times.push({
                            time: slot.querySelector('.time')?.textContent,
                            price: slot.querySelector('.price')?.textContent,
                            available: !slot.classList.contains('unavailable')
                        });
                    });
                    return times;
                }''')
                
                return tee_times
                
            except Exception as e:
                logger.error(f"Failed to get tee times: {str(e)}")
                return []
            finally:
                await browser.close()

async def test_client():
    """Test the TeeitUp API client"""
    # Check environment variables
    email = os.getenv("TEEITUP_EMAIL")
    password = os.getenv("TEEITUP_PASSWORD")
    
    logger.info("\n=== Environment Check ===")
    logger.info(f"Email configured: {'Yes' if email else 'No'}")
    logger.info(f"Password configured: {'Yes' if password else 'No'}")
    
    if not email or not password:
        logger.error("Missing credentials in environment variables")
        return
    
    client = TeeitUpClient(email, password)
    await client.login()
    
    # Test dates
    dates = [
        (datetime.now() + timedelta(days=x)).strftime("%Y-%m-%d")
        for x in [1, 2, 5]  # Tomorrow, day after, and 5 days from now
    ]
    
    for date in dates:
        logger.info(f"\nSearching for tee times on {date}:")
        
        for name, facility_id in client.facility_map.items():
            logger.info(f"\n🏌️ {name}:")
            tee_times = await client.get_tee_times(date, facility_id)
            
            if tee_times:
                for time in tee_times:
                    if time['available']:
                        logger.info(f"  • {time['time']}: {time['price']}")
            else:
                logger.info("No tee times available")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_client()) 