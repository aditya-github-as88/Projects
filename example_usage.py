#!/usr/bin/env python3
"""
Example Usage Script
Demonstrates how to use the Log Analyzer Agent
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.main_agent import LogAnalyzerAgent


def example_basic_analysis():
    """Example 1: Basic log file analysis"""
    print("\n" + "="*60)
    print("Example 1: Basic Log File Analysis")
    print("="*60 + "\n")
    
    # Initialize agent
    agent = LogAnalyzerAgent()
    
    # Analyze a sample log file
    log_file = "tests/sample_data/application.log"
    
    print(f"Analyzing: {log_file}\n")
    
    result = agent.execute_skill_workflow(
        f"analyze this log file and generate a report: {log_file}",
        log_file_path=log_file
    )
    
    print(result)


def example_error_detection():
    """Example 2: Focus on error detection"""
    print("\n" + "="*60)
    print("Example 2: Error Detection Focus")
    print("="*60 + "\n")
    
    from tools.log_parser import LogParser
    from tools.error_detector import ErrorDetector
    
    # Parse logs
    parser = LogParser()
    log_file = "tests/sample_data/application.log"
    
    print(f"Parsing: {log_file}")
    parsed = parser.parse_file(log_file)
    print(f"✓ Parsed {parsed['parsed_lines']} entries\n")
    
    # Detect errors
    detector = ErrorDetector()
    errors = detector.detect_errors(parsed)
    
    print(f"Error Detection Results:")
    print(f"  Total Errors: {errors['total_errors']}")
    print(f"  Unique Types: {errors['unique_error_types']}")
    print(f"  Critical Errors: {errors['critical_errors']}")
    print(f"  Error Rate: {errors['error_percentage']}%")
    
    print(f"\nTop 3 Errors:")
    for i, error in enumerate(errors['top_errors'][:3], 1):
        print(f"  {i}. {error['type']} ({error['occurrences']} times)")


def example_pattern_analysis():
    """Example 3: Pattern analysis"""
    print("\n" + "="*60)
    print("Example 3: Pattern Analysis")
    print("="*60 + "\n")
    
    from tools.log_parser import LogParser
    from tools.pattern_analyzer import PatternAnalyzer
    
    # Parse logs
    parser = LogParser()
    log_file = "tests/sample_data/application.log"
    
    parsed = parser.parse_file(log_file)
    
    # Analyze patterns
    analyzer = PatternAnalyzer()
    patterns = analyzer.analyze_patterns(parsed)
    
    print(f"Pattern Analysis Results:")
    print(f"  Patterns Found: {patterns['pattern_count']}")
    print(f"  Anomalies Detected: {patterns['anomaly_count']}")
    
    if patterns['patterns']:
        print(f"\nRecurring Patterns:")
        for pattern in patterns['patterns'][:3]:
            print(f"  - {pattern['description']}")
    
    if patterns['anomalies']:
        print(f"\nAnomalies:")
        for anomaly in patterns['anomalies'][:3]:
            print(f"  - {anomaly['description']}")


def example_custom_workflow():
    """Example 4: Custom workflow with individual tools"""
    print("\n" + "="*60)
    print("Example 4: Custom Workflow")
    print("="*60 + "\n")
    
    from tools.log_parser import LogParser
    from tools.error_detector import ErrorDetector
    from tools.pattern_analyzer import PatternAnalyzer
    from tools.report_generator import ReportGenerator
    
    log_file = "tests/sample_data/apache_access.log"
    
    # Step 1: Parse
    print("Step 1: Parsing logs...")
    parser = LogParser()
    parsed = parser.parse_file(log_file)
    print(f"✓ Parsed {parsed['parsed_lines']} entries")
    
    # Step 2: Detect errors
    print("\nStep 2: Detecting errors...")
    detector = ErrorDetector()
    errors = detector.detect_errors(parsed)
    print(f"✓ Found {errors['total_errors']} errors")
    
    # Step 3: Analyze patterns
    print("\nStep 3: Analyzing patterns...")
    analyzer = PatternAnalyzer()
    patterns = analyzer.analyze_patterns(parsed)
    print(f"✓ Found {patterns['pattern_count']} patterns")
    
    # Step 4: Generate report
    print("\nStep 4: Generating report...")
    generator = ReportGenerator()
    
    results = {
        'log-parsing': parsed,
        'error-detection': errors,
        'pattern-analysis': patterns
    }
    
    report = generator.generate_report(results)
    output_path = generator.save_report(report, format="markdown")
    
    print(f"✓ Report saved to: {output_path}")
    
    # Show executive summary
    print("\n" + "="*60)
    print("Executive Summary:")
    print("="*60)
    print(report['executive_summary'])


def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("LOG ANALYZER AGENT - EXAMPLE USAGE")
    print("="*80)
    
    examples = [
        ("Basic Analysis", example_basic_analysis),
        ("Error Detection", example_error_detection),
        ("Pattern Analysis", example_pattern_analysis),
        ("Custom Workflow", example_custom_workflow)
    ]
    
    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nRunning all examples...\n")
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\nError in {name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("All examples completed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
