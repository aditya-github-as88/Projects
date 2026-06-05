---
name: pattern-analysis
description: "Analyzes patterns, trends, and anomalies in log data. Use when user mentions 'find patterns', 'detect anomalies', 'analyze trends', or 'identify unusual behavior'. Also triggers on 'pattern detection', 'anomaly detection', or 'trend analysis'."
compatibility: "Works with claude.ai, Claude Code, and API. Requires parsed logs and optionally error detection results."
license: MIT
metadata:
  author: Log Analyzer Team
  version: 1.0.0
  category: pattern-analysis
  depends-on: [log-parsing]
  tags: [patterns, anomalies, trends, analysis, detection]
---

# Pattern Analysis Skill

## Purpose

This skill identifies patterns, trends, and anomalies in log data. It detects recurring sequences, unusual spikes, behavioral changes, and correlations. Helps identify root causes, predict issues, and understand system behavior over time.

## When to Use This Skill

Trigger this skill when:
- User asks to "find patterns" or "detect anomalies"
- User mentions "unusual behavior", "strange activity", or "outliers"
- User requests "trend analysis" or "pattern detection"
- User asks "what's causing this" or "why did this happen"
- User wants to "correlate events" or "find relationships"

## Instructions

### Step 1: Identify Recurring Patterns

Find sequences or events that repeat:

```python
from tools.pattern_analyzer import PatternAnalyzer

analyzer = PatternAnalyzer()
patterns = analyzer.find_recurring_patterns(
    parsed_logs,
    min_frequency=3  # Must occur at least 3 times
)
```

**Pattern types detected**:
- **Temporal patterns**: Events occurring at specific times (every hour, daily)
- **Sequence patterns**: Event A always followed by Event B
- **Request patterns**: Same endpoint called repeatedly with specific parameters
- **Error patterns**: Same error with predictable triggers
- **User behavior patterns**: Typical user actions

**Pattern structure**:
```python
{
    "pattern_id": "PAT001",
    "type": "temporal",
    "description": "Database connection errors every 30 minutes",
    "frequency": 48,  # Occurred 48 times
    "confidence": 0.95,
    "first_seen": "2026-05-21T00:00:00Z",
    "last_seen": "2026-05-21T23:59:59Z",
    "examples": [...]  # Sample occurrences
}
```

Execute:
```python
python scripts/find_patterns.py --input parsed.json --min-freq 3 --output patterns.json
```

### Step 2: Detect Anomalies

Identify unusual events or behaviors:

```python
anomalies = analyzer.detect_anomalies(
    parsed_logs,
    threshold=0.05  # 5% deviation = anomaly
)
```

**Anomaly detection methods**:
1. **Statistical**: Values beyond mean ± 3 standard deviations
2. **Frequency-based**: Events occurring much more/less than expected
3. **Sequential**: Unexpected event sequences
4. **Time-based**: Events at unusual times
5. **Volume-based**: Sudden spikes or drops

**Anomaly types**:
- **Volume anomalies**: Request spike (10x normal)
- **Error anomalies**: Error rate spike
- **Response time anomalies**: Slow requests
- **Behavioral anomalies**: Unusual user actions
- **Missing data anomalies**: Expected events didn't occur

**Output structure**:
```python
{
    "anomaly_id": "ANO001",
    "type": "volume",
    "severity": "high",
    "description": "Request volume 15x above baseline",
    "baseline": 100,  # requests/minute
    "observed": 1500,
    "deviation": 14.0,  # standard deviations
    "timestamp": "2026-05-21T14:23:00Z",
    "duration": "15 minutes",
    "possible_causes": [
        "Traffic spike",
        "Bot activity",
        "Viral content"
    ]
}
```

### Step 3: Analyze Time-Series Trends

Identify trends over time:

```python
trends = analyzer.analyze_trends(
    parsed_logs,
    metrics=["request_count", "error_rate", "response_time"],
    interval="1hour"
)
```

**Trend types**:
- **Increasing**: Metric growing over time
- **Decreasing**: Metric declining over time
- **Stable**: No significant change
- **Seasonal**: Regular patterns (hourly, daily, weekly)
- **Volatile**: High variance, unpredictable

