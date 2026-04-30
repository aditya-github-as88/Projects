"""
Module: Prompt Optimization
Description: Techniques for systematically improving prompt performance
Experimental approaches to find optimal prompts
"""

def iteration_experiment_template():
    """Template for testing prompt iterations"""
    template = """
    PROMPT OPTIMIZATION EXPERIMENT
    
    Original Prompt:
    "Tell me about machine learning"
    
    Iteration 1 (More Specific):
    "Explain machine learning in 3-4 sentences for someone with basic tech knowledge"
    
    Iteration 2 (Added Structure):
    "Explain machine learning including:
     - What it is
     - How it differs from traditional programming
     - A practical example"
    
    Iteration 3 (Optimized with Role):
    "You are a tech educator. Explain machine learning in a way that's clear for beginners.
     Include a practical example they can relate to."
    
    Metrics to Compare:
    - Clarity (1-10)
    - Completeness (1-10)
    - Relevance (1-10)
    - Usefulness (1-10)
    """
    return template


def parameter_optimization():
    """Optimize different prompt parameters"""
    parameters = """
    KEY PARAMETERS TO OPTIMIZE:
    
    1. LENGTH
       Short: "Summarize this"
       Long: "Provide a detailed, comprehensive summary covering all major points"
       → Test: Does more detail increase quality?
    
    2. SPECIFICITY
       Vague: "Write a story"
       Specific: "Write a 200-word science fiction story about first contact"
       → Test: Does specificity improve output quality?
    
    3. TONE
       Neutral: "Explain quantum mechanics"
       Friendly: "Help me understand quantum mechanics in a fun way"
       Formal: "Provide a rigorous explanation of quantum mechanics"
       → Test: Which tone works best for your use case?
    
    4. EXAMPLES
       No examples: "Classify these reviews"
       With examples: "Classify reviews as positive/negative. Example: 'Great!' = positive"
       → Test: Do examples improve classification accuracy?
    
    5. CONSTRAINTS
       Open: "Generate ideas"
       Constrained: "Generate 5 creative ideas for a new app"
       → Test: Do constraints improve focus and relevance?
    """
    return parameters


def a_b_testing_framework():
    """Framework for A/B testing prompts"""
    framework = """
    A/B TESTING FRAMEWORK FOR PROMPTS
    
    Setup:
    - Prompt A: Current/baseline prompt
    - Prompt B: Modified version
    - Test Input: Sample data or questions
    - Metrics: Define what you're measuring
    
    Procedure:
    1. Run both prompts on the same input
    2. Evaluate outputs using defined metrics
    3. Record results
    4. Repeat with multiple test cases
    5. Analyze: Which prompt performed better overall?
    
    Metrics Examples:
    - Accuracy (% correct answers)
    - Relevance (1-10 scale)
    - Completeness (all required elements included)
    - Clarity (easy to understand)
    - Efficiency (conciseness)
    
    Example Test:
    Input: "Explain photosynthesis"
    
    Prompt A: "Explain photosynthesis"
    Prompt B: "Explain photosynthesis in simple terms for a 10-year-old"
    
    Evaluate both outputs on clarity and completeness
    """
    return framework


def temperature_and_parameters():
    """Understanding temperature and other parameters"""
    guide = """
    MODEL PARAMETERS AND THEIR EFFECTS:
    
    TEMPERATURE (Creativity vs. Consistency)
    - 0.0: Deterministic (same input = same output)
    - 0.5: Balanced (some variation, mostly consistent)
    - 1.0: Creative (more variation, less predictable)
    - 2.0: Very Creative (highly unpredictable)
    
    When to use:
    - Low temperature (0.0-0.3): Factual tasks, analysis, coding
    - Medium temperature (0.5-0.7): Normal content generation
    - High temperature (0.8-1.0): Creative writing, brainstorming
    
    MAX_TOKENS:
    - Limits response length
    - Longer = more detailed but slower
    - Shorter = quicker but may cut off content
    
    TOP_K and TOP_P:
    - Control diversity of responses
    - Lower values = more focused
    - Higher values = more diverse
    """
    return guide


def optimization_checklist():
    """Checklist for optimizing a prompt"""
    checklist = """
    PROMPT OPTIMIZATION CHECKLIST:
    
    ☐ Is the task clear and specific?
    ☐ Have you provided sufficient context?
    ☐ Are examples included if needed?
    ☐ Is the desired output format specified?
    ☐ Have you considered the audience?
    ☐ Are there any ambiguous terms that need clarification?
    ☐ Have you included any necessary constraints?
    ☐ Could the prompt be shorter while maintaining clarity?
    ☐ Have you tested it with multiple inputs?
    ☐ Have you compared it with alternative versions?
    ☐ Is the tone appropriate for the use case?
    ☐ Have you considered edge cases?
    ☐ Is the prompt focused on one task or multiple tasks?
    ☐ Could adding structure (steps, bullets) improve clarity?
    ☐ Have you included role/persona if relevant?
    """
    return checklist


if __name__ == "__main__":
    print("=== Prompt Optimization ===\n")
    print("1. Iteration Template:")
    print(iteration_experiment_template())
    print("\n2. Parameter Optimization:")
    print(parameter_optimization())
    print("\n3. A/B Testing Framework:")
    print(a_b_testing_framework())
    print("\n4. Temperature & Parameters:")
    print(temperature_and_parameters())
    print("\n5. Optimization Checklist:")
    print(optimization_checklist())
