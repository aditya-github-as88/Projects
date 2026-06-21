---
name: report-generation
description: "Generates comprehensive reports from log analysis results. Use when user mentions 'create report', 'generate summary', 'export results', or 'show analysis report'. Also triggers on 'summary report', 'analysis output', or 'export findings'."
compatibility: "Works with claude.ai, Claude Code, and API. Generates reports in markdown, HTML, JSON, and text formats."
license: MIT
metadata:
  author: Log Analyzer Team
  version: 1.0.0
  category: reporting
  depends-on: [log-parsing, error-detection, pattern-analysis]
  tags: [reporting, visualization, summary, export]
---

# Report Generation Skill

## Purpose

This skill generates comprehensive, actionable reports from log analysis results. It consolidates data from parsing, error detection, and pattern analysis into structured reports with visualizations, statistics, and recommendations. Supports multiple output formats.

## When to Use This Skill

Trigger this skill when:
- User asks to "create report" or "generate summary"
- User mentions "show me the results" or "export analysis"
- After completing analysis and user needs deliverable
- User requests specific format: "markdown report", "HTML output"
- User asks for "executive summary" or "detailed findings"

## Instructions

### Step 1: Aggregate Analysis Results

Collect data from all analysis steps:

```python
from tools.report_generator import ReportGenerator

generator = ReportGenerator()
aggregated_data = generator.aggregate_results(
    parsed_logs=parsed_logs,
    errors=error_detection_results,
    patterns=pattern_analysis_results,
    anomalies=anomaly_results
)
```

**Data aggregated**:
- Log parsing statistics (total lines, format, time range)
- Error counts and categories
- Critical errors list
- Patterns identified
- Anomalies detected
- Trends and correlations
- Performance metrics

### Step 2: Generate Executive Summary

Create high-level overview:

```python
executive_summary = generator.create_executive_summary(aggregated_data)
```

**Summary includes**:
- **Status**: Overall system health (Good/Warning/Critical)
- **Time Range**: Period analyzed
- **Total Entries**: Number of log lines processed
- **Error Rate**: Percentage and trend
- **Critical Issues**: Count of urgent problems
- **Key Findings**: Top 3-5 insights
- **Recommendations**: Priority actions

**Example output**:
```markdown
## Executive Summary

**Status**: ⚠️ WARNING  
**Analysis Period**: 2026-05-21 00:00 - 2026-05-21 23:59 (24 hours)  
**Total Log Entries**: 156,234  
**Error Rate**: 2.3% (↑ 45% from baseline)

### Critical Issues
- 12 CRITICAL errors detected
- Database connection pool exhaustion pattern
- Memory leak suspected (increasing trend)

### Key Findings
1. Database errors spike every 30 minutes (correlation with scheduled job)
2. Traffic anomaly at 14:23 (15x normal) - appears legitimate
3. Response time degrading during peak hours (cache inefficiency)

### Priority Recommendations
1. **URGENT**: Increase database connection pool size
2. **HIGH**: Investigate memory leak in user service
3. **MEDIUM**: Optimize cache strategy for peak hours
```

### Step 3: Create Detailed Sections

Generate detailed sections for each analysis area:

```python
sections = generator.create_detailed_sections(aggregated_data)
```

**Sections created**:

**A. Log Parsing Summary**
- File information (name, size, format)
- Parse statistics (success rate, errors)
- Time range and coverage
- Sample entries

**B. Error Analysis**
- Total errors by severity
- Error categories and distribution
- Top 10 most frequent errors
- Critical errors with details
- Error timeline chart
- Error examples

**C. Pattern Analysis**
- Recurring patterns found
- Pattern descriptions and frequencies
- Confidence scores
- Implications of each pattern

**D. Anomaly Detection**
- Anomalies identified
- Severity and impact
- Possible causes
- Time of occurrence

**E. Trends and Correlations**
- Metric trends over time
- Correlations discovered
- Peak times analysis
- Forecasts (if applicable)

### Step 4: Add Visualizations

Include visual representations (ASCII charts or data for rendering):

