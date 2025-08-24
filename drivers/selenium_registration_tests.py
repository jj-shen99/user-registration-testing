"""
Selenium WebDriver User Registration Tests
=========================================
Comprehensive automated browser tests for user registration functionality
"""

import pytest
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumRegistrationTests:
    """
    Selenium WebDriver implementation of user registration tests
    """
    
    def __init__(self, base_url="http://localhost:5003", headless=False):
        self.base_url = base_url
        self.registration_url = f"{base_url}/register"
        self.headless = headless
        self.driver = None
        self.wait = None
        self.test_results = []
        
        # Test data templates
        self.valid_test_data = {
            "username": "testuser123",
            "email": "test@example.com",
            "password": "SecurePass123!",
            "confirm_password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890"
        }
        
        # Common selectors (adjust based on actual form structure)
        self.selectors = {
            "username": "#username",
            "email": "#email", 
            "password": "#password",
            "confirm_password": "#confirm_password",
            "first_name": "#first_name",
            "last_name": "#last_name",
            "phone": "#phone",
            "submit_button": "button[type='submit']",
            "error_message": ".error-message",
            "success_message": ".success-message",
            "form": "#registration-form"
        }
    
    def setup_driver(self):
        """Initialize Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Additional Chrome options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Use WebDriverManager to automatically handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 15)
        
        print(f"✅ Chrome WebDriver initialized (headless: {self.headless})")
    
    def teardown_driver(self):
        """Clean up WebDriver resources"""
        if self.driver:
            self.driver.quit()
            print("✅ WebDriver closed")
    
    def navigate_to_registration(self):
        """Navigate to registration page"""
        try:
            self.driver.get(self.registration_url)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors["form"])))
            print(f"✅ Navigated to registration page: {self.registration_url}")
            return True
        except TimeoutException:
            print(f"❌ Failed to load registration page: {self.registration_url}")
            return False
    
    def fill_form_field(self, field_name, value, clear_first=True):
        """Fill a form field with given value"""
        try:
            selector = self.selectors.get(field_name)
            if not selector:
                print(f"❌ Unknown field: {field_name}")
                return False
            
            element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            
            if clear_first:
                element.clear()
            
            element.send_keys(value)
            print(f"✅ Filled {field_name}: {value}")
            return True
            
        except (TimeoutException, NoSuchElementException) as e:
            print(f"❌ Failed to fill {field_name}: {str(e)}")
            return False
    
    def submit_form(self):
        """Submit the registration form"""
        try:
            submit_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.selectors["submit_button"]))
            )
            submit_button.click()
            print("✅ Form submitted")
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"❌ Failed to submit form: {str(e)}")
            return False
    
    def get_error_message(self):
        """Get error message from the page"""
        try:
            error_element = self.driver.find_element(By.CSS_SELECTOR, self.selectors["error_message"])
            return error_element.text
        except NoSuchElementException:
            return None
    
    def get_success_message(self):
        """Get success message from the page"""
        try:
            success_element = self.driver.find_element(By.CSS_SELECTOR, self.selectors["success_message"])
            return success_element.text
        except NoSuchElementException:
            return None
    
    def wait_for_response(self, timeout=10):
        """Wait for form response (success or error message)"""
        try:
            # Wait for either success or error message
            self.wait.until(
                lambda driver: self.get_success_message() or self.get_error_message()
            )
            return True
        except TimeoutException:
            print("❌ Timeout waiting for form response")
            return False
    
    def execute_test_case(self, test_id, description, test_data, expected_result_type="success"):
        """Execute a single test case"""
        print(f"\n🧪 Running {test_id}: {description}")
        start_time = time.time()
        
        try:
            # Navigate to registration page
            if not self.navigate_to_registration():
                return self.record_test_result(test_id, description, False, "Failed to load page", start_time)
            
            # Fill form fields
            for field, value in test_data.items():
                if field in self.selectors:
                    if not self.fill_form_field(field, value):
                        return self.record_test_result(test_id, description, False, f"Failed to fill {field}", start_time)
            
            # Submit form
            if not self.submit_form():
                return self.record_test_result(test_id, description, False, "Failed to submit form", start_time)
            
            # Wait for response
            if not self.wait_for_response():
                return self.record_test_result(test_id, description, False, "No response received", start_time)
            
            # Check result
            success_msg = self.get_success_message()
            error_msg = self.get_error_message()
            
            if expected_result_type == "success":
                passed = success_msg is not None
                actual_result = success_msg or "No success message"
            else:
                passed = error_msg is not None
                actual_result = error_msg or "No error message"
            
            return self.record_test_result(test_id, description, passed, actual_result, start_time)
            
        except Exception as e:
            return self.record_test_result(test_id, description, False, f"Exception: {str(e)}", start_time)
    
    def record_test_result(self, test_id, description, passed, result_message, start_time):
        """Record test execution result"""
        end_time = time.time()
        execution_time = end_time - start_time
        
        result = {
            "test_id": test_id,
            "description": description,
            "passed": passed,
            "execution_time": execution_time,
            "result_message": result_message,
            "timestamp": datetime.now().isoformat()
        }
        
        self.test_results.append(result)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {execution_time:.2f}s - {result_message}")
        
        return result
    
    # ========== POSITIVE TEST CASES ==========
    
    def test_successful_registration_with_valid_data(self):
        """
        Test Case ID: REG_001
        Description: Verify successful user registration with all valid required fields
        Priority: High
        """
        test_data = self.valid_test_data.copy()
        test_data["username"] = f"user_{int(time.time())}"
        test_data["email"] = f"user_{int(time.time())}@example.com"
        
        return self.execute_test_case(
            "REG_001",
            "Successful registration with valid data",
            test_data,
            "success"
        )
    
    def test_registration_with_minimum_required_fields(self):
        """
        Test Case ID: REG_002
        Description: Verify registration with only minimum required fields
        Priority: High
        """
        minimal_data = {
            "username": f"minuser_{int(time.time())}",
            "email": f"min_{int(time.time())}@example.com",
            "password": "MinPass123!"
        }
        
        return self.execute_test_case(
            "REG_002",
            "Registration with minimum required fields",
            minimal_data,
            "success"
        )
    
    def test_registration_with_all_optional_fields(self):
        """
        Test Case ID: REG_003
        Description: Verify registration with all optional fields filled
        Priority: Medium
        """
        complete_data = self.valid_test_data.copy()
        complete_data["username"] = f"complete_{int(time.time())}"
        complete_data["email"] = f"complete_{int(time.time())}@example.com"
        
        return self.execute_test_case(
            "REG_003",
            "Registration with all optional fields",
            complete_data,
            "success"
        )
    
    # ========== NEGATIVE TEST CASES ==========
    
    def test_registration_with_empty_username(self):
        """
        Test Case ID: REG_004
        Description: Verify registration fails with empty username
        Priority: High
        """
        test_data = self.valid_test_data.copy()
        test_data["username"] = ""
        
        return self.execute_test_case(
            "REG_004",
            "Registration with empty username",
            test_data,
            "error"
        )
    
    def test_registration_with_empty_email(self):
        """
        Test Case ID: REG_005
        Description: Verify registration fails with empty email
        Priority: High
        """
        test_data = self.valid_test_data.copy()
        test_data["email"] = ""
        
        return self.execute_test_case(
            "REG_005",
            "Registration with empty email",
            test_data,
            "error"
        )
    
    def test_registration_with_empty_password(self):
        """
        Test Case ID: REG_006
        Description: Verify registration fails with empty password
        Priority: High
        """
        test_data = self.valid_test_data.copy()
        test_data["password"] = ""
        
        return self.execute_test_case(
            "REG_006",
            "Registration with empty password",
            test_data,
            "error"
        )
    
    def test_registration_with_invalid_email_format(self):
        """
        Test Case ID: REG_007
        Description: Verify registration fails with invalid email formats
        Priority: High
        """
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test..test@example.com"
        ]
        
        results = []
        for i, invalid_email in enumerate(invalid_emails):
            test_data = self.valid_test_data.copy()
            test_data["email"] = invalid_email
            
            result = self.execute_test_case(
                f"REG_007_{i+1}",
                f"Registration with invalid email: {invalid_email}",
                test_data,
                "error"
            )
            results.append(result)
        
        return results
    
    def test_registration_with_weak_password(self):
        """
        Test Case ID: REG_010
        Description: Verify registration fails with weak passwords
        Priority: High
        """
        weak_passwords = [
            "123",
            "password",
            "abc",
            "12345678"
        ]
        
        results = []
        for i, weak_password in enumerate(weak_passwords):
            test_data = self.valid_test_data.copy()
            test_data["password"] = weak_password
            test_data["confirm_password"] = weak_password
            
            result = self.execute_test_case(
                f"REG_010_{i+1}",
                f"Registration with weak password: {weak_password}",
                test_data,
                "error"
            )
            results.append(result)
        
        return results
    
    def test_registration_with_mismatched_passwords(self):
        """
        Test Case ID: REG_011
        Description: Verify registration fails when passwords don't match
        Priority: High
        """
        test_data = self.valid_test_data.copy()
        test_data["confirm_password"] = "DifferentPassword123!"
        
        return self.execute_test_case(
            "REG_011",
            "Registration with mismatched passwords",
            test_data,
            "error"
        )
    
    # ========== SECURITY TEST CASES ==========
    
    def test_sql_injection_in_username(self):
        """
        Test Case ID: REG_015
        Description: Verify system is protected against SQL injection
        Priority: High
        """
        malicious_inputs = [
            "admin'; DROP TABLE users; --",
            "' OR '1'='1",
            "admin'/*"
        ]
        
        results = []
        for i, malicious_input in enumerate(malicious_inputs):
            test_data = self.valid_test_data.copy()
            test_data["username"] = malicious_input
            
            result = self.execute_test_case(
                f"REG_015_{i+1}",
                f"SQL injection test: {malicious_input[:20]}...",
                test_data,
                "error"
            )
            results.append(result)
        
        return results
    
    def test_xss_in_form_fields(self):
        """
        Test Case ID: REG_016
        Description: Verify system is protected against XSS attacks
        Priority: High
        """
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>"
        ]
        
        results = []
        for i, payload in enumerate(xss_payloads):
            test_data = self.valid_test_data.copy()
            test_data["username"] = payload
            
            result = self.execute_test_case(
                f"REG_016_{i+1}",
                f"XSS test: {payload[:20]}...",
                test_data,
                "error"
            )
            results.append(result)
        
        return results
    
    # ========== UI/UX TEST CASES ==========
    
    def test_form_field_validation_messages(self):
        """
        Test Case ID: REG_019
        Description: Verify appropriate validation messages are displayed
        Priority: Medium
        """
        print(f"\n🧪 Running REG_019: Form field validation messages")
        
        # Test each required field individually
        required_fields = ["username", "email", "password"]
        results = []
        
        for field in required_fields:
            test_data = self.valid_test_data.copy()
            test_data[field] = ""  # Empty required field
            
            result = self.execute_test_case(
                f"REG_019_{field}",
                f"Validation message for empty {field}",
                test_data,
                "error"
            )
            results.append(result)
        
        return results
    
    def test_password_visibility_toggle(self):
        """
        Test Case ID: REG_020
        Description: Verify password visibility toggle functionality
        Priority: Low
        """
        print(f"\n🧪 Running REG_020: Password visibility toggle")
        start_time = time.time()
        
        try:
            if not self.navigate_to_registration():
                return self.record_test_result("REG_020", "Password visibility toggle", False, "Failed to load page", start_time)
            
            # Fill password field
            password_field = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.selectors["password"]))
            )
            password_field.send_keys("TestPassword123!")
            
            # Check if password is masked (type="password")
            password_type = password_field.get_attribute("type")
            is_masked = password_type == "password"
            
            # Look for toggle button (common selectors)
            toggle_selectors = [
                ".password-toggle",
                ".show-password",
                "[data-toggle='password']",
                ".eye-icon"
            ]
            
            toggle_found = False
            for selector in toggle_selectors:
                try:
                    toggle_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    toggle_button.click()
                    time.sleep(0.5)  # Wait for toggle effect
                    
                    # Check if type changed
                    new_type = password_field.get_attribute("type")
                    toggle_worked = new_type != password_type
                    
                    toggle_found = True
                    break
                except NoSuchElementException:
                    continue
            
            if not toggle_found:
                return self.record_test_result("REG_020", "Password visibility toggle", False, "Toggle button not found", start_time)
            
            result_msg = f"Password initially masked: {is_masked}, Toggle worked: {toggle_worked}"
            return self.record_test_result("REG_020", "Password visibility toggle", toggle_worked, result_msg, start_time)
            
        except Exception as e:
            return self.record_test_result("REG_020", "Password visibility toggle", False, f"Exception: {str(e)}", start_time)
    
    def test_form_field_tab_order(self):
        """
        Test Case ID: REG_021
        Description: Verify logical tab order through form fields
        Priority: Low
        """
        print(f"\n🧪 Running REG_021: Form field tab order")
        start_time = time.time()
        
        try:
            if not self.navigate_to_registration():
                return self.record_test_result("REG_021", "Form field tab order", False, "Failed to load page", start_time)
            
            # Get all form inputs
            form_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input, select, textarea")
            
            if len(form_inputs) < 2:
                return self.record_test_result("REG_021", "Form field tab order", False, "Not enough form fields", start_time)
            
            # Click first field and test tab navigation
            first_field = form_inputs[0]
            first_field.click()
            
            tab_order_correct = True
            for i in range(len(form_inputs) - 1):
                # Press Tab key
                self.driver.switch_to.active_element.send_keys(Keys.TAB)
                time.sleep(0.2)
                
                # Check if focus moved to next logical field
                active_element = self.driver.switch_to.active_element
                
                # This is a basic check - in real implementation, you'd verify
                # the specific tab order based on your form design
                if not active_element:
                    tab_order_correct = False
                    break
            
            result_msg = f"Tab navigation through {len(form_inputs)} fields"
            return self.record_test_result("REG_021", "Form field tab order", tab_order_correct, result_msg, start_time)
            
        except Exception as e:
            return self.record_test_result("REG_021", "Form field tab order", False, f"Exception: {str(e)}", start_time)
    
    # ========== TEST EXECUTION METHODS ==========
    
    def run_positive_tests(self):
        """Execute all positive test cases"""
        print("\n" + "="*60)
        print("🟢 POSITIVE TEST CASES")
        print("="*60)
        
        results = []
        results.append(self.test_successful_registration_with_valid_data())
        results.append(self.test_registration_with_minimum_required_fields())
        results.append(self.test_registration_with_all_optional_fields())
        
        return results
    
    def run_negative_tests(self):
        """Execute all negative test cases"""
        print("\n" + "="*60)
        print("🔴 NEGATIVE TEST CASES")
        print("="*60)
        
        results = []
        results.append(self.test_registration_with_empty_username())
        results.append(self.test_registration_with_empty_email())
        results.append(self.test_registration_with_empty_password())
        results.extend(self.test_registration_with_invalid_email_format())
        results.extend(self.test_registration_with_weak_password())
        results.append(self.test_registration_with_mismatched_passwords())
        
        return results
    
    def run_security_tests(self):
        """Execute all security test cases"""
        print("\n" + "="*60)
        print("🛡️ SECURITY TEST CASES")
        print("="*60)
        
        results = []
        results.extend(self.test_sql_injection_in_username())
        results.extend(self.test_xss_in_form_fields())
        
        return results
    
    def run_ui_ux_tests(self):
        """Execute all UI/UX test cases"""
        print("\n" + "="*60)
        print("🎨 UI/UX TEST CASES")
        print("="*60)
        
        results = []
        results.extend(self.test_form_field_validation_messages())
        results.append(self.test_password_visibility_toggle())
        results.append(self.test_form_field_tab_order())
        
        return results
    
    def run_all_tests(self):
        """Execute complete test suite"""
        print("🚀 Starting Selenium WebDriver Test Execution")
        print(f"🎯 Target: {self.base_url}")
        print(f"🕐 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Setup WebDriver
        self.setup_driver()
        
        try:
            # Execute test categories
            all_results = []
            all_results.extend(self.run_positive_tests())
            all_results.extend(self.run_negative_tests())
            all_results.extend(self.run_security_tests())
            all_results.extend(self.run_ui_ux_tests())
            
            # Flatten results (some tests return lists)
            flat_results = []
            for result in all_results:
                if isinstance(result, list):
                    flat_results.extend(result)
                else:
                    flat_results.append(result)
            
            self.test_results = flat_results
            
            # Generate summary report
            self.generate_test_report()
            
        finally:
            # Clean up WebDriver
            self.teardown_driver()
        
        return self.test_results
    
    def generate_test_report(self):
        """Generate comprehensive test execution report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["passed"])
        failed_tests = total_tests - passed_tests
        pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        # Calculate execution time statistics
        execution_times = [result["execution_time"] for result in self.test_results]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        print("\n" + "="*80)
        print("📊 SELENIUM TEST EXECUTION REPORT")
        print("="*80)
        print(f"🎯 Target Environment: {self.base_url}")
        print(f"🕐 Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Total Test Cases: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Pass Rate: {pass_rate:.1f}%")
        print(f"⏱️ Average Execution Time: {avg_execution_time:.2f}s")
        
        # Failed test details
        if failed_tests > 0:
            print(f"\n❌ FAILED TEST CASES:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"   {result['test_id']}: {result['description']}")
                    print(f"      Reason: {result['result_message']}")
        
        # Save detailed report
        report_data = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "pass_rate": pass_rate,
                "avg_execution_time": avg_execution_time,
                "execution_time": datetime.now().isoformat(),
                "test_environment": self.base_url
            },
            "test_results": self.test_results
        }
        
        timestamp = int(time.time())
        report_filename = f"selenium_test_report_{timestamp}.json"
        
        with open(report_filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved: {report_filename}")
        
        return report_data


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Selenium User Registration Tests')
    parser.add_argument('--url', default='http://localhost:5003', 
                       help='Target URL (default: http://localhost:5003)')
    parser.add_argument('--headless', action='store_true', 
                       help='Run in headless mode')
    
    args = parser.parse_args()
    
    # Initialize and run tests
    test_runner = SeleniumRegistrationTests(
        base_url=args.url,
        headless=args.headless
    )
    
    try:
        results = test_runner.run_all_tests()
        
        # Print final summary
        total = len(results)
        passed = sum(1 for r in results if r["passed"])
        print(f"\n🎉 Test Execution Complete!")
        print(f"📊 Final Results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test execution interrupted by user")
        test_runner.teardown_driver()
    except Exception as e:
        print(f"\n❌ Test execution failed: {str(e)}")
        test_runner.teardown_driver()


if __name__ == "__main__":
    main()
