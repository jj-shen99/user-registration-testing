"""
Fixed Test Results Dashboard
===========================
Creates comprehensive graphical dashboard for test results analysis
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import glob


class TestResultsDashboard:
    """
    Creates comprehensive test results dashboard
    """
    
    def __init__(self):
        self.test_data = None
        self.processed_data = {}
        self.load_test_data()
        self.process_data()
    
    def load_test_data(self):
        """Load test data from JSON report or use sample data"""
        # Try to find the most recent test report
        report_files = glob.glob("registration_test_report_*.json")
        
        if report_files:
            latest_report = max(report_files)
            print(f"📊 Loading test report: {latest_report}")
            try:
                with open(latest_report, 'r') as f:
                    self.test_data = json.load(f)
                print("✅ Successfully loaded test data")
                return
            except Exception as e:
                print(f"❌ Error loading report: {e}")
        
        print("📊 Using enhanced sample test data")
        self.create_enhanced_sample_data()
    
    def create_enhanced_sample_data(self):
        """Create comprehensive sample test data with proper categories"""
        self.test_data = {
            "summary": {
                "total_tests": 12,
                "passed": 12,
                "failed": 0,
                "pass_rate": 100.0,
                "execution_time": "2025-08-24T12:20:08.896020",
                "test_environment": "http://localhost:5003"
            },
            "test_results": [
                # Positive Tests
                {
                    "test_id": "REG_001",
                    "description": "Successful registration with valid data",
                    "passed": True,
                    "actual_response": {"response_time": 0.44, "status_code": 201},
                    "execution_time": 0.45,
                    "timestamp": "2025-08-24T12:19:53.645345"
                },
                {
                    "test_id": "REG_002", 
                    "description": "Registration with minimum required fields",
                    "passed": True,
                    "actual_response": {"response_time": 1.99, "status_code": 201},
                    "execution_time": 2.0,
                    "timestamp": "2025-08-24T12:19:55.645345"
                },
                {
                    "test_id": "REG_003",
                    "description": "Registration with all optional fields",
                    "passed": True,
                    "actual_response": {"response_time": 1.94, "status_code": 201},
                    "execution_time": 1.95,
                    "timestamp": "2025-08-24T12:19:57.645345"
                },
                # Negative Tests
                {
                    "test_id": "REG_004",
                    "description": "Registration with empty username",
                    "passed": True,
                    "actual_response": {"response_time": 0.98, "status_code": 400},
                    "execution_time": 0.99,
                    "timestamp": "2025-08-24T12:19:59.645345"
                },
                {
                    "test_id": "REG_005",
                    "description": "Registration with empty email",
                    "passed": True,
                    "actual_response": {"response_time": 0.20, "status_code": 400},
                    "execution_time": 0.21,
                    "timestamp": "2025-08-24T12:20:01.645345"
                },
                {
                    "test_id": "REG_006",
                    "description": "Registration with empty password",
                    "passed": True,
                    "actual_response": {"response_time": 1.40, "status_code": 400},
                    "execution_time": 1.41,
                    "timestamp": "2025-08-24T12:20:03.645345"
                },
                {
                    "test_id": "REG_007",
                    "description": "Registration with invalid email format",
                    "passed": True,
                    "actual_response": {"response_time": 1.70, "status_code": 400},
                    "execution_time": 1.71,
                    "timestamp": "2025-08-24T12:20:05.645345"
                },
                # Security Tests
                {
                    "test_id": "REG_015",
                    "description": "SQL injection protection",
                    "passed": True,
                    "actual_response": {"response_time": 1.71, "status_code": 400},
                    "execution_time": 1.72,
                    "timestamp": "2025-08-24T12:20:07.645345"
                },
                {
                    "test_id": "REG_016",
                    "description": "XSS attack protection",
                    "passed": True,
                    "actual_response": {"response_time": 1.62, "status_code": 400},
                    "execution_time": 1.63,
                    "timestamp": "2025-08-24T12:20:09.645345"
                },
                # Boundary Tests
                {
                    "test_id": "REG_012a",
                    "description": "Username below minimum length",
                    "passed": True,
                    "actual_response": {"response_time": 1.10, "status_code": 400},
                    "execution_time": 1.11,
                    "timestamp": "2025-08-24T12:20:11.645345"
                },
                {
                    "test_id": "REG_013a",
                    "description": "Password below minimum length",
                    "passed": True,
                    "actual_response": {"response_time": 1.26, "status_code": 400},
                    "execution_time": 1.27,
                    "timestamp": "2025-08-24T12:20:13.645345"
                },
                # Performance Test
                {
                    "test_id": "REG_023",
                    "description": "Registration response time",
                    "passed": True,
                    "actual_response": {"response_time": 1.31, "status_code": 201},
                    "execution_time": 1.32,
                    "timestamp": "2025-08-24T12:20:15.645345"
                }
            ]
        }
    
    def categorize_test(self, test_id):
        """Categorize test based on test ID prefix"""
        if test_id.startswith("REG_001") or test_id.startswith("REG_002") or test_id.startswith("REG_003"):
            return "Positive"
        elif test_id.startswith("REG_004") or test_id.startswith("REG_005") or test_id.startswith("REG_006") or test_id.startswith("REG_007"):
            return "Negative"
        elif test_id.startswith("REG_015") or test_id.startswith("REG_016"):
            return "Security"
        elif test_id.startswith("REG_012") or test_id.startswith("REG_013"):
            return "Boundary"
        elif test_id.startswith("REG_023") or test_id.startswith("REG_024"):
            return "Performance"
        else:
            return "Other"
    
    def get_priority(self, test_id):
        """Determine priority based on test ID"""
        if test_id.startswith(("REG_001", "REG_002", "REG_004", "REG_005", "REG_006", "REG_007", "REG_015", "REG_016")):
            return "High"
        elif test_id.startswith(("REG_003", "REG_012", "REG_013", "REG_023")):
            return "Medium"
        else:
            return "Low"
    
    def process_data(self):
        """Process raw test data for analysis"""
        results = self.test_data["test_results"]
        
        # Initialize data structures
        self.processed_data = {
            "categories": {},
            "priorities": {},
            "response_times": [],
            "status_codes": {},
            "timeline_data": [],
            "performance_metrics": {}
        }
        
        # Process each test result
        for i, test in enumerate(results):
            # Categorize test
            category = self.categorize_test(test["test_id"])
            priority = self.get_priority(test["test_id"])
            
            # Extract metrics
            response_time = test["actual_response"]["response_time"]
            status_code = test["actual_response"]["status_code"]
            passed = test["passed"]
            
            # Update categories
            if category not in self.processed_data["categories"]:
                self.processed_data["categories"][category] = {
                    "count": 0, "passed": 0, "response_times": []
                }
            self.processed_data["categories"][category]["count"] += 1
            if passed:
                self.processed_data["categories"][category]["passed"] += 1
            self.processed_data["categories"][category]["response_times"].append(response_time)
            
            # Update priorities
            if priority not in self.processed_data["priorities"]:
                self.processed_data["priorities"][priority] = 0
            self.processed_data["priorities"][priority] += 1
            
            # Update other metrics
            self.processed_data["response_times"].append(response_time)
            
            if status_code not in self.processed_data["status_codes"]:
                self.processed_data["status_codes"][status_code] = 0
            self.processed_data["status_codes"][status_code] += 1
            
            # Timeline data
            self.processed_data["timeline_data"].append({
                "order": i,
                "test_id": test["test_id"],
                "response_time": response_time,
                "passed": passed,
                "category": category
            })
        
        # Calculate performance metrics
        rt = self.processed_data["response_times"]
        self.processed_data["performance_metrics"] = {
            "avg_response_time": np.mean(rt),
            "min_response_time": np.min(rt),
            "max_response_time": np.max(rt),
            "std_response_time": np.std(rt),
            "under_threshold": sum(1 for t in rt if t < 3.0),
            "total_tests": len(rt)
        }
    
    def create_dashboard(self):
        """Create comprehensive dashboard visualization"""
        # Set up the figure
        fig = plt.figure(figsize=(20, 16))
        fig.suptitle('🚀 User Registration Test Results Dashboard\n🎯 Target: localhost:5003', 
                     fontsize=24, fontweight='bold', y=0.98)
        
        summary = self.test_data["summary"]
        categories = self.processed_data["categories"]
        priorities = self.processed_data["priorities"]
        response_times = self.processed_data["response_times"]
        status_codes = self.processed_data["status_codes"]
        timeline = self.processed_data["timeline_data"]
        perf = self.processed_data["performance_metrics"]
        
        # 1. Overall Pass/Fail Results (Top Left)
        ax1 = plt.subplot(3, 4, 1)
        labels = ['✅ Passed', '❌ Failed']
        sizes = [summary["passed"], summary["failed"]]
        colors = ['#2ecc71', '#e74c3c']
        explode = (0.1, 0) if summary["failed"] == 0 else (0, 0.1)
        
        wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                          startangle=90, explode=explode, shadow=True)
        ax1.set_title(f'📊 Overall Results\n{summary["total_tests"]} Total Tests', 
                     fontweight='bold', fontsize=12)
        
        # 2. Test Categories (Top Center-Left)
        ax2 = plt.subplot(3, 4, 2)
        cat_names = list(categories.keys())
        cat_counts = [categories[cat]["count"] for cat in cat_names]
        colors_cat = plt.cm.Set3(np.linspace(0, 1, len(cat_names)))
        
        bars = ax2.bar(cat_names, cat_counts, color=colors_cat, edgecolor='black', linewidth=1)
        ax2.set_title('📂 Tests by Category', fontweight='bold', fontsize=12)
        ax2.set_ylabel('Number of Tests')
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Response Time Distribution (Top Center-Right)
        ax3 = plt.subplot(3, 4, 3)
        n, bins, patches = ax3.hist(response_times, bins=8, color='skyblue', alpha=0.8, 
                                   edgecolor='black', linewidth=1)
        
        # Color bars based on performance
        for i, patch in enumerate(patches):
            if bins[i] > 2.0:
                patch.set_facecolor('#e74c3c')  # Red for slow
            elif bins[i] > 1.0:
                patch.set_facecolor('#f39c12')  # Orange for medium
            else:
                patch.set_facecolor('#2ecc71')  # Green for fast
        
        ax3.axvline(perf["avg_response_time"], color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {perf["avg_response_time"]:.2f}s')
        ax3.axvline(3.0, color='orange', linestyle='--', linewidth=2,
                   label='Threshold: 3.0s')
        ax3.set_title('⏱️ Response Time Distribution', fontweight='bold', fontsize=12)
        ax3.set_xlabel('Response Time (seconds)')
        ax3.set_ylabel('Frequency')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Priority Distribution (Top Right)
        ax4 = plt.subplot(3, 4, 4)
        pri_names = list(priorities.keys())
        pri_counts = list(priorities.values())
        colors_pri = {'High': '#e74c3c', 'Medium': '#f39c12', 'Low': '#2ecc71'}
        bar_colors = [colors_pri.get(p, '#95a5a6') for p in pri_names]
        
        bars = ax4.bar(pri_names, pri_counts, color=bar_colors, edgecolor='black', linewidth=1)
        ax4.set_title('🎯 Tests by Priority', fontweight='bold', fontsize=12)
        ax4.set_ylabel('Number of Tests')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # 5. Response Time by Category (Middle Left)
        ax5 = plt.subplot(3, 4, 5)
        cat_means = [np.mean(categories[cat]["response_times"]) for cat in cat_names]
        cat_stds = [np.std(categories[cat]["response_times"]) for cat in cat_names]
        
        bars = ax5.bar(cat_names, cat_means, yerr=cat_stds, capsize=5, 
                      color=colors_cat, alpha=0.8, edgecolor='black', linewidth=1)
        ax5.set_title('📈 Avg Response Time by Category', fontweight='bold', fontsize=12)
        ax5.set_ylabel('Response Time (seconds)')
        plt.setp(ax5.get_xticklabels(), rotation=45, ha='right')
        ax5.grid(True, alpha=0.3)
        
        # 6. Test Timeline (Middle Center)
        ax6 = plt.subplot(3, 4, (6, 7))
        timeline_colors = ['#2ecc71' if item["passed"] else '#e74c3c' for item in timeline]
        timeline_rt = [item["response_time"] for item in timeline]
        timeline_order = [item["order"] for item in timeline]
        
        scatter = ax6.scatter(timeline_order, timeline_rt, c=timeline_colors, s=120, 
                             alpha=0.8, edgecolors='black', linewidth=1)
        
        # Add test ID labels for key points
        for item in timeline:
            if item["response_time"] > 1.8 or item["response_time"] < 0.3:
                ax6.annotate(item["test_id"], (item["order"], item["response_time"]), 
                            xytext=(5, 5), textcoords='offset points', 
                            fontsize=8, rotation=45)
        
        ax6.axhline(y=3.0, color='orange', linestyle='--', alpha=0.7, linewidth=2,
                   label='Performance Threshold (3s)')
        ax6.axhline(y=perf["avg_response_time"], color='red', linestyle=':', alpha=0.7, linewidth=2,
                   label=f'Average ({perf["avg_response_time"]:.2f}s)')
        ax6.set_title('📅 Test Execution Timeline', fontweight='bold', fontsize=12)
        ax6.set_xlabel('Test Execution Order')
        ax6.set_ylabel('Response Time (seconds)')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        
        # 7. Status Code Distribution (Middle Right)
        ax7 = plt.subplot(3, 4, 8)
        status_names = [str(code) for code in status_codes.keys()]
        status_counts = list(status_codes.values())
        status_colors = ['#2ecc71' if int(code) == 201 else '#e74c3c' for code in status_names]
        
        bars = ax7.bar(status_names, status_counts, color=status_colors, 
                      edgecolor='black', linewidth=1)
        ax7.set_title('🌐 HTTP Status Codes', fontweight='bold', fontsize=12)
        ax7.set_ylabel('Count')
        ax7.set_xlabel('Status Code')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax7.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # 8. Performance Metrics (Bottom Left)
        ax8 = plt.subplot(3, 4, 9)
        ax8.axis('off')
        
        metrics_text = f"""📈 PERFORMANCE SUMMARY
        
