# Quick Start Guide

Get started with Log Analyzer Agent in 5 minutes.

## Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt --break-system-packages

# 2. (Optional) Set Claude API key for future API mode
export ANTHROPIC_API_KEY="your-api-key"
```

## Basic Usage

### Analyze a Log File

```bash
# Direct analysis
python agent/main_agent.py --file /path/to/your/logfile.log

# Interactive mode
python agent/main_agent.py --interactive
```

### Example with Sample Data

```bash
# Analyze the sample Apache log
python agent/main_agent.py --file tests/sample_data/apache_access.log

# Analyze the sample application log
python agent/main_agent.py --file tests/sample_data/application.log

# Analyze the sample JSON log
python agent/main_agent.py --file tests/sample_data/json_logs.log
```

## What You'll Get

After analysis, you'll receive:

1. **Console Output** - Summary of findings
2. **Report File** - Detailed analysis in `outputs/` directory

Example output:
```
✓ Parsed 156,234 log entries
✓ Found 1,523 errors (47 unique types)
✓ Identified 12 patterns, 5 anomalies
✓ Report saved to: outputs/log_analysis_report_20260521_143052.md
```

## Understanding the Report

The generated report includes:

- **Executive Summary** - Status, error rate, critical issues
- **Log Parsing Stats** - File info, parse success rate
- **Error Analysis** - Categories, top errors, critical issues
- **Pattern Analysis** - Recurring patterns, anomalies, trends
- **Recommendations** - Prioritized action items

## Interactive Mode

In interactive mode:

```bash
python agent/main_agent.py --interactive

# Then use commands:
You: analyze tests/sample_data/application.log
You: quit
```

## Using Individual Tools

### Parse Logs Only

```bash
python tools/log_parser.py tests/sample_data/apache_access.log
# Output: apache_access.log_parsed.json
```

### Detect Errors

```bash
# First parse logs
python tools/log_parser.py tests/sample_data/application.log

# Then detect errors
python tools/error_detector.py tests/sample_data/application.log_parsed.json
# Output: application.log_parsed_errors.json
```

### Analyze Patterns

```bash
python tools/pattern_analyzer.py tests/sample_data/application.log_parsed.json
# Output: application.log_parsed_patterns.json
```

### Generate Report

```bash
# Requires all analysis results in a directory
python tools/report_generator.py /path/to/results/
```

## Running Tests

```bash
# Run all tests
bash run_tests.sh

# Or run individually
python tests/test_log_parser.py
python tests/test_error_detector.py
```

## Common Use Cases

### 1. Debug Production Issues

```bash
# Download production logs
scp server:/var/log/app.log ./production.log

# Analyze
python agent/main_agent.py --file production.log

# Review the report in outputs/
```

### 2. Monitor Error Trends

```bash
# Analyze today's logs
python agent/main_agent.py --file /var/log/app.log

# Compare with yesterday's report
diff outputs/log_analysis_report_today.md outputs/log_analysis_report_yesterday.md
```

### 3. Performance Analysis

```bash
# Analyze logs for response time patterns
python agent/main_agent.py --file /var/log/nginx/access.log

# Check for slow endpoints in the report
grep "response_time" outputs/latest_report.md
```

## Configuration

Edit `config/settings.py` to customize:

```python
# Maximum file size (MB)
MAX_LOG_FILE_SIZE_MB = 500

# Maximum lines to analyze
MAX_LINES_TO_ANALYZE = 100000

# Error detection keywords
ERROR_KEYWORDS = ['error', 'exception', 'failed', ...]

# Report format (markdown, html, json, text)
DEFAULT_REPORT_FORMAT = "markdown"
```

## Troubleshooting

### Parse Rate Low (<90%)

```bash
# Check log format
python tools/log_parser.py --help

# Try specifying format manually
# (Edit log_parser.py to add custom format)
```

### Out of Memory

```bash
# Reduce chunk size in config/settings.py
CHUNK_SIZE = 5000  # Instead of 10000

# Or sample the log file
head -n 50000 large.log > sample.log
python agent/main_agent.py --file sample.log
```

### Slow Performance

- Reduce `MAX_LINES_TO_ANALYZE` in config
- Process smaller time ranges
- Use faster storage (SSD)

## Next Steps

1. **Read the README** - Full documentation
2. **Review Skills** - Check `skills/*/SKILL.md` files
3. **Customize** - Edit `config/settings.py`
4. **Extend** - Add custom error patterns or formats

## Support

- Issues: Check error messages in console
- Documentation: See README.md and skills/*/references/
- Examples: Run sample data in tests/sample_data/

## Tips

✓ **Start Small** - Test with sample data first
✓ **Check Reports** - Review outputs/ for detailed findings
✓ **Customize** - Adjust error keywords for your app
✓ **Automate** - Add to CI/CD for continuous monitoring
✓ **Share** - Export JSON reports for dashboards

Happy log analyzing! 🔍