```python
visualizations = generator.create_visualizations(aggregated_data)
```

**Visualization types**:

**Error Timeline** (ASCII bar chart):
```
Errors per Hour (24-hour period)
00:00 ▓▓░░░░░░░░ 45
01:00 ▓░░░░░░░░░ 23
02:00 ▓░░░░░░░░░ 18
...
14:00 ▓▓▓▓▓▓▓▓▓▓ 247  ← Spike detected
15:00 ▓▓▓▓░░░░░░ 156
...
```

**Error Distribution** (pie chart data):
```
Error Categories:
  Database:      45% ████████████████░░░░
  Network:       30% ███████████░░░░░░░░░
  Application:   25% █████████░░░░░░░░░░░
```

**Trend Line** (ASCII):
```
Error Rate Trend (24 hours)
 200|                            ╱╲
    |                          ╱    ╲
 150|                        ╱        ╲
    |                    ╱╱              ╲
 100|        ╱╲      ╱╱                    ╲
    |    ╱╱    ╲╱╲╱                          ╲
  50|╱╱                                        ╲
    └────────────────────────────────────────────
     00:00        06:00        12:00        18:00
```

### Step 5: Include Recommendations

Generate actionable recommendations:

```python
recommendations = generator.generate_recommendations(
    errors=errors,
    patterns=patterns,
    anomalies=anomalies
)
```

**Recommendation structure**:
```python
{
    "priority": "urgent|high|medium|low",
    "category": "performance|reliability|security|optimization",
    "title": "Short description",
    "problem": "What's wrong",
    "impact": "What happens if not fixed",
    "recommendation": "What to do",
    "effort": "low|medium|high",
    "evidence": ["ERR001", "PAT003"]  # References
}
```

**Example**:
```markdown
## Recommendations

### 🔴 URGENT

**1. Increase Database Connection Pool**
- **Problem**: Connection pool exhausted every 30 minutes
- **Impact**: Application errors, degraded performance
- **Action**: Increase pool size from 50 to 100 connections
- **Effort**: Low (configuration change)
- **Evidence**: Pattern PAT001, Error ERR023

### 🟡 HIGH

**2. Investigate Memory Leak**
- **Problem**: Memory usage increasing 5% per hour
- **Impact**: Service crash within 20 hours
- **Action**: Profile user service, check for unclosed resources
- **Effort**: High (requires investigation)
- **Evidence**: Trend TRD002, Anomaly ANO005
```

### Step 6: Format Output

Format report in requested format:

```python
report = generator.format_report(
    summary=executive_summary,
    sections=sections,
    visualizations=visualizations,
    recommendations=recommendations,
    format="markdown"  # or "html", "json", "text"
)
```

**Supported formats**:

**Markdown** (.md):
- Human-readable
- GitHub/GitLab compatible
- Easy to version control
- Supports tables, charts, code blocks

**HTML** (.html):
- Interactive visualizations
- Clickable navigation
- Styled presentation
- Embeddable charts

**JSON** (.json):
- Machine-readable
- API integration
- Data processing
- Structured for databases

**Text** (.txt):
- Plain text
- Email-friendly
- Terminal output
- No special formatting

### Step 7: Save and Deliver

Save report to output directory:

```python
output_path = generator.save_report(
    report=report,
    filename="log_analysis_report",
    format="markdown"
)

print(f"Report saved to: {output_path}")
```

**File naming convention**:
```
log_analysis_report_YYYYMMDD_HHMMSS.{ext}

Examples:
- log_analysis_report_20260521_143052.md
- log_analysis_report_20260521_143052.html
- log_analysis_report_20260521_143052.json
```

## Error Handling

### No Data Available
**Condition**: No analysis results to report
**Action**:
1. Create minimal report showing what was attempted
2. List reasons for no data
3. Suggest next steps
4. Include metadata about analysis attempt

### Incomplete Analysis
**Condition**: Some analysis steps failed
**Action**:
1. Report what succeeded
2. Note missing sections clearly
3. Include partial results
4. Explain failures

