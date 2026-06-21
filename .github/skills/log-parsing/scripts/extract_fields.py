#!/usr/bin/env python3
"""
Extract Fields Script
Extracts specific fields from parsed log data
"""

import json
import argparse
from typing import Dict, List, Any


def extract_fields(
    parsed_logs: Dict[str, Any],
    fields: List[str]
) -> List[Dict[str, Any]]:
    """Extract specific fields from log entries"""
    entries = parsed_logs.get('entries', [])
    extracted = []
    
    for entry in entries:
        extracted_entry = {}
        for field in fields:
            if field in entry:
                extracted_entry[field] = entry[field]
            else:
                extracted_entry[field] = None
        extracted.append(extracted_entry)
    
    return extracted


def main():
    parser = argparse.ArgumentParser(description='Extract fields from parsed logs')
    parser.add_argument('--input', required=True, help='Input JSON file')
    parser.add_argument('--fields', required=True, help='Comma-separated fields to extract')
    parser.add_argument('--output', required=True, help='Output JSON file')
    
    args = parser.parse_args()
    
    # Load input
    with open(args.input, 'r') as f:
        parsed_logs = json.load(f)
    
    # Extract fields
    fields = [f.strip() for f in args.fields.split(',')]
    extracted = extract_fields(parsed_logs, fields)
    
    # Save output
    with open(args.output, 'w') as f:
        json.dump(extracted, f, indent=2)
    
    print(f"Extracted {len(extracted)} entries with fields: {', '.join(fields)}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
