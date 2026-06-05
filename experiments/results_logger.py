"""
Results Logger

Utilities for logging and tracking experiment results.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


def save_experiment_result(result: Dict[str, Any], output_path: str = "experiment_results.json") -> None:
    """
    Save experiment results to a JSON file.
    """
    path = Path(output_path)
    data = []
    if path.exists():
        with open(path, "r", encoding="utf-8") as handle:
            try:
                data = json.load(handle)
            except json.JSONDecodeError:
                data = []

    result["timestamp"] = datetime.utcnow().isoformat() + "Z"
    data.append(result)

    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    print(f"Saved experiment result to {path}")


def log_sample_experiment() -> None:
    """
    Example experiment log entry.
    """
    result = {
        "experiment_id": "exp_001",
        "variation": "Prompt A",
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "metrics": {
            "accuracy": 0.93,
            "response_time_ms": 450,
            "token_usage": 84
        },
        "notes": "Prompt A performed better on precision than Prompt B."
    }
    save_experiment_result(result)


def load_experiment_results(output_path: str = "experiment_results.json") -> Any:
    """
    Load stored experiment results from disk.
    """
    path = Path(output_path)
    if not path.exists():
        print(f"No experiment results found at {path}")
        return []

    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def print_experiment_summary(output_path: str = "experiment_results.json") -> None:
    """
    Print a summary of saved experiment results.
    """
    results = load_experiment_results(output_path)
    if not results:
        return

    print("\n=== Experiment Summary ===")
    for item in results:
        print(f"- {item['experiment_id']}: {item['variation']} (model={item['model']}, accuracy={item['metrics']['accuracy']})")


if __name__ == "__main__":
    log_sample_experiment()
    print_experiment_summary()