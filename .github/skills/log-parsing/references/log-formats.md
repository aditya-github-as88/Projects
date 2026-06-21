# Log Format Reference

This document provides detailed specifications for all supported log formats.

## Apache Combined Log Format

### Format Specification
```
%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-agent}i"
```

### Example
```
192.168.1.100 - - [21/May/2026:10:23:45 +0000] "GET /api/users HTTP/1.1" 200 1234 "https://example.com" "Mozilla/5.0"
```

### Fields
- `%h`: Client IP address
- `%l`: Identity (usually `-`)
- `%u`: User ID (usually `-`)
- `%t`: Timestamp
- `%r`: Request (method, path, protocol)
- `%>s`: Status code
- `%b`: Response size in bytes
- `%{Referer}i`: Referer header
- `%{User-agent}i`: User agent string

### Regex Pattern
```regex
(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>[^\s]+) HTTP/[^"]+" (?P<status>\d+) (?P<size>\d+|-) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"
```

## Nginx Log Format

### Format Specification
Similar to Apache Combined, with slight variations.

### Example
```
192.168.1.100 - - [21/May/2026:10:23:45 +0000] "GET /api/users HTTP/1.1" 200 1234 "https://example.com" "Mozilla/5.0"
```

### Additional Fields (if configured)
- `$request_time`: Request processing time
- `$upstream_response_time`: Backend response time
- `$pipe`: Pipelined request indicator

## Syslog Format (RFC3164)

### Format Specification
```
<priority>timestamp hostname process[pid]: message
```

### Example
```
May 21 10:23:45 webserver nginx[1234]: Connection established
```

### Fields
- `priority`: Facility and severity (often omitted in logs)
- `timestamp`: Month Day HH:MM:SS
- `hostname`: Server hostname
- `process`: Process name
- `pid`: Process ID
- `message`: Log message

### Regex Pattern
```regex
(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+) (?P<hostname>\S+) (?P<process>\w+)(\[(?P<pid>\d+)\])?: (?P<message>.*)
```

## JSON Log Format

### Format Specification
One JSON object per line (JSONL/NDJSON format).

### Example
```json
{"timestamp":"2026-05-21T10:23:45Z","level":"INFO","message":"User logged in","user_id":12345}
```

### Common Fields
- `timestamp` or `time` or `@timestamp`: ISO 8601 timestamp
- `level` or `severity`: Log level
- `message` or `msg`: Log message
- Custom fields: Any additional JSON fields

## Application Log Format

### Format Specification
Generic format with timestamp, level, and message.

### Example
```
2026-05-21T10:23:45Z [INFO] UserService: User 12345 logged in
```

### Pattern
```
timestamp [level] component: message
```

### Variations
- With thread ID: `timestamp [level] [thread-id] component: message`
- With logger name: `timestamp [level] logger.name - message`
- Custom formats configurable via regex

## Docker Container Logs

### Format Specification
Docker wraps application logs with metadata.

### Example
```json
{"log":"Application started\n","stream":"stdout","time":"2026-05-21T10:23:45.123456789Z"}
```

### Fields
- `log`: The actual log message
- `stream`: stdout or stderr
- `time`: ISO 8601 timestamp

### Alternative Format
```
2026-05-21T10:23:45.123456789Z [container_id] Application started
```

## Kubernetes Pod Logs

### Format Specification
K8s logs include pod metadata and application logs.

### Example
```json
{
  "log": "Application started\n",
  "stream": "stdout",
  "time": "2026-05-21T10:23:45.123456789Z",
  "kubernetes": {
    "pod_name": "myapp-abc123",
    "namespace_name": "production",
    "container_name": "app"
  }
}
```

### Fields
- Standard Docker log fields
- `kubernetes.pod_name`: Pod identifier
- `kubernetes.namespace_name`: Namespace
- `kubernetes.container_name`: Container within pod

## Custom Format

For logs that don't match known patterns, the parser attempts to extract:

1. **Timestamp**: Any ISO 8601 or recognizable date/time format
2. **Log Level**: Keywords like ERROR, WARN, INFO, DEBUG
3. **Message**: Remaining content

### Best Effort Parsing

The custom parser:
- Searches for timestamp patterns
- Looks for log level keywords
- Treats remaining text as message
- Preserves raw line for reference

