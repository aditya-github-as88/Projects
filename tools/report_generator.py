"""
Report Generator Tool
Generates comprehensive reports from log analysis results
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """Generate analysis reports in multiple formats"""
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "outputs"
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_report(self, analysis_results: Dict[str, Any], format: str = "markdown") -> Dict[str, Any]:
        """Main entry point - generate complete report"""
        # Aggregate all results
        aggregated = self.aggregate_results(analysis_results)
        
        # Create executive summary
        executive_summary = self.create_executive_summary(aggregated)
        
        # Create detailed sections
        sections = self.create_detailed_sections(aggregated)
        
        # Add visualizations
        visualizations = self.create_visualizations(aggregated)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(aggregated)
        
        # Format report
        report = {
            'executive_summary': executive_summary,
            'sections': sections,
            'visualizations': visualizations,
            'recommendations': recommendations,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'format': format
            }
        }
        
        return report
    
    def aggregate_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate data from all analysis steps"""
        return {
            'parsing': results.get('log-parsing', {}),
            'errors': results.get('error-detection', {}),
            'patterns': results.get('pattern-analysis', {}),
            'timestamp': datetime.now().isoformat()
        }
    
    def create_executive_summary(self, data: Dict[str, Any]) -> str:
        """Create executive summary"""
        parsing = data.get('parsing', {})
        errors = data.get('errors', {})
        patterns = data.get('patterns', {})
        
        # Determine overall status
        error_rate = errors.get('error_percentage', 0)
        critical_count = errors.get('critical_errors', 0)
        
        if critical_count > 0 or error_rate > 5:
            status = "🔴 CRITICAL"
        elif error_rate > 2:
            status = "⚠️  WARNING"
        else:
            status = "✅ GOOD"
        
        # Build summary
        summary = f"""## Executive Summary

**Status**: {status}
**Analysis Period**: {parsing.get('metadata', {}).get('start_time', 'N/A')} to {parsing.get('metadata', {}).get('end_time', 'N/A')}
**Total Log Entries**: {parsing.get('parsed_lines', 0):,}
**Error Rate**: {error_rate}%"""
        
        if errors:
            summary += f"""

### Critical Issues
- {critical_count} CRITICAL errors detected
- {errors.get('total_errors', 0):,} total errors found
- {errors.get('unique_error_types', 0)} unique error types
"""
        
        if patterns and patterns.get('insights'):
            summary += f"""
### Key Findings
"""
            for i, insight in enumerate(patterns['insights'][:3], 1):
                summary += f"{i}. {insight['title']}\n"
        
        # Add recommendations preview
        if critical_count > 0:
            summary += f"""
### Priority Actions Required
1. **URGENT**: Investigate {critical_count} critical errors
2. **HIGH**: Review error trends and patterns
3. **MEDIUM**: Optimize based on pattern analysis
"""
        
        return summary
    
    def create_detailed_sections(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Create detailed report sections"""
        sections = {}
        
        # Section 1: Log Parsing Summary
        sections['parsing'] = self._create_parsing_section(data.get('parsing', {}))
        
        # Section 2: Error Analysis
        sections['errors'] = self._create_error_section(data.get('errors', {}))
        
        # Section 3: Pattern Analysis
        sections['patterns'] = self._create_pattern_section(data.get('patterns', {}))
        
        return sections
    
    def create_visualizations(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Create ASCII visualizations"""
        visualizations = {}
        
        errors = data.get('errors', {})
        
        # Error timeline
        if errors.get('timeline', {}).get('buckets'):
            visualizations['error_timeline'] = self._create_timeline_chart(
                errors['timeline']['buckets']
            )
        
        # Error distribution
        if errors.get('error_distribution'):
            visualizations['error_distribution'] = self._create_bar_chart(
                errors['error_distribution']
            )
        
        return visualizations
    
    def generate_recommendations(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        recommendations = []
        
        errors = data.get('errors', {})
        patterns = data.get('patterns', {})
        
        # Critical error recommendations
        if errors.get('critical_errors', 0) > 0:
            recommendations.append({
                'priority': 'urgent',
                'category': 'reliability',
                'title': 'Address Critical Errors',
                'problem': f"{errors['critical_errors']} critical errors detected",
                'impact': 'Service disruption, data loss, or system instability',
                'recommendation': 'Investigate and resolve critical errors immediately',
                'effort': 'high'
            })
        
        # High error rate recommendation
        if errors.get('error_percentage', 0) > 5:
            recommendations.append({
                'priority': 'high',
                'category': 'reliability',
                'title': 'Reduce Error Rate',
                'problem': f"Error rate at {errors['error_percentage']}%",
                'impact': 'Poor user experience, potential service degradation',
                'recommendation': 'Review error patterns and implement fixes',
                'effort': 'medium'
            })
        
        # Pattern-based recommendations
        if patterns and patterns.get('insights'):
            for insight in patterns['insights'][:3]:
                recommendations.append({
                    'priority': insight.get('severity', 'medium'),
                    'category': 'optimization',
                    'title': insight['title'],
                    'problem': insight['description'],
                    'impact': 'Performance degradation or resource waste',
                    'recommendation': insight.get('recommendation', 'Investigate and optimize'),
                    'effort': 'medium'
                })
        
        # Sort by priority
        priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 999))
        
        return recommendations
    
    def save_report(
        self,
        report: Dict[str, Any],
        filename: str = "log_analysis_report",
        format: str = "markdown"
    ) -> str:
        """Save report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == "markdown":
            output_file = self.output_dir / f"{filename}_{timestamp}.md"
            content = self._format_as_markdown(report)
        elif format == "html":
            output_file = self.output_dir / f"{filename}_{timestamp}.html"
            content = self._format_as_html(report)
        elif format == "json":
            output_file = self.output_dir / f"{filename}_{timestamp}.json"
            content = json.dumps(report, indent=2, default=str)
        else:  # text
            output_file = self.output_dir / f"{filename}_{timestamp}.txt"
            content = self._format_as_text(report)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_file)
    
    def _create_parsing_section(self, parsing: Dict[str, Any]) -> str:
        """Create log parsing summary section"""
        section = f"""## Log Parsing Summary

