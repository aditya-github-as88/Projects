---
name: error-detection
description: "Detects and categorizes errors from parsed log data. Use when user mentions 'find errors', 'detect issues', 'identify problems', or 'show error logs'. Also triggers on 'error analysis', 'critical errors', or 'failure investigation'."
compatibility: "Works with claude.ai, Claude Code, and API. Requires parsed log data from log-parsing skill."
license: MIT
metadata:
  author: Log Analyzer Team
  version: 1.0.0
  category: error-analysis
  depends-on: [log-parsing]
  tags: [errors, detection, categorization, debugging]
---

# Error Detection Skill

## Purpose

This skill identifies, categorizes, and analyzes errors in parsed log data. It detects error patterns, groups similar errors, calculates error rates, and identifies critical issues requiring immediate attention. Works on output from the log-parsing skill.

## When to Use This Skill

Trigger this skill when:
- User asks to "find errors" or "detect problems"
- User mentions "show me errors", "what failed", or "critical issues"
- User requests "error analysis" or "failure investigation"
- After log-parsing completes and user needs error insights
- User asks about "error rates", "failure patterns", or "exception analysis"

## Instructions

### Step 1: Filter Error-Level Entries

Extract entries with error severity levels:

```python
from tools.error_detector import ErrorDetector

detector = ErrorDetector()
error_entries = detector.filter_errors(
    parsed_logs,
    levels=["CRITICAL", "ERROR", "FATAL", "PANIC"]
)
```

**Severity level mapping**:
- **CRITICAL/FATAL**: System-breaking errors
- **ERROR**: Application errors, exceptions
- **WARNING**: Potential issues
- **INFO/DEBUG**: Excluded from error detection

**Filtering logic**:
1. Check `level` field if present
2. Scan message for error keywords if no level field
3. Check status codes (5xx = server errors)
4. Look for exception indicators

### Step 2: Categorize Errors

Group errors into categories by type:

```python
categorized_errors = detector.categorize_errors(error_entries)
```

**Error categories**:
- **Database Errors**: Connection failures, query errors, timeouts
- **Network Errors**: Connection refused, timeouts, DNS failures
- **Authentication Errors**: Auth failures, token expired, permission denied
- **Application Errors**: NullPointer, IndexOutOfBounds, runtime exceptions
- **Configuration Errors**: Missing config, invalid settings
- **Resource Errors**: Out of memory, disk full, file not found
- **Timeout Errors**: Request timeouts, slow queries
- **Validation Errors**: Invalid input, constraint violations

**Categorization methods**:
- Keyword matching in error messages
- Exception class names
- Error codes
- Stack trace analysis
- HTTP status codes (for web logs)

Execute:
```python
python scripts/categorize_errors.py --input parsed.json --output categorized.json
```

### Step 3: Extract Error Details

For each error, extract detailed information:

```python
error_details = detector.extract_error_details(categorized_errors)
```

**Details extracted**:
- **Error message**: Full error text
- **Exception type**: Class name (e.g., `NullPointerException`)
- **Stack trace**: If present
- **Timestamp**: When error occurred
- **Frequency**: How many times this error appears
- **Affected component**: Service, module, or function
- **User/Session**: If identifiable
- **Request context**: URL, method, parameters

**Output structure**:
```python
{
    "error_id": "ERR001",
    "category": "database",
    "type": "ConnectionTimeout",
    "message": "Connection to database timed out after 30s",
    "stack_trace": "...",
    "first_seen": "2026-05-21T10:23:45Z",
    "last_seen": "2026-05-21T15:42:12Z",
    "occurrences": 47,
    "affected_endpoints": ["/api/users", "/api/orders"],
    "severity": "ERROR",
    "examples": [...]  # Sample log entries
}
```

### Step 4: Group Similar Errors

Identify duplicate/similar errors to find patterns:

```python
grouped_errors = detector.group_similar_errors(
    error_details,
    similarity_threshold=0.8
)
```

**Similarity detection**:
- Error message text similarity (Levenshtein distance)
- Same exception type
- Same stack trace signature
- Same affected component

**Grouping rules**:
1. Identical error messages → same group
2. Messages with only numbers/IDs different → same group (parameterized errors)
3. Same exception with similar stack trace → same group
4. Group size limited to avoid over-grouping

**Benefit**: Reduces 10,000 errors to 50 unique error types

### Step 5: Calculate Error Metrics

Compute error statistics:

```python
metrics = detector.calculate_metrics(grouped_errors, parsed_logs)
```

**Metrics calculated**:
- **Error rate**: Errors per minute/hour
- **Error percentage**: % of total log entries that are errors
- **Error distribution**: By category, by time, by component
- **Critical error count**: Number of CRITICAL/FATAL errors
- **Top errors**: Most frequent errors
- **Error trend**: Increasing/decreasing over time
- **MTBF** (Mean Time Between Failures): Average time between errors

**Output**:
```python
{
    "total_errors": 1523,
    "unique_error_types": 47,
    "error_rate_per_hour": 63.5,
    "error_percentage": 2.3,
    "critical_errors": 12,
    "error_distribution": {
        "database": 45%,
        "network": 30%,
        "application": 25%
    },
    "trending": "increasing",  # vs. previous time period
    "mtbf_minutes": 28.5
}
```

### Step 6: Identify Critical Errors

Flag errors requiring immediate attention:

```python
critical_errors = detector.identify_critical_errors(grouped_errors)
```

**Criticality factors**:
- **Severity level**: CRITICAL/FATAL automatically flagged
- **Frequency**: Occurring > 100 times/hour
- **Impact**: Affecting multiple users/sessions
- **Trend**: Rapidly increasing error rate
- **Business impact**: Errors in payment/checkout/auth systems
- **Data loss**: Errors involving data corruption/loss

