"""
Test Results Dashboard Generator
===============================
Creates interactive graphical dashboard for user registration test results analysis
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.offline as pyo


class TestResultsDashboard:
    """
    Generates comprehensive graphical dashboard for test results analysis
    """
    
    def __init__(self, json_report_file=None):
        self.json_report_file = json_report_file
        self.test_data = None
        self.df = None
        
        # Set up styling
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        if json_report_file:
            self.load_test_data()
        else:
            self.generate_sample_data()
    
    def load_test_data(self):
        """Load test data from JSON report file"""
        try:
            with open(self.json_report_file, 'r') as f:
                self.test_data = json.load(f)
            self.create_dataframe()
        except FileNotFoundError:
            print(f"Report file {self.json_report_file} not found. Using sample data.")
            self.generate_sample_data()
    
    def generate_sample_data(self):
        """Generate sample test data for demonstration"""
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
                {
                    "test_id": "REG_001",
                    "description": "Successful registration with valid data",
                    "category": "Positive",
                    "priority": "High",
                    "actual_response": {"response_time": 0.44, "status_code": 201},
                    "passed": True,
                    "execution_time": 0.45
                },
                {
                    "test_id": "REG_002", 
                    "description": "Registration with minimum required fields",
                    "category": "Positive",
                    "priority": "High",
                    "actual_response": {"response_time": 1.99, "status_code": 201},
                    "passed": True,
                    "execution_time": 2.0
                },
                {
                    "test_id": "REG_003",
                    "description": "Registration with all optional fields",
                    "category": "Positive", 
                    "priority": "Medium",
                    "actual_response": {"response_time": 1.94, "status_code": 201},
                    "passed": True,
                    "execution_time": 1.95
                },
                {
                    "test_id": "REG_004",
                    "description": "Registration with empty username",
                    "category": "Negative",
                    "priority": "High",
                    "actual_response": {"response_time": 0.98, "status_code": 400},
                    "passed": True,
                    "execution_time": 0.99
                },
                {
                    "test_id": "REG_005",
                    "description": "Registration with empty email",
                    "category": "Negative",
                    "priority": "High", 
                    "actual_response": {"response_time": 0.20, "status_code": 400},
                    "passed": True,
                    "execution_time": 0.21
                },
                {
                    "test_id": "REG_006",
                    "description": "Registration with empty password",
                    "category": "Negative",
                    "priority": "High",
                    "actual_response": {"response_time": 1.40, "status_code": 400},
                    "passed": True,
                    "execution_time": 1.41
                },
                {
                    "test_id": "REG_007",
                    "description": "Registration with invalid email format",
                    "category": "Negative",
                    "priority": "High",
                    "actual_response": {"response_time": 1.70, "status_code": 400},
                    "passed": True,
                    "execution_time": 1.71
                },
                {
                    "test_id": "REG_015",
                    "description": "SQL injection protection",
                    "category": "Security",
                    "priority": "High",
                    "actual_response": {"response_time": 1.71, "status_code": 400},
                    "passed": True,
                    "execution_time": 1.72
                },
                {
                    "test_id": "REG_016",
                    "description": "XSS attack protection",
                    "category": "Security",
                    "priority": "High",
                    "actual_response": {"response_time": 1.62, "status_code": 400},
                    "passed": True,
                    "execution_time": 1.63
                },
                {
                    "test_id": "REG_012a",
                    "description": "Username below minimum length",
                    "category": "Boundary",
                    "priority": "Medium",
                    "actual_response": {"response_time": 1.10, "status_code": 400},
                    "passed": True,
                    "execution_time": 1.11
                },
                {
                    "test_id": "REG_013a",
                    "description": "Password below minimum length", 
                    "category": "Boundary",
                    "priority": "Medium",
                    "actual_response": {"response_time": 1.26, "status_code": 400},
                    "passed": True,
                    "execution_time": 1.27
                },
                {
                    "test_id": "REG_023",
                    "description": "Registration response time",
                    "category": "Performance",
                    "priority": "Medium",
                    "actual_response": {"response_time": 1.31, "status_code": 201},
                    "passed": True,
                    "execution_time": 1.32
                }
            ]
        }
        self.create_dataframe()
    
    def create_dataframe(self):
        """Convert test results to pandas DataFrame for easier analysis"""
        results = []
        for test in self.test_data["test_results"]:
            result = {
                "test_id": test["test_id"],
                "description": test["description"],
                "category": test.get("category", self.categorize_test(test["test_id"])),
                "priority": test.get("priority", "Medium"),
                "passed": test["passed"],
                "response_time": test["actual_response"]["response_time"],
                "status_code": test["actual_response"]["status_code"],
                "execution_time": test.get("execution_time", test["actual_response"]["response_time"])
            }
            results.append(result)
        
        self.df = pd.DataFrame(results)
    
    def categorize_test(self, test_id):
        """Categorize test based on test ID"""
        if test_id.startswith("REG_001") or test_id.startswith("REG_002") or test_id.startswith("REG_003"):
            return "Positive"
        elif test_id.startswith("REG_004") or test_id.startswith("REG_005") or test_id.startswith("REG_006") or test_id.startswith("REG_007"):
            return "Negative"
        elif test_id.startswith("REG_015") or test_id.startswith("REG_016"):
            return "Security"
        elif test_id.startswith("REG_012") or test_id.startswith("REG_013"):
            return "Boundary"
        elif test_id.startswith("REG_023"):
            return "Performance"
        else:
            return "Other"
    
    def create_matplotlib_dashboard(self):
        """Create comprehensive matplotlib dashboard"""
        fig = plt.figure(figsize=(20, 16))
        fig.suptitle('User Registration Test Results Dashboard\nTarget: localhost:5003', 
                     fontsize=20, fontweight='bold', y=0.98)
        
        # 1. Overall Pass/Fail Summary (Top Left)
        ax1 = plt.subplot(3, 4, 1)
        summary = self.test_data["summary"]
        labels = ['Passed', 'Failed']
        sizes = [summary["passed"], summary["failed"]]
        colors = ['#2ecc71', '#e74c3c']
        
        wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                          startangle=90, textprops={'fontsize': 10})
        ax1.set_title(f'Overall Results\n{summary["total_tests"]} Total Tests', fontweight='bold')
        
        # 2. Test Categories Distribution (Top Center-Left)
        ax2 = plt.subplot(3, 4, 2)
        category_counts = self.df['category'].value_counts()
        colors_cat = plt.cm.Set3(np.linspace(0, 1, len(category_counts)))
        bars = ax2.bar(category_counts.index, category_counts.values, color=colors_cat)
        ax2.set_title('Tests by Category', fontweight='bold')
        ax2.set_ylabel('Number of Tests')
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom')
        
        # 3. Response Time Distribution (Top Center-Right)
        ax3 = plt.subplot(3, 4, 3)
        response_times = self.df['response_time']
        ax3.hist(response_times, bins=8, color='skyblue', alpha=0.7, edgecolor='black')
        ax3.axvline(response_times.mean(), color='red', linestyle='--', 
                   label=f'Mean: {response_times.mean():.2f}s')
        ax3.axvline(3.0, color='orange', linestyle='--', 
                   label='Threshold: 3.0s')
        ax3.set_title('Response Time Distribution', fontweight='bold')
        ax3.set_xlabel('Response Time (seconds)')
        ax3.set_ylabel('Frequency')
        ax3.legend()
        
        # 4. Priority vs Pass Rate (Top Right)
        ax4 = plt.subplot(3, 4, 4)
        priority_stats = self.df.groupby('priority').agg({
            'passed': ['count', 'sum']
        }).round(2)
        priority_stats.columns = ['Total', 'Passed']
        priority_stats['Pass_Rate'] = (priority_stats['Passed'] / priority_stats['Total'] * 100)
        
        bars = ax4.bar(priority_stats.index, priority_stats['Pass_Rate'], 
                      color=['#e74c3c', '#f39c12', '#2ecc71'])
        ax4.set_title('Pass Rate by Priority', fontweight='bold')
        ax4.set_ylabel('Pass Rate (%)')
        ax4.set_ylim(0, 105)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        # 5. Response Time by Category (Middle Left)
        ax5 = plt.subplot(3, 4, 5)
        category_response = self.df.groupby('category')['response_time'].agg(['mean', 'std']).fillna(0)
        bars = ax5.bar(category_response.index, category_response['mean'], 
                      yerr=category_response['std'], capsize=5, color=colors_cat)
        ax5.set_title('Avg Response Time by Category', fontweight='bold')
        ax5.set_ylabel('Response Time (seconds)')
        plt.setp(ax5.get_xticklabels(), rotation=45, ha='right')
        
        # 6. Test Timeline (Middle Center)
        ax6 = plt.subplot(3, 4, (6, 7))
        test_order = range(len(self.df))
        colors_timeline = ['green' if passed else 'red' for passed in self.df['passed']]
        scatter = ax6.scatter(test_order, self.df['response_time'], 
                             c=colors_timeline, s=100, alpha=0.7)
        ax6.set_title('Test Execution Timeline', fontweight='bold')
        ax6.set_xlabel('Test Execution Order')
        ax6.set_ylabel('Response Time (seconds)')
        ax6.axhline(y=3.0, color='orange', linestyle='--', alpha=0.7, label='Threshold')
        ax6.legend()
        
        # 7. Status Code Distribution (Middle Right)
        ax7 = plt.subplot(3, 4, 8)
        status_counts = self.df['status_code'].value_counts()
        colors_status = ['#2ecc71' if code == 201 else '#e74c3c' for code in status_counts.index]
        bars = ax7.bar([str(code) for code in status_counts.index], 
                      status_counts.values, color=colors_status)
        ax7.set_title('HTTP Status Codes', fontweight='bold')
        ax7.set_ylabel('Count')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax7.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom')
        
        # 8. Performance Metrics Summary (Bottom Left)
        ax8 = plt.subplot(3, 4, 9)
        ax8.axis('off')
        
        perf_metrics = {
            'Total Tests': summary["total_tests"],
            'Pass Rate': f"{summary['pass_rate']:.1f}%",
            'Avg Response Time': f"{response_times.mean():.2f}s",
            'Max Response Time': f"{response_times.max():.2f}s",
            'Min Response Time': f"{response_times.min():.2f}s",
            'Tests Under 3s': f"{(response_times < 3.0).sum()}/{len(response_times)}"
        }
        
        y_pos = 0.9
        ax8.text(0.1, y_pos, 'Performance Summary', fontsize=14, fontweight='bold')
        y_pos -= 0.15
        
        for metric, value in perf_metrics.items():
            ax8.text(0.1, y_pos, f'{metric}:', fontsize=11, fontweight='bold')
            ax8.text(0.6, y_pos, str(value), fontsize=11)
            y_pos -= 0.12
        
        # 9. Category Performance Heatmap (Bottom Center)
        ax9 = plt.subplot(3, 4, (10, 11))
        
        # Create pivot table for heatmap
        heatmap_data = self.df.pivot_table(
            values='response_time', 
            index='category', 
            columns='priority', 
            aggfunc='mean'
        ).fillna(0)
        
        if not heatmap_data.empty:
            im = ax9.imshow(heatmap_data.values, cmap='RdYlGn_r', aspect='auto')
            ax9.set_xticks(range(len(heatmap_data.columns)))
            ax9.set_yticks(range(len(heatmap_data.index)))
            ax9.set_xticklabels(heatmap_data.columns)
            ax9.set_yticklabels(heatmap_data.index)
            ax9.set_title('Response Time Heatmap\n(Category vs Priority)', fontweight='bold')
            
            # Add text annotations
            for i in range(len(heatmap_data.index)):
                for j in range(len(heatmap_data.columns)):
                    value = heatmap_data.iloc[i, j]
                    if value > 0:
                        ax9.text(j, i, f'{value:.2f}s', ha='center', va='center',
                               color='white' if value > heatmap_data.values.mean() else 'black')
            
            plt.colorbar(im, ax=ax9, label='Response Time (s)')
        
        # 10. Test Results Summary Table (Bottom Right)
        ax10 = plt.subplot(3, 4, 12)
        ax10.axis('off')
        
        # Create summary table data
        table_data = []
        for category in self.df['category'].unique():
            cat_data = self.df[self.df['category'] == category]
            table_data.append([
                category,
                len(cat_data),
                cat_data['passed'].sum(),
                f"{(cat_data['passed'].sum() / len(cat_data) * 100):.0f}%",
                f"{cat_data['response_time'].mean():.2f}s"
            ])
        
        table = ax10.table(cellText=table_data,
                          colLabels=['Category', 'Total', 'Passed', 'Pass%', 'Avg Time'],
                          cellLoc='center',
                          loc='center',
                          colWidths=[0.25, 0.15, 0.15, 0.15, 0.2])
        
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        ax10.set_title('Category Summary', fontweight='bold', pad=20)
        
        # Style the table
        for i in range(len(table_data) + 1):
            for j in range(5):
                cell = table[(i, j)]
                if i == 0:  # Header row
                    cell.set_facecolor('#3498db')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#ecf0f1' if i % 2 == 0 else 'white')
        
        plt.tight_layout()
        return fig
    
    def create_interactive_dashboard(self):
        """Create interactive Plotly dashboard"""
        # Create subplots
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=[
                'Test Results Overview', 'Response Time by Category', 'Test Timeline',
                'Category Distribution', 'Priority Analysis', 'Status Code Distribution',
                'Performance Metrics', 'Response Time Distribution', 'Test Details'
            ],
            specs=[
                [{"type": "pie"}, {"type": "bar"}, {"type": "scatter"}],
                [{"type": "bar"}, {"type": "bar"}, {"type": "bar"}],
                [{"type": "table"}, {"type": "histogram"}, {"type": "bar"}]
            ]
        )
        
        # 1. Overall Results Pie Chart
        summary = self.test_data["summary"]
        fig.add_trace(
            go.Pie(
                labels=['Passed', 'Failed'],
                values=[summary["passed"], summary["failed"]],
                marker_colors=['#2ecc71', '#e74c3c'],
                name="Overall Results"
            ),
            row=1, col=1
        )
        
        # 2. Response Time by Category
        category_response = self.df.groupby('category')['response_time'].mean()
        fig.add_trace(
            go.Bar(
                x=category_response.index,
                y=category_response.values,
                marker_color='lightblue',
                name="Avg Response Time"
            ),
            row=1, col=2
        )
        
        # 3. Test Timeline
        fig.add_trace(
            go.Scatter(
                x=list(range(len(self.df))),
                y=self.df['response_time'],
                mode='markers+lines',
                marker=dict(
                    color=['green' if passed else 'red' for passed in self.df['passed']],
                    size=10
                ),
                text=self.df['test_id'],
                name="Timeline"
            ),
            row=1, col=3
        )
        
        # 4. Category Distribution
        category_counts = self.df['category'].value_counts()
        fig.add_trace(
            go.Bar(
                x=category_counts.index,
                y=category_counts.values,
                marker_color='lightcoral',
                name="Test Count"
            ),
            row=2, col=1
        )
        
        # 5. Priority Analysis
        priority_stats = self.df.groupby('priority').size()
        fig.add_trace(
            go.Bar(
                x=priority_stats.index,
                y=priority_stats.values,
                marker_color='lightsalmon',
                name="Priority Count"
            ),
            row=2, col=2
        )
        
        # 6. Status Code Distribution
        status_counts = self.df['status_code'].value_counts()
        fig.add_trace(
            go.Bar(
                x=[str(code) for code in status_counts.index],
                y=status_counts.values,
                marker_color=['#2ecc71' if code == 201 else '#e74c3c' for code in status_counts.index],
                name="Status Codes"
            ),
            row=2, col=3
        )
        
        # 7. Performance Metrics Table
        perf_data = [
            ['Total Tests', summary["total_tests"]],
            ['Pass Rate', f"{summary['pass_rate']:.1f}%"],
            ['Avg Response Time', f"{self.df['response_time'].mean():.2f}s"],
            ['Max Response Time', f"{self.df['response_time'].max():.2f}s"],
            ['Min Response Time', f"{self.df['response_time'].min():.2f}s"]
        ]
        
        fig.add_trace(
            go.Table(
                header=dict(values=['Metric', 'Value'],
                           fill_color='lightblue',
                           align='left'),
                cells=dict(values=[[row[0] for row in perf_data], 
                                  [row[1] for row in perf_data]],
                          fill_color='lightgray',
                          align='left')
            ),
            row=3, col=1
        )
        
        # 8. Response Time Distribution
        fig.add_trace(
            go.Histogram(
                x=self.df['response_time'],
                nbinsx=10,
                marker_color='skyblue',
                name="Response Time Dist"
            ),
            row=3, col=2
        )
        
        # 9. Test Details
        test_details = self.df.groupby('category').agg({
            'passed': 'sum',
            'response_time': 'mean'
        }).round(2)
        
        fig.add_trace(
            go.Bar(
                x=test_details.index,
                y=test_details['response_time'],
                marker_color='lightgreen',
                name="Category Performance"
            ),
            row=3, col=3
        )
        
        # Update layout
        fig.update_layout(
            height=1200,
            title_text="User Registration Test Results - Interactive Dashboard<br>Target: localhost:5003",
            title_x=0.5,
            showlegend=False
        )
        
        return fig
    
    def save_dashboards(self):
        """Save both matplotlib and plotly dashboards"""
        # Save matplotlib dashboard
        matplotlib_fig = self.create_matplotlib_dashboard()
        matplotlib_fig.savefig('test_results_dashboard_static.png', dpi=300, bbox_inches='tight')
        matplotlib_fig.savefig('test_results_dashboard_static.pdf', bbox_inches='tight')
        print("✅ Static dashboard saved as 'test_results_dashboard_static.png' and '.pdf'")
        
        # Save interactive plotly dashboard
        plotly_fig = self.create_interactive_dashboard()
        pyo.plot(plotly_fig, filename='test_results_dashboard_interactive.html', auto_open=False)
        print("✅ Interactive dashboard saved as 'test_results_dashboard_interactive.html'")
        
        return matplotlib_fig, plotly_fig
    
    def generate_dashboard_summary(self):
        """Generate text summary of dashboard insights"""
        summary = f"""
