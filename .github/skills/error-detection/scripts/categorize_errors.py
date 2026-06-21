#!/usr/bin/env python3
"""
Categorize Errors Script
Categorizes errors from parsed logs
"""

import json
import argparse
from collections import defaultdict


ERROR_CATEGORIES = {
    'database': [
        'connection', 'query', 'sql', 'database', 'db', 'timeout',
        'deadlock', 'constraint', 'transaction'
    ],
    'network': [
        'connection refused', 'timeout', 'network', 'socket', 'dns',
        'unreachable', 'host', 'port'
    ],
    'authentication': [
        'auth', 'authentication', 'unauthorized', 'forbidden',
        'permission denied', 'access denied'
    ],
    'application': [
        'nullpointer', 'null', 'exception', 'runtime', 'assertion'
    ],
    'configuration': [
        'config', 'configuration', 'missing', 'not found'
    ],
    'resource': [
        'memory', 'disk', 'cpu', 'out of', 'full', 'exhausted'
    ]
}


def categorize_error(entry: dict) -> str:
    """Categorize a single error entry"""
    message = entry.get('message', '').lower()
    raw_line = entry.get('raw_line', '').lower()
    text = message + ' ' + raw_line
    
    # Find matching category
    category = 'unknown'
    max_matches = 0
    
    for cat_name, keywords in ERROR_CATEGORIES.items():
        matches = sum(1 for keyword in keywords if keyword in text)
        if matches > max_matches:
            max_matches = matches
            category = cat_name
    
    return category


def categorize_errors(parsed_logs: dict) -> dict:
    """Categorize all error entries"""
    entries = parsed_logs.get('entries', [])
    
    # Filter errors
    error_entries = [
        e for e in entries
        if e.get('level', '').upper() in ['ERROR', 'CRITICAL', 'FATAL']
    ]
    
    # Categorize
    categorized = defaultdict(list)
    for entry in error_entries:
        category = categorize_error(entry)
        categorized[category].append(entry)
    
    return dict(categorized)


def main():
    parser = argparse.ArgumentParser(description='Categorize errors in logs')
    parser.add_argument('--input', required=True, help='Input JSON file')
    parser.add_argument('--output', required=True, help='Output JSON file')
    
    args = parser.parse_args()
    
    # Load input
    with open(args.input, 'r') as f:
        parsed_logs = json.load(f)
    
    # Categorize errors
    categorized = categorize_errors(parsed_logs)
    
    # Print summary
    print("\nError Categorization Summary:")
    print("=" * 40)
    for category, entries in sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"{category:15s}: {len(entries):6d} errors")
    
    # Save output
    with open(args.output, 'w') as f:
        json.dump(categorized, f, indent=2)
    
    print(f"\nSaved to: {args.output}")


if __name__ == "__main__":
    main()
