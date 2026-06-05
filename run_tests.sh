#!/bin/bash
# Run all tests for Log Analyzer Agent

echo "=================================="
echo "Log Analyzer Agent - Test Suite"
echo "=================================="
echo ""

# Change to project root
cd "$(dirname "$0")"

# Set Python path
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Run tests
echo "Running test_log_parser.py..."
python3 tests/test_log_parser.py
PARSER_RESULT=$?

echo ""
echo "Running test_error_detector.py..."
python3 tests/test_error_detector.py
DETECTOR_RESULT=$?

echo ""
echo "=================================="
echo "Test Results Summary"
echo "=================================="
echo "Log Parser Tests: $([ $PARSER_RESULT -eq 0 ] && echo '✓ PASSED' || echo '✗ FAILED')"
echo "Error Detector Tests: $([ $DETECTOR_RESULT -eq 0 ] && echo '✓ PASSED' || echo '✗ FAILED')"
echo "=================================="

# Exit with error if any test failed
if [ $PARSER_RESULT -ne 0 ] || [ $DETECTOR_RESULT -ne 0 ]; then
    exit 1
fi

exit 0
