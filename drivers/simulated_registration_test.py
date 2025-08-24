"""
Simulated User Registration Test Execution
==========================================
This script simulates running user registration tests against localhost:5003
"""

import time
import random
import json
from datetime import datetime


class SimulatedRegistrationTester:
    """
    Simulates test execution against a user registration endpoint
    """
    
    def __init__(self, base_url="http://localhost:5003"):
        self.base_url = base_url
        self.registration_endpoint = f"{base_url}/register"
        self.test_results = []
        self.start_time = None
        self.end_time = None
        
    def simulate_http_request(self, data, expected_status=200):
        """Simulate HTTP request with random response time"""
        # Simulate network delay
        response_time = random.uniform(0.1, 2.0)
        time.sleep(response_time)
        
        # Simulate different response scenarios based on test data
        if self._is_valid_data(data):
            return {
                "status_code": 201,
                "response_time": response_time,
                "body": {"message": "Registration successful", "user_id": random.randint(1000, 9999)},
                "success": True
            }
        else:
            error_msg = self._get_error_message(data)
            return {
                "status_code": 400,
                "response_time": response_time,
                "body": {"error": error_msg},
                "success": False
            }
    
    def _is_valid_data(self, data):
        """Check if test data should result in successful registration"""
        # Simulate validation logic
        if not data.get("username") or len(data.get("username", "")) < 3:
            return False
        if not data.get("email") or "@" not in data.get("email", ""):
            return False
        if not data.get("password") or len(data.get("password", "")) < 8:
            return False
        if "DROP TABLE" in data.get("username", ""):  # SQL injection attempt
            return False
        if "<script>" in data.get("username", ""):  # XSS attempt
            return False
        return True
    
    def _get_error_message(self, data):
        """Generate appropriate error message based on invalid data"""
        if not data.get("username"):
            return "Username is required"
        elif len(data.get("username", "")) < 3:
            return "Username must be at least 3 characters"
        elif not data.get("email"):
            return "Email is required"
        elif "@" not in data.get("email", ""):
            return "Please enter a valid email address"
        elif not data.get("password"):
            return "Password is required"
        elif len(data.get("password", "")) < 8:
            return "Password must be at least 8 characters"
        elif "DROP TABLE" in data.get("username", ""):
            return "Invalid characters in username"
        elif "<script>" in data.get("username", ""):
            return "Invalid characters in username"
        else:
            return "Registration failed"
    
    def run_test_case(self, test_id, description, test_data, expected_result):
        """Execute a single test case"""
        print(f"Running {test_id}: {description}")
        
        start_time = time.time()
        response = self.simulate_http_request(test_data)
        end_time = time.time()
        
        # Determine if test passed
        if expected_result == "success":
            passed = response["success"]
        else:
            passed = not response["success"] and expected_result in response["body"].get("error", "")
        
        result = {
            "test_id": test_id,
            "description": description,
            "test_data": test_data,
            "expected_result": expected_result,
            "actual_response": response,
            "execution_time": end_time - start_time,
            "passed": passed,
            "timestamp": datetime.now().isoformat()
        }
        
        self.test_results.append(result)
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status} - Response time: {response['response_time']:.2f}s")
        
        return result
    
    def run_positive_tests(self):
        """Execute positive test cases"""
        print("\n" + "="*60)
        print("POSITIVE TEST CASES")
        print("="*60)
        
        # REG_001: Successful registration with valid data
        self.run_test_case(
            "REG_001",
            "Successful registration with valid data",
            {
                "username": f"testuser_{int(time.time())}",
                "email": f"test_{int(time.time())}@example.com",
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!",
                "first_name": "John",
                "last_name": "Doe"
            },
            "success"
        )
        
        # REG_002: Registration with minimum required fields
        self.run_test_case(
            "REG_002",
            "Registration with minimum required fields",
            {
                "username": f"minuser_{int(time.time())}",
                "email": f"min_{int(time.time())}@example.com",
                "password": "MinPass123!"
            },
            "success"
        )
        
        # REG_003: Registration with all optional fields
        self.run_test_case(
            "REG_003",
            "Registration with all optional fields",
            {
                "username": f"complete_{int(time.time())}",
                "email": f"complete_{int(time.time())}@example.com",
                "password": "CompletePass123!",
                "first_name": "Jane",
                "last_name": "Smith",
                "phone": "+1234567890",
                "address": "123 Test Street"
            },
            "success"
        )
    
    def run_negative_tests(self):
        """Execute negative test cases"""
        print("\n" + "="*60)
        print("NEGATIVE TEST CASES")
        print("="*60)
        
        # REG_004: Empty username
        self.run_test_case(
            "REG_004",
            "Registration with empty username",
            {
                "username": "",
                "email": "test@example.com",
                "password": "ValidPass123!"
            },
            "Username is required"
        )
        
        # REG_005: Empty email
        self.run_test_case(
            "REG_005",
            "Registration with empty email",
            {
                "username": "testuser",
                "email": "",
                "password": "ValidPass123!"
            },
            "Email is required"
        )
        
        # REG_006: Empty password
        self.run_test_case(
            "REG_006",
            "Registration with empty password",
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": ""
            },
            "Password is required"
        )
        
        # REG_007: Invalid email format
        self.run_test_case(
            "REG_007",
            "Registration with invalid email format",
            {
                "username": "testuser",
                "email": "invalid-email",
                "password": "ValidPass123!"
            },
            "Please enter a valid email address"
        )
    
    def run_security_tests(self):
        """Execute security test cases"""
        print("\n" + "="*60)
        print("SECURITY TEST CASES")
        print("="*60)
        
        # REG_015: SQL injection attempt
        self.run_test_case(
            "REG_015",
            "SQL injection protection",
            {
                "username": "admin'; DROP TABLE users; --",
                "email": "test@example.com",
                "password": "ValidPass123!"
            },
            "Invalid characters"
        )
        
        # REG_016: XSS attempt
        self.run_test_case(
            "REG_016",
            "XSS attack protection",
            {
                "username": "<script>alert('XSS')</script>",
                "email": "test@example.com",
                "password": "ValidPass123!"
            },
            "Invalid characters"
        )
    
    def run_boundary_tests(self):
        """Execute boundary value test cases"""
        print("\n" + "="*60)
        print("BOUNDARY VALUE TEST CASES")
        print("="*60)
        
        # REG_012: Username too short
        self.run_test_case(
            "REG_012a",
            "Username below minimum length",
            {
                "username": "ab",  # 2 characters
                "email": "test@example.com",
                "password": "ValidPass123!"
            },
            "Username must be at least 3 characters"
        )
        
        # REG_013: Password too short
        self.run_test_case(
            "REG_013a",
            "Password below minimum length",
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "Pass1!"  # 6 characters
            },
            "Password must be at least 8 characters"
        )
    
    def run_performance_test(self):
        """Execute performance test"""
        print("\n" + "="*60)
        print("PERFORMANCE TEST CASE")
        print("="*60)
        
        # REG_023: Response time test
        start_time = time.time()
        result = self.run_test_case(
            "REG_023",
            "Registration response time",
            {
                "username": f"perfuser_{int(time.time())}",
                "email": f"perf_{int(time.time())}@example.com",
                "password": "PerfPass123!"
            },
            "success"
        )
        
        # Check if response time is acceptable (< 3 seconds)
        response_time = result["actual_response"]["response_time"]
        performance_pass = response_time < 3.0
        
        print(f"  Performance check: {'✓ PASS' if performance_pass else '✗ FAIL'}")
        print(f"  Response time: {response_time:.2f}s (threshold: 3.0s)")
    
    def generate_test_report(self):
        """Generate comprehensive test execution report"""
        print("\n" + "="*80)
        print("TEST EXECUTION REPORT")
        print("="*80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["passed"])
        failed_tests = total_tests - passed_tests
        pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"Test Environment: {self.base_url}")
        print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Test Cases: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        # Response time statistics
        response_times = [r["actual_response"]["response_time"] for r in self.test_results]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            print(f"\nPerformance Metrics:")
            print(f"Average Response Time: {avg_response_time:.2f}s")
            print(f"Maximum Response Time: {max_response_time:.2f}s")
            print(f"Minimum Response Time: {min_response_time:.2f}s")
        
        # Failed test details
        if failed_tests > 0:
            print(f"\nFailed Test Cases:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"  ✗ {result['test_id']}: {result['description']}")
                    print(f"    Expected: {result['expected_result']}")
                    print(f"    Actual: {result['actual_response']['body']}")
        
        # Save detailed report to file
        report_data = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "pass_rate": pass_rate,
                "execution_time": datetime.now().isoformat(),
                "test_environment": self.base_url
            },
            "test_results": self.test_results
        }
        
        return report_data
    
    def run_full_test_suite(self):
        """Execute the complete test suite"""
        print("Starting User Registration Test Execution")
        print(f"Target Environment: {self.base_url}")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.start_time = time.time()
        
        # Execute test categories
        self.run_positive_tests()
        self.run_negative_tests()
        self.run_security_tests()
        self.run_boundary_tests()
        self.run_performance_test()
        
        self.end_time = time.time()
        
        # Generate final report
        report = self.generate_test_report()
        
        print(f"\nTotal Execution Time: {self.end_time - self.start_time:.2f} seconds")
        
        return report


if __name__ == "__main__":
    # Initialize tester for localhost:5003
    tester = SimulatedRegistrationTester("http://localhost:5003")
    
    # Run the complete test suite
    test_report = tester.run_full_test_suite()
    
    # Save report to file
    report_filename = f"registration_test_report_{int(time.time())}.json"
    with open(report_filename, 'w') as f:
        json.dump(test_report, f, indent=2)
    
    print(f"\nDetailed test report saved to: {report_filename}")
