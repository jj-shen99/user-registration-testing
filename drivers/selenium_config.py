"""
Selenium Test Configuration
===========================
Configuration settings for Selenium WebDriver tests
"""

import os
from selenium.webdriver.common.by import By

class SeleniumConfig:
    """Configuration class for Selenium tests"""
    
    # Test Environment Settings
    DEFAULT_BASE_URL = "http://localhost:5003"
    DEFAULT_TIMEOUT = 15
    IMPLICIT_WAIT = 10
    
    # Browser Settings
    BROWSER_OPTIONS = {
        "chrome": {
            "headless": False,
            "window_size": "1920,1080",
            "additional_options": [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-extensions",
                "--disable-web-security"
            ]
        },
        "firefox": {
            "headless": False,
            "window_size": "1920,1080"
        }
    }
    
    # Form Element Selectors
    # These can be customized based on your actual registration form
    SELECTORS = {
        # Form container
        "form": "#registration-form",
        "form_alt": "form[name='registration']",
        "form_fallback": "form",
        
        # Input fields
        "username": "#username",
        "username_alt": "input[name='username']",
        
        "email": "#email", 
        "email_alt": "input[name='email']",
        
        "password": "#password",
        "password_alt": "input[name='password']",
        
        "confirm_password": "#confirm_password",
        "confirm_password_alt": "input[name='confirm_password']",
        
        "first_name": "#first_name",
        "first_name_alt": "input[name='first_name']",
        
        "last_name": "#last_name",
        "last_name_alt": "input[name='last_name']",
        
        "phone": "#phone",
        "phone_alt": "input[name='phone']",
        
        # Buttons
        "submit_button": "button[type='submit']",
        "submit_button_alt": "input[type='submit']",
        "submit_button_fallback": ".submit-btn",
        
        # Messages
        "error_message": ".error-message",
        "error_message_alt": ".alert-danger",
        "error_message_fallback": "[class*='error']",
        
        "success_message": ".success-message",
        "success_message_alt": ".alert-success",
        "success_message_fallback": "[class*='success']",
        
        # UI Elements
        "password_toggle": ".password-toggle",
        "password_toggle_alt": ".show-password",
        "password_toggle_fallback": "[data-toggle='password']"
    }
    
    # Test Data Templates
    VALID_TEST_DATA = {
        "username": "testuser123",
        "email": "test@example.com",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+1234567890"
    }
    
    # Test Categories
    TEST_CATEGORIES = {
        "positive": ["REG_001", "REG_002", "REG_003"],
        "negative": ["REG_004", "REG_005", "REG_006", "REG_007", "REG_010", "REG_011"],
        "security": ["REG_015", "REG_016"],
        "ui_ux": ["REG_019", "REG_020", "REG_021"],
        "boundary": ["REG_012", "REG_013"],
        "performance": ["REG_023"]
    }
    
    # Expected Results
    EXPECTED_RESULTS = {
        "success_indicators": [
            "registration successful",
            "account created",
            "welcome",
            "success"
        ],
        "error_indicators": [
            "required",
            "invalid",
            "error",
            "failed",
            "missing"
        ]
    }
    
    # Security Test Payloads
    SECURITY_PAYLOADS = {
        "sql_injection": [
            "admin'; DROP TABLE users; --",
            "' OR '1'='1",
            "admin'/*",
            "1' UNION SELECT * FROM users--",
            "'; DELETE FROM users; --"
        ],
        "xss": [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//",
            "<svg onload=alert('XSS')>"
        ]
    }
    
    # Validation Test Data
    INVALID_EMAILS = [
        "invalid-email",
        "@example.com",
        "test@",
        "test..test@example.com",
        "test@example",
        "test@.com",
        ".test@example.com",
        "test@example.",
        "test@ex ample.com"
    ]
    
    WEAK_PASSWORDS = [
        "123",
        "password",
        "abc",
        "12345678",
        "Password",  # No special chars/numbers
        "password123",  # No uppercase/special chars
        "PASSWORD123",  # No lowercase/special chars
        "Pass123"  # Too short
    ]
    
    # Performance Thresholds
    PERFORMANCE_THRESHOLDS = {
        "max_page_load_time": 5.0,  # seconds
        "max_form_submit_time": 3.0,  # seconds
        "max_validation_time": 1.0   # seconds
    }
    
    @classmethod
    def get_selector_with_fallbacks(cls, field_name):
        """Get selector with fallback options"""
        selectors = []
        base_selector = cls.SELECTORS.get(field_name)
        alt_selector = cls.SELECTORS.get(f"{field_name}_alt")
        fallback_selector = cls.SELECTORS.get(f"{field_name}_fallback")
        
        if base_selector:
            selectors.append(base_selector)
        if alt_selector:
            selectors.append(alt_selector)
        if fallback_selector:
            selectors.append(fallback_selector)
            
        return selectors
    
    @classmethod
    def get_test_data_for_category(cls, category):
        """Get test data specific to a test category"""
        if category == "minimal":
            return {
                "username": "minuser",
                "email": "min@example.com",
                "password": "MinPass123!"
            }
        elif category == "complete":
            return cls.VALID_TEST_DATA.copy()
        else:
            return cls.VALID_TEST_DATA.copy()
    
    @classmethod
    def is_success_message(cls, message):
        """Check if message indicates success"""
        if not message:
            return False
        message_lower = message.lower()
        return any(indicator in message_lower for indicator in cls.EXPECTED_RESULTS["success_indicators"])
    
    @classmethod
    def is_error_message(cls, message):
        """Check if message indicates error"""
        if not message:
            return False
        message_lower = message.lower()
        return any(indicator in message_lower for indicator in cls.EXPECTED_RESULTS["error_indicators"])
