"""
Module: Variations
Description: Experiment with different prompt styles and approaches
Sandbox for testing and exploring prompt engineering variations
"""


def variation_testing_framework():
    """Framework for testing prompt variations"""
    framework = """
    PROMPT VARIATION TESTING FRAMEWORK
    
    Base Prompt: [Original prompt you want to improve]
    
    VARIATION 1: Length
    ├─ Version A: Shorter/more concise
    ├─ Version B: Longer/more detailed
    └─ Test: Which produces better results?
    
    VARIATION 2: Structure
    ├─ Version A: Prose/paragraph format
    ├─ Version B: Numbered steps
    ├─ Version C: Bullet points
    └─ Test: Does structure affect quality?
    
    VARIATION 3: Tone/Style
    ├─ Version A: Formal/professional
    ├─ Version B: Casual/conversational
    ├─ Version C: Technical/specialized
    └─ Test: How does tone influence results?
    
    VARIATION 4: Context/Examples
    ├─ Version A: No examples
    ├─ Version B: One example
    ├─ Version C: Multiple examples
    └─ Test: Do examples improve performance?
    
    VARIATION 5: Specificity
    ├─ Version A: General request
    ├─ Version B: More specific requirements
    ├─ Version C: Very detailed constraints
    └─ Test: Does specificity matter?
    
    EVALUATION METRICS:
    - Quality score (1-10)
    - Relevance (does it answer the question?)
    - Completeness (covers all aspects?)
    - Clarity (easy to understand?)
    - Usability (actionable?)
    
    PROCESS:
    1. Run each variation with same input
    2. Score outputs on metrics
    3. Compare scores
    4. Identify best variation
    5. Learn what worked
    """
    return framework


def prompt_style_experiments():
    """Different prompt styles to experiment with"""
    styles = """
    PROMPT STYLE EXPERIMENTS
    
    1. DIRECT INSTRUCTION
    "Summarize this text in 3 sentences."
    
    2. QUESTION FORMAT
    "How would you summarize this text in 3 sentences?"
    
    3. STORY FORMAT
    "Imagine you're teaching someone about this topic. 
     How would you summarize it in 3 sentences?"
    
    4. CONSTRAINT-BASED
    "Summarize this text using exactly 3 sentences,
     each with 10-15 words."
    
    5. ROLE-BASED
    "You are an expert summarizer. Summarize this text in 3 sentences."
    
    6. EXAMPLE-BASED
    "Summarize this text in 3 sentences. 
     Example format: [show example]"
    
    7. OBJECTIVE-BASED
    "To prepare someone for a quiz, summarize this text in 3 sentences."
    
    8. CONSEQUENCE-BASED
    "Summarize this text in 3 sentences - your answer will be used 
     to train a new model."
    
    TEST: Which style produces the best summaries?
    """
    return styles


def parameter_experiment_template():
    """Template for testing different parameters"""
    template = """
    PARAMETER EXPERIMENT TEMPLATE
    
    Parameter: [Name of parameter to test]
    Variable Name: [Variable name in prompt]
    Baseline Value: [Current/default value]
    
    Values to Test:
    - Value 1: [Low/short/simple variant]
    - Value 2: [Medium/baseline]
    - Value 3: [High/long/complex variant]
    - Value 4: [Extreme variant]
    
    Test Process:
    For each value:
    1. Set parameter to value
    2. Run prompt with test input
    3. Evaluate output on metrics
    4. Record results
    
    Evaluation Metrics:
    - Quality (1-10)
    - Speed (response time)
    - Relevance (1-10)
    - Completeness (1-10)
    
    Results Summary:
    ┌───────────┬────────┬───────┬──────────┬──────────┐
    │ Value     │ Quality│ Speed │ Relevance│Complete  │
    ├───────────┼────────┼───────┼──────────┼──────────┤
    │ Value 1   │        │       │          │          │
    │ Value 2   │        │       │          │          │
    │ Value 3   │        │       │          │          │
    │ Value 4   │        │       │          │          │
    └───────────┴────────┴───────┴──────────┴──────────┘
    
    Conclusion:
    Best value: [Based on metrics]
    Why: [Reasoning]
    """
    return template