## Timestamp Formats

### Supported Formats

| Format | Example | Notes |
|--------|---------|-------|
| ISO 8601 | `2026-05-21T10:23:45Z` | Preferred format |
| ISO 8601 with TZ | `2026-05-21T10:23:45+05:30` | With timezone |
| ISO 8601 with ms | `2026-05-21T10:23:45.123Z` | With milliseconds |
| Apache | `21/May/2026:10:23:45 +0000` | Apache/Nginx format |
| Syslog | `May 21 10:23:45` | No year, uses current |
| Unix Epoch | `1716285825` | Seconds since 1970 |
| Unix Epoch ms | `1716285825123` | Milliseconds since 1970 |

### Timezone Handling

- All timestamps normalized to UTC
- Timezone info preserved if present
- Local time converted to UTC when possible

## Field Definitions

### Common Fields Across Formats

| Field | Type | Description |
|-------|------|-------------|
| timestamp | string | ISO 8601 timestamp (UTC) |
| level | string | Log level (ERROR, WARN, INFO, DEBUG) |
| message | string | Log message text |
| ip_address | string | Client IP (web logs) |
| method | string | HTTP method (web logs) |
| path | string | URL path (web logs) |
| status_code | integer | HTTP status code |
| response_size | integer | Response size in bytes |
| response_time | float | Processing time in seconds |
| user_agent | string | User agent string |
| referer | string | HTTP referer |
| hostname | string | Server hostname |
| process | string | Process/service name |
| pid | integer | Process ID |

### Extended Fields (Format Specific)

- **Application Logs**: logger, thread, class, method
- **Docker**: container_id, container_name
- **Kubernetes**: pod_name, namespace, labels
- **Web Logs**: session_id, user_id, cache_status

## Log Level Mapping

### Standard Levels

| Level | Severity | Description |
|-------|----------|-------------|
| DEBUG | 7 | Detailed debug information |
| INFO | 6 | Informational messages |
| NOTICE | 5 | Normal but significant |
| WARNING/WARN | 4 | Warning messages |
| ERROR | 3 | Error conditions |
| CRITICAL/CRIT | 2 | Critical conditions |
| ALERT | 1 | Immediate action required |
| EMERGENCY/PANIC | 0 | System unusable |

### HTTP Status Code Mapping

| Status Code | Log Level |
|-------------|-----------|
| 2xx | INFO |
| 3xx | INFO |
| 4xx | WARNING |
| 5xx | ERROR |

## Multiline Patterns

### Stack Traces (Java)
```
Exception in thread "main" java.lang.NullPointerException
    at com.example.MyClass.method(MyClass.java:123)
    at com.example.Main.main(Main.java:45)
```

### Stack Traces (Python)
```
Traceback (most recent call last):
  File "script.py", line 10, in <module>
    main()
  File "script.py", line 5, in main
    raise ValueError("Error")
ValueError: Error
```

### Multiline Messages
```
2026-05-21 10:23:45 [ERROR] Processing failed
Additional context line 1
Additional context line 2
End of multiline message
```

### Detection Rules

1. Lines starting with whitespace = continuation
2. Exception keywords followed by indented lines
3. "Caused by" or "Suppressed" in Java traces
4. "File" in Python traces

## Format Detection Algorithm

1. **Check first 100 lines** for patterns
2. **Score each format** based on matches:
   - JSON: Lines start with `{` → +1 per match
   - Apache/Nginx: Regex match → +1 per match
   - Syslog: Pattern match → +1 per match
   - Docker/K8s: Specific keywords → +1 per match
3. **Return highest scoring format**
4. **Fallback to custom** if no clear winner

## Best Practices

1. **Validate Format**: Check parse success rate (>90% expected)
2. **Handle Errors**: Log unparseable lines for review
3. **Preserve Raw Data**: Keep original line for debugging
4. **Normalize Early**: Convert timestamps immediately
5. **Extract Completely**: Get all relevant fields
6. **Document Custom Formats**: Add patterns for new formats

## Adding New Formats

To add support for a new format:

1. Define regex pattern
2. Create parser function
3. Add to format detection logic
4. Test with sample logs
5. Document format specification
6. Add to this reference

## Examples

See `examples/` directory for sample logs in each format.
