---
name: log-parsing
description: "Parses log files in various formats including Apache, Nginx, syslog, JSON, Docker, and Kubernetes logs. Use when user mentions 'parse logs', 'read log file', 'analyze logs', or provides a log file path. Also triggers on 'extract log data', 'process log file', or 'load logs'."
compatibility: "Works with claude.ai, Claude Code, and API. Supports text and JSON log formats. Requires file system access."
license: MIT
metadata:
  author: Log Analyzer Team
  version: 1.0.0
  category: log-processing
  tags: [logs, parsing, apache, nginx, syslog, json, kubernetes]
---

# Log Parsing Skill

## Purpose

This skill parses log files in multiple formats and extracts structured data. It's the foundational skill that must run before error detection or pattern analysis. Handles common log formats (Apache, Nginx, syslog) as well as structured formats (JSON) and container logs (Docker, Kubernetes).

## When to Use This Skill

Trigger this skill when:
- User provides a log file path or uploads a log file
- User says "parse this log", "analyze these logs", or "read log file"
- User mentions specific log types: "Apache logs", "Nginx access logs", "syslog"
- User asks to "extract data from logs" or "process log files"
- Any task requiring log file reading as the first step

## Instructions

### Step 1: Identify Log Format

Detect the log format by examining the file structure:

```python
from tools.log_parser import LogParser

parser = LogParser()
log_format = parser.detect_format(log_file_path)
```

**Supported formats**:
- **Apache/Nginx**: Common/Combined access log format
- **Syslog**: RFC3164 and RFC5424 formats
- **JSON**: One JSON object per line
- **Application**: Custom application logs with timestamps
- **Docker**: Docker container logs
- **Kubernetes**: K8s pod logs

**Format detection logic**:
1. Check for JSON structure (starts with `{`)
2. Look for Apache/Nginx patterns (IP address at start, HTTP status codes)
3. Check for syslog format (priority, timestamp, hostname)
4. Check for Docker/K8s identifiers
5. Fallback to generic timestamp-based parsing

### Step 2: Parse Log Entries

Parse each log line into structured format:

```python
parsed_logs = parser.parse_file(
    file_path=log_file_path,
    log_format=log_format,
    max_lines=100000
)
```

**Expected output structure**:
```python
{
    "format": "apache",
    "total_lines": 15234,
    "parsed_lines": 15200,
    "errors": 34,
    "entries": [
        {
            "timestamp": "2026-05-21T10:23:45Z",
            "level": "INFO",
            "ip_address": "192.168.1.100",
            "method": "GET",
            "path": "/api/users",
            "status_code": 200,
            "response_time": 0.125,
            "message": "Request successful",
            "raw_line": "..."
        },
        ...
    ],
    "metadata": {
        "start_time": "2026-05-21T00:00:00Z",
        "end_time": "2026-05-21T23:59:59Z",
        "duration_hours": 24
    }
}
```

### Step 3: Extract Key Fields

For each log format, extract relevant fields:

**Apache/Nginx logs**:
- IP address
- Timestamp
- HTTP method (GET, POST, etc.)
- Request path/URL
- Status code
- Response size
- User agent
- Referer

**Syslog**:
- Timestamp
- Hostname
- Process name/PID
- Severity level
- Message

**JSON logs**:
- All JSON fields preserved
- Timestamp normalization
- Level/severity extraction

**Application logs**:
- Timestamp
- Log level (ERROR, WARN, INFO, DEBUG)
- Thread/Process ID
- Logger name
- Message
- Stack trace (if present)

Execute field extraction:
```python
python scripts/extract_fields.py --input logs.txt --format apache --output parsed.json
```

### Step 4: Normalize Timestamps

Convert all timestamps to ISO 8601 format (UTC):

```python
normalized_logs = parser.normalize_timestamps(parsed_logs)
```

**Common timestamp formats handled**:
- Apache: `[21/May/2026:10:23:45 +0000]`
- ISO 8601: `2026-05-21T10:23:45Z`
- Unix epoch: `1716285825`
- Syslog: `May 21 10:23:45`
- Custom formats configurable via regex

**Timestamp parsing script**:
```python
python scripts/normalize_timestamps.py --input parsed.json --output normalized.json
```

### Step 5: Handle Multiline Entries

Detect and combine multiline log entries (e.g., stack traces):

```python
combined_logs = parser.combine_multiline(
    parsed_logs,
    multiline_patterns=["Exception", "Traceback", "Stack trace"]
)
```

**Multiline detection rules**:
1. Lines starting with whitespace/tab → continuation of previous entry
2. Stack trace patterns (e.g., `at java.lang.`, `File "/path"`)
3. Exception indicators followed by indented lines
4. Custom patterns defined in `references/multiline-patterns.txt`

### Step 6: Chunk Large Files

For files exceeding size limits, process in chunks:

```python
for chunk in parser.parse_in_chunks(
    file_path=log_file_path,
    chunk_size=10000
):
    # Process each chunk
    process_log_chunk(chunk)
```

**Chunking strategy**:
- Read 10,000 lines per chunk (configurable)
- Maintain state across chunks for multiline entries
- Aggregate statistics after all chunks processed
- Memory-efficient streaming for large files

### Step 7: Validate and Report

Validate parsed data and report statistics:

