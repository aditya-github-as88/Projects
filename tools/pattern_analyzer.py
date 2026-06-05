"""
Pattern Analyzer Tool
Analyzes patterns, trends, and anomalies in log data
"""

import json
import statistics
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, Counter


class PatternAnalyzer:
    """Analyze patterns and anomalies in log data"""
    
    def __init__(self):
        self.min_pattern_frequency = 3
        self.anomaly_threshold = 3.0  # Standard deviations
    
    def analyze_patterns(self, parsed_logs: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point - analyze all patterns"""
        entries = parsed_logs.get('entries', [])
        
        # Find recurring patterns
        patterns = self.find_recurring_patterns(entries)
        
        # Detect anomalies
        anomalies = self.detect_anomalies(entries)
        
        # Analyze trends
        trends = self.analyze_trends(entries)
        
        # Find correlations (if error data available)
        correlations = self.find_correlations(entries)
        
        # Identify peak times
        peaks = self.identify_peaks(entries)
        
        # Find sequential patterns
        sequences = self.find_sequences(entries)
        
        # Generate insights
        insights = self.generate_insights(patterns, anomalies, trends)
        
        return {
            'pattern_count': len(patterns),
            'anomaly_count': len(anomalies),
            'patterns': patterns,
            'anomalies': anomalies,
            'trends': trends,
            'correlations': correlations,
            'peak_times': peaks,
            'sequences': sequences,
            'insights': insights
        }
    
    def find_recurring_patterns(
        self,
        entries: List[Dict[str, Any]],
        min_frequency: int = None
    ) -> List[Dict[str, Any]]:
        """Find recurring patterns in logs"""
        if min_frequency is None:
            min_frequency = self.min_pattern_frequency
        
        patterns = []
        
        # Pattern 1: Temporal patterns (same error at regular intervals)
        temporal = self._find_temporal_patterns(entries, min_frequency)
        patterns.extend(temporal)
        
        # Pattern 2: Request patterns (same endpoint/path repeatedly)
        request_patterns = self._find_request_patterns(entries, min_frequency)
        patterns.extend(request_patterns)
        
        # Pattern 3: Error message patterns
        error_patterns = self._find_error_message_patterns(entries, min_frequency)
        patterns.extend(error_patterns)
        
        return patterns
    
    def detect_anomalies(
        self,
        entries: List[Dict[str, Any]],
        threshold: float = None
    ) -> List[Dict[str, Any]]:
        """Detect anomalies in log data"""
        if threshold is None:
            threshold = self.anomaly_threshold
        
        anomalies = []
        
        # Volume anomalies
        volume_anomalies = self._detect_volume_anomalies(entries, threshold)
        anomalies.extend(volume_anomalies)
        
        # Response time anomalies (if available)
        if any('response_time' in e for e in entries):
            response_anomalies = self._detect_response_anomalies(entries, threshold)
            anomalies.extend(response_anomalies)
        
        # Error rate anomalies
        error_anomalies = self._detect_error_rate_anomalies(entries, threshold)
        anomalies.extend(error_anomalies)
        
        return anomalies
    
    def analyze_trends(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends over time"""
        if not entries:
            return {}
        
        # Group by time buckets
        hourly_data = self._group_by_hour(entries)
        
        if len(hourly_data) < 2:
            return {'trend': 'insufficient_data'}
        
        # Calculate request volume trend
        volumes = [data['count'] for data in hourly_data]
        volume_trend = self._calculate_trend(volumes)
        
        # Calculate error rate trend
        error_rates = [
            (data['errors'] / data['count'] * 100) if data['count'] > 0 else 0
            for data in hourly_data
        ]
        error_trend = self._calculate_trend(error_rates)
        
        return {
            'volume_trend': volume_trend,
            'error_rate_trend': error_trend,
            'hourly_data': hourly_data
        }
    
    def find_correlations(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find correlations between events"""
        correlations = []
        
        # Correlate high traffic with errors
        traffic_error_corr = self._correlate_traffic_errors(entries)
        if traffic_error_corr:
            correlations.append(traffic_error_corr)
        
        # Correlate specific paths with errors
        path_error_corr = self._correlate_paths_errors(entries)
        correlations.extend(path_error_corr)
        
        return correlations
    
    def identify_peaks(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify peak activity times"""
        hourly_data = self._group_by_hour(entries)
        
        if not hourly_data:
            return {}
        
        # Find peak hour
        peak_hour = max(hourly_data, key=lambda x: x['count'])
        low_hour = min(hourly_data, key=lambda x: x['count'])
        
        # Calculate average
        avg_count = statistics.mean([d['count'] for d in hourly_data])
        
        return {
            'peak_hour': peak_hour['hour'],
            'peak_count': peak_hour['count'],
            'low_hour': low_hour['hour'],
            'low_count': low_hour['count'],
            'average': round(avg_count, 2),
            'peak_vs_average': round((peak_hour['count'] / avg_count - 1) * 100, 2) if avg_count > 0 else 0
        }
    
    def find_sequences(
        self,
        entries: List[Dict[str, Any]],
        min_support: int = 5
    ) -> List[Dict[str, Any]]:
        """Find sequential patterns"""
        sequences = []
        
        # Look for error -> retry -> success patterns
        retry_sequences = self._find_retry_patterns(entries, min_support)
        sequences.extend(retry_sequences)
        
        return sequences
    
    def generate_insights(
        self,
        patterns: List[Dict[str, Any]],
        anomalies: List[Dict[str, Any]],
        trends: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate actionable insights from patterns"""
        insights = []
        
        # Insight from patterns
        for pattern in patterns:
            if pattern['frequency'] >= 10:
                insights.append({
                    'type': 'pattern',
                    'severity': 'medium' if pattern['frequency'] < 50 else 'high',
                    'title': f"Recurring pattern detected: {pattern['description']}",
                    'description': f"This pattern occurs {pattern['frequency']} times",
                    'recommendation': self._get_pattern_recommendation(pattern)
                })
        
        # Insights from anomalies
        for anomaly in anomalies:
            insights.append({
                'type': 'anomaly',
                'severity': anomaly.get('severity', 'medium'),
                'title': f"Anomaly detected: {anomaly['description']}",
                'description': f"Deviation: {anomaly.get('deviation', 'N/A')}",
                'recommendation': self._get_anomaly_recommendation(anomaly)
            })
        
        # Insights from trends
        if trends.get('error_rate_trend', {}).get('direction') == 'increasing':
            insights.append({
                'type': 'trend',
                'severity': 'high',
                'title': "Error rate is increasing",
                'description': f"Error rate increasing by {trends['error_rate_trend'].get('change_percent', 0):.1f}%",
                'recommendation': "Investigate recent changes or deployments that may have introduced errors"
            })
        
        return insights
    
    def _find_temporal_patterns(
        self,
        entries: List[Dict[str, Any]],
        min_frequency: int
    ) -> List[Dict[str, Any]]:
        """Find patterns that occur at regular intervals"""
        patterns = []
        
        # Group errors by message
        error_groups = defaultdict(list)
        for entry in entries:
            if entry.get('level') in ['ERROR', 'CRITICAL']:
                message = entry.get('message', '')[:100]  # First 100 chars
                if entry.get('timestamp'):
                    error_groups[message].append(entry['timestamp'])
        
        # Check for regular intervals
        for message, timestamps in error_groups.items():
            if len(timestamps) >= min_frequency:
                # Calculate intervals
                intervals = self._calculate_intervals(timestamps)
                if intervals and self._is_regular(intervals):
                    avg_interval = statistics.mean(intervals)
                    patterns.append({
                        'pattern_id': f"PAT{len(patterns)+1:03d}",
                        'type': 'temporal',
                        'description': f"Error occurs regularly every {self._format_interval(avg_interval)}",
                        'frequency': len(timestamps),
                        'message_preview': message[:80],
                        'interval_minutes': avg_interval,
                        'confidence': 0.9
                    })
        
        return patterns
    
    def _find_request_patterns(
        self,
        entries: List[Dict[str, Any]],
        min_frequency: int
    ) -> List[Dict[str, Any]]:
        """Find repeated request patterns"""
        patterns = []
        
        # Count requests by path
        path_counter = Counter()
        for entry in entries:
            path = entry.get('path')
            if path:
                path_counter[path] += 1
        
        # Find high-frequency paths
        for path, count in path_counter.most_common(10):
            if count >= min_frequency:
                patterns.append({
                    'pattern_id': f"PAT{len(patterns)+1:03d}",
                    'type': 'request',
                    'description': f"Frequent requests to {path}",
                    'frequency': count,
                    'path': path,
                    'confidence': 0.95
                })
        
        return patterns
    
    def _find_error_message_patterns(
        self,
        entries: List[Dict[str, Any]],
        min_frequency: int
    ) -> List[Dict[str, Any]]:
        """Find repeated error messages"""
        patterns = []
        
        # Count error messages
        error_messages = Counter()
        for entry in entries:
            if entry.get('level') in ['ERROR', 'CRITICAL']:
                message = entry.get('message', '')
                # Parameterize message (remove numbers, IDs)
                parameterized = self._parameterize(message)
                error_messages[parameterized] += 1
        
        # Find frequent error messages
        for message, count in error_messages.most_common(10):
            if count >= min_frequency:
                patterns.append({
                    'pattern_id': f"PAT{len(patterns)+1:03d}",
                    'type': 'error_message',
                    'description': f"Repeated error: {message[:80]}",
                    'frequency': count,
                    'message': message,
                    'confidence': 0.85
                })
        
        return patterns
    
    def _detect_volume_anomalies(
        self,
        entries: List[Dict[str, Any]],
        threshold: float
    ) -> List[Dict[str, Any]]:
        """Detect volume spikes/drops"""
        anomalies = []
        
        hourly_data = self._group_by_hour(entries)
        if len(hourly_data) < 3:
            return anomalies
        
        volumes = [d['count'] for d in hourly_data]
        mean_volume = statistics.mean(volumes)
        
        if len(volumes) < 2:
            return anomalies
        
        stdev_volume = statistics.stdev(volumes) if len(volumes) > 1 else 0
        
        # Find anomalies
        for data in hourly_data:
            if stdev_volume > 0:
                deviation = (data['count'] - mean_volume) / stdev_volume
                
                if abs(deviation) >= threshold:
                    anomaly_type = 'spike' if deviation > 0 else 'drop'
                    anomalies.append({
                        'anomaly_id': f"ANO{len(anomalies)+1:03d}",
                        'type': 'volume',
                        'subtype': anomaly_type,
                        'severity': 'high' if abs(deviation) > 5 else 'medium',
                        'description': f"Volume {anomaly_type} detected at {data['hour']}",
                        'baseline': round(mean_volume, 2),
                        'observed': data['count'],
                        'deviation': round(deviation, 2),
                        'timestamp': data['hour']
                    })
        
        return anomalies
    
    def _detect_response_anomalies(
        self,
        entries: List[Dict[str, Any]],
        threshold: float
    ) -> List[Dict[str, Any]]:
        """Detect response time anomalies"""
        anomalies = []
        
        # Collect response times
        response_times = []
        for entry in entries:
            rt = entry.get('response_time')
            if rt and rt > 0:
                response_times.append({'time': entry.get('timestamp'), 'value': rt})
        
        if len(response_times) < 10:
            return anomalies
        
        values = [rt['value'] for rt in response_times]
        mean_rt = statistics.mean(values)
        stdev_rt = statistics.stdev(values) if len(values) > 1 else 0
        
        # Find slow responses
        if stdev_rt > 0:
            for rt in response_times:
                deviation = (rt['value'] - mean_rt) / stdev_rt
                if deviation >= threshold:
                    anomalies.append({
                        'anomaly_id': f"ANO{len(anomalies)+1:03d}",
                        'type': 'response_time',
                        'severity': 'high' if deviation > 5 else 'medium',
                        'description': f"Slow response detected",
                        'baseline': round(mean_rt, 3),
                        'observed': round(rt['value'], 3),
                        'deviation': round(deviation, 2),
                        'timestamp': rt['time']
                    })
        
        return anomalies
    
    def _detect_error_rate_anomalies(
        self,
        entries: List[Dict[str, Any]],
        threshold: float
    ) -> List[Dict[str, Any]]:
        """Detect error rate anomalies"""
        anomalies = []
        
        hourly_data = self._group_by_hour(entries)
        if len(hourly_data) < 3:
            return anomalies
        
        error_rates = [
            (d['errors'] / d['count'] * 100) if d['count'] > 0 else 0
            for d in hourly_data
        ]
        
        mean_rate = statistics.mean(error_rates)
        stdev_rate = statistics.stdev(error_rates) if len(error_rates) > 1 else 0
        
        if stdev_rate > 0:
            for i, data in enumerate(hourly_data):
                rate = error_rates[i]
                deviation = (rate - mean_rate) / stdev_rate
                
                if deviation >= threshold:
                    anomalies.append({
                        'anomaly_id': f"ANO{len(anomalies)+1:03d}",
                        'type': 'error_rate',
                        'severity': 'high',
                        'description': f"Error rate spike at {data['hour']}",
                        'baseline': round(mean_rate, 2),
                        'observed': round(rate, 2),
                        'deviation': round(deviation, 2),
                        'timestamp': data['hour']
                    })
        
        return anomalies
    
    def _group_by_hour(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Group entries by hour"""
        hourly = defaultdict(lambda: {'count': 0, 'errors': 0})
        
        for entry in entries:
            ts = entry.get('timestamp')
            if not ts:
                continue
            
            try:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                hour_key = dt.strftime('%Y-%m-%d %H:00')
                
                hourly[hour_key]['count'] += 1
                if entry.get('level') in ['ERROR', 'CRITICAL']:
                    hourly[hour_key]['errors'] += 1
            except:
                continue
        
        return [
            {'hour': hour, **data}
            for hour, data in sorted(hourly.items())
        ]
    
    def _calculate_trend(self, values: List[float]) -> Dict[str, Any]:
        """Calculate trend direction and magnitude"""
        if len(values) < 2:
            return {'direction': 'stable', 'change_percent': 0}
        
        # Simple linear trend
        start_avg = statistics.mean(values[:len(values)//3])
        end_avg = statistics.mean(values[-len(values)//3:])
        
        change_percent = ((end_avg - start_avg) / start_avg * 100) if start_avg > 0 else 0
        
        if change_percent > 10:
            direction = 'increasing'
        elif change_percent < -10:
            direction = 'decreasing'
        else:
            direction = 'stable'
        
        return {
            'direction': direction,
            'change_percent': round(change_percent, 2),
            'start_value': round(start_avg, 2),
            'end_value': round(end_avg, 2)
        }
    
    def _correlate_traffic_errors(self, entries: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Check if high traffic correlates with errors"""
        hourly = self._group_by_hour(entries)
        
        if len(hourly) < 3:
            return None
        
        # Calculate correlation coefficient
        volumes = [h['count'] for h in hourly]
        errors = [h['errors'] for h in hourly]
        
        if len(volumes) < 2:
            return None
        
        # Simple correlation check
        high_traffic_hours = [h for h in hourly if h['count'] > statistics.mean(volumes)]
        high_error_hours = [h for h in hourly if h['errors'] > statistics.mean(errors)]
        
        overlap = len(set(h['hour'] for h in high_traffic_hours) & set(h['hour'] for h in high_error_hours))
        
        if overlap >= len(high_traffic_hours) * 0.7:  # 70% overlap
            return {
                'correlation_id': 'COR001',
                'event_a': 'high_traffic',
                'event_b': 'high_errors',
                'correlation_strength': round(overlap / len(high_traffic_hours), 2),
                'description': 'High traffic correlates with increased errors'
            }
        
        return None
    
    def _correlate_paths_errors(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find paths with high error rates"""
        correlations = []
        
        path_stats = defaultdict(lambda: {'total': 0, 'errors': 0})
        
        for entry in entries:
            path = entry.get('path')
            if not path:
                continue
            
            path_stats[path]['total'] += 1
            status = entry.get('status_code', 200)
            if status >= 500 or entry.get('level') == 'ERROR':
                path_stats[path]['errors'] += 1
        
        # Find problematic paths
        for path, stats in path_stats.items():
            if stats['total'] >= 10:  # Minimum requests
                error_rate = stats['errors'] / stats['total']
                if error_rate > 0.1:  # >10% error rate
                    correlations.append({
                        'correlation_id': f"COR{len(correlations)+2:03d}",
                        'event_a': f"requests_to_{path}",
                        'event_b': 'errors',
                        'correlation_strength': round(error_rate, 2),
                        'description': f"Path {path} has {error_rate*100:.1f}% error rate"
                    })
        
        return correlations
    
    def _find_retry_patterns(
        self,
        entries: List[Dict[str, Any]],
        min_support: int
    ) -> List[Dict[str, Any]]:
        """Find error -> retry -> success patterns"""
        # Simplified implementation
        return []
    
    def _calculate_intervals(self, timestamps: List[str]) -> List[float]:
        """Calculate time intervals between timestamps in minutes"""
        if len(timestamps) < 2:
            return []
        
        try:
            dts = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in sorted(timestamps)]
            intervals = []
            for i in range(len(dts) - 1):
                interval_minutes = (dts[i+1] - dts[i]).total_seconds() / 60
                intervals.append(interval_minutes)
            return intervals
        except:
            return []
    
    def _is_regular(self, intervals: List[float], tolerance: float = 0.2) -> bool:
        """Check if intervals are regular (within tolerance)"""
        if len(intervals) < 2:
            return False
        
        mean_interval = statistics.mean(intervals)
        if mean_interval == 0:
            return False
        
        # Check if all intervals are within tolerance of mean
        for interval in intervals:
            deviation = abs(interval - mean_interval) / mean_interval
            if deviation > tolerance:
                return False
        
        return True
    
    def _format_interval(self, minutes: float) -> str:
        """Format interval in human-readable form"""
        if minutes < 1:
            return f"{minutes*60:.0f} seconds"
        elif minutes < 60:
            return f"{minutes:.0f} minutes"
        else:
            return f"{minutes/60:.1f} hours"
    
    def _parameterize(self, message: str) -> str:
        """Remove specific values from message"""
        import re
        message = re.sub(r'\d+', '<NUM>', message)
        message = re.sub(r'[0-9a-fA-F]{8,}', '<ID>', message)
        return message
    
    def _get_pattern_recommendation(self, pattern: Dict[str, Any]) -> str:
        """Get recommendation for a pattern"""
        if pattern['type'] == 'temporal':
            return "Investigate scheduled jobs or periodic tasks that may be causing this issue"
        elif pattern['type'] == 'request':
            return "Monitor this endpoint for performance issues or consider caching"
        else:
            return "Investigate root cause of this recurring error"
    
    def _get_anomaly_recommendation(self, anomaly: Dict[str, Any]) -> str:
        """Get recommendation for an anomaly"""
        if anomaly['type'] == 'volume':
            if anomaly['subtype'] == 'spike':
                return "Investigate cause of traffic spike - could be legitimate growth or an attack"
            else:
                return "Check for system issues causing reduced traffic"
        elif anomaly['type'] == 'error_rate':
            return "Immediate investigation required - error rate spike detected"
        else:
            return "Review logs around this time for related issues"


def main():
    """Test the pattern analyzer"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pattern_analyzer.py <parsed_logs.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    with open(input_file, 'r') as f:
        parsed_logs = json.load(f)
    
    analyzer = PatternAnalyzer()
    results = analyzer.analyze_patterns(parsed_logs)
    
    print("\n" + "="*60)
    print("PATTERN ANALYSIS RESULTS")
    print("="*60)
    print(f"Patterns found: {results['pattern_count']}")
    print(f"Anomalies detected: {results['anomaly_count']}")
    
    if results['patterns']:
        print(f"\nTop patterns:")
        for pattern in results['patterns'][:5]:
            print(f"  - {pattern['description']} (freq: {pattern['frequency']})")
    
    if results['anomalies']:
        print(f"\nAnomalies:")
        for anomaly in results['anomalies'][:5]:
            print(f"  - {anomaly['description']} (severity: {anomaly['severity']})")
    
    if results['insights']:
        print(f"\nInsights:")
        for insight in results['insights'][:3]:
            print(f"  - [{insight['severity'].upper()}] {insight['title']}")
    
    # Save results
    output_file = input_file.replace('.json', '_patterns.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✓ Full results saved to: {output_file}")


if __name__ == "__main__":
    main()
