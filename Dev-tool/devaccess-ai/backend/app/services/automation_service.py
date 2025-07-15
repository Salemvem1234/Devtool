"""
Advanced Automation Service for DevAccess AI
Handles web automation, account creation, and monitoring
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

from app.core.config import settings
from app.models.account import Account
from app.models.software import Software
from app.services.email_service import EmailService
from app.services.password_service import PasswordService
from app.services.captcha_service import CaptchaService

logger = logging.getLogger(__name__)

class AutomationStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRY = "retry"

@dataclass
class AutomationResult:
    status: AutomationStatus
    account_id: Optional[int] = None
    credentials: Optional[Dict[str, str]] = None
    error_message: Optional[str] = None
    screenshots: Optional[List[str]] = None
    execution_time: Optional[float] = None
    api_tokens: Optional[Dict[str, str]] = None

class SoftwareAutomator:
    """Base class for software-specific automation"""
    
    def __init__(self, software: Software):
        self.software = software
        self.driver = None
        self.wait = None
        self.email_service = EmailService()
        self.password_service = PasswordService()
        self.captcha_service = CaptchaService()
    
    def setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver with optimal settings"""
        chrome_options = Options()
        
        if settings.AUTOMATION_HEADLESS:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-blink-features=VizDisplayCompositor')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Performance optimizations
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-javascript')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        
        if settings.SELENIUM_GRID_URL:
            driver = webdriver.Remote(
                command_executor=settings.SELENIUM_GRID_URL,
                options=chrome_options
            )
        else:
            driver = webdriver.Chrome(options=chrome_options)
        
        driver.set_window_size(1920, 1080)
        return driver
    
    async def create_account(self, email_domain: str = None, usage_context: str = None) -> AutomationResult:
        """Create account for this software"""
        start_time = datetime.now()
        
        try:
            # Generate credentials
            email = await self.email_service.generate_email(domain=email_domain)
            password = self.password_service.generate_password()
            
            # Setup driver
            self.driver = self.setup_driver()
            self.wait = WebDriverWait(self.driver, settings.AUTOMATION_TIMEOUT)
            
            # Navigate to signup page
            await self._navigate_to_signup()
            
            # Fill signup form
            await self._fill_signup_form(email, password)
            
            # Handle CAPTCHA if present
            if await self._detect_captcha():
                await self._solve_captcha()
            
            # Submit form
            await self._submit_signup_form()
            
            # Verify account creation
            await self._verify_account_creation()
            
            # Extract API tokens if available
            api_tokens = await self._extract_api_tokens()
            
            # Handle email verification if needed
            if await self._requires_email_verification():
                await self._handle_email_verification(email)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AutomationResult(
                status=AutomationStatus.SUCCESS,
                credentials={"email": email, "password": password},
                execution_time=execution_time,
                api_tokens=api_tokens
            )
            
        except TimeoutException as e:
            logger.error(f"Timeout during automation: {e}")
            return AutomationResult(
                status=AutomationStatus.FAILED,
                error_message=f"Timeout: {str(e)}"
            )
        except WebDriverException as e:
            logger.error(f"WebDriver error: {e}")
            return AutomationResult(
                status=AutomationStatus.FAILED,
                error_message=f"WebDriver error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error during automation: {e}")
            return AutomationResult(
                status=AutomationStatus.FAILED,
                error_message=f"Unexpected error: {str(e)}"
            )
        finally:
            if self.driver:
                self.driver.quit()
    
    async def _navigate_to_signup(self):
        """Navigate to signup page - override in subclasses"""
        raise NotImplementedError
    
    async def _fill_signup_form(self, email: str, password: str):
        """Fill signup form - override in subclasses"""
        raise NotImplementedError
    
    async def _detect_captcha(self) -> bool:
        """Detect if CAPTCHA is present"""
        try:
            captcha_elements = [
                "//div[contains(@class, 'captcha')]",
                "//iframe[contains(@src, 'recaptcha')]",
                "//div[contains(@class, 'g-recaptcha')]",
                "//div[contains(@class, 'h-captcha')]"
            ]
            
            for xpath in captcha_elements:
                try:
                    self.driver.find_element(By.XPATH, xpath)
                    return True
                except:
                    continue
            
            return False
        except Exception:
            return False
    
    async def _solve_captcha(self):
        """Solve CAPTCHA using external service"""
        # Implementation depends on CAPTCHA service
        pass
    
    async def _submit_signup_form(self):
        """Submit signup form - override in subclasses"""
        raise NotImplementedError
    
    async def _verify_account_creation(self):
        """Verify account was created successfully"""
        # Check for success indicators
        success_indicators = [
            "//div[contains(text(), 'success')]",
            "//div[contains(text(), 'welcome')]",
            "//div[contains(text(), 'account created')]",
            "//div[contains(@class, 'dashboard')]"
        ]
        
        for xpath in success_indicators:
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                return True
            except TimeoutException:
                continue
        
        # Check URL for dashboard/success page
        current_url = self.driver.current_url.lower()
        if any(keyword in current_url for keyword in ['dashboard', 'welcome', 'success']):
            return True
        
        raise Exception("Could not verify account creation")
    
    async def _extract_api_tokens(self) -> Dict[str, str]:
        """Extract API tokens from the interface"""
        # Override in subclasses for software-specific token extraction
        return {}
    
    async def _requires_email_verification(self) -> bool:
        """Check if email verification is required"""
        verification_indicators = [
            "//div[contains(text(), 'verify')]",
            "//div[contains(text(), 'email sent')]",
            "//div[contains(text(), 'check your email')]"
        ]
        
        for xpath in verification_indicators:
            try:
                self.driver.find_element(By.XPATH, xpath)
                return True
            except:
                continue
        
        return False
    
    async def _handle_email_verification(self, email: str):
        """Handle email verification process"""
        # Get verification email
        verification_email = await self.email_service.get_verification_email(email)
        
        if verification_email:
            # Extract verification link
            verification_link = self.email_service.extract_verification_link(verification_email)
            
            if verification_link:
                # Navigate to verification link
                self.driver.get(verification_link)
                
                # Wait for verification to complete
                self.wait.until(EC.url_contains('verified'))