**File**: {parsing.get('file_path', 'N/A')}
**Format**: {parsing.get('format', 'N/A')}
**File Size**: {parsing.get('file_size_mb', 0):.2f} MB
**Total Lines**: {parsing.get('total_lines', 0):,}
**Successfully Parsed**: {parsing.get('parsed_lines', 0):,}
**Parse Errors**: {parsing.get('errors', 0)}
**Parse Success Rate**: {(parsing.get('parsed_lines', 0) / parsing.get('total_lines', 1) * 100):.1f}%

**Time Range**:
- Start: {parsing.get('metadata', {}).get('start_time', 'N/A')}
- End: {parsing.get('metadata', {}).get('end_time', 'N/A')}
- Duration: {parsing.get('metadata', {}).get('duration_hours', 0):.1f} hours
"""
        
        # Sample entries
        if parsing.get('entries'):
            section += "\n**Sample Entries** (first 3):\n"
            for i, entry in enumerate(parsing['entries'][:3], 1):
                timestamp = entry.get('timestamp', 'N/A')
                level = entry.get('level', 'INFO')
                message = entry.get('message', entry.get('raw_line', ''))[:100]
                section += f"\n{i}. [{timestamp}] {level}: {message}\n"
        
        return section
    
    def _create_error_section(self, errors: Dict[str, Any]) -> str:
        """Create error analysis section"""
        section = f"""## Error Analysis

**Total Errors**: {errors.get('total_errors', 0):,}
**Unique Error Types**: {errors.get('unique_error_types', 0)}
**Error Rate**: {errors.get('error_percentage', 0)}%
**Errors Per Hour**: {errors.get('error_rate_per_hour', 0):.1f}
**Critical Errors**: {errors.get('critical_errors', 0)}

### Error Distribution by Category
"""
        
        # Error distribution
        if errors.get('error_distribution'):
            for category, percentage in sorted(
                errors['error_distribution'].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                section += f"- **{category.title()}**: {percentage:.1f}%\n"
        
        # Top errors
        if errors.get('top_errors'):
            section += "\n### Top 10 Most Frequent Errors\n"
            for i, error in enumerate(errors['top_errors'][:10], 1):
                section += f"\n**{i}. {error['type']}** ({error['occurrences']} occurrences)\n"
                section += f"   - Category: {error['category']}\n"
                section += f"   - Severity: {error['severity']}\n"
                section += f"   - Message: {error['message_template'][:100]}\n"
        
        # Critical errors
        if errors.get('critical_error_list'):
            section += "\n### Critical Errors Requiring Immediate Attention\n"
            for error in errors['critical_error_list'][:5]:
                section += f"\n**{error['error_id']}: {error['type']}**\n"
                section += f"- Occurrences: {error['occurrences']}\n"
                section += f"- First seen: {error['first_seen']}\n"
                section += f"- Last seen: {error['last_seen']}\n"
                section += f"- Reasons: {', '.join(error.get('critical_reasons', []))}\n"
        
        return section
    
    def _create_pattern_section(self, patterns: Dict[str, Any]) -> str:
        """Create pattern analysis section"""
        section = f"""## Pattern Analysis