def creative_prompt_variations():
    """Creative and unconventional prompt variations"""
    variations = """
    CREATIVE PROMPT VARIATIONS
    
    1. REVERSE ENGINEERING
    Instead of: "Write a poem about nature"
    Try: "I want a poem that makes readers appreciate nature. 
          What poem would achieve this?"
    
    2. HYPOTHETICAL SCENARIO
    Instead of: "Explain machine learning"
    Try: "If you had to explain machine learning to a 10-year-old 
         using only cooking metaphors, what would you say?"
    
    3. ADVERSARIAL APPROACH
    Instead of: "Generate ideas for a product"
    Try: "What are the worst possible ideas for a product in this category?
         Now, how could we make them actually work?"
    
    4. MULTIPLE PERSPECTIVES
    Instead of: "Analyze this decision"
    Try: "Analyze this decision from 3 perspectives:
         business, employee, customer. Which matters most?"
    
    5. CONSTRAINT CREATIVITY
    Instead of: "Write a story"
    Try: "Write a story using exactly 100 words, 
          containing the words: purple, forgotten, bicycle"
    
    6. COMPARATIVE ANALYSIS
    Instead of: "What's the best solution?"
    Try: "Compare these 3 solutions. Which is best for each scenario?"
    
    7. PREDICTION + REASONING
    Instead of: "What will happen?"
    Try: "Predict what will happen, then explain the reasoning 
          that led to your prediction"
    
    8. ABSTRACTION LEVELS
    Instead of: "Explain climate change"
    Try: "Explain climate change at 3 levels:
          - For a 5-year-old
          - For a high school student
          - For a climate scientist"
    """
    return variations


def debugging_poor_outputs():
    """Techniques for fixing prompts that produce poor results"""
    techniques = """
    DEBUGGING POOR PROMPT OUTPUTS
    
    SYMPTOM: Output is off-topic
    FIXES:
    - Add specific focus statement at start
    - Include what NOT to do
    - Provide example of good output
    - Narrow the scope
    
    SYMPTOM: Output is too vague
    FIXES:
    - Add "be specific" instruction
    - Request specific examples
    - Ask for exact numbers/details
    - Use structured output format
    
    SYMPTOM: Output is incomplete
    FIXES:
    - List exactly what's needed
    - Use checklist format
    - Ask for summary + details
    - Increase max_tokens
    
    SYMPTOM: Output is too long
    FIXES:
    - Add word/token limit
    - Request summary format
    - Ask for bullet points instead of prose
    - Increase specificity (less room for tangents)
    
    SYMPTOM: Output quality varies wildly
    FIXES:
    - Lower temperature (more consistent)
    - Add more specific constraints
    - Include examples
    - Simplify the task
    
    SYMPTOM: Output ignores instructions
    FIXES:
    - Put instructions first
    - Use ALL CAPS for critical instructions
    - Repeat key instructions multiple times
    - Use structured format with clear sections
    
    SYMPTOM: Output is inaccurate
    FIXES:
    - Ask for sources/citations
    - Request step-by-step reasoning
    - Add context/background
    - Be more specific about what's needed
    """
    return techniques


def learning_log_template():
    """Template for logging what you learn from experiments"""
    template = """
    LEARNING LOG ENTRY
    
    Date: [Date of experiment]
    Experiment: [What you tested]
    
    HYPOTHESIS:
    [What did you think would happen?]
    
    METHODS:
    Base prompt: [Original prompt]
    Variations tested: [What you changed]
    Test inputs: [What data/examples you used]
    
    RESULTS:
    [What actually happened - results table or description]
    
    FINDINGS:
    1. [Key finding]
    2. [Key finding]
    3. [Key finding]
    
    INSIGHTS:
    [What this teaches us about prompt engineering]
    
    NEXT STEPS:
    [What to test next based on findings]
    
    ACTIONABLE TIPS:
    - [Tip 1]
    - [Tip 2]
    - [Tip 3]
    """
    return template


if __name__ == "__main__":
    print("=== Variations ===\n")
    print("1. Testing Framework:")
    print(variation_testing_framework())
    print("\n2. Style Experiments:")
    print(prompt_style_experiments())
    print("\n3. Parameter Template:")
    print(parameter_experiment_template())
    print("\n4. Creative Variations:")
    print(creative_prompt_variations())
    print("\n5. Debugging Techniques:")
    print(debugging_poor_outputs())
    print("\n6. Learning Log:")
    print(learning_log_template())
