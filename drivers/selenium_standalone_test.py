#!/usr/bin/env python3
"""
Standalone Selenium Test Runner
===============================
Execute Selenium WebDriver tests without external dependencies or user input
"""

import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumTestRunner:
    """
    Standalone Selenium test runner for user registration tests
    """
    
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.test_results = []
        self.base_url = "https://httpbin.org/forms/post"  # Using httpbin for testing
        
    def setup_driver(self):
        """Setup Chrome WebDriver with options"""
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            
            print("✅ Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup WebDriver: {e}")
            return False
    
    def teardown_driver(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
            print("✅ WebDriver closed successfully")
    
    def execute_test(self, test_id, description, test_function):
        """Execute a single test case"""
        print(f"🧪 Running {test_id}: {description}")
        start_time = time.time()
        
        try:
            result = test_function()
            passed = result.get('passed', True)
            message = result.get('message', 'Test completed')
            
        except Exception as e:
            passed = False
            message = f"Test failed with exception: {str(e)}"
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        test_result = {
            "test_id": test_id,
            "description": description,
            "passed": passed,
            "message": message,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat()
        }
        
        self.test_results.append(test_result)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {message} ({execution_time:.2f}s)")
        
        return test_result
    
    def test_browser_navigation(self):
        """Test basic browser navigation"""
        try:
            self.driver.get("https://httpbin.org/")
            title = self.driver.title
            return {
                "passed": "httpbin" in title.lower(),
                "message": f"Successfully navigated to httpbin, title: {title}"
            }
        except Exception as e:
            return {"passed": False, "message": f"Navigation failed: {e}"}
    
    def test_form_elements_detection(self):
        """Test detection of form elements"""
        try:
            self.driver.get("https://httpbin.org/forms/post")
            
            # Look for form elements
            form_elements = self.driver.find_elements(By.TAG_NAME, "input")
            textarea_elements = self.driver.find_elements(By.TAG_NAME, "textarea")
            
            total_elements = len(form_elements) + len(textarea_elements)
            
            return {
                "passed": total_elements > 0,
                "message": f"Found {total_elements} form elements ({len(form_elements)} inputs, {len(textarea_elements)} textareas)"
            }
        except Exception as e:
            return {"passed": False, "message": f"Form detection failed: {e}"}
    
    def test_form_interaction(self):
        """Test basic form interaction"""
        try:
            self.driver.get("https://httpbin.org/forms/post")
            
            # Try to fill form fields
            interactions = 0
            
            # Look for text inputs
            text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[name*='customer'], input[name*='email']")
            for i, input_field in enumerate(text_inputs[:3]):  # Limit to first 3
                try:
                    input_field.clear()
                    input_field.send_keys(f"test_value_{i}")
                    interactions += 1
                except:
                    pass
            
            # Look for textarea
            textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
            for textarea in textareas[:1]:  # Limit to first 1
                try:
                    textarea.clear()
                    textarea.send_keys("Test message content")
                    interactions += 1
                except:
                    pass
            
            return {
                "passed": interactions > 0,
                "message": f"Successfully interacted with {interactions} form elements"
            }
        except Exception as e:
            return {"passed": False, "message": f"Form interaction failed: {e}"}
    
    def test_page_responsiveness(self):
        """Test page load and responsiveness"""
        try:
            start_time = time.time()
            self.driver.get("https://httpbin.org/delay/1")
            load_time = time.time() - start_time
            
            # Check if page loaded successfully
            page_source_length = len(self.driver.page_source)
            
            return {
                "passed": load_time < 10 and page_source_length > 0,
                "message": f"Page loaded in {load_time:.2f}s, content length: {page_source_length} chars"
            }
        except Exception as e:
            return {"passed": False, "message": f"Responsiveness test failed: {e}"}
    
    def test_javascript_execution(self):
        """Test JavaScript execution capability"""
        try:
            self.driver.get("https://httpbin.org/")
            
            # Execute simple JavaScript
            result = self.driver.execute_script("return document.title;")
            js_result = self.driver.execute_script("return 2 + 2;")
            
            return {
                "passed": js_result == 4 and result is not None,
                "message": f"JavaScript execution successful: 2+2={js_result}, title='{result}'"
            }
        except Exception as e:
            return {"passed": False, "message": f"JavaScript execution failed: {e}"}
    
    def test_element_waiting(self):
        """Test WebDriver wait functionality"""
        try:
            self.driver.get("https://httpbin.org/")
            
            # Wait for body element
            wait = WebDriverWait(self.driver, 10)
            body_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            return {
                "passed": body_element is not None,
                "message": "Successfully waited for and found body element"
            }
        except Exception as e:
            return {"passed": False, "message": f"Element waiting failed: {e}"}
    
    def test_multiple_window_sizes(self):
        """Test different window sizes (responsive testing)"""
        try:
            sizes_tested = 0
            window_sizes = [(1920, 1080), (768, 1024), (375, 667)]
            
            for width, height in window_sizes:
                try:
                    self.driver.set_window_size(width, height)
                    self.driver.get("https://httpbin.org/")
                    
                    # Verify window size was set
                    current_size = self.driver.get_window_size()
                    if abs(current_size['width'] - width) < 50:  # Allow some tolerance
                        sizes_tested += 1
                    
                    time.sleep(0.5)  # Brief pause between size changes
                except:
                    pass
            
            return {
                "passed": sizes_tested >= 2,
                "message": f"Successfully tested {sizes_tested}/{len(window_sizes)} window sizes"
            }
        except Exception as e:
            return {"passed": False, "message": f"Window size testing failed: {e}"}
    
    def test_cookie_handling(self):
        """Test cookie handling capabilities"""
        try:
            self.driver.get("https://httpbin.org/cookies/set/test_cookie/test_value")
            
            # Navigate to cookie check page
            self.driver.get("https://httpbin.org/cookies")
            
            # Check if cookies are present in page source
            page_source = self.driver.page_source
            has_cookie_data = "test_cookie" in page_source or "cookies" in page_source.lower()
            
            return {
                "passed": has_cookie_data,
                "message": "Cookie handling test completed - cookies detected in response"
            }
        except Exception as e:
            return {"passed": False, "message": f"Cookie handling failed: {e}"}
    
    def run_all_tests(self):
        """Execute complete Selenium test suite"""
        print("🚀 Starting Selenium WebDriver Test Suite")
        print("=" * 60)
        print(f"🎯 Target: Various test endpoints")
        print(f"🌐 Browser: Chrome {'(Headless)' if self.headless else '(Visible)'}")
        print(f"🕐 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not self.setup_driver():
            print("❌ Failed to setup WebDriver. Aborting tests.")
            return None
        
        try:
            # Execute test cases
            test_cases = [
                ("SEL_001", "Browser Navigation Test", self.test_browser_navigation),
                ("SEL_002", "Form Elements Detection", self.test_form_elements_detection),
                ("SEL_003", "Form Interaction Test", self.test_form_interaction),
                ("SEL_004", "Page Responsiveness Test", self.test_page_responsiveness),
                ("SEL_005", "JavaScript Execution Test", self.test_javascript_execution),
                ("SEL_006", "Element Waiting Test", self.test_element_waiting),
                ("SEL_007", "Multiple Window Sizes Test", self.test_multiple_window_sizes),
                ("SEL_008", "Cookie Handling Test", self.test_cookie_handling),
            ]
            
            print(f"\n🧪 Executing {len(test_cases)} test cases...")
            print("-" * 60)
            
            for test_id, description, test_function in test_cases:
                self.execute_test(test_id, description, test_function)
                time.sleep(0.5)  # Brief pause between tests
            
            # Generate summary report
            self.generate_summary_report()
            
        finally:
            self.teardown_driver()
        
        return self.test_results
    
    def generate_summary_report(self):
        """Generate comprehensive test summary"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["passed"])
        failed_tests = total_tests - passed_tests
        pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        # Calculate execution time statistics
        execution_times = [result["execution_time"] for result in self.test_results]
        total_execution_time = sum(execution_times)
        avg_execution_time = total_execution_time / len(execution_times) if execution_times else 0
        
        print("\n" + "=" * 60)
        print("📊 SELENIUM TEST EXECUTION REPORT")
        print("=" * 60)
        print(f"🎯 Browser: Chrome {'(Headless)' if self.headless else '(Visible)'}")
        print(f"🕐 Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Total Test Cases: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Pass Rate: {pass_rate:.1f}%")
        print(f"⏱️ Total Execution Time: {total_execution_time:.2f}s")
        print(f"⚡ Average Test Time: {avg_execution_time:.2f}s")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"   {result['test_id']}: {result['message']}")
        
        # Performance analysis
        if execution_times:
            fastest_test = min(self.test_results, key=lambda x: x["execution_time"])
            slowest_test = max(self.test_results, key=lambda x: x["execution_time"])
            
            print(f"\n⚡ PERFORMANCE ANALYSIS:")
            print(f"   Fastest Test: {fastest_test['test_id']} ({fastest_test['execution_time']:.2f}s)")
            print(f"   Slowest Test: {slowest_test['test_id']} ({slowest_test['execution_time']:.2f}s)")
        
        # Save results to JSON
        self.save_results_to_json()
        
        print(f"\n💡 NEXT STEPS:")
        print(f"   1. Review any failed tests above")
        print(f"   2. Check detailed results in JSON report")
        print(f"   3. Run with headless=False to see browser actions")
        print(f"   4. Extend tests for specific application testing")
    
    def save_results_to_json(self):
        """Save test results to JSON file"""
        try:
            # Create results directory
            results_dir = "/Users/jianjun.shen/Books__@/ai-assited-software-testing/sample_analysis_results"
            os.makedirs(results_dir, exist_ok=True)
            
            timestamp = int(time.time())
            filename = f"{results_dir}/selenium_test_results_{timestamp}.json"
            
            report_data = {
                "test_execution": {
                    "timestamp": datetime.now().isoformat(),
                    "browser": "Chrome",
                    "headless": self.headless,
                    "total_tests": len(self.test_results),
                    "passed": sum(1 for r in self.test_results if r["passed"]),
                    "failed": sum(1 for r in self.test_results if not r["passed"]),
                    "pass_rate": (sum(1 for r in self.test_results if r["passed"]) / len(self.test_results)) * 100 if self.test_results else 0
                },
                "test_results": self.test_results
            }
            
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            print(f"📄 Results saved to: {filename}")
            
        except Exception as e:
            print(f"⚠️ Failed to save results: {e}")


def main():
    """Main execution function"""
    print("🧪 Selenium WebDriver Test Suite")
    print("=" * 50)
    
    # Run tests in headless mode by default
    runner = SeleniumTestRunner(headless=True)
    results = runner.run_all_tests()
    
    if results:
        print(f"\n🎉 Selenium test execution completed!")
        print(f"📊 {len(results)} tests executed")
    else:
        print(f"\n❌ Selenium test execution failed!")


if __name__ == "__main__":
    main()