**Metrics analyzed**:
- Request volume
- Error rate
- Response time/latency
- Resource usage (if logged)
- User activity
- Specific error counts

**Output**:
```python
{
    "metric": "error_rate",
    "trend": "increasing",
    "change_percent": 45.2,  # 45% increase
    "start_value": 1.2,  # errors per minute
    "end_value": 1.74,
    "time_range": {
        "start": "2026-05-21T00:00:00Z",
        "end": "2026-05-21T23:59:59Z"
    },
    "seasonality": "hourly",  # Peaks every hour
    "forecast": {
        "next_hour": 1.95,
        "confidence": 0.82
    }
}
```

### Step 4: Correlate Events

Find relationships between different events:

```python
correlations = analyzer.correlate_events(
    parsed_logs,
    event_types=["errors", "deployments", "traffic_spikes"]
)
```

**Correlation types**:
- **Temporal**: Event A precedes Event B
- **Causal**: Event A causes Event B
- **Concurrent**: Events A and B occur together
- **Inverse**: When A increases, B decreases

**Use cases**:
- Deployments → error spikes
- Traffic increase → response time degradation
- Specific endpoint calls → database errors
- Time of day → error types

**Output**:
```python
{
    "correlation_id": "COR001",
    "event_a": "deployment",
    "event_b": "database_errors",
    "correlation_strength": 0.89,  # Strong correlation
    "type": "temporal",
    "lag_seconds": 120,  # Errors start 2 min after deployment
    "occurrences": 12,  # Seen 12 times
    "description": "Database errors spike within 2 minutes of deployment"
}
```

Execute:
```python
python scripts/correlate_events.py --input parsed.json --output correlations.json
```

### Step 5: Identify Peak Times

Determine when system is most/least active:

```python
peak_analysis = analyzer.identify_peaks(
    parsed_logs,
    metrics=["request_volume", "error_rate"]
)
```

**Peak types**:
- **Daily peaks**: Busiest hours of the day
- **Weekly peaks**: Busiest days of the week
- **Monthly peaks**: End-of-month patterns
- **Error peaks**: When errors are most frequent

**Output**:
```python
{
    "metric": "request_volume",
    "peak_times": [
        {
            "period": "daily",
            "peak_hour": 14,  # 2 PM
            "peak_value": 5000,  # requests/hour
            "baseline": 1200
        },
        {
            "period": "weekly",
            "peak_day": "Monday",
            "peak_value": 45000,  # requests/day
            "baseline": 28000
        }
    ],
    "low_times": [
        {
            "period": "daily",
            "low_hour": 3,  # 3 AM
            "low_value": 200
        }
    ]
}
```

### Step 6: Detect Sequential Patterns

Find ordered event sequences:

```python
sequences = analyzer.find_sequences(
    parsed_logs,
    min_support=5  # Must occur at least 5 times
)
```

**Sequence examples**:
- User login → API call → database query → logout
- Request → 500 error → retry → success
- High CPU → memory increase → OOM error
- Cache miss → database query → slow response

**Output**:
```python
{
    "sequence_id": "SEQ001",
    "pattern": ["login", "api_call", "database_query", "error"],
    "frequency": 23,
    "avg_duration": "2.5 seconds",
    "success_rate": 0.35,  # Only 35% complete successfully
    "description": "Login followed by API call that queries database and fails"
}
```

### Step 7: Generate Pattern Insights

Provide actionable insights from patterns:

```python
insights = analyzer.generate_insights(
    patterns, anomalies, trends, correlations
)
```

**Insight types**:
- **Root cause identification**: What's causing errors
- **Performance bottlenecks**: Where system slows down
- **Capacity planning**: When to scale
- **Optimization opportunities**: What to improve
- **Risk factors**: Potential issues

**Output**:
```python
{
    "insights": [
        {
            "type": "root_cause",
            "severity": "high",
            "title": "Database connection pool exhaustion",
            "description": "Pattern shows DB errors every 30 min correlating with connection pool reaching max capacity",
            "evidence": ["PAT001", "COR003", "ANO002"],
            "recommendation": "Increase connection pool size or reduce connection timeout"
        },
        {
            "type": "optimization",
            "severity": "medium",
            "title": "Cache inefficiency at peak times",
            "description": "Cache miss rate increases 300% during peak hours (2-4 PM)",
            "evidence": ["SEQ005", "PEAK002"],
            "recommendation": "Pre-warm cache before peak hours or increase cache size"
        }
    ]
}
```

