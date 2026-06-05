#!/usr/bin/env python3
"""
Tests for Log Parser Tool
"""

import unittest
import json
import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))

from log_parser import LogParser


class TestLogParser(unittest.TestCase):
    """Test cases for LogParser"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = LogParser()
        self.sample_dir = Path(__file__).parent / 'sample_data'
    
    def test_detect_apache_format(self):
        """Test Apache log format detection"""
        apache_log = self.sample_dir / 'apache_access.log'
        format_detected = self.parser.detect_format(str(apache_log))
        self.assertIn(format_detected, ['apache', 'nginx'])
    
    def test_detect_json_format(self):
        """Test JSON log format detection"""
        json_log = self.sample_dir / 'json_logs.log'
        format_detected = self.parser.detect_format(str(json_log))
        self.assertEqual(format_detected, 'json')
    
    def test_detect_application_format(self):
        """Test application log format detection"""
        app_log = self.sample_dir / 'application.log'
        format_detected = self.parser.detect_format(str(app_log))
        self.assertIn(format_detected, ['application', 'custom'])
    
    def test_parse_apache_log(self):
        """Test parsing Apache log file"""
        apache_log = self.sample_dir / 'apache_access.log'
        result = self.parser.parse_file(str(apache_log))
        
        self.assertGreater(result['parsed_lines'], 0)
        self.assertEqual(result['format'], 'apache')
        self.assertIn('entries', result)
        
        # Check first entry has expected fields
        if result['entries']:
            entry = result['entries'][0]
            self.assertIn('ip_address', entry)
            self.assertIn('method', entry)
            self.assertIn('path', entry)
            self.assertIn('status_code', entry)
    
    def test_parse_json_log(self):
        """Test parsing JSON log file"""
        json_log = self.sample_dir / 'json_logs.log'
        result = self.parser.parse_file(str(json_log))
        
        self.assertGreater(result['parsed_lines'], 0)
        self.assertEqual(result['format'], 'json')
        
        # Check entries have expected fields
        if result['entries']:
            entry = result['entries'][0]
            self.assertIn('timestamp', entry)
            self.assertIn('level', entry)
            self.assertIn('service', entry)
    
    def test_parse_application_log(self):
        """Test parsing application log file"""
        app_log = self.sample_dir / 'application.log'
        result = self.parser.parse_file(str(app_log))
        
        self.assertGreater(result['parsed_lines'], 0)
        self.assertIn('entries', result)
        
        # Check entries have timestamps and levels
        if result['entries']:
            entry = result['entries'][0]
            self.assertIn('timestamp', entry)
            self.assertIn('level', entry)
    
    def test_timestamp_normalization(self):
        """Test timestamp normalization"""
        timestamp1 = "21/May/2026:10:23:45 +0000"
        normalized1 = self.parser._parse_apache_timestamp(timestamp1)
        self.assertIsNotNone(normalized1)
        self.assertIn('T', normalized1)  # ISO format
        
        timestamp2 = "2026-05-21T10:23:45Z"
        normalized2 = self.parser._normalize_timestamp(timestamp2)
        self.assertIsNotNone(normalized2)
    
    def test_level_extraction(self):
        """Test log level extraction"""
        text1 = "This is an ERROR message"
        level1 = self.parser._extract_level(text1)
        self.assertEqual(level1, 'ERROR')
        
        text2 = "Information: User logged in"
        level2 = self.parser._extract_level(text2)
        self.assertEqual(level2, 'INFO')
        
        text3 = "No level here"
        level3 = self.parser._extract_level(text3)
        self.assertEqual(level3, 'INFO')  # Default
    
    def test_status_to_level(self):
        """Test HTTP status code to level conversion"""
        self.assertEqual(self.parser._status_to_level(200), 'INFO')
        self.assertEqual(self.parser._status_to_level(404), 'WARNING')
        self.assertEqual(self.parser._status_to_level(500), 'ERROR')
    
    def test_parse_rate(self):
        """Test parse success rate"""
        app_log = self.sample_dir / 'application.log'
        result = self.parser.parse_file(str(app_log))
        
        success_rate = (result['parsed_lines'] / result['total_lines']) * 100
        self.assertGreater(success_rate, 80)  # At least 80% should parse


class TestLogParserEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        self.parser = LogParser()
    
    def test_empty_file(self):
        """Test parsing empty file"""
        # Create temporary empty file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            temp_file = f.name
        
        try:
            result = self.parser.parse_file(temp_file)
            self.assertEqual(result['parsed_lines'], 0)
        finally:
            Path(temp_file).unlink()
    
    def test_nonexistent_file(self):
        """Test parsing non-existent file"""
        with self.assertRaises(FileNotFoundError):
            self.parser.parse_file('/nonexistent/file.log')
    
    def test_max_lines_limit(self):
        """Test max lines limit"""
        app_log = Path(__file__).parent / 'sample_data' / 'application.log'
        result = self.parser.parse_file(str(app_log), max_lines=10)
        
        self.assertLessEqual(result['total_lines'], 10)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLogParser))
    suite.addTests(loader.loadTestsFromTestCase(TestLogParserEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
