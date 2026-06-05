#!/usr/bin/env python3
"""
Tests for Error Detector Tool
"""

import unittest
import json
import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))

from error_detector import ErrorDetector


class TestErrorDetector(unittest.TestCase):
    """Test cases for ErrorDetector"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = ErrorDetector()
        
        # Create sample parsed logs
        self.sample_logs = {
            'total_lines': 100,
            'parsed_lines': 100,
            'entries': [
                {
                    'timestamp': '2026-05-21T10:00:00Z',
                    'level': 'ERROR',
                    'message': 'Database connection timeout',
                    'raw_line': 'ERROR: Database connection timeout'
                },
                {
                    'timestamp': '2026-05-21T10:00:01Z',
                    'level': 'ERROR',
                    'message': 'Database connection timeout',
                    'raw_line': 'ERROR: Database connection timeout'
                },
                {
                    'timestamp': '2026-05-21T10:00:02Z',
                    'level': 'INFO',
                    'message': 'User logged in',
                    'raw_line': 'INFO: User logged in'
                },
                {
                    'timestamp': '2026-05-21T10:00:03Z',
                    'level': 'CRITICAL',
                    'message': 'Out of memory error',
                    'raw_line': 'CRITICAL: Out of memory error'
                },
                {
                    'timestamp': '2026-05-21T10:00:04Z',
                    'level': 'ERROR',
                    'message': 'Network timeout',
                    'raw_line': 'ERROR: Network timeout'
                },
            ],
            'metadata': {
                'start_time': '2026-05-21T10:00:00Z',
                'end_time': '2026-05-21T10:00:04Z',
                'duration_hours': 0.001
            }
        }
    
    def test_filter_errors(self):
        """Test error filtering"""
        entries = self.sample_logs['entries']
        error_entries = self.detector.filter_errors(entries)
        
        # Should have 4 errors (3 ERROR + 1 CRITICAL)
        self.assertEqual(len(error_entries), 4)
        
        # All should be ERROR or CRITICAL level
        for entry in error_entries:
            self.assertIn(entry['level'], ['ERROR', 'CRITICAL'])
    
    def test_categorize_errors(self):
        """Test error categorization"""
        entries = self.sample_logs['entries']
        error_entries = self.detector.filter_errors(entries)
        categorized = self.detector.categorize_errors(error_entries)
        
        # Should have categories
        self.assertIsInstance(categorized, dict)
        
        # Database errors should be categorized
        if 'database' in categorized:
            self.assertGreater(len(categorized['database']), 0)
        
        # Resource errors should be categorized
        if 'resource' in categorized:
            self.assertGreater(len(categorized['resource']), 0)
    
    def test_extract_error_details(self):
        """Test error detail extraction"""
        entries = self.sample_logs['entries']
        error_entries = self.detector.filter_errors(entries)
        categorized = self.detector.categorize_errors(error_entries)
        details = self.detector.extract_error_details(categorized)
        
        # Should have details for each error
        self.assertEqual(len(details), 4)
        
        # Each detail should have required fields
        for detail in details:
            self.assertIn('error_id', detail)
            self.assertIn('category', detail)
            self.assertIn('message', detail)
            self.assertIn('severity', detail)
    
    def test_group_similar_errors(self):
        """Test error grouping"""
        entries = self.sample_logs['entries']
        error_entries = self.detector.filter_errors(entries)
        categorized = self.detector.categorize_errors(error_entries)
        details = self.detector.extract_error_details(categorized)
        grouped = self.detector.group_similar_errors(details)
        
        # Should group similar errors together
        # Two identical "Database connection timeout" should be grouped
        database_groups = [g for g in grouped if 'database' in g['message_template'].lower()]
        if database_groups:
            # Should have at least 2 occurrences
            self.assertGreaterEqual(database_groups[0]['occurrences'], 2)
    
    def test_calculate_metrics(self):
        """Test metrics calculation"""
        entries = self.sample_logs['entries']
        error_entries = self.detector.filter_errors(entries)
        categorized = self.detector.categorize_errors(error_entries)
        details = self.detector.extract_error_details(categorized)
        grouped = self.detector.group_similar_errors(details)
        
        metrics = self.detector.calculate_metrics(grouped, self.sample_logs)
        
        # Check metrics exist
        self.assertIn('total_errors', metrics)
        self.assertIn('error_percentage', metrics)
        self.assertIn('error_rate_per_hour', metrics)
        self.assertIn('distribution', metrics)
        
        # Check values are reasonable
        self.assertEqual(metrics['total_errors'], 4)
        self.assertGreater(metrics['error_percentage'], 0)
    
    def test_identify_critical_errors(self):
        """Test critical error identification"""
        entries = self.sample_logs['entries']
        error_entries = self.detector.filter_errors(entries)
        categorized = self.detector.categorize_errors(error_entries)
        details = self.detector.extract_error_details(categorized)
        grouped = self.detector.group_similar_errors(details)
        
        critical = self.detector.identify_critical_errors(grouped)
        
        # Should identify at least one critical error (Out of memory)
        self.assertGreaterEqual(len(critical), 1)
        
        # Critical errors should have reasons
        for error in critical:
            self.assertIn('critical_reasons', error)
            self.assertGreater(len(error['critical_reasons']), 0)
    
    def test_parameterize_message(self):
        """Test message parameterization"""
        msg1 = "User 12345 failed to login"
        msg2 = "User 67890 failed to login"
        
        param1 = self.detector._parameterize_message(msg1)
        param2 = self.detector._parameterize_message(msg2)
        
        # Should be the same after parameterization
        self.assertEqual(param1, param2)
        self.assertIn('<NUM>', param1)
    
    def test_full_detection_pipeline(self):
        """Test complete error detection pipeline"""
        result = self.detector.detect_errors(self.sample_logs)
        
        # Check all expected fields exist
        self.assertIn('total_errors', result)
        self.assertIn('unique_error_types', result)
        self.assertIn('error_percentage', result)
        self.assertIn('critical_errors', result)
        self.assertIn('grouped_errors', result)
        self.assertIn('top_errors', result)
        
        # Check values
        self.assertEqual(result['total_errors'], 4)
        self.assertGreater(result['unique_error_types'], 0)


class TestErrorDetectorEdgeCases(unittest.TestCase):
    """Test edge cases for error detector"""
    
    def setUp(self):
        self.detector = ErrorDetector()
    
    def test_no_errors(self):
        """Test with logs containing no errors"""
        logs = {
            'entries': [
                {'level': 'INFO', 'message': 'Test', 'timestamp': '2026-05-21T10:00:00Z'}
            ],
            'parsed_lines': 1,
            'metadata': {'duration_hours': 1}
        }
        
        result = self.detector.detect_errors(logs)
        self.assertEqual(result['total_errors'], 0)
    
    def test_empty_logs(self):
        """Test with empty logs"""
        logs = {
            'entries': [],
            'parsed_lines': 0,
            'metadata': {'duration_hours': 0}
        }
        
        result = self.detector.detect_errors(logs)
        self.assertEqual(result['total_errors'], 0)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestErrorDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorDetectorEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