📊 Total Tests: {summary['total_tests']}
✅ Pass Rate: {summary['pass_rate']:.1f}%
⏱️ Avg Response: {perf['avg_response_time']:.2f}s
🚀 Fastest: {perf['min_response_time']:.2f}s
🐌 Slowest: {perf['max_response_time']:.2f}s
🎯 Under 3s: {perf['under_threshold']}/{perf['total_tests']}
📊 Std Dev: {perf['std_response_time']:.2f}s"""
        
        ax8.text(0.05, 0.95, metrics_text, fontsize=11, fontweight='bold',
                verticalalignment='top', transform=ax8.transAxes,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
        
        # 9. Category Performance Matrix (Bottom Center)
        ax9 = plt.subplot(3, 4, 10)
        
        # Create performance indicators
        quality_labels = ['Security\nTests', 'High Priority\nTests', 'Fast Tests\n(<1s)', 'All Passed']
        security_count = categories.get("Security", {"count": 0})["count"]
        high_priority = priorities.get("High", 0)
        fast_tests = sum(1 for rt in response_times if rt < 1.0)
        all_passed = summary["passed"]
        
        quality_values = [security_count, high_priority, fast_tests, all_passed]
        quality_colors = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
        
        bars = ax9.bar(quality_labels, quality_values, color=quality_colors, 
                      alpha=0.8, edgecolor='black', linewidth=1)
        ax9.set_title('🛡️ Quality Indicators', fontweight='bold', fontsize=12)
        ax9.set_ylabel('Count')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax9.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # 10. Category Pass Rates (Bottom Center-Right)
        ax10 = plt.subplot(3, 4, 11)
        
        cat_pass_rates = []
        cat_labels = []
        for cat, data in categories.items():
            if data["count"] > 0:
                pass_rate = (data["passed"] / data["count"]) * 100
                cat_pass_rates.append(pass_rate)
                cat_labels.append(cat)
        
        if cat_pass_rates:
            bars = ax10.bar(cat_labels, cat_pass_rates, 
                           color=['#2ecc71' if rate == 100 else '#f39c12' for rate in cat_pass_rates],
                           edgecolor='black', linewidth=1)
            ax10.set_title('📊 Pass Rate by Category', fontweight='bold', fontsize=12)
            ax10.set_ylabel('Pass Rate (%)')
            ax10.set_ylim(0, 105)
            plt.setp(ax10.get_xticklabels(), rotation=45, ha='right')
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax10.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{height:.0f}%', ha='center', va='bottom', fontweight='bold')
        
        # 11. Summary Table (Bottom Right)
        ax11 = plt.subplot(3, 4, 12)
        ax11.axis('off')
        
        # Create summary table data
        table_data = []
        for cat, data in categories.items():
            if data["count"] > 0:
                avg_time = np.mean(data["response_times"])
                pass_rate = (data["passed"] / data["count"]) * 100
                table_data.append([cat, data["count"], f'{pass_rate:.0f}%', f'{avg_time:.2f}s'])
        
        if table_data:
            table = ax11.table(cellText=table_data,
                              colLabels=['Category', 'Tests', 'Pass%', 'Avg Time'],
                              cellLoc='center',
                              loc='center',
                              colWidths=[0.3, 0.2, 0.2, 0.25])
            
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 2.5)
            ax11.set_title('📋 Category Summary', fontweight='bold', fontsize=12, pad=20)
            
            # Style the table
            for i in range(len(table_data) + 1):
                for j in range(4):
                    cell = table[(i, j)]
                    if i == 0:  # Header row
                        cell.set_facecolor('#3498db')
                        cell.set_text_props(weight='bold', color='white')
                    else:
                        cell.set_facecolor('#ecf0f1' if i % 2 == 0 else 'white')
        
        plt.tight_layout()
        return fig
    
    def save_dashboard(self):
        """Save dashboard in multiple formats"""
        fig = self.create_dashboard()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save PNG
        png_filename = f'test_dashboard_{timestamp}.png'
        fig.savefig(png_filename, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"✅ Dashboard saved: {png_filename}")
        
        # Save PDF
        pdf_filename = f'test_dashboard_{timestamp}.pdf'
        fig.savefig(pdf_filename, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"✅ PDF saved: {pdf_filename}")
        
        return fig, png_filename, pdf_filename
    
    def print_summary(self):
        """Print comprehensive test summary"""
        summary = self.test_data["summary"]
        perf = self.processed_data["performance_metrics"]
        categories = self.processed_data["categories"]
        
        print("\n" + "="*80)
        print("🚀 TEST RESULTS DASHBOARD SUMMARY")
        print("="*80)
        print(f"🎯 Target: {summary['test_environment']}")
        print(f"📅 Execution: {summary['execution_time']}")
        print(f"📊 Results: {summary['passed']}/{summary['total_tests']} passed ({summary['pass_rate']:.1f}%)")
        
        print(f"\n⏱️ PERFORMANCE:")
        print(f"   Average: {perf['avg_response_time']:.2f}s")
        print(f"   Range: {perf['min_response_time']:.2f}s - {perf['max_response_time']:.2f}s")
        print(f"   Under 3s: {perf['under_threshold']}/{perf['total_tests']} tests")
        
        print(f"\n📂 CATEGORIES:")
        for cat, data in categories.items():
            avg_time = np.mean(data["response_times"])
            pass_rate = (data["passed"] / data["count"]) * 100
            print(f"   {cat}: {data['count']} tests, {pass_rate:.0f}% pass, {avg_time:.2f}s avg")


def main():
    """Main execution function"""
    print("🚀 Generating Test Results Dashboard...")
    
    # Create dashboard
    dashboard = TestResultsDashboard()
    
    # Print summary
    dashboard.print_summary()
    
    # Generate and save dashboard
    fig, png_file, pdf_file = dashboard.save_dashboard()
    
    print(f"\n🎉 Dashboard Complete!")
    print(f"📁 Files: {png_file}, {pdf_file}")
    
    # Show dashboard
    plt.show()


if __name__ == "__main__":
    main()
