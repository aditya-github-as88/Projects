"""
Configuration settings for Log Analyzer Agent
Following Claude Skills handbook best practices
"""

import os
from pathlib import Path
from typing import List, Dict, Any

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
SKILLS_DIR = PROJECT_ROOT / ".github" / "skills"
TOOLS_DIR = PROJECT_ROOT / "tools"
HOOKS_DIR = PROJECT_ROOT / "hooks"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
OUTPUTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Claude API Configuration
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # Always use Sonnet 4 for API
MAX_TOKENS = 8000
TEMPERATURE = 0.0  # Deterministic for analysis tasks

# Skills Configuration - Priority order for loading
AVAILABLE_SKILLS = [
    {
        "name": "log-parsing",
        "path": SKILLS_DIR / "log-parsing",
        "priority": 1,  # First - must parse before anything else
        "enabled": True
    },
    {
        "name": "error-detection",
        "path": SKILLS_DIR / "error-detection",
        "priority": 2,  # Detect errors from parsed logs
        "enabled": True
    },
    {
        "name": "pattern-analysis",
        "path": SKILLS_DIR / "pattern-analysis",
        "priority": 3,  # Analyze patterns in errors and logs
        "enabled": True
    },
    {
        "name": "report-generation",
        "path": SKILLS_DIR / "report-generation",
        "priority": 4,  # Final - generate reports from analysis
        "enabled": True
    }
]

# Log File Processing Configuration
SUPPORTED_LOG_FORMATS = [
    "apache",
    "nginx",
    "syslog",
    "json",
    "custom",
    "application",
    "docker",
    "kubernetes"
]

# Log parsing limits
MAX_LOG_FILE_SIZE_MB = 500  # Maximum file size to process
MAX_LINES_TO_ANALYZE = 100000  # Maximum lines per file
CHUNK_SIZE = 10000  # Process logs in chunks

# Error Detection Configuration
ERROR_SEVERITY_LEVELS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
ERROR_KEYWORDS = [
    "error", "exception", "failed", "failure", "fatal", "critical",
    "panic", "crash", "timeout", "refused", "denied", "invalid"
]

# Pattern Analysis Configuration
MIN_PATTERN_FREQUENCY = 3  # Minimum occurrences to be considered a pattern
ANOMALY_THRESHOLD = 0.05  # 5% deviation considered anomalous
TIME_WINDOW_MINUTES = 60  # Time window for pattern analysis

# Report Configuration
REPORT_FORMATS = ["markdown", "html", "json", "text"]
DEFAULT_REPORT_FORMAT = "markdown"
INCLUDE_CHARTS = True
MAX_ERROR_EXAMPLES = 10  # Max examples per error type in report

# Workflow Configuration
WORKFLOW_TIMEOUT = 600  # 10 minutes max per workflow
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = LOGS_DIR / "agent.log"
LOG_ROTATION_SIZE_MB = 10
LOG_RETENTION_DAYS = 30

def get_skill_config(skill_name: str) -> Dict[str, Any]:
    """Get configuration for a specific skill"""
    for skill in AVAILABLE_SKILLS:
        if skill["name"] == skill_name:
            return skill
    return None

def get_enabled_skills() -> List[Dict[str, Any]]:
    """Get list of enabled skills sorted by priority"""
    return sorted(
        [s for s in AVAILABLE_SKILLS if s["enabled"]],
        key=lambda x: x["priority"]
    )

def get_supported_formats() -> List[str]:
    """Get list of supported log formats"""
    return SUPPORTED_LOG_FORMATS

def validate_log_file(file_path: Path) -> Dict[str, Any]:
    """Validate if log file can be processed"""
    if not file_path.exists():
        return {"valid": False, "error": "File does not exist"}
    
    if not file_path.is_file():
        return {"valid": False, "error": "Path is not a file"}
    
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    if file_size_mb > MAX_LOG_FILE_SIZE_MB:
        return {
            "valid": False,
            "error": f"File size ({file_size_mb:.2f}MB) exceeds maximum ({MAX_LOG_FILE_SIZE_MB}MB)"
        }
    
    return {"valid": True, "size_mb": file_size_mb}