class CursorAutomator(SoftwareAutomator):
    """Cursor IDE automation"""
    
    async def _navigate_to_signup(self):
        self.driver.get("https://cursor.sh/signup")
    
    async def _fill_signup_form(self, email: str, password: str):
        # Wait for form to load
        email_field = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        password_field = self.driver.find_element(By.ID, "password")
        
        # Fill form
        email_field.send_keys(email)
        password_field.send_keys(password)
    
    async def _submit_signup_form(self):
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

class VercelAutomator(SoftwareAutomator):
    """Vercel automation"""
    
    async def _navigate_to_signup(self):
        self.driver.get("https://vercel.com/signup")
    
    async def _fill_signup_form(self, email: str, password: str):
        # Vercel uses GitHub/GitLab OAuth by default
        # This is a simplified example
        email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys(email)
    
    async def _submit_signup_form(self):
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
        submit_button.click()

class AutomationService:
    """Main automation service"""
    
    def __init__(self):
        self.automators = {
            "cursor": CursorAutomator,
            "vercel": VercelAutomator,
            # Add more automators as needed
        }
    
    async def create_account(self, software_name: str, email_domain: str = None, usage_context: str = None) -> AutomationResult:
        """Create account for specified software"""
        if software_name not in self.automators:
            return AutomationResult(
                status=AutomationStatus.FAILED,
                error_message=f"No automator available for {software_name}"
            )
        
        # Get software info (mock for now)
        software = Software(name=software_name, url=f"https://{software_name}.com")
        
        # Create automator instance
        automator = self.automators[software_name](software)
        
        # Execute automation
        result = await automator.create_account(email_domain, usage_context)
        
        # Log result
        logger.info(f"Account creation for {software_name}: {result.status.value}")
        
        return result
    
    async def create_multiple_accounts(self, software_accounts: Dict[str, int], email_domain: str = None, usage_context: str = None) -> List[AutomationResult]:
        """Create multiple accounts for different software"""
        results = []
        
        for software_name, count in software_accounts.items():
            for i in range(count):
                result = await self.create_account(software_name, email_domain, usage_context)
                results.append(result)
                
                # Add delay between requests to avoid rate limiting
                await asyncio.sleep(2)
        
        return results
    
    async def get_supported_software(self) -> List[str]:
        """Get list of supported software"""
        return list(self.automators.keys())
    
    async def validate_automation_feasibility(self, software_name: str) -> Dict[str, Any]:
        """Validate if automation is feasible for given software"""
        if software_name not in self.automators:
            return {
                "feasible": False,
                "reason": "No automator available",
                "success_rate": 0.0
            }
        
        # Mock success rate - in production, track actual success rates
        success_rates = {
            "cursor": 0.85,
            "vercel": 0.75,
            # Add more as needed
        }
        
        return {
            "feasible": True,
            "success_rate": success_rates.get(software_name, 0.5),
            "estimated_time": "2-5 minutes",
            "requirements": ["Valid email domain", "CAPTCHA solving capability"]
        }

# Global service instance
automation_service = AutomationService()
