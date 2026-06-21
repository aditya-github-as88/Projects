# Error Patterns Reference

This document catalogs common error patterns and how to detect them.

## Error Categories

### Database Errors

**Keywords**: connection, query, sql, database, timeout, deadlock, constraint

**Common Patterns**:
```
- Connection timeout
- Connection refused
- Too many connections
- Deadlock detected
- Query timeout
- Constraint violation
- Table doesn't exist
- Syntax error in SQL
```

**Example Messages**:
```
java.sql.SQLException: Connection timed out
Could not connect to database: Connection refused
FATAL: too many connections for role "user"
ERROR: deadlock detected
Query execution timeout after 30 seconds
```

**Severity**: Usually ERROR or CRITICAL

**Recommended Actions**:
- Check connection pool settings
- Verify database is running
- Review query performance
- Check for lock contention

### Network Errors

**Keywords**: connection refused, timeout, network, socket, dns, unreachable

**Common Patterns**:
```
- Connection refused
- Network timeout
- DNS resolution failure
- Host unreachable
- Socket error
- Connection reset
```

**Example Messages**:
```
Connection refused to host:port
Network timeout after 30s
DNS lookup failed for hostname
No route to host
Connection reset by peer
```

**Severity**: ERROR or WARNING

**Recommended Actions**:
- Verify network connectivity
- Check firewall rules
- Confirm service is running
- Review DNS configuration

### Authentication Errors

**Keywords**: auth, authentication, unauthorized, forbidden, permission denied

**Common Patterns**:
```
- Invalid credentials
- Token expired
- Permission denied
- Unauthorized access
- Authentication failed
- Access denied
```

**Example Messages**:
```
Authentication failed for user
Invalid credentials provided
Access token has expired
Permission denied for resource
User not authorized to perform action
```

**Severity**: WARNING or ERROR

**Recommended Actions**:
- Verify credentials
- Check token expiration
- Review permissions
- Audit access logs

### Application Errors

**Keywords**: exception, nullpointer, runtime, assertion, index

**Common Patterns**:
```
- NullPointerException
- IndexOutOfBoundsException
- IllegalArgumentException
- RuntimeException
- AssertionError
- ClassCastException
```

**Example Messages**:
```
java.lang.NullPointerException at method()
IndexOutOfBoundsException: Index 5 out of bounds for length 3
IllegalArgumentException: Invalid parameter value
Unexpected runtime error in processing
```

**Severity**: ERROR

**Recommended Actions**:
- Review stack trace
- Check input validation
- Add null checks
- Verify array bounds

### Configuration Errors

**Keywords**: config, configuration, missing, not found, invalid

**Common Patterns**:
```
- Missing configuration
- Invalid configuration value
- File not found
- Property not set
- Environment variable missing
```

**Example Messages**:
```
Configuration file not found: config.yml
Missing required property: database.url
Invalid value for setting: max_connections
Environment variable DB_HOST not set
```

**Severity**: CRITICAL or ERROR

**Recommended Actions**:
- Verify configuration files exist
- Check environment variables
- Validate configuration values
- Review deployment process

### Resource Errors

**Keywords**: memory, disk, cpu, out of, full, exhausted

**Common Patterns**:
```
- Out of memory
- Disk full
- CPU overload
- Connection pool exhausted
- Thread pool exhausted
- File handle limit reached
```

**Example Messages**:
```
java.lang.OutOfMemoryError: Java heap space
Disk space exhausted on /var
CPU usage at 100%
Connection pool exhausted, waiting for available connection
Too many open files
```

**Severity**: CRITICAL

**Recommended Actions**:
- Increase resource limits
- Check for memory leaks
- Clean up disk space
- Scale resources
- Review resource allocation

### Timeout Errors

**Keywords**: timeout, timed out, deadline, expired

**Common Patterns**:
```
- Request timeout
- Connection timeout
- Read timeout
- Operation timeout
- Deadline exceeded
```

**Example Messages**:
```
Request timed out after 30s
Connection timeout to remote service
Read timeout on socket
Operation timed out waiting for response
context deadline exceeded
```

**Severity**: WARNING or ERROR

**Recommended Actions**:
- Increase timeout values
- Optimize slow operations
- Check network latency
- Review service performance

### Validation Errors

**Keywords**: validation, invalid, constraint, format, parse

**Common Patterns**:
```
- Invalid input format
- Validation failed
- Constraint violation
- Parse error
- Format mismatch
```

**Example Messages**:
```
Validation failed for field: email
Invalid date format: expected YYYY-MM-DD
Constraint violation: value out of range
Parse error: malformed JSON
```

**Severity**: WARNING

**Recommended Actions**:
- Review input validation
- Check data formats
- Validate constraints
- Improve error messages

## Error Detection Strategies

### 1. Level-Based Detection

Check the `level` field:
```python
if entry.get('level') in ['CRITICAL', 'ERROR', 'FATAL']:
    # This is an error
```

### 2. Keyword-Based Detection

