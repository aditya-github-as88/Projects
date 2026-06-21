"""
Error Detector Tool
Detects and categorizes errors from parsed log data
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict, Counter


class ErrorDetector:
    """Detect and categorize errors in log data"""
    
    def __init__(self):
        # Error keywords by category
        self.error_categories = {
            'database': [
                'connection', 'query', 'sql', 'database', 'db', 'timeout',
                'deadlock', 'constraint', 'transaction', 'commit', 'rollback'
            ],
            'network': [
                'connection refused', 'timeout', 'network', 'socket', 'dns',
                'unreachable', 'host', 'port', 'tcp', 'http'
            ],
            'authentication': [
                'auth', 'authentication', 'unauthorized', 'forbidden',
                'permission denied', 'access denied', 'token', 'login', 'credential'
            ],
            'application': [
                'nullpointer', 'null', 'exception', 'runtime', 'assertion',
                'index', 'array', 'illegal', 'invalid state'
            ],
            'configuration': [
                'config', 'configuration', 'missing', 'not found', 'invalid',
                'property', 'setting', 'environment'
            ],
            'resource': [
                'memory', 'disk', 'cpu', 'out of', 'full', 'exhausted',
                'quota', 'limit', 'capacity'
            ],
            'timeout': [
                'timeout', 'timed out', 'deadline', 'expired', 'slow'
            ],
            'validation': [
                'validation', 'invalid', 'constraint', 'format', 'parse'
            ]
        }
        
        # Critical error indicators
        self.critical_indicators = [
            'fatal', 'critical', 'panic', 'crash', 'abort',
            'out of memory', 'segmentation fault', 'core dump',
            'system failure', 'cannot recover'
        ]
        
        # Compile regex patterns
        self.exception_pattern = re.compile(
            r'(\w+Exception|\w+Error)(?:\s*:\s*(.+))?'
        )
    
    def detect_errors(self, parsed_logs: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point - detect all errors in parsed logs"""
        entries = parsed_logs.get('entries', [])
        
        # Filter error-level entries
        error_entries = self.filter_errors(entries)
        
        # Categorize errors
        categorized = self.categorize_errors(error_entries)
        
        # Extract detailed error information
        error_details = self.extract_error_details(categorized)
        
        # Group similar errors
        grouped_errors = self.group_similar_errors(error_details)
        
        # Calculate metrics
        metrics = self.calculate_metrics(grouped_errors, parsed_logs)
        
        # Identify critical errors
        critical_errors = self.identify_critical_errors(grouped_errors)
        
        # Create timeline
        timeline = self.create_error_timeline(grouped_errors)
        
        return {
            'total_errors': len(error_entries),
            'unique_error_types': len(grouped_errors),
            'error_percentage': metrics['error_percentage'],
            'error_rate_per_hour': metrics['error_rate_per_hour'],
            'critical_errors': len(critical_errors),
            'error_distribution': metrics['distribution'],
            'categorized_errors': categorized,
            'grouped_errors': grouped_errors,
            'critical_error_list': critical_errors,
            'timeline': timeline,
            'top_errors': self.get_top_errors(grouped_errors, limit=10)
        }
    
    def filter_errors(
        self,
        entries: List[Dict[str, Any]],
        levels: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Filter entries by error severity levels"""
        if levels is None:
            levels = ['CRITICAL', 'ERROR', 'FATAL', 'PANIC']
        
        error_entries = []
        
        for entry in entries:
            # Check log level
            level = entry.get('level', '').upper()
            if level in levels:
                error_entries.append(entry)
                continue
            
            # Check status code (5xx = server error)
            status = entry.get('status_code', 0)
            if status >= 500:
                error_entries.append(entry)
                continue
            
            # Check message for error keywords
            message = entry.get('message', '').lower()
            if any(keyword in message for keyword in ['error', 'exception', 'failed', 'failure']):
                error_entries.append(entry)
        
        return error_entries
    
    def categorize_errors(self, error_entries: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize errors by type"""
        categorized = defaultdict(list)
        
        for entry in error_entries:
            message = entry.get('message', '').lower()
            raw_line = entry.get('raw_line', '').lower()
            text = message + ' ' + raw_line
            
            # Find matching category
            category = 'unknown'
            max_matches = 0
            
            for cat_name, keywords in self.error_categories.items():
                matches = sum(1 for keyword in keywords if keyword in text)
                if matches > max_matches:
                    max_matches = matches
                    category = cat_name
            
            categorized[category].append(entry)
        
        return dict(categorized)
    
    def extract_error_details(self, categorized_errors: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Extract detailed information from errors"""
        error_details = []
        error_id = 1
        
        for category, entries in categorized_errors.items():
            for entry in entries:
                # Extract exception type and message
                exception_info = self._extract_exception(entry)
                
                detail = {
                    'error_id': f"ERR{error_id:03d}",
                    'category': category,
                    'type': exception_info.get('type', 'Unknown'),
                    'message': exception_info.get('message', entry.get('message', '')),
                    'timestamp': entry.get('timestamp'),
                    'level': entry.get('level', 'ERROR'),
                    'severity': self._determine_severity(entry),
                    'affected_component': self._extract_component(entry),
                    'raw_entry': entry
                }
                
                error_details.append(detail)
                error_id += 1
        
        return error_details
    
    def group_similar_errors(
        self,
        error_details: List[Dict[str, Any]],
        similarity_threshold: float = 0.8
    ) -> List[Dict[str, Any]]:
        """Group similar errors together"""
        groups = []
        processed = set()
        
        for i, error1 in enumerate(error_details):
            if i in processed:
                continue
            
            # Create new group
            group = {
                'error_id': error1['error_id'],
                'category': error1['category'],
                'type': error1['type'],
                'message_template': self._parameterize_message(error1['message']),
                'occurrences': 1,
                'first_seen': error1['timestamp'],
                'last_seen': error1['timestamp'],
                'severity': error1['severity'],
                'examples': [error1]
            }
            
            # Find similar errors
            for j, error2 in enumerate(error_details[i+1:], start=i+1):
                if j in processed:
                    continue
                
                if self._are_similar(error1, error2, similarity_threshold):
                    group['occurrences'] += 1
                    group['last_seen'] = error2['timestamp']
                    if len(group['examples']) < 5:
                        group['examples'].append(error2)
                    processed.add(j)
            
            groups.append(group)
            processed.add(i)
        
        # Sort by occurrence count
        groups.sort(key=lambda x: x['occurrences'], reverse=True)
        
        return groups
    
    def calculate_metrics(
        self,
        grouped_errors: List[Dict[str, Any]],
        parsed_logs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate error statistics"""
        total_lines = parsed_logs.get('parsed_lines', 0)
        total_errors = sum(g['occurrences'] for g in grouped_errors)
        
        # Error percentage
        error_percentage = (total_errors / total_lines * 100) if total_lines > 0 else 0
        
        # Error rate per hour
        duration_hours = parsed_logs.get('metadata', {}).get('duration_hours', 1)
        error_rate_per_hour = total_errors / duration_hours if duration_hours > 0 else 0
        
        # Distribution by category
        distribution = defaultdict(int)
        for group in grouped_errors:
            distribution[group['category']] += group['occurrences']
        
        # Convert to percentages
        if total_errors > 0:
            distribution = {
                cat: (count / total_errors * 100)
                for cat, count in distribution.items()
            }
        
        return {
            'total_errors': total_errors,
            'error_percentage': round(error_percentage, 2),
            'error_rate_per_hour': round(error_rate_per_hour, 2),
            'distribution': dict(distribution)
        }
    
    def identify_critical_errors(self, grouped_errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify critical errors requiring immediate attention"""
        critical = []
        
        for group in grouped_errors:
            is_critical = False
            reasons = []
            
            # Check severity
            if group['severity'] == 'CRITICAL':
                is_critical = True
                reasons.append('Critical severity level')
            
            # Check frequency
            if group['occurrences'] > 100:
                is_critical = True
                reasons.append(f"High frequency ({group['occurrences']} occurrences)")
            
            # Check for critical keywords
            message = group['message_template'].lower()
            for indicator in self.critical_indicators:
                if indicator in message:
                    is_critical = True
                    reasons.append(f"Critical indicator: {indicator}")
                    break
            
            # Check category
            if group['category'] in ['resource', 'database']:
                if group['occurrences'] > 50:
                    is_critical = True
                    reasons.append(f"Critical category with high frequency")
            
            if is_critical:
                critical.append({
                    **group,
                    'critical_reasons': reasons
                })
        
        return critical
    
    def create_error_timeline(
        self,
        grouped_errors: List[Dict[str, Any]],
        interval: str = '1hour'
    ) -> Dict[str, Any]:
        """Create timeline of errors"""
        # Collect all timestamps
        all_timestamps = []
        for group in grouped_errors:
            for example in group['examples']:
                ts = example.get('timestamp')
                if ts:
                    all_timestamps.append(ts)
        
        if not all_timestamps:
            return {'buckets': [], 'interval': interval}
        
        # Parse timestamps and create buckets
        from datetime import datetime, timedelta
        
        timestamps = []
        for ts in all_timestamps:
            try:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                timestamps.append(dt)
            except:
                continue
        
        if not timestamps:
            return {'buckets': [], 'interval': interval}
        
        # Create hourly buckets
        start_time = min(timestamps)
        end_time = max(timestamps)
        
        buckets = []
        current_time = start_time.replace(minute=0, second=0, microsecond=0)
        
        while current_time <= end_time:
            next_time = current_time + timedelta(hours=1)
            
            # Count errors in this bucket
            bucket_errors = [ts for ts in timestamps if current_time <= ts < next_time]
            
            buckets.append({
                'timestamp': current_time.isoformat(),
                'error_count': len(bucket_errors)
            })
            
            current_time = next_time
        
        return {
            'interval': interval,
            'buckets': buckets
        }
    
    def get_top_errors(self, grouped_errors: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
        """Get top N most frequent errors"""
        return grouped_errors[:limit]
    
    def _extract_exception(self, entry: Dict[str, Any]) -> Dict[str, str]:
        """Extract exception type and message"""
        message = entry.get('message', '')
        
        match = self.exception_pattern.search(message)
        if match:
            return {
                'type': match.group(1),
                'message': match.group(2) if match.group(2) else message
            }
        
        return {
            'type': 'Unknown',
            'message': message
        }
    
    def _determine_severity(self, entry: Dict[str, Any]) -> str:
        """Determine error severity"""
        level = entry.get('level', '').upper()
        
        if level in ['CRITICAL', 'FATAL', 'PANIC']:
            return 'CRITICAL'
        elif level == 'ERROR':
            # Check message for critical indicators
            message = entry.get('message', '').lower()
            if any(indicator in message for indicator in self.critical_indicators):
                return 'CRITICAL'
            return 'ERROR'
        elif level == 'WARNING':
            return 'WARNING'
        else:
            return 'ERROR'  # Default
    
    def _extract_component(self, entry: Dict[str, Any]) -> str:
        """Extract affected component/service name"""
        # Try to extract from common fields
        component = entry.get('service') or entry.get('logger') or entry.get('process')
        
        if component:
            return component
        
        # Try to extract from message
        message = entry.get('message', '')
        
        # Look for common patterns
        patterns = [
            r'\[(\w+)\]',  # [ServiceName]
            r'(\w+Service)',  # UserService
            r'(\w+Controller)',  # ApiController
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                return match.group(1)
        
        return 'unknown'
    
    def _parameterize_message(self, message: str) -> str:
        """Replace specific values with placeholders for grouping"""
        # Replace numbers
        message = re.sub(r'\d+', '<NUM>', message)
        
        # Replace IDs (hexadecimal)
        message = re.sub(r'[0-9a-fA-F]{8,}', '<ID>', message)
        
        # Replace IP addresses
        message = re.sub(r'\d+\.\d+\.\d+\.\d+', '<IP>', message)
        
        # Replace UUIDs
        message = re.sub(
            r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',
            '<UUID>',
            message
        )
        
        return message
    
    def _are_similar(
        self,
        error1: Dict[str, Any],
        error2: Dict[str, Any],
        threshold: float
    ) -> bool:
        """Check if two errors are similar"""
        # Must be same category
        if error1['category'] != error2['category']:
            return False
        
        # Must be same exception type
        if error1['type'] != error2['type']:
            return False
        
        # Compare parameterized messages
        msg1 = self._parameterize_message(error1['message'])
        msg2 = self._parameterize_message(error2['message'])
        
        if msg1 == msg2:
            return True
        
        # Calculate similarity (simple approach)
        similarity = self._calculate_similarity(msg1, msg2)
        
        return similarity >= threshold
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        # Simple word-based similarity
        words1 = set(str1.lower().split())
        words2 = set(str2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)


def main():
    """Test the error detector"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python error_detector.py <parsed_logs.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    with open(input_file, 'r') as f:
        parsed_logs = json.load(f)
    
    detector = ErrorDetector()
    results = detector.detect_errors(parsed_logs)
    
    print("\n" + "="*60)
    print("ERROR DETECTION RESULTS")
    print("="*60)
    print(f"Total errors: {results['total_errors']:,}")
    print(f"Unique error types: {results['unique_error_types']}")
    print(f"Error rate: {results['error_percentage']}%")
    print(f"Errors per hour: {results['error_rate_per_hour']:.1f}")
    print(f"Critical errors: {results['critical_errors']}")
    
    print(f"\nError distribution:")
    for category, percentage in sorted(
        results['error_distribution'].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"  {category:15s}: {percentage:6.2f}%")
    
    print(f"\nTop 5 errors:")
    for i, error in enumerate(results['top_errors'][:5], 1):
        print(f"\n{i}. [{error['error_id']}] {error['type']}")
        print(f"   Category: {error['category']}")
        print(f"   Occurrences: {error['occurrences']}")
        print(f"   Message: {error['message_template'][:80]}")
    
    # Save results
    output_file = input_file.replace('.json', '_errors.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✓ Full results saved to: {output_file}")


if __name__ == "__main__":
    main()