**Patterns Found**: {patterns.get('pattern_count', 0)}
**Anomalies Detected**: {patterns.get('anomaly_count', 0)}
"""
        
        # Patterns
        if patterns.get('patterns'):
            section += "\n### Recurring Patterns\n"
            for pattern in patterns['patterns'][:10]:
                section += f"\n**{pattern.get('pattern_id', 'N/A')}**: {pattern['description']}\n"
                section += f"- Type: {pattern['type']}\n"
                section += f"- Frequency: {pattern['frequency']}\n"
                section += f"- Confidence: {pattern.get('confidence', 0):.2f}\n"
        
        # Anomalies
        if patterns.get('anomalies'):
            section += "\n### Anomalies\n"
            for anomaly in patterns['anomalies'][:10]:
                section += f"\n**{anomaly.get('anomaly_id', 'N/A')}**: {anomaly['description']}\n"
                section += f"- Type: {anomaly['type']}\n"
                section += f"- Severity: {anomaly['severity']}\n"
                section += f"- Deviation: {anomaly.get('deviation', 'N/A')}\n"
        
        # Trends
        if patterns.get('trends'):
            section += "\n### Trends\n"
            trends = patterns['trends']
            if trends.get('volume_trend'):
                vt = trends['volume_trend']
                section += f"- **Traffic Volume**: {vt['direction']} ({vt['change_percent']:+.1f}%)\n"
            if trends.get('error_rate_trend'):
                et = trends['error_rate_trend']
                section += f"- **Error Rate**: {et['direction']} ({et['change_percent']:+.1f}%)\n"
        
        # Peak times
        if patterns.get('peak_times'):
            peaks = patterns['peak_times']
            section += f"\n### Peak Activity Times\n"
            section += f"- **Peak Hour**: {peaks.get('peak_hour', 'N/A')} ({peaks.get('peak_count', 0):,} events)\n"
            section += f"- **Low Hour**: {peaks.get('low_hour', 'N/A')} ({peaks.get('low_count', 0):,} events)\n"
            section += f"- **Average**: {peaks.get('average', 0):,.0f} events per hour\n"
        
        # Insights
        if patterns.get('insights'):
            section += "\n### Key Insights\n"
            for insight in patterns['insights']:
                emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(insight['severity'], '⚪')
                section += f"\n{emoji} **{insight['title']}**\n"
                section += f"- {insight['description']}\n"
                section += f"- Recommendation: {insight.get('recommendation', 'N/A')}\n"
        
        return section
    
    def _create_timeline_chart(self, buckets: List[Dict[str, Any]]) -> str:
        """Create ASCII timeline chart"""
        if not buckets:
            return "No timeline data available"
        
        max_count = max(b['error_count'] for b in buckets)
        if max_count == 0:
            return "No errors in timeline"
        
        chart = "Error Timeline (errors per hour)\n\n"
        
        for bucket in buckets:
            hour = bucket['timestamp'].split('T')[1][:5]  # HH:MM
            count = bucket['error_count']
            bar_length = int((count / max_count) * 40)
            bar = '█' * bar_length
            chart += f"{hour} │{bar} {count}\n"
        
        return chart
    
    def _create_bar_chart(self, data: Dict[str, float]) -> str:
        """Create ASCII bar chart"""
        if not data:
            return "No distribution data available"
        
        chart = "Error Distribution by Category\n\n"
        
        max_percentage = max(data.values())
        
        for category, percentage in sorted(data.items(), key=lambda x: x[1], reverse=True):
            bar_length = int((percentage / max_percentage) * 30)
            bar = '█' * bar_length
            chart += f"{category:15s} │{bar} {percentage:.1f}%\n"
        
        return chart
    
    def _format_as_markdown(self, report: Dict[str, Any]) -> str:
        """Format report as Markdown"""
        md = f"""# Log Analysis Report

**Generated**: {report['metadata']['generated_at']}

---

{report['executive_summary']}

---

{report['sections'].get('parsing', '')}

---

{report['sections'].get('errors', '')}

---

{report['sections'].get('patterns', '')}

---

## Visualizations

### Error Timeline
```
{report['visualizations'].get('error_timeline', 'No data')}
```

### Error Distribution
```
{report['visualizations'].get('error_distribution', 'No data')}
```

---

## Recommendations

"""
        
        for rec in report['recommendations']:
            emoji = {'urgent': '🔴', 'high': '🟡', 'medium': '🔵', 'low': '🟢'}.get(rec['priority'], '⚪')
            md += f"""
### {emoji} {rec['priority'].upper()}: {rec['title']}

- **Problem**: {rec['problem']}
- **Impact**: {rec['impact']}
- **Recommendation**: {rec['recommendation']}
- **Effort**: {rec['effort']}

"""
        
        md += "\n---\n\n*Report generated by Log Analyzer Agent*\n"
        
        return md
    
    def _format_as_html(self, report: Dict[str, Any]) -> str:
        """Format report as HTML"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Log Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; }}
        .summary {{ background: #f4f4f4; padding: 20px; border-left: 4px solid #4CAF50; }}
        .critical {{ background: #ffebee; border-left: 4px solid #f44336; }}
        .warning {{ background: #fff3e0; border-left: 4px solid #ff9800; }}
        .section {{ margin: 30px 0; }}
        pre {{ background: #f5f5f5; padding: 15px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
    </style>
</head>
<body>
    <h1>Log Analysis Report</h1>
    <p><strong>Generated:</strong> {report['metadata']['generated_at']}</p>
    
    <div class="summary">
        {self._markdown_to_html(report['executive_summary'])}
    </div>
    
    <div class="section">
        {self._markdown_to_html(report['sections'].get('parsing', ''))}
    </div>
    
    <div class="section">
        {self._markdown_to_html(report['sections'].get('errors', ''))}
    </div>
    
    <div class="section">
        {self._markdown_to_html(report['sections'].get('patterns', ''))}
    </div>
    
    <div class="section">
        <h2>Recommendations</h2>
"""
        
        for rec in report['recommendations']:
            priority_class = 'critical' if rec['priority'] == 'urgent' else 'warning'
            html += f"""
        <div class="{priority_class}" style="margin: 20px 0; padding: 15px;">
            <h3>{rec['priority'].upper()}: {rec['title']}</h3>
            <p><strong>Problem:</strong> {rec['problem']}</p>
            <p><strong>Impact:</strong> {rec['impact']}</p>
            <p><strong>Recommendation:</strong> {rec['recommendation']}</p>
            <p><strong>Effort:</strong> {rec['effort']}</p>
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        return html
    
    def _format_as_text(self, report: Dict[str, Any]) -> str:
        """Format report as plain text"""
        text = f"""LOG ANALYSIS REPORT
{'='*80}

Generated: {report['metadata']['generated_at']}

{report['executive_summary']}

{'='*80}

{report['sections'].get('parsing', '')}

{'='*80}

{report['sections'].get('errors', '')}

{'='*80}

{report['sections'].get('patterns', '')}

{'='*80}

RECOMMENDATIONS
{'='*80}

"""
        
        for i, rec in enumerate(report['recommendations'], 1):
            text += f"""
{i}. [{rec['priority'].upper()}] {rec['title']}
   Problem: {rec['problem']}
   Impact: {rec['impact']}
   Recommendation: {rec['recommendation']}
   Effort: {rec['effort']}

"""
        
        return text
    
    def _markdown_to_html(self, markdown: str) -> str:
        """Simple Markdown to HTML conversion"""
        # Basic conversion - in production, use a proper Markdown library
        html = markdown
        html = html.replace('\n## ', '\n<h2>').replace('\n', '</h2>\n', 1)
        html = html.replace('\n### ', '\n<h3>').replace('\n', '</h3>\n', 1)
        html = html.replace('**', '<strong>').replace('**', '</strong>')
        html = html.replace('\n', '<br>\n')
        return html


def main():
    """Test the report generator"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python report_generator.py <analysis_results_dir>")
        print("  Expects parsed.json, errors.json, patterns.json in the directory")
        sys.exit(1)
    
    results_dir = Path(sys.argv[1])
    
    # Load all results
    results = {}
    
    parsed_file = results_dir / "parsed.json"
    if parsed_file.exists():
        with open(parsed_file) as f:
            results['log-parsing'] = json.load(f)
    
    errors_file = results_dir / "errors.json"
    if errors_file.exists():
        with open(errors_file) as f:
            results['error-detection'] = json.load(f)
    
    patterns_file = results_dir / "patterns.json"
    if patterns_file.exists():
        with open(patterns_file) as f:
            results['pattern-analysis'] = json.load(f)
    
    # Generate report
    generator = ReportGenerator()
    report = generator.generate_report(results)
    
    # Save in multiple formats
    md_path = generator.save_report(report, format="markdown")
    print(f"✓ Markdown report: {md_path}")
    
    html_path = generator.save_report(report, format="html")
    print(f"✓ HTML report: {html_path}")
    
    json_path = generator.save_report(report, format="json")
    print(f"✓ JSON report: {json_path}")
    
    print("\n" + "="*60)
    print("EXECUTIVE SUMMARY")
    print("="*60)
    print(report['executive_summary'])


if __name__ == "__main__":
    main()