### Format Not Supported
**Condition**: User requests unsupported format
**Action**:
1. List supported formats
2. Suggest closest alternative
3. Offer to generate in multiple formats
4. Default to markdown

## Examples

### Example 1: Full Analysis Report

**Input**: Complete log analysis results
**User says**: "Generate a comprehensive report"

**Actions**:
1. Aggregate all analysis results
2. Create executive summary showing WARNING status
3. Generate all sections with details
4. Include ASCII visualizations
5. Add 8 prioritized recommendations
6. Format as markdown
7. Save to outputs/log_analysis_report_20260521_143052.md

**Result**: 15-page markdown report with all findings and recommendations

### Example 2: Executive Summary Only

**Input**: Analysis results
**User says**: "Give me just the executive summary"

**Actions**:
1. Generate executive summary
2. Include only key findings (top 3)
3. List critical errors count
4. Add top 2 priority recommendations
5. Format as concise markdown
6. Output to screen (not saved)

**Result**: 1-page executive summary for quick review

### Example 3: JSON Export for API

**Input**: Analysis results
**User says**: "Export results as JSON"

**Actions**:
1. Aggregate all data
2. Structure in JSON format
3. Include all metrics and findings
4. Preserve data types
5. Save to outputs/log_analysis_report_20260521_143052.json

**Result**: Structured JSON file ready for API consumption

## Performance Optimization

### Lazy Visualization Generation
- Generate charts only if requested
- Use ASCII for speed
- Pre-calculate common metrics

### Template Caching
- Cache report templates
- Reuse section formatters
- Pre-compile regex patterns

### Efficient Formatting
- Stream large reports
- Generate sections independently
- Parallelize format conversion

## Integration with Other Skills

### With log-parsing
Uses:
- Parse statistics
- File metadata
- Sample log entries

### With error-detection
Uses:
- Error counts and categories
- Critical errors list
- Error timeline data
- Top errors

### With pattern-analysis
Uses:
- Identified patterns
- Anomalies
- Trends
- Correlations
- Insights

## Best Practices

1. **Start with executive summary** - Readers want overview first
2. **Use clear headings** - Easy navigation
3. **Include visualizations** - Data easier to understand
4. **Provide examples** - Show actual log entries
5. **Make recommendations actionable** - Specific, measurable actions
6. **Prioritize findings** - Urgent first
7. **Include metadata** - When analyzed, what files, versions

## Report Template Structure

```markdown
# Log Analysis Report

**Generated**: 2026-05-21 14:30:52 UTC  
**Analysis Period**: 2026-05-21 00:00 - 23:59  
**Log File**: /var/log/application.log  
**Total Entries**: 156,234

---

## Executive Summary
[Status, key findings, critical issues]

---

## Log Parsing Summary
[File info, parse stats, coverage]

---

## Error Analysis
[Error counts, categories, top errors, timeline]

---

## Pattern Analysis
[Patterns found, frequencies, implications]

---

## Anomaly Detection
[Anomalies, severity, causes]

---

## Trends and Correlations
[Metric trends, correlations, forecasts]

---

## Recommendations
[Prioritized action items]

---

## Appendix
[Sample logs, detailed data, references]
```

## Troubleshooting

### Report Too Large
If report exceeds reasonable size:
1. Limit error examples (max 10 per type)
2. Summarize patterns (top 20 only)
3. Use pagination for HTML
4. Offer to generate sections separately

### Missing Sections
If expected sections absent:
1. Check if analysis step ran
2. Verify data availability
3. Note missing sections in report
4. Explain why missing

### Formatting Issues
If output format broken:
1. Validate input data
2. Check template compatibility
3. Test with minimal data
4. Fall back to plain text

### Poor Readability
If report hard to read:
1. Improve heading hierarchy
2. Add more whitespace
3. Use tables for structured data
4. Simplify visualizations

## References

See `references/report-templates.md` for:
- Complete report templates
- Section layouts
- Formatting guidelines
- Example reports

See `references/visualization-guide.md` for:
- ASCII chart creation
- Data-to-chart conversion
- Color coding (if supported)
- Chart selection guide
