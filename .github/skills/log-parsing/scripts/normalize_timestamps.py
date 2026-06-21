#!/usr/bin/env python3
"""
Normalize Timestamps Script
Converts all timestamps to ISO 8601 format
"""

import json
import argparse
from datetime import datetime
from typing import Dict, Any


def normalize_timestamp(timestamp: Any) -> str:
    """Normalize various timestamp formats to ISO 8601"""
    if not timestamp:
        return None
    
    if isinstance(timestamp, (int, float)):
        # Unix epoch
        return datetime.fromtimestamp(timestamp).isoformat()
    
    if isinstance(timestamp, str):
        # Try parsing various formats
        formats = [
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S%z',
            '%d/%b/%Y:%H:%M:%S %z',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(timestamp, fmt)
                return dt.isoformat()
            except:
                continue
        
        # Return as-is if can't parse
        return timestamp
    
    return None


def normalize_all_timestamps(parsed_logs: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize all timestamps in parsed logs"""
    for entry in parsed_logs.get('entries', []):
        if 'timestamp' in entry:
            entry['timestamp'] = normalize_timestamp(entry['timestamp'])
    
    return parsed_logs


def main():
    parser = argparse.ArgumentParser(description='Normalize timestamps in logs')
    parser.add_argument('--input', required=True, help='Input JSON file')
    parser.add_argument('--output', required=True, help='Output JSON file')
    
    args = parser.parse_args()
    
    # Load input
    with open(args.input, 'r') as f:
        parsed_logs = json.load(f)
    
    # Normalize timestamps
    normalized = normalize_all_timestamps(parsed_logs)
    
    # Save output
    with open(args.output, 'w') as f:
        json.dump(normalized, f, indent=2)
    
    print(f"Normalized {len(normalized.get('entries', []))} timestamps")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