```python
validation = parser.validate_parsed_logs(parsed_logs)

print(f"Total lines: {validation['total_lines']}")
print(f"Successfully parsed: {validation['parsed_lines']}")
print(f"Parse errors: {validation['errors']}")
print(f"Format: {validation['format']}")
```

**Validation checks**:
- Timestamp validity (all entries have valid timestamps)
- Required field presence
- Data type correctness
- Format consistency
- Parse error rate < 5%

## Error Handling

### Unrecognized Format
**Error**: Cannot detect log format
**Cause**: File doesn't match any known patterns
**Solution**:
1. Check first 100 lines for patterns
2. Try generic timestamp-based parsing
3. Ask user to specify format manually
4. Provide format detection hints based on content

### Parse Errors
**Error**: Failed to parse line N
**Cause**: Malformed log entry or unexpected format
**Solution**:
1. Skip malformed lines, log error
2. Collect all parse errors for review
3. If error rate > 10%, ask user to verify format
4. Provide sample of unparseable lines

### Large File Timeout
**Error**: File processing exceeds time limit
**Cause**: File too large or complex parsing logic
**Solution**:
1. Process in chunks with progress reporting
2. Sample logs if file > 100MB
3. Adjust chunk size based on file size
4. Offer to process subset (e.g., last 24 hours)

### Encoding Issues
**Error**: Unicode decode error
**Cause**: File has non-UTF-8 encoding
**Solution**:
1. Try common encodings (UTF-8, Latin-1, ASCII)
2. Use error handling mode ('replace' or 'ignore')
3. Report encoding used
4. Recommend file re-encoding if needed

## Examples

### Example 1: Parse Apache Access Log

**User says**: "Parse this Apache access log: /var/log/apache2/access.log"

**Actions**:
1. Detect format: Apache Combined Log Format
2. Parse each line extracting IP, timestamp, method, path, status
3. Normalize all timestamps to ISO 8601
4. Return 15,234 parsed entries

**Result**: Structured data with all HTTP requests, ready for error detection

### Example 2: Parse JSON Application Logs

**User says**: "Analyze this JSON log file: app.log"

**Actions**:
1. Detect format: JSON (one object per line)
2. Parse JSON objects, extract timestamp and level fields
3. Preserve all JSON attributes
4. Normalize timestamps
5. Return 8,492 parsed entries

**Result**: Structured JSON data with normalized timestamps

### Example 3: Parse Kubernetes Pod Logs

**User says**: "Read logs from k8s-pod.log"

**Actions**:
1. Detect format: Kubernetes pod logs
2. Extract container ID, pod name, namespace
3. Parse application logs within K8s format
4. Handle multiline stack traces
5. Return 23,156 parsed entries with K8s metadata

**Result**: Parsed logs with Kubernetes context preserved

## Performance Optimization

### Streaming vs. Loading
- **Small files (<10MB)**: Load entirely into memory
- **Medium files (10-100MB)**: Stream with 10K line chunks
- **Large files (>100MB)**: Stream with 50K line chunks or sample

### Caching
- Cache regex patterns (compile once)
- Cache format detection (don't re-detect per file)
- Cache timezone conversions

### Parallel Processing
- For multiple files: process in parallel
- For single large file: sequential (preserve order)

### Memory Management
- Release processed chunks immediately
- Don't store raw lines unless needed
- Store only structured data

## Integration with Other Skills

### With error-detection
After parsing, error-detection skill:
- Receives parsed entries
- Filters by log level (ERROR, CRITICAL)
- Categorizes error types

### With pattern-analysis
Pattern analysis uses:
- Normalized timestamps for time-series analysis
- Structured fields for pattern matching
- Message text for similarity detection

### With report-generation
Report generation uses:
- Parse statistics (success rate, format info)
- Sample entries for report examples
- Metadata (time range, total entries)

## Best Practices

1. **Always detect format first** - Don't assume
2. **Normalize timestamps early** - Simplifies later analysis
3. **Handle multiline entries** - Critical for stack traces
4. **Validate parse rate** - Alert if < 90% parse success
5. **Preserve raw lines** - Include in output for verification
6. **Report parsing statistics** - Total, parsed, errors
7. **Use streaming for large files** - Don't load all into memory

## Troubleshooting

### Low Parse Success Rate
If < 90% of lines parse successfully:
1. Review format detection decision
2. Check sample of unparsed lines
3. Look for custom format variations
4. Add custom patterns if needed

### Slow Performance
If parsing takes too long:
1. Check file size - consider sampling
2. Verify chunk size is appropriate
3. Reduce regex complexity
4. Process in parallel if multiple files

### Memory Issues
If running out of memory:
1. Reduce chunk size
2. Don't store raw lines
3. Process and discard immediately
4. Use streaming exclusively

### Timestamp Parsing Failures
If timestamps don't parse:
1. Check timezone handling
2. Verify timestamp format regex
3. Look for custom timestamp formats
4. Add format to `references/timestamp-formats.txt`

## References

See `references/log-formats.md` for:
- Complete format specifications
- Regex patterns for each format
- Field definitions and types
- Example log entries

See `references/timestamp-formats.md` for:
- All supported timestamp formats
- Timezone handling rules
- Parsing priority order
- Custom format configuration
