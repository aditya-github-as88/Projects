# Pattern Types Reference

This document describes different types of patterns detected in log analysis.

## Pattern Categories

### 1. Temporal Patterns

**Definition**: Events that occur at regular time intervals.

**Examples**:
- Errors every 30 minutes (scheduled job issue)
- Traffic spike every day at 2 PM (lunch hour)
- Backup logs every 24 hours (automated backup)

**Detection Method**:
1. Group events by type/message
2. Extract timestamps
3. Calculate intervals between occurrences
4. Check if intervals are regular (within tolerance)

**Confidence Calculation**:
```python
confidence = 1.0 - (std_dev(intervals) / mean(intervals))
```

High confidence (>0.9) indicates very regular pattern.

**Use Cases**:
- Identify scheduled jobs causing issues
- Detect periodic resource exhaustion
- Find recurring system maintenance windows

### 2. Sequential Patterns

**Definition**: Events that follow a specific order.

**Examples**:
- Request → Error → Retry → Success
- Login → API Call → Database Query → Logout
- Cache Miss → Database Query → Cache Write

**Detection Method**:
1. Track event sequences by session/user/request ID
2. Find common subsequences using pattern mining
3. Calculate support (frequency) for each sequence

**Representation**:
```
Pattern: [Event A] → [Event B] → [Event C]
Support: 45 occurrences
Confidence: 0.85
Average Duration: 2.3 seconds
```

**Use Cases**:
- Understand user workflows
- Identify error recovery patterns
- Optimize request flows

### 3. Frequency Patterns

**Definition**: Events occurring more often than expected.

**Examples**:
- Specific endpoint called 10,000 times/hour
- Same error repeated 500 times
- High cache miss rate (80% vs. expected 20%)

**Detection Method**:
```python
if actual_frequency > (baseline * threshold):
    # High-frequency pattern detected
```

**Metrics**:
- **Absolute Frequency**: Raw count
- **Relative Frequency**: Compared to baseline
- **Rate**: Events per time unit

**Use Cases**:
- Detect API abuse
- Identify popular endpoints
- Find retry loops

### 4. Correlation Patterns

**Definition**: Events that co-occur or follow causally.

**Examples**:
- Deployment → Error spike (correlation: 0.89)
- High traffic → Slow response time (correlation: 0.75)
- Cache clear → Database load increase (correlation: 0.82)

**Detection Method**:
1. Identify event types to correlate
2. Align events by time windows
3. Calculate correlation coefficient
4. Determine lag time (if sequential)

**Correlation Strength**:
- 0.9 - 1.0: Very strong
- 0.7 - 0.9: Strong
- 0.5 - 0.7: Moderate
- 0.3 - 0.5: Weak
- < 0.3: Very weak or none

**Use Cases**:
- Find root causes of issues
- Predict cascading failures
- Optimize system behavior

### 5. Anomaly Patterns

**Definition**: Events that deviate significantly from normal behavior.

**Types**:

#### Point Anomalies
Single events that are unusual.
```
Example: Response time of 30s when average is 0.5s
```

#### Contextual Anomalies
Events unusual in specific context.
```
Example: 1000 requests at 3 AM (normal during day, unusual at night)
```

#### Collective Anomalies
Group of events unusual together.
```
Example: 100 simultaneous authentication failures
```

**Detection Methods**:

**Statistical**:
```python
z_score = (value - mean) / std_dev
if abs(z_score) > 3:  # 3 standard deviations
    # Anomaly detected
```

**Interquartile Range (IQR)**:
```python
Q1 = percentile(data, 25)
Q3 = percentile(data, 75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

if value < lower_bound or value > upper_bound:
    # Anomaly
```

**Use Cases**:
- Detect attacks or abuse
- Find system malfunctions
- Identify unusual user behavior

### 6. Trend Patterns

**Definition**: Directional changes over time.

**Types**:

#### Increasing Trend
```
Metric growing over time
Example: Error rate: 1% → 2% → 3% → 5%
```

#### Decreasing Trend
```
Metric declining over time
Example: Response time: 500ms → 400ms → 300ms → 200ms
```

#### Stable Trend
```
Metric consistent over time
Example: Request volume: 1000±50 requests/hour
```

#### Seasonal Trend
```
Metric varies in predictable cycles
Example: Traffic peaks every weekday at 2 PM
```

**Detection Method**:
```python
# Simple linear regression
from scipy.stats import linregress
slope, intercept, r_value, p_value, std_err = linregress(time, values)

if slope > 0 and p_value < 0.05:
    trend = "increasing"
elif slope < 0 and p_value < 0.05:
    trend = "decreasing"
else:
    trend = "stable"
```

**Use Cases**:
- Capacity planning
- Performance monitoring
- Early warning systems

### 7. Burst Patterns

**Definition**: Sudden spikes or drops in activity.

**Examples**:
- Traffic spike from 100 to 10,000 requests/minute
- Error burst: 0 to 500 errors in 5 minutes
- Connection pool exhaustion event