**Critical error indicators**:
- Database connection failures (affect all users)
- Out of memory errors (service crash)
- Authentication system failures (security issue)
- Payment processing errors (revenue impact)
- Data corruption errors (data integrity)

Execute:
```python
python scripts/identify_critical.py --input categorized.json --output critical.json
```

### Step 7: Generate Error Timeline

Create timeline showing when errors occurred:

```python
timeline = detector.create_error_timeline(
    grouped_errors,
    interval="1hour"  # or "5min", "1day"
)
```

**Timeline structure**:
```python
{
    "interval": "1hour",
    "time_range": {
        "start": "2026-05-21T00:00:00Z",
        "end": "2026-05-21T23:59:59Z"
    },
    "buckets": [
        {
            "timestamp": "2026-05-21T00:00:00Z",
            "total_errors": 45,
            "by_category": {
                "database": 20,
                "network": 15,
                "application": 10
            },
            "critical_errors": 2
        },
        ...
    ]
}
```

**Use cases**:
- Identify error spikes
- Correlate with deployments/changes
- Detect patterns (errors at specific times)
- Visualize error trends

## Error Handling

### No Errors Found
**Condition**: No error-level entries in logs
**Action**:
1. Report success: "No errors detected"
2. Show warning count if warnings present
3. Provide summary statistics
4. Confirm log coverage (time range)

### Too Many Errors
**Condition**: > 10,000 unique errors
**Action**:
1. Focus on critical errors first
2. Group aggressively (higher similarity threshold)
3. Sample less frequent errors
4. Recommend filtering by time range or component

### Incomplete Stack Traces
**Condition**: Error logged without stack trace
**Action**:
1. Use error message for categorization
2. Flag as "incomplete information"
3. Group by message similarity
4. Recommend enabling detailed logging

### Ambiguous Error Messages
**Condition**: Generic errors like "Error occurred"
**Action**:
1. Use surrounding context for categorization
2. Check for error codes
3. Analyze timing patterns
4. Recommend improving error messages

## Examples

### Example 1: Detect Database Errors

**Input**: 50,000 parsed log entries
**User says**: "Find all database errors"

**Actions**:
1. Filter for ERROR/CRITICAL levels
2. Identify database-related keywords: "connection", "query", "timeout", "SQLException"
3. Group similar errors
4. Found: 247 database errors in 8 unique types
5. Top error: "Connection timeout" (134 occurrences)

**Result**: Database errors categorized, showing connection pool exhaustion pattern

### Example 2: Critical Error Investigation

**Input**: Parsed logs from production system
**User says**: "Show me critical errors from the last hour"

**Actions**:
1. Filter logs from last 60 minutes
2. Extract CRITICAL and FATAL level errors
3. Identify 12 critical errors
4. Top critical: "OutOfMemoryError" occurring every 3 minutes
5. Impact: Affecting 500+ users

**Result**: Critical errors identified, memory issue flagged for immediate action

### Example 3: Error Trend Analysis

**Input**: 24 hours of parsed logs
**User says**: "Analyze error trends over the past day"

**Actions**:
1. Create hourly timeline of errors
2. Calculate error rate per hour
3. Identify spike at 14:00-15:00 (600 errors vs. baseline 50/hour)
4. Categorize spike errors: 95% network timeouts
5. Correlate with deployment at 13:55

**Result**: Error spike linked to deployment, network timeout issue identified

## Performance Optimization

### Efficient Filtering
- Index logs by level field
- Use binary search for timestamp filtering
- Skip INFO/DEBUG early

### Smart Grouping
- Hash error messages for quick comparison
- Use sampling for > 10K errors
- Cache similarity calculations

### Parallel Processing
- Categorize errors in parallel
- Process time buckets concurrently
- Aggregate results at end

## Integration with Other Skills

### With log-parsing
Receives:
- Parsed log entries
- Normalized timestamps
- Extracted fields

### With pattern-analysis
Provides:
- Categorized errors for pattern detection
- Error frequencies for anomaly detection
- Timeline data for correlation analysis

### With report-generation
Provides:
- Error summaries and statistics
- Top errors list
- Critical errors section
- Error timeline for charts

## Best Practices

1. **Start with critical errors** - Triage by severity
2. **Group similar errors** - Reduce noise
3. **Calculate error rates** - Context matters
4. **Identify trends** - Increasing errors need attention
5. **Provide examples** - Include sample log entries
6. **Link related errors** - Same root cause
7. **Consider impact** - User-facing vs. internal

## Troubleshooting

### False Positives
If detecting non-errors as errors:
1. Refine keyword list
2. Check log level mapping
3. Exclude known patterns (warnings that aren't errors)
4. Adjust categorization rules

### Missed Errors
If not catching known errors:
1. Add error keywords
2. Check log level detection
3. Scan for exceptions without ERROR level
4. Review categorization coverage

### Over-Grouping
If unrelated errors grouped together:
1. Lower similarity threshold
2. Require exact exception type match
3. Use stack trace for differentiation
4. Add context-based grouping

### Slow Performance
If error detection is slow:
1. Filter by level earlier
2. Sample if > 100K errors
3. Process time buckets in parallel
4. Cache frequent operations

## References

See `references/error-patterns.md` for:
- Common error patterns by type
- Error categorization rules
- Exception type mappings
- Keyword dictionaries

See `references/error-severity.md` for:
- Severity level definitions
- Criticality criteria
- Business impact assessment
- Priority assignment rules