## Error Handling

### Insufficient Data
**Condition**: Not enough data for pattern detection
**Action**:
1. Report minimum data requirements
2. Analyze what's available with low confidence
3. Suggest collecting more data
4. Provide partial results

### High Noise
**Condition**: Too many false positive patterns
**Action**:
1. Increase minimum frequency threshold
2. Apply statistical filters
3. Focus on high-confidence patterns
4. Remove outliers

### No Patterns Found
**Condition**: Data appears random, no patterns
**Action**:
1. Report findings honestly
2. Show basic statistics
3. Look for very subtle patterns
4. Confirm data quality is sufficient

## Examples

### Example 1: Detect Error Pattern

**Input**: 24 hours of parsed logs with errors
**User says**: "Find patterns in the errors"

**Actions**:
1. Analyze error timing across 24 hours
2. Detect pattern: Database errors every 30 minutes
3. Frequency: 48 occurrences
4. Confidence: 95%
5. Possible cause: Scheduled job overwhelming database

**Result**: Temporal pattern identified, scheduled job suspected

### Example 2: Anomaly Detection

**Input**: Parsed logs showing traffic spike
**User says**: "Detect any anomalies in the logs"

**Actions**:
1. Calculate baseline request rate: 100 req/min
2. Detect spike at 14:23: 1,500 req/min (15x baseline)
3. Duration: 15 minutes
4. No corresponding error spike (unusual)
5. Identify as traffic anomaly

**Result**: Traffic anomaly detected, appears to be legitimate traffic (not attack)

### Example 3: Correlation Analysis

**Input**: Logs with deployment markers and error data
**User says**: "Are deployments causing errors?"

**Actions**:
1. Identify 12 deployment events
2. Track error rates before/after each
3. Find correlation: errors increase 85% within 2 min of deployment
4. Correlation strength: 0.89 (strong)
5. Pattern repeats across all 12 deployments

**Result**: Strong correlation confirmed, deployments consistently trigger errors

## Performance Optimization

### Sampling for Large Datasets
- Use sampling for > 1M log entries
- Stratified sampling preserves patterns
- Sample at least 100K entries

### Efficient Pattern Detection
- Use hash-based pattern matching
- Index by timestamp
- Pre-filter irrelevant entries

### Parallel Processing
- Detect different pattern types in parallel
- Process time windows concurrently
- Aggregate results efficiently

## Integration with Other Skills

### With log-parsing
Receives:
- Parsed log entries with timestamps
- Normalized data for comparison

### With error-detection
Uses:
- Error categories
- Error frequencies
- Error timelines

### With report-generation
Provides:
- Pattern summaries
- Anomaly alerts
- Trend visualizations
- Correlation insights

## Best Practices

1. **Set appropriate thresholds** - Too low = false positives
2. **Consider time windows** - Patterns may be time-specific
3. **Validate patterns** - Check confidence and frequency
4. **Look for correlations** - Don't just find patterns, explain them
5. **Provide context** - Raw patterns aren't useful without interpretation
6. **Track changes** - Compare to historical baselines
7. **Generate insights** - Translate patterns to actions

## Troubleshooting

### Too Many Patterns
If detecting excessive patterns:
1. Increase minimum frequency
2. Raise confidence threshold
3. Filter low-impact patterns
4. Focus on actionable patterns

### Missing Known Patterns
If not detecting expected patterns:
1. Lower thresholds
2. Check time window alignment
3. Verify data completeness
4. Review pattern definitions

### False Anomalies
If flagging normal events as anomalies:
1. Adjust baseline calculation
2. Increase deviation threshold
3. Consider seasonality
4. Use rolling baselines

### Slow Analysis
If pattern analysis is slow:
1. Sample large datasets
2. Limit time range
3. Process in parallel
4. Use approximate algorithms

## References

See `references/pattern-types.md` for:
- Pattern classification
- Detection algorithms
- Confidence calculation
- Real-world examples

See `references/anomaly-detection.md` for:
- Statistical methods
- Thresholds and tuning
- False positive handling
- Validation techniques