**Detection Method**:
```python
# Compare current window to baseline
current_rate = count_events(current_window)
baseline_rate = mean(historical_rates)

if current_rate > (baseline_rate * burst_threshold):
    # Burst detected
    magnitude = current_rate / baseline_rate
```

**Characteristics**:
- **Duration**: How long burst lasts
- **Magnitude**: How much higher than baseline
- **Recovery Time**: How long to return to normal

**Use Cases**:
- Detect DDoS attacks
- Identify viral content
- Find system overloads

### 8. Cyclic Patterns

**Definition**: Events that repeat in cycles.

**Examples**:
- Daily pattern: Traffic peaks at noon
- Weekly pattern: Lower traffic on weekends
- Hourly pattern: Batch job runs every hour

**Detection Method**:
1. Group events by time period (hour, day, week)
2. Calculate average for each period
3. Check for consistent peaks/troughs
4. Use Fourier analysis for complex cycles

**Representation**:
```
Pattern: Daily cycle
Peak: 14:00 (2 PM)
Trough: 03:00 (3 AM)
Peak/Trough Ratio: 5.2x
Confidence: 0.93
```

**Use Cases**:
- Optimize resource allocation
- Schedule maintenance windows
- Predict capacity needs

## Pattern Confidence Scores

### Calculation Methods

**Frequency-Based**:
```python
confidence = min(1.0, frequency / 100)  # Cap at 100 occurrences
```

**Regularity-Based**:
```python
confidence = 1.0 - (coefficient_of_variation)
# where CV = std_dev / mean
```

**Statistical-Based**:
```python
confidence = 1.0 - p_value  # Statistical significance
```

### Interpretation

| Confidence | Interpretation |
|------------|----------------|
| 0.95 - 1.0 | Very High - Act on this pattern |
| 0.80 - 0.95 | High - Likely actionable |
| 0.60 - 0.80 | Medium - Investigate further |
| 0.40 - 0.60 | Low - May be noise |
| < 0.40 | Very Low - Likely false positive |

## Pattern Validation

### Techniques

**1. Cross-Validation**
- Split data into training/validation sets
- Detect patterns in training set
- Verify patterns exist in validation set

**2. Temporal Validation**
- Detect patterns in historical data
- Check if patterns continue in recent data
- Patterns that persist are more reliable

**3. Statistical Testing**
- Null hypothesis: Pattern is random
- Calculate p-value
- p-value < 0.05 suggests real pattern

**4. Domain Validation**
- Do patterns make business sense?
- Can patterns be explained?
- Are patterns actionable?

## Pattern Prioritization

### Priority Matrix

| Impact | Frequency | Priority |
|--------|-----------|----------|
| High | High | P0 - Critical |
| High | Low | P1 - Important |
| Low | High | P2 - Monitor |
| Low | Low | P3 - Ignore |

### Impact Assessment

**High Impact Patterns**:
- Affect revenue (payment errors)
- Affect security (auth failures)
- Affect availability (service crashes)
- Affect user experience (slow responses)

**Low Impact Patterns**:
- Internal logging patterns
- Non-critical background tasks
- Optional features
- Debug information

### Frequency Assessment

**High Frequency**: 
- Occurs > 10 times per hour
- Affects > 100 users
- Consumes significant resources

**Low Frequency**:
- Occurs < 10 times per hour
- Affects few users
- Minimal resource impact

## Real-World Pattern Examples

### Example 1: Database Connection Pool Exhaustion

**Pattern Type**: Temporal + Correlation

**Observation**:
- Errors every 30 minutes
- Correlates with scheduled job execution
- Connection count spikes to pool maximum

**Analysis**:
```
Temporal Pattern: Every 30 min (confidence: 0.95)
Correlation: job_start → connection_spike (0.89)
Impact: High (service degradation)
Frequency: High (48 times/day)
Priority: P0
```

**Recommendation**: Increase connection pool or optimize job queries

### Example 2: Cache Inefficiency

**Pattern Type**: Sequential + Frequency

**Observation**:
- Cache miss → DB query sequence occurs frequently
- Cache miss rate 80% (expected 20%)
- Concentrated during peak hours

**Analysis**:
```
Sequential Pattern: cache_miss → db_query (support: 8000)
Frequency: 80% miss rate vs 20% baseline
Trend: Worsening during peak hours
Impact: Medium (performance degradation)
Priority: P1
```

**Recommendation**: Pre-warm cache before peak hours

### Example 3: Retry Storm

**Pattern Type**: Sequential + Burst

**Observation**:
- Request → Error → Immediate Retry pattern
- Burst of 5000 retries in 2 minutes
- Amplifies original problem

**Analysis**:
```
Sequential: request → error → retry (no backoff)
Burst: 2500x normal rate
Duration: 2 minutes
Impact: High (cascading failure)
Priority: P0
```

**Recommendation**: Implement exponential backoff

## Tools and Scripts

- `find_patterns.py`: General pattern detection
- `correlate_events.py`: Correlation analysis
- `detect_anomalies.py`: Anomaly detection
- `trend_analysis.py`: Trend calculation

## References

- Time Series Analysis Methods
- Statistical Pattern Recognition
- Anomaly Detection Algorithms
- Correlation Analysis Techniques