Search message for error keywords:
```python
error_keywords = ['error', 'exception', 'failed', 'failure']
message = entry.get('message', '').lower()
if any(kw in message for kw in error_keywords):
    # Likely an error
```

### 3. Status Code Detection

For web logs, check HTTP status:
```python
status = entry.get('status_code', 0)
if status >= 500:
    # Server error
elif status >= 400:
    # Client error (maybe warning)
```

### 4. Exception Detection

Look for exception class names:
```python
import re
exception_pattern = r'(\w+Exception|\w+Error)'
if re.search(exception_pattern, message):
    # Contains exception
```

## Error Grouping

### Parameterization

Remove specific values to group similar errors:

**Before**:
```
Connection timeout to server 192.168.1.100:3306
Connection timeout to server 192.168.1.101:3306
Connection timeout to server 192.168.1.102:3306
```

**After Parameterization**:
```
Connection timeout to server <IP>:<PORT>
```

**Regex Replacements**:
```python
# Remove IP addresses
message = re.sub(r'\d+\.\d+\.\d+\.\d+', '<IP>', message)

# Remove port numbers
message = re.sub(r':(\d+)', ':<PORT>', message)

# Remove numbers
message = re.sub(r'\d+', '<NUM>', message)

# Remove UUIDs
message = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<UUID>', message)

# Remove hexadecimal IDs
message = re.sub(r'[0-9a-fA-F]{8,}', '<ID>', message)
```

### Similarity Matching

Compare parameterized messages:

```python
def are_similar(msg1, msg2, threshold=0.8):
    words1 = set(msg1.lower().split())
    words2 = set(msg2.lower().split())
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    similarity = len(intersection) / len(union)
    return similarity >= threshold
```

## Critical Error Identification

### Indicators

An error is critical if:

1. **Severity Level**: CRITICAL, FATAL, PANIC
2. **High Frequency**: Occurring > 100 times/hour
3. **Business Impact**: Affects payment, auth, data integrity
4. **System Impact**: Out of memory, disk full, crash
5. **Security Impact**: Authentication bypass, data breach

### Priority Matrix

| Impact | Frequency | Priority |
|--------|-----------|----------|
| High | High | P0 (Critical) |
| High | Low | P1 (High) |
| Low | High | P2 (Medium) |
| Low | Low | P3 (Low) |

### Examples

**P0 - Critical**:
```
- OutOfMemoryError (affects all users)
- Database connection pool exhausted (service down)
- Payment processing failure (revenue impact)
```

**P1 - High**:
```
- Authentication service degraded (some users affected)
- Slow query detected (performance impact)
- API rate limit exceeded (some requests failing)
```

**P2 - Medium**:
```
- Cache miss rate increased (minor performance impact)
- Validation warning (data quality issue)
- Deprecated API usage (future breaking change)
```

**P3 - Low**:
```
- Debug message in production (log noise)
- Non-critical feature unavailable (workaround exists)
- Configuration recommendation (optimization opportunity)
```

## Stack Trace Processing

### Extracting Stack Traces

Java example:
```
Exception in thread "main" java.lang.NullPointerException: Cannot invoke method on null object
    at com.example.UserService.getUser(UserService.java:45)
    at com.example.UserController.handleRequest(UserController.java:23)
    at javax.servlet.http.HttpServlet.service(HttpServlet.java:790)
```

**Extract**:
- Exception type: `NullPointerException`
- Message: `Cannot invoke method on null object`
- Stack frames: List of method calls
- Source file/line: For each frame

### Stack Trace Signature

Create signature for grouping:
```python
def stack_signature(stack_trace):
    # Take top 3 frames from application code
    app_frames = [
        frame for frame in frames
        if 'com.example' in frame  # Your package
    ][:3]
    
    return ' -> '.join(app_frames)
```

## Error Message Patterns

### Regex Patterns

**Java Exceptions**:
```regex
(\w+Exception): (.+?)(?:\n|\r|$)
```

**Python Exceptions**:
```regex
(\w+Error): (.+?)(?:\n|\r|$)
```

**Generic Error**:
```regex
(?i)error:?\s*(.+)
```

**HTTP Errors**:
```regex
HTTP (\d{3}) (.+)
```

## Best Practices

1. **Categorize Consistently**: Use same categories across all logs
2. **Parameterize Early**: Group similar errors before analysis
3. **Preserve Context**: Keep original message for reference
4. **Calculate Metrics**: Error rate, frequency, trends
5. **Prioritize**: Focus on critical errors first
6. **Track Over Time**: Monitor error trends
7. **Root Cause**: Link related errors
8. **Document Patterns**: Update this reference with new patterns

## Tools

### Error Detection
- `tools/error_detector.py`: Main error detection tool
- `scripts/categorize_errors.py`: Categorization script

### Reference Data
- `error-patterns.md`: This file
- `error-severity.md`: Severity definitions

## Examples

See `examples/errors/` for sample error logs demonstrating each category.