# Test Results Dashboard Summary

## Key Insights from localhost:5003 Testing

### Overall Performance
- **Total Tests**: {self.test_data['summary']['total_tests']}
- **Pass Rate**: {self.test_data['summary']['pass_rate']:.1f}%
- **Average Response Time**: {self.df['response_time'].mean():.2f}s
- **Performance Threshold Compliance**: {(self.df['response_time'] < 3.0).sum()}/{len(self.df)} tests under 3s

### Category Analysis
"""
        
        for category in self.df['category'].unique():
            cat_data = self.df[self.df['category'] == category]
            summary += f"""
**{category} Tests**:
- Count: {len(cat_data)}
- Pass Rate: {(cat_data['passed'].sum() / len(cat_data) * 100):.0f}%
- Avg Response Time: {cat_data['response_time'].mean():.2f}s"""
        
        summary += f"""

### Performance Highlights
- **Fastest Test**: {self.df.loc[self.df['response_time'].idxmin(), 'test_id']} ({self.df['response_time'].min():.2f}s)
- **Slowest Test**: {self.df.loc[self.df['response_time'].idxmax(), 'test_id']} ({self.df['response_time'].max():.2f}s)
- **Most Critical**: {len(self.df[self.df['priority'] == 'High'])} high-priority tests
- **Security Coverage**: {len(self.df[self.df['category'] == 'Security'])} security tests

