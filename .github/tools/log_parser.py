"""
Log Parser Tool
Parses various log file formats into structured data
"""

import re
import json
from typing import Dict, List, Any, Optional, Iterator
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class LogParser:
    """Parse log files in multiple formats"""
    
    def __init__(self):
        self.formats = {
            'apache': self._parse_apache,
            'nginx': self._parse_nginx,
            'syslog': self._parse_syslog,
            'json': self._parse_json,
            'application': self._parse_application,
            'docker': self._parse_docker,
            'kubernetes': self._parse_kubernetes,
            'custom': self._parse_custom
        }
        
        # Compile regex patterns once
        self.patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for efficiency"""
        return {
            'apache_combined': re.compile(
                r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] '
                r'"(?P<method>\w+) (?P<path>[^\s]+) HTTP/[^"]+" '
                r'(?P<status>\d+) (?P<size>\d+|-) '
                r'"(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
            ),
            'nginx_combined': re.compile(
                r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] '
                r'"(?P<method>\w+) (?P<path>[^\s]+)[^"]*" '
                r'(?P<status>\d+) (?P<size>\d+) '
                r'"(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
            ),
            'syslog': re.compile(
                r'(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+) '
                r'(?P<hostname>\S+) '
                r'(?P<process>\w+)(\[(?P<pid>\d+)\])?: '
                r'(?P<message>.*)'
            ),
            'timestamp_iso': re.compile(
                r'(?P<timestamp>\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)'
            ),
            'log_level': re.compile(
                r'\b(?P<level>DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL|FATAL|PANIC)\b',
                re.IGNORECASE
            ),
            'exception': re.compile(
                r'(?P<exception>\w+Exception|\w+Error)(?P<trace>(?:\s+at\s+.+|\s+File\s+".+".+)*)',
                re.MULTILINE
            )
        }
    
    def detect_format(self, file_path: str) -> str:
        """Detect log format by examining content"""
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            # Read first 100 lines for detection
            sample_lines = [f.readline() for _ in range(100) if f.readline()]
        
        # Count matches for each format
        format_scores = defaultdict(int)
        
        for line in sample_lines:
            if not line.strip():
                continue
            
            # Check for JSON
            if line.strip().startswith('{'):
                try:
                    json.loads(line)
                    format_scores['json'] += 1
                except:
                    pass
            
            # Check for Apache/Nginx
            if self.patterns['apache_combined'].match(line):
                format_scores['apache'] += 1
            elif self.patterns['nginx_combined'].match(line):
                format_scores['nginx'] += 1
            
            # Check for syslog
            if self.patterns['syslog'].match(line):
                format_scores['syslog'] += 1
            
            # Check for Docker/K8s
            if 'container_id' in line.lower() or 'pod_name' in line.lower():
                format_scores['kubernetes'] += 1
            elif line.strip().startswith('time=') or '"container_name":' in line:
                format_scores['docker'] += 1
            
            # Check for generic application logs (timestamp + level)
            if self.patterns['timestamp_iso'].search(line) and self.patterns['log_level'].search(line):
                format_scores['application'] += 1
        
        # Return format with highest score
        if format_scores:
            detected_format = max(format_scores, key=format_scores.get)
            return detected_format
        
        return 'custom'
    
    def parse_file(
        self,
        file_path: str,
        log_format: Optional[str] = None,
        max_lines: int = 100000
    ) -> Dict[str, Any]:
        """Parse a log file and return structured data"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Log file not found: {file_path}")
        
        # Detect format if not provided
        if log_format is None:
            log_format = self.detect_format(str(file_path))
        
        print(f"Detected format: {log_format}")
        
        # Get parser function
        parser_func = self.formats.get(log_format, self._parse_custom)
        
        # Parse file
        entries = []
        total_lines = 0
        parse_errors = 0
        
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                total_lines += 1
                if total_lines > max_lines:
                    print(f"Warning: Reached max lines limit ({max_lines})")
                    break
                
                if not line.strip():
                    continue
                
                try:
                    parsed = parser_func(line)
                    if parsed:
                        entries.append(parsed)
                except Exception as e:
                    parse_errors += 1
        
        # Calculate metadata
        timestamps = [e['timestamp'] for e in entries if e.get('timestamp')]
        
        metadata = {
            'start_time': min(timestamps) if timestamps else None,
            'end_time': max(timestamps) if timestamps else None,
            'duration_hours': 0
        }
        
        if metadata['start_time'] and metadata['end_time']:
            try:
                start_dt = datetime.fromisoformat(metadata['start_time'].replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(metadata['end_time'].replace('Z', '+00:00'))
                metadata['duration_hours'] = (end_dt - start_dt).total_seconds() / 3600
            except:
                pass
        
        return {
            'format': log_format,
            'total_lines': total_lines,
            'parsed_lines': len(entries),
            'errors': parse_errors,
            'entries': entries,
            'metadata': metadata,
            'file_path': str(file_path),
            'file_size_mb': file_path.stat().st_size / (1024 * 1024)
        }
    
    def _parse_apache(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse Apache combined log format"""
        match = self.patterns['apache_combined'].match(line)
        if not match:
            return None
        
        groups = match.groupdict()
        
        return {
            'timestamp': self._parse_apache_timestamp(groups['timestamp']),
            'ip_address': groups['ip'],
            'method': groups['method'],
            'path': groups['path'],
            'status_code': int(groups['status']),
            'response_size': int(groups['size']) if groups['size'] != '-' else 0,
            'referer': groups['referer'],
            'user_agent': groups['user_agent'],
            'level': self._status_to_level(int(groups['status'])),
            'raw_line': line.strip()
        }
    
    def _parse_nginx(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse Nginx log format"""
        match = self.patterns['nginx_combined'].match(line)
        if not match:
            return None
        
        groups = match.groupdict()
        
        return {
            'timestamp': self._parse_apache_timestamp(groups['timestamp']),
            'ip_address': groups['ip'],
            'method': groups['method'],
            'path': groups['path'],
            'status_code': int(groups['status']),
            'response_size': int(groups['size']),
            'referer': groups['referer'],
            'user_agent': groups['user_agent'],
            'level': self._status_to_level(int(groups['status'])),
            'raw_line': line.strip()
        }
    
    def _parse_syslog(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse syslog format"""
        match = self.patterns['syslog'].match(line)
        if not match:
            return None
        
        groups = match.groupdict()
        
        return {
            'timestamp': self._parse_syslog_timestamp(groups['timestamp']),
            'hostname': groups['hostname'],
            'process': groups['process'],
            'pid': groups.get('pid'),
            'message': groups['message'],
            'level': self._extract_level(groups['message']),
            'raw_line': line.strip()
        }
    
    def _parse_json(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse JSON log format"""
        try:
            data = json.loads(line)
            
            # Normalize common fields
            entry = {
                'timestamp': self._normalize_timestamp(
                    data.get('timestamp') or data.get('time') or data.get('@timestamp')
                ),
                'level': (data.get('level') or data.get('severity') or 'INFO').upper(),
                'message': data.get('message') or data.get('msg') or '',
                'raw_line': line.strip()
            }
            
            # Preserve all other fields
            for key, value in data.items():
                if key not in ['timestamp', 'time', '@timestamp', 'level', 'severity', 'message', 'msg']:
                    entry[key] = value
            
            return entry
        except json.JSONDecodeError:
            return None
    
    def _parse_application(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse generic application log format"""
        # Extract timestamp
        ts_match = self.patterns['timestamp_iso'].search(line)
        timestamp = ts_match.group('timestamp') if ts_match else None
        
        # Extract log level
        level_match = self.patterns['log_level'].search(line)
        level = level_match.group('level').upper() if level_match else 'INFO'
        
        # Extract message (everything after level)
        if level_match:
            message_start = level_match.end()
            message = line[message_start:].strip(' :-]')
        else:
            message = line.strip()
        
        return {
            'timestamp': self._normalize_timestamp(timestamp),
            'level': level,
            'message': message,
            'raw_line': line.strip()
        }
    
    def _parse_docker(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse Docker container logs"""
        # Docker logs are usually JSON
        if line.strip().startswith('{'):
            return self._parse_json(line)
        
        # Or time= format
        if line.startswith('time='):
            parts = line.split(' ', 1)
            timestamp = parts[0].replace('time=', '') if parts else None
            message = parts[1] if len(parts) > 1 else ''
            
            return {
                'timestamp': self._normalize_timestamp(timestamp),
                'level': self._extract_level(message),
                'message': message.strip(),
                'raw_line': line.strip()
            }
        
        return self._parse_application(line)
    
    def _parse_kubernetes(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse Kubernetes pod logs"""
        # K8s logs are often JSON with pod metadata
        if line.strip().startswith('{'):
            entry = self._parse_json(line)
            if entry:
                # Extract K8s metadata if present
                if 'kubernetes' in entry:
                    k8s_meta = entry['kubernetes']
                    entry['pod_name'] = k8s_meta.get('pod_name')
                    entry['namespace'] = k8s_meta.get('namespace_name')
                    entry['container_name'] = k8s_meta.get('container_name')
                return entry
        
        return self._parse_application(line)
    
    def _parse_custom(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse custom/unknown format - best effort"""
        return {
            'timestamp': self._extract_any_timestamp(line),
            'level': self._extract_level(line),
            'message': line.strip(),
            'raw_line': line.strip()
        }
    
    def _parse_apache_timestamp(self, timestamp_str: str) -> str:
        """Convert Apache timestamp to ISO format"""
        # Example: 21/May/2026:10:23:45 +0000
        try:
            dt = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z')
            return dt.isoformat()
        except:
            return timestamp_str
    
    def _parse_syslog_timestamp(self, timestamp_str: str) -> str:
        """Convert syslog timestamp to ISO format"""
        # Example: May 21 10:23:45
        try:
            # Add current year
            current_year = datetime.now().year
            dt = datetime.strptime(f"{timestamp_str} {current_year}", '%b %d %H:%M:%S %Y')
            return dt.isoformat()
        except:
            return timestamp_str
    
    def _normalize_timestamp(self, timestamp: Any) -> Optional[str]:
        """Normalize timestamp to ISO 8601 format"""
        if not timestamp:
            return None
        
        if isinstance(timestamp, (int, float)):
            # Unix epoch
            return datetime.fromtimestamp(timestamp).isoformat()
        
        if isinstance(timestamp, str):
            # Try parsing various formats
            for fmt in [
                '%Y-%m-%dT%H:%M:%S.%fZ',
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S%z',
            ]:
                try:
                    dt = datetime.strptime(timestamp, fmt)
                    return dt.isoformat()
                except:
                    continue
            
            # Return as-is if can't parse
            return timestamp
        
        return None
    
    def _extract_any_timestamp(self, line: str) -> Optional[str]:
        """Extract any timestamp from line"""
        match = self.patterns['timestamp_iso'].search(line)
        if match:
            return self._normalize_timestamp(match.group('timestamp'))
        return None
    
    def _extract_level(self, text: str) -> str:
        """Extract log level from text"""
        match = self.patterns['log_level'].search(text)
        if match:
            return match.group('level').upper()
        return 'INFO'
    
    def _status_to_level(self, status_code: int) -> str:
        """Convert HTTP status code to log level"""
        if status_code >= 500:
            return 'ERROR'
        elif status_code >= 400:
            return 'WARNING'
        else:
            return 'INFO'


def main():
    """Test the log parser"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python log_parser.py <log_file>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    
    parser = LogParser()
    result = parser.parse_file(log_file)
    
    print("\n" + "="*60)
    print("LOG PARSING RESULTS")
    print("="*60)
    print(f"Format: {result['format']}")
    print(f"Total lines: {result['total_lines']:,}")
    print(f"Parsed lines: {result['parsed_lines']:,}")
    print(f"Parse errors: {result['errors']}")
    print(f"File size: {result['file_size_mb']:.2f} MB")
    print(f"\nTime range:")
    print(f"  Start: {result['metadata']['start_time']}")
    print(f"  End: {result['metadata']['end_time']}")
    print(f"  Duration: {result['metadata']['duration_hours']:.2f} hours")
    
    print(f"\nSample entries (first 3):")
    for i, entry in enumerate(result['entries'][:3], 1):
        print(f"\n{i}. {entry.get('timestamp', 'N/A')} [{entry.get('level', 'INFO')}]")
        print(f"   {entry.get('message', entry.get('raw_line', ''))[:100]}")
    
    # Save to JSON
    output_file = f"{log_file}_parsed.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n✓ Full results saved to: {output_file}")


if __name__ == "__main__":
    main()
