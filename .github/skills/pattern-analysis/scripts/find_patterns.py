#!/usr/bin/env python3
"""
Find Patterns Script
Identifies recurring patterns in log data
"""

import json
import argparse
from collections import defaultdict, Counter
from datetime import datetime


def find_temporal_patterns(entries, min_frequency=3):
    """Find patterns that occur at regular intervals"""
    patterns = []
    
    # Group errors by message
    error_groups = defaultdict(list)
    for entry in entries:
        if entry.get('level') in ['ERROR', 'CRITICAL']:
            message = entry.get('message', '')[:100]
            if entry.get('timestamp'):
                error_groups[message].append(entry['timestamp'])
    
    # Check for regular intervals
    for message, timestamps in error_groups.items():
        if len(timestamps) >= min_frequency:
            # Calculate intervals
            try:
                dts = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in sorted(timestamps)]
                intervals = []
                for i in range(len(dts) - 1):
                    interval_minutes = (dts[i+1] - dts[i]).total_seconds() / 60
                    intervals.append(interval_minutes)
                
                # Check if regular
                if intervals and is_regular(intervals):
                    avg_interval = sum(intervals) / len(intervals)
                    patterns.append({
                        'type': 'temporal',
                        'description': f"Error occurs every {format_interval(avg_interval)}",
                        'frequency': len(timestamps),
                        'message_preview': message[:80],
                        'interval_minutes': avg_interval
                    })
            except:
                continue
    
    return patterns


def find_request_patterns(entries, min_frequency=3):
    """Find repeated request patterns"""
    patterns = []
    
    # Count requests by path
    path_counter = Counter()
    for entry in entries:
        path = entry.get('path')
        if path:
            path_counter[path] += 1
    
    # Find high-frequency paths
    for path, count in path_counter.most_common(20):
        if count >= min_frequency:
            patterns.append({
                'type': 'request',
                'description': f"Frequent requests to {path}",
                'frequency': count,
                'path': path
            })
    
    return patterns


def is_regular(intervals, tolerance=0.2):
    """Check if intervals are regular within tolerance"""
    if len(intervals) < 2:
        return False
    
    mean_interval = sum(intervals) / len(intervals)
    if mean_interval == 0:
        return False
    
    # Check if all intervals are within tolerance
    for interval in intervals:
        deviation = abs(interval - mean_interval) / mean_interval
        if deviation > tolerance:
            return False
    
    return True


def format_interval(minutes):
    """Format interval in human-readable form"""
    if minutes < 1:
        return f"{minutes*60:.0f} seconds"
    elif minutes < 60:
        return f"{minutes:.0f} minutes"
    else:
        return f"{minutes/60:.1f} hours"


def main():
    parser = argparse.ArgumentParser(description='Find patterns in logs')
    parser.add_argument('--input', required=True, help='Input JSON file (parsed logs)')
    parser.add_argument('--min-freq', type=int, default=3, help='Minimum frequency')
    parser.add_argument('--output', required=True, help='Output JSON file')
    
    args = parser.parse_args()
    
    # Load input
    with open(args.input, 'r') as f:
        parsed_logs = json.load(f)
    
    entries = parsed_logs.get('entries', [])
    
    # Find patterns
    print("Finding patterns...")
    temporal_patterns = find_temporal_patterns(entries, args.min_freq)
    request_patterns = find_request_patterns(entries, args.min_freq)
    
    all_patterns = temporal_patterns + request_patterns
    
    # Print summary
    print(f"\nFound {len(all_patterns)} patterns:")
    print("=" * 60)
    for i, pattern in enumerate(all_patterns, 1):
        print(f"{i}. [{pattern['type']}] {pattern['description']}")
        print(f"   Frequency: {pattern['frequency']}")
    
    # Save output
    output = {
        'pattern_count': len(all_patterns),
        'patterns': all_patterns
    }
    
    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved to: {args.output}")


if __name__ == "__main__":
    main()
