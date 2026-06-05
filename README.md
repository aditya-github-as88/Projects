# Log Analyzer Agent

An intelligent log analysis system built following Claude Skills handbook best practices. Analyzes log files using multiple specialized skills to detect errors, identify patterns, spot anomalies, and generate comprehensive reports.

## Features

- **Multi-Format Log Parsing**: Supports Apache, Nginx, syslog, JSON, Docker, Kubernetes, and custom formats
- **Error Detection**: Identifies, categorizes, and prioritizes errors automatically
- **Pattern Analysis**: Detects recurring patterns, anomalies, and trends
- **Comprehensive Reporting**: Generates reports in Markdown, HTML, JSON, and text formats
- **Skills-Based Architecture**: Follows Claude Skills handbook for modular, maintainable design

## Architecture

The agent uses a **skills-based architecture** where each skill handles a specific aspect of log analysis:

### Skills

1. **log-parsing** - Parses log files in various formats into structured data
2. **error-detection** - Detects and categorizes errors from parsed logs
3. **pattern-analysis** - Identifies patterns, anomalies, and trends
4. **report-generation** - Generates comprehensive analysis reports

Skills are loaded dynamically based on the user's query, following the progressive disclosure pattern from the Claude Skills handbook.

## Project Structure

```
log-analyzer-agent/
├── agent/
│   └── main_agent.py          # Main agent coordinator
├── skills/
│   ├── log-parsing/
│   │   ├── SKILL.md            # Skill definition
│   │   ├── scripts/            # Helper scripts
│   │   └── references/         # Documentation
│   ├── error-detection/
│   ├── pattern-analysis/
│   └── report-generation/
├── tools/
│   ├── log_parser.py           # Log parsing tool
│   ├── error_detector.py       # Error detection tool
│   ├── pattern_analyzer.py     # Pattern analysis tool
│   └── report_generator.py     # Report generation tool
├── config/
│   └── settings.py             # Configuration
├── outputs/                    # Generated reports
├── logs/                       # Agent logs
└── tests/                      # Test files
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd log-analyzer-agent

# Install dependencies
pip install -r requirements.txt --break-system-packages

# (Optional) Set Claude API key for future API mode
export ANTHROPIC_API_KEY="your-api-key"
```

## Usage

### Interactive Mode

```bash
python agent/main_agent.py --interactive
```

Then use commands:
```
analyze /path/to/logfile.log
```

### Direct Analysis

```bash
python agent/main_agent.py --file /path/to/logfile.log
```

### Using Individual Tools

```bash
# Parse logs
python tools/log_parser.py /path/to/logfile.log

# Detect errors
python tools/error_detector.py parsed_log.json

# Analyze patterns
python tools/pattern_analyzer.py parsed_log.json

# Generate report
python tools/report_generator.py /path/to/results/
```

## Example

```bash
# Analyze an Apache access log
python agent/main_agent.py --file /var/log/apache2/access.log

# Output:
# ✓ Parsed 156,234 log entries
# ✓ Found 1,523 errors (47 unique types)
# ✓ Identified 12 patterns, 5 anomalies
# ✓ Report saved to: outputs/log_analysis_report_20260521_143052.md
```

## Supported Log Formats

- **Apache/Nginx**: Common and Combined log formats
- **Syslog**: RFC3164 and RFC5424 formats
- **JSON**: One JSON object per line
- **Application Logs**: Generic timestamp + level + message
- **Docker**: Container logs
- **Kubernetes**: Pod logs
- **Custom**: Best-effort parsing for unknown formats

## Report Output

The agent generates comprehensive reports including:

- **Executive Summary**: Overall status and key findings
- **Log Parsing Stats**: Parse success rate, coverage, time range
- **Error Analysis**: Error counts, categories, top errors, critical issues
- **Pattern Analysis**: Recurring patterns, anomalies, trends
- **Visualizations**: ASCII charts for timelines and distributions
- **Recommendations**: Prioritized action items

### Report Formats

- **Markdown** (.md): Human-readable, version-control friendly
- **HTML** (.html): Styled presentation with navigation
- **JSON** (.json): Machine-readable for APIs
- **Text** (.txt): Plain text for email/terminal

## Configuration

Edit `config/settings.py` to customize:

- Maximum log file size
- Maximum lines to analyze
- Error detection keywords
- Pattern analysis thresholds
- Report formats and options

## Skills Design

Following the Claude Skills handbook:

### Progressive Disclosure

Skills use a three-level system:
1. **Frontmatter** (YAML): Always loaded - just enough to decide if skill is needed
2. **Instructions** (Markdown): Loaded when skill is active - full guidance
3. **References**: Loaded on-demand - detailed documentation

### Skill Triggering

Skills trigger based on keywords in user queries:
- "parse" → log-parsing
- "error", "failure" → error-detection
- "pattern", "anomaly" → pattern-analysis
- "report", "summary" → report-generation

### Skill Coordination

The main agent:
1. Analyzes user query
2. Determines required skills
3. Loads skill instructions
4. Executes skills in proper order
5. Aggregates results

## Development

### Adding a New Skill

1. Create skill directory: `skills/new-skill/`
2. Create `SKILL.md` with YAML frontmatter and instructions
3. Add skill to `config/settings.py`
4. Create tool in `tools/` if needed
5. Update agent skill detection logic

### Testing

```bash
# Run tests
python -m pytest tests/

# Test individual components
python tools/log_parser.py test_data/sample.log
python tools/error_detector.py test_data/parsed.json
```

## Best Practices

Based on the Claude Skills handbook:

1. **Keep skills focused**: Each skill does one thing well
2. **Use clear descriptions**: Trigger phrases in frontmatter
3. **Progressive disclosure**: Don't load unnecessary context
4. **Error handling**: Graceful degradation
5. **Validate inputs**: Check file size, format, completeness
6. **Provide examples**: Show sample outputs
7. **Document thoroughly**: References for complex topics

## Limitations

- Maximum file size: 500 MB (configurable)
- Maximum lines: 100,000 per file (configurable)
- Requires UTF-8 encoding (or compatible)
- Pattern detection requires minimum 3 occurrences
- Some log formats may require manual format specification

## Troubleshooting

### Parse Errors

If parse success rate < 90%:
- Check log format detection
- Review unparsed lines
- Specify format manually
- Check for custom format variations

### High Memory Usage

If running out of memory:
- Reduce chunk size in config
- Process smaller time ranges
- Sample large files
- Use streaming mode

### Slow Performance

If analysis is slow:
- Check file size
- Reduce analysis depth
- Process in chunks
- Use parallel processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the skills handbook patterns
4. Add tests for new features
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

Built following the **Claude Skills Handbook** best practices:
- Progressive disclosure pattern
- Skills-based architecture
- Composability and portability
- Clear documentation and examples

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the skills handbook for patterns
- Review skill SKILL.md files for documentation

---

**Log Analyzer Agent** - Intelligent log analysis powered by Claude Skills