### Dashboard Files Generated
- `test_results_dashboard_static.png` - High-resolution static dashboard
- `test_results_dashboard_static.pdf` - PDF version for reports
- `test_results_dashboard_interactive.html` - Interactive web dashboard
"""
        
        return summary


def main():
    """Main function to generate dashboard"""
    print("🚀 Generating Test Results Dashboard...")
    
    # Try to find the most recent test report
    import glob
    report_files = glob.glob("registration_test_report_*.json")
    
    if report_files:
        # Use the most recent report file
        latest_report = max(report_files)
        print(f"📊 Using test report: {latest_report}")
        dashboard = TestResultsDashboard(latest_report)
    else:
        print("📊 No test report found, using sample data")
        dashboard = TestResultsDashboard()
    
    # Generate and save dashboards
    matplotlib_fig, plotly_fig = dashboard.save_dashboards()
    
    # Generate summary
    summary = dashboard.generate_dashboard_summary()
    with open('dashboard_summary.md', 'w') as f:
        f.write(summary)
    print("✅ Dashboard summary saved as 'dashboard_summary.md'")
    
    # Display matplotlib dashboard
    plt.show()
    
    print("\n🎉 Dashboard generation complete!")
    print("📁 Files generated:")
    print("   - test_results_dashboard_static.png (High-res image)")
    print("   - test_results_dashboard_static.pdf (PDF report)")
    print("   - test_results_dashboard_interactive.html (Interactive web)")
    print("   - dashboard_summary.md (Text summary)")


if __name__ == "__main__":
    main()
