"""
Main Agent for Log Analyzer
Following Claude Skills handbook best practices

This agent:
1. Loads skills dynamically based on user query
2. Coordinates skill execution in proper order
3. Manages conversation state
4. Processes log files through the complete analysis pipeline
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import anthropic

# Import configuration
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import (
    CLAUDE_API_KEY, CLAUDE_MODEL, MAX_TOKENS, TEMPERATURE,
    SKILLS_DIR, get_enabled_skills, validate_log_file
)


class SkillLoader:
    """Loads and manages skills following Claude handbook structure"""
    
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.loaded_skills = {}
        
    def load_skill(self, skill_name: str) -> Dict[str, Any]:
        """Load a skill's SKILL.md file and parse frontmatter"""
        skill_path = self.skills_dir / skill_name / "SKILL.md"
        
        if not skill_path.exists():
            raise FileNotFoundError(f"SKILL.md not found for {skill_name}")
        
        with open(skill_path, 'r') as f:
            content = f.read()
        
        # Parse YAML frontmatter (between --- delimiters)
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                instructions = parts[2].strip()
            else:
                raise ValueError(f"Invalid SKILL.md format for {skill_name}")
        else:
            raise ValueError(f"SKILL.md missing frontmatter for {skill_name}")
        
        return {
            "name": frontmatter.get("name"),
            "description": frontmatter.get("description"),
            "compatibility": frontmatter.get("compatibility"),
            "license": frontmatter.get("license"),
            "metadata": frontmatter.get("metadata", {}),
            "instructions": instructions,
            "path": skill_path.parent
        }
    
    def load_all_enabled_skills(self) -> Dict[str, Dict[str, Any]]:
        """Load all enabled skills"""
        enabled_skills = get_enabled_skills()
        
        for skill_config in enabled_skills:
            skill_name = skill_config["name"]
            try:
                skill_data = self.load_skill(skill_name)
                self.loaded_skills[skill_name] = skill_data
                print(f"✓ Loaded skill: {skill_name}")
            except Exception as e:
                print(f"✗ Failed to load skill {skill_name}: {e}")
        
        return self.loaded_skills
    
    def get_skill_by_name(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Get a loaded skill by name"""
        return self.loaded_skills.get(skill_name)
    
    def get_skill_descriptions(self) -> List[Dict[str, str]]:
        """Get minimal skill info for Claude's context (Level 1 - frontmatter only)"""
        descriptions = []
        for skill_name, skill_data in self.loaded_skills.items():
            descriptions.append({
                "name": skill_data["name"],
                "description": skill_data["description"]
            })
        return descriptions


class ConversationState:
    """Manages conversation state and analysis results"""
    
    def __init__(self):
        self.messages = []
        self.active_skills = set()
        self.analysis_results = {}
        self.current_log_file = None
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        self.messages.append({
            "role": role,
            "content": content
        })
    
    def activate_skill(self, skill_name: str):
        """Mark a skill as active in current context"""
        self.active_skills.add(skill_name)
    
    def store_result(self, skill_name: str, result: Any):
        """Store analysis result from a skill"""
        self.analysis_results[skill_name] = result
    
    def get_result(self, skill_name: str) -> Optional[Any]:
        """Get stored result from a skill"""
        return self.analysis_results.get(skill_name)
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.messages
    
    def clear(self):
        """Clear conversation state"""
        self.messages = []
        self.active_skills = set()
        self.analysis_results = {}
        self.current_log_file = None


class LogAnalyzerAgent:
    """Main agent that coordinates skills and handles log analysis"""
    
    def __init__(self):
        # Initialize Claude API client (for future use with API mode)
        self.client = None
        if CLAUDE_API_KEY:
            self.client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        
        self.skill_loader = SkillLoader(SKILLS_DIR)
        self.state = ConversationState()
        self.model = CLAUDE_MODEL
        
        # Load all skills at initialization
        print("\n" + "="*60)
        print("Log Analyzer Agent - Initializing")
        print("="*60)
        print("\nLoading skills...")
        self.skills = self.skill_loader.load_all_enabled_skills()
        print(f"\n✓ Loaded {len(self.skills)} skills")
        print("="*60 + "\n")
        
    def determine_required_skills(self, user_message: str) -> List[str]:
        """
        Determine which skills are needed based on user message.
        Uses skill descriptions (Level 1) to make determination.
        """
        required_skills = []
        user_lower = user_message.lower()
        
        # Check for log file references
        has_log_file = any(word in user_lower for word in ['.log', 'log file', 'parse', 'analyze log'])
        
        # Skill triggering logic based on keywords
        
        # log-parsing: Always first if analyzing logs
        if has_log_file or 'parse' in user_lower or 'read log' in user_lower:
            required_skills.append('log-parsing')
        
        # error-detection: If looking for errors
        if any(word in user_lower for word in ['error', 'failure', 'exception', 'critical', 'find error', 'detect']):
            if 'log-parsing' not in required_skills:
                required_skills.append('log-parsing')  # Need parsing first
            required_skills.append('error-detection')
        
        # pattern-analysis: If looking for patterns or anomalies
        if any(word in user_lower for word in ['pattern', 'anomaly', 'trend', 'unusual', 'spike', 'correlat']):
            if 'log-parsing' not in required_skills:
                required_skills.append('log-parsing')
            required_skills.append('pattern-analysis')
        
        # report-generation: If requesting a report
        if any(word in user_lower for word in ['report', 'summary', 'export', 'generate report', 'show result']):
            # Need all previous skills for complete report
            if 'log-parsing' not in required_skills:
                required_skills.append('log-parsing')
            if 'error-detection' not in required_skills:
                required_skills.append('error-detection')
            if 'pattern-analysis' not in required_skills:
                required_skills.append('pattern-analysis')
            required_skills.append('report-generation')
        
        # Default: If log file mentioned but no specific task, do full analysis
        if has_log_file and not required_skills:
            required_skills = ['log-parsing', 'error-detection', 'pattern-analysis', 'report-generation']
        
        # If no skills determined, ask user for clarification
        if not required_skills:
            return []
        
        return required_skills
    
    def build_system_prompt(self, required_skills: List[str]) -> str:
        """
        Build system prompt with skill context.
        Uses progressive disclosure: Level 1 (all skills) + Level 2 (required skills only)
        """
        # Level 1: All skill descriptions (always loaded)
        skill_summaries = self.skill_loader.get_skill_descriptions()
        
        system_prompt = """You are a log analysis AI agent specialized in parsing, analyzing, and reporting on log files.

You can analyze various log formats including Apache, Nginx, syslog, JSON, Docker, and Kubernetes logs. You detect errors, identify patterns, spot anomalies, and generate comprehensive reports.

Available Skills (use these based on user needs):
"""
        
        for skill_info in skill_summaries:
            system_prompt += f"\n- **{skill_info['name']}**: {skill_info['description']}"
        
        # Level 2: Full instructions for required skills only
        if required_skills:
            system_prompt += "\n\n" + "="*60
            system_prompt += "\nACTIVE SKILLS FOR THIS REQUEST"
            system_prompt += "\n" + "="*60 + "\n"
            
            for skill_name in required_skills:
                skill_data = self.skills.get(skill_name)
                if skill_data:
                    system_prompt += f"\n\n## {skill_data['name'].upper()} SKILL\n\n"
                    system_prompt += skill_data['instructions']
                    self.state.activate_skill(skill_name)
        
        return system_prompt
    
    def execute_skill_workflow(self, user_message: str, log_file_path: Optional[str] = None) -> str:
        """
        Execute the complete skill workflow for log analysis.
        This is the local execution mode (not using Claude API).
        """
        from tools.log_parser import LogParser
        from tools.error_detector import ErrorDetector
        from tools.pattern_analyzer import PatternAnalyzer
        from tools.report_generator import ReportGenerator
        
        required_skills = self.determine_required_skills(user_message)
        
        if not required_skills:
            return "I can help you analyze log files. Please provide a log file path or ask me to parse, find errors, detect patterns, or generate a report."
        
        print(f"\n📋 Required skills: {', '.join(required_skills)}\n")
        
        results = {}
        
        # Execute skills in order
        for skill_name in required_skills:
            print(f"▶️  Executing: {skill_name}")
            
            try:
                if skill_name == 'log-parsing':
                    if not log_file_path:
                        return "Please provide a log file path to analyze."
                    
                    # Validate file
                    validation = validate_log_file(Path(log_file_path))
                    if not validation["valid"]:
                        return f"Error: {validation['error']}"
                    
                    # Parse logs
                    parser = LogParser()
                    parsed_logs = parser.parse_file(log_file_path)
                    results['log-parsing'] = parsed_logs
                    self.state.store_result('log-parsing', parsed_logs)
                    
                    print(f"  ✓ Parsed {parsed_logs['parsed_lines']:,} log entries")
                
                elif skill_name == 'error-detection':
                    parsed_logs = results.get('log-parsing')
                    if not parsed_logs:
                        print("  ⚠️  Skipping: No parsed logs available")
                        continue
                    
                    detector = ErrorDetector()
                    errors = detector.detect_errors(parsed_logs)
                    results['error-detection'] = errors
                    self.state.store_result('error-detection', errors)
                    
                    print(f"  ✓ Found {errors['total_errors']} errors ({errors['unique_error_types']} unique types)")
                
                elif skill_name == 'pattern-analysis':
                    parsed_logs = results.get('log-parsing')
                    if not parsed_logs:
                        print("  ⚠️  Skipping: No parsed logs available")
                        continue
                    
                    analyzer = PatternAnalyzer()
                    patterns = analyzer.analyze_patterns(parsed_logs)
                    results['pattern-analysis'] = patterns
                    self.state.store_result('pattern-analysis', patterns)
                    
                    print(f"  ✓ Identified {patterns['pattern_count']} patterns, {patterns['anomaly_count']} anomalies")
                
                elif skill_name == 'report-generation':
                    generator = ReportGenerator()
                    report = generator.generate_report(results)
                    results['report-generation'] = report
                    
                    # Save report
                    output_path = generator.save_report(report, format="markdown")
                    print(f"  ✓ Report saved to: {output_path}")
                    
                    return f"Analysis complete! Report saved to: {output_path}\n\n{report['executive_summary']}"
            
            except Exception as e:
                print(f"  ✗ Error: {e}")
                return f"Error during {skill_name}: {str(e)}"
        
        # If no report generation, provide summary
        if 'report-generation' not in required_skills:
            summary = self.generate_summary(results)
            return summary
        
        return "Analysis complete!"
    
    def generate_summary(self, results: Dict[str, Any]) -> str:
        """Generate a quick summary from results"""
        summary = "\n" + "="*60 + "\n"
        summary += "ANALYSIS SUMMARY\n"
        summary += "="*60 + "\n\n"
        
        if 'log-parsing' in results:
            parsed = results['log-parsing']
            summary += f"📄 Log Parsing:\n"
            summary += f"  - Total entries: {parsed['parsed_lines']:,}\n"
            summary += f"  - Format: {parsed['format']}\n"
            summary += f"  - Time range: {parsed['metadata']['start_time']} to {parsed['metadata']['end_time']}\n\n"
        
        if 'error-detection' in results:
            errors = results['error-detection']
            summary += f"❌ Error Detection:\n"
            summary += f"  - Total errors: {errors['total_errors']}\n"
            summary += f"  - Unique types: {errors['unique_error_types']}\n"
            summary += f"  - Error rate: {errors['error_percentage']}%\n"
            summary += f"  - Critical errors: {errors['critical_errors']}\n\n"
        
        if 'pattern-analysis' in results:
            patterns = results['pattern-analysis']
            summary += f"📊 Pattern Analysis:\n"
            summary += f"  - Patterns found: {patterns['pattern_count']}\n"
            summary += f"  - Anomalies detected: {patterns['anomaly_count']}\n\n"
        
        summary += "="*60 + "\n"
        
        return summary
    
    def start_interactive_session(self):
        """Start an interactive chat session"""
        print("\n" + "="*60)
        print("Log Analyzer Agent - Interactive Session")
        print("="*60)
        print("Skills loaded:", ", ".join(self.skills.keys()))
        print("\nCommands:")
        print("  - analyze <log_file_path>  : Analyze a log file")
        print("  - quit                     : Exit")
        print("  - clear                    : Reset conversation")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'quit':
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'clear':
                    self.state.clear()
                    print("Conversation cleared.")
                    continue
                
                # Parse command
                if user_input.startswith('analyze '):
                    log_file = user_input[8:].strip()
                    response = self.execute_skill_workflow(
                        f"analyze this log file: {log_file}",
                        log_file_path=log_file
                    )
                else:
                    response = self.execute_skill_workflow(user_input)
                
                print(f"\n{response}\n")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Log Analyzer Agent")
    parser.add_argument('--file', '-f', help='Log file to analyze')
    parser.add_argument('--interactive', '-i', action='store_true', help='Start interactive session')
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = LogAnalyzerAgent()
    
    if args.interactive or not args.file:
        # Start interactive session
        agent.start_interactive_session()
    elif args.file:
        # Analyze specific file
        result = agent.execute_skill_workflow(
            f"analyze this log file and generate a report: {args.file}",
            log_file_path=args.file
        )
        print(result)


if __name__ == "__main__":
    main()
