#!/usr/bin/env python3
"""
Selenium Test Runner
===================
Execute Selenium WebDriver tests for user registration functionality
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['selenium', 'webdriver_manager']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "-r", "selenium_requirements.txt"
            ])
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    return True

def start_local_server():
    """Start a simple HTTP server for testing the sample form"""
    import http.server
    import socketserver
    import threading
    
    PORT = 5003
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' or self.path == '/register':
                self.path = '/sample_registration_form.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🌐 Starting test server at http://localhost:{PORT}")
            
            # Start server in background thread
            server_thread = threading.Thread(target=httpd.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            return httpd, PORT
    except OSError as e:
        print(f"❌ Failed to start server on port {PORT}: {e}")
        return None, None

def run_selenium_tests(headless=False, target_url=None):
    """Execute the Selenium test suite"""
    try:
        from selenium_registration_tests import SeleniumRegistrationTests
        
        # Use provided URL or default
        base_url = target_url or "http://localhost:5003"
        
        print(f"🚀 Initializing Selenium tests...")
        print(f"🎯 Target URL: {base_url}")
        print(f"🖥️ Headless mode: {headless}")
        
        # Create test runner
        test_runner = SeleniumRegistrationTests(
            base_url=base_url,
            headless=headless
        )
        
        # Execute tests
        results = test_runner.run_all_tests()
        
        return results
        
    except ImportError as e:
        print(f"❌ Failed to import test module: {e}")
        return None
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return None

def run_demo_tests():
    """Run a quick demo of key test cases"""
    print("🎬 Running Selenium Test Demo...")
    
    try:
        from selenium_registration_tests import SeleniumRegistrationTests
        
        # Initialize test runner
        test_runner = SeleniumRegistrationTests(
            base_url="http://localhost:5003",
            headless=False  # Show browser for demo
        )
        
        # Setup driver
        test_runner.setup_driver()
        
        try:
            print("\n📋 Demo Test Cases:")
            
            # Run a few key tests
            results = []
            
            # 1. Positive test
            print("\n1️⃣ Testing successful registration...")
            result = test_runner.test_successful_registration_with_valid_data()
            results.append(result)
            
            # 2. Negative test
            print("\n2️⃣ Testing empty username validation...")
            result = test_runner.test_registration_with_empty_username()
            results.append(result)
            
            # 3. Security test
            print("\n3️⃣ Testing SQL injection protection...")
            security_results = test_runner.test_sql_injection_in_username()
            results.extend(security_results)
            
            # 4. UI test
            print("\n4️⃣ Testing password visibility toggle...")
            result = test_runner.test_password_visibility_toggle()
            results.append(result)
            
            # Summary
            total = len(results)
            passed = sum(1 for r in results if r["passed"])
            
            print(f"\n🎉 Demo Complete!")
            print(f"📊 Results: {passed}/{total} tests passed")
            
            return results
            
        finally:
            test_runner.teardown_driver()
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return None

def main():
    """Main execution function"""
    print("🚀 Selenium WebDriver Test Runner")
    print("=" * 50)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check if we're in the right directory
    if not (current_dir / "selenium_registration_tests.py").exists():
        print("❌ selenium_registration_tests.py not found in current directory")
        print("💡 Please run this script from the /drivers directory")
        return
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        print("❌ Dependency check failed")
        return
    
    # Start local test server
    print("\n🌐 Starting local test server...")
    server, port = start_local_server()
    
    if not server:
        print("❌ Failed to start test server")
        print("💡 You can still run tests against an external URL")
        target_url = input("Enter target URL (or press Enter to skip): ").strip()
        if not target_url:
            return
    else:
        target_url = f"http://localhost:{port}"
        print(f"✅ Test server running at {target_url}")
        time.sleep(2)  # Give server time to start
    
    # Ask user for test mode
    print("\n🎯 Test Execution Options:")
    print("1. Run demo tests (recommended for first time)")
    print("2. Run full test suite")
    print("3. Run full test suite (headless)")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    try:
        if choice == "1":
            print("\n🎬 Starting demo tests...")
            results = run_demo_tests()
        elif choice == "2":
            print("\n🧪 Starting full test suite...")
            results = run_selenium_tests(headless=False, target_url=target_url)
        elif choice == "3":
            print("\n🧪 Starting full test suite (headless)...")
            results = run_selenium_tests(headless=True, target_url=target_url)
        else:
            print("❌ Invalid choice")
            return
        
        if results:
            total = len(results)
            passed = sum(1 for r in results if r["passed"])
            print(f"\n🎉 Test execution completed!")
            print(f"📊 Final results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        else:
            print("❌ No test results available")
            
    except KeyboardInterrupt:
        print("\n⚠️ Test execution interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        if server:
            print("\n🛑 Shutting down test server...")
            server.shutdown()

if __name__ == "__main__":
    main()
