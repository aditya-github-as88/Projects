"""
Module: Results Logger
Description: Track and log prompt experiment results for analysis
Compare outputs and measure effectiveness
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


class PromptExperimentLogger:
    """Logger for tracking prompt engineering experiments"""
    
    def __init__(self, experiment_name: str):
        """Initialize logger for an experiment"""
        self.experiment_name = experiment_name
        self.created_at = datetime.now().isoformat()
        self.trials = []
    
    def log_trial(self, prompt_version: str, input_text: str, 
                 output_text: str, metrics: Dict[str, float]):
        """Log a single trial"""
        trial = {
            "timestamp": datetime.now().isoformat(),
            "prompt_version": prompt_version,
            "input": input_text,
            "output": output_text,
            "metrics": metrics
        }
        self.trials.append(trial)
    
    def calculate_average_metrics(self) -> Dict[str, float]:
        """Calculate average metrics across all trials"""
        if not self.trials:
            return {}
        
        all_metrics = [trial["metrics"] for trial in self.trials]
        metric_names = all_metrics[0].keys()
        
        averages = {}
        for metric in metric_names:
            values = [m[metric] for m in all_metrics]
            averages[metric] = sum(values) / len(values)
        
        return averages
    
    def compare_versions(self) -> Dict:
        """Compare results across different prompt versions"""
        if not self.trials:
            return {}
        
        # Group by prompt version
        versions = {}
        for trial in self.trials:
            version = trial["prompt_version"]
            if version not in versions:
                versions[version] = []
            versions[version].append(trial["metrics"])
        
        # Calculate averages per version
        comparison = {}
        for version, metrics_list in versions.items():
            metric_names = metrics_list[0].keys()
            averages = {}
            for metric in metric_names:
                values = [m[metric] for m in metrics_list]
                averages[metric] = sum(values) / len(values)
            comparison[version] = averages
        
        return comparison
    
    def get_best_version(self, metric_name: str = "overall_quality") -> str:
        """Get the best performing prompt version for a metric"""
        comparison = self.compare_versions()
        if not comparison:
            return None
        
        best = max(comparison.items(), 
                  key=lambda x: x[1].get(metric_name, 0))
        return best[0]
    
    def export_results(self, filename: str = None) -> str:
        """Export results to JSON format"""
        if filename is None:
            filename = f"experiment_{self.experiment_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            "experiment_name": self.experiment_name,
            "created_at": self.created_at,
            "trials": self.trials,
            "comparison": self.compare_versions(),
            "average_metrics": self.calculate_average_metrics()
        }
        
        return json.dumps(data, indent=2)


def experiment_template():
    """Template for running a prompt experiment"""
    template = """
    EXPERIMENT TEMPLATE: [Experiment Name]
    
    OBJECTIVE:
    [What are you trying to understand about prompts?]
    
    HYPOTHESIS:
    [What do you think will work better?]
    
    VARIABLES:
    - Independent variable: [What you're changing]
    - Dependent variables: [What you're measuring]
    - Control: [What stays the same]
    
    DESIGN:
    Version A: [First prompt variation]
    Version B: [Second prompt variation]
    Version C: [Third prompt variation (optional)]
    
    TEST DATA:
    Input 1: [Test input]
    Input 2: [Test input]
    Input 3: [Test input]
    
    METRICS:
    - Quality (1-10): How good is the output?
    - Relevance (1-10): Does it answer the question?
    - Clarity (1-10): Is it easy to understand?
    - Completeness (1-10): Does it cover everything needed?
    - Efficiency (1-10): Is it concise?
    
    PROCEDURE:
    1. Run Version A with all test inputs
    2. Score each output on all metrics
    3. Record results
    4. Repeat for Version B and C
    5. Compare average scores
    6. Analyze findings
    
    RESULTS TABLE:
    ┌──────────┬─────────┬──────────┬─────────┬──────────┬──────────┐
    │ Version  │ Quality │ Relevance│ Clarity │ Complete │ Efficient│
    ├──────────┼─────────┼──────────┼─────────┼──────────┼──────────┤
    │ Version A│         │          │         │          │          │
    │ Version B│         │          │         │          │          │
    │ Version C│         │          │         │          │          │
    └──────────┴─────────┴──────────┴─────────┴──────────┴──────────┘
    
    CONCLUSION:
    [Which version was best? Why?]
    
    INSIGHTS:
    [What did this teach us about prompts?]
    """
    return template


def metrics_guide():
    """Guide to selecting and defining metrics"""
    guide = """
    METRICS SELECTION GUIDE
    
    QUALITY METRICS:
    - Accuracy: Correctness of facts (0-100%)
    - Relevance: Appropriateness to the question (1-10)
    - Clarity: Ease of understanding (1-10)
    - Completeness: Covers all required elements (1-10)
    
    EFFICIENCY METRICS:
    - Response length: Word/token count
    - Conciseness: Information per word
    - Speed: Time to generate (ms)
    - Cost: Tokens used × price
    
    ENGAGEMENT METRICS:
    - Creativity score (1-10)
    - Originality (1-10)
    - Interest level (1-10)
    
    CONSISTENCY METRICS:
    - Variance across inputs (low = better)
    - Reproducibility (can we get same result?)
    - Stability (small changes shouldn't drastically affect output)
    
    PRACTICAL METRICS:
    - Actionability: Can the output be acted upon? (yes/no)
    - Usefulness: Would users find it useful? (1-10)
    - Feasibility: Is it realistic? (1-10)
    
    HOW TO DEFINE:
    1. Metric name: [Clear, specific name]
    2. Definition: [What exactly are you measuring?]
    3. Scale: [1-10, percentage, count, etc.]
    4. Rubric: [What does each score mean?]
    5. Scoring method: [How do you evaluate?]
    
    EXAMPLE RUBRIC:
    Clarity (1-10):
    1-2: Confusing, difficult to follow
    3-4: Somewhat unclear, needs improvement
    5-6: Adequately clear, mostly understandable
    7-8: Clear and well-organized
    9-10: Exceptionally clear and well-articulated
    """
    return guide


def analysis_techniques():
    """Techniques for analyzing experiment results"""
    techniques = """
    ANALYSIS TECHNIQUES FOR EXPERIMENTS
    
    1. SUMMARY STATISTICS
    - Calculate mean, median, standard deviation
    - Identify min/max values
    - Look for outliers
    
    2. VISUAL COMPARISON
    - Create bar charts of metrics by version
    - Plot trends across test inputs
    - Show distribution of scores
    
    3. STATISTICAL TESTING
    - Compare averages between versions
    - Calculate if differences are significant
    - Use appropriate test (t-test, etc.)
    
    4. CORRELATION ANALYSIS
    - Do certain metrics correlate?
    - Which metrics most important?
    - Discover relationships
    
    5. QUALITATIVE ANALYSIS
    - Read outputs from each version
    - Note patterns and themes
    - Identify quality differences not captured by metrics
    
    6. COST-BENEFIT ANALYSIS
    - Quality improvement vs. token usage
    - Speed vs. accuracy tradeoffs
    - Cost per unit of improvement
    
    COMMON FINDINGS:
    - Version A best for quality
    - Version B best for speed
    - Tradeoff between competing metrics
    - One version clearly superior
    - Versions comparable, other factors matter
    
    INTERPRETATION:
    Don't just look at numbers—understand WHY
    Read the actual outputs
    Consider practical implications
    Think about next experiments to run
    """
    return techniques


if __name__ == "__main__":
    print("=== Results Logger ===\n")
    print("1. Experiment Template:")
    print(experiment_template())
    print("\n2. Metrics Guide:")
    print(metrics_guide())
    print("\n3. Analysis Techniques:")
    print(analysis_techniques())
    print("\nExample Usage:")
    print("logger = PromptExperimentLogger('test_experiment')")
    print("logger.log_trial('v1', 'input', 'output', {'quality': 8.5})")
    print("print(logger.compare_versions())")
