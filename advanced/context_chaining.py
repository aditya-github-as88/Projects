"""
Module: Context Chaining
Description: Linking multiple prompts where output of one becomes input to the next
Building complex reasoning by chaining simpler prompts
"""

def simple_chain_example():
    """Basic example of chaining prompts"""
    chain = """
    PROMPT 1 (Research):
    Research the top 3 programming languages in 2024 and explain why.
    OUTPUT: [Language list with reasons]
    
    PROMPT 2 (Analysis - uses output of Prompt 1):
    Given that {OUTPUT_1} are the top languages, 
    which would be best for a beginner to learn first?
    OUTPUT: [Recommendation]
    
    PROMPT 3 (Implementation - uses output of Prompt 2):
    Create a 4-week learning path for mastering {OUTPUT_2}
    OUTPUT: [Learning plan]
    """
    return chain


def research_to_summary_chain():
    """Chain from research to actionable summary"""
    chain = """
    Step 1 - Research:
    "List the key trends in remote work in 2024"
    
    Step 2 - Analysis:
    "Given these trends: {Step1_Output}, what are the implications for companies?"
    
    Step 3 - Recommendations:
    "Based on the implications {Step2_Output}, provide 3 actionable recommendations"
    
    Step 4 - Summary:
    "Summarize all findings in an executive summary for leadership"
    """
    return chain


def information_extraction_chain():
    """Chain for extracting and synthesizing information"""
    chain = """
    PHASE 1 - Information Extraction:
    Prompt: "Extract the key facts from this article about climate change"
    
    PHASE 2 - Categorization:
    Input: [Facts from Phase 1]
    Prompt: "Organize these facts into categories: causes, effects, solutions"
    
    PHASE 3 - Synthesis:
    Input: [Categorized facts from Phase 2]
    Prompt: "Create a comprehensive overview combining all categories"
    """
    return chain


def multi_perspective_chain():
    """Analyze something from multiple perspectives in sequence"""
    chain = """
    PROMPT 1 - Business Perspective:
    "Analyze this business decision from a financial viewpoint"
    OUTPUT: Financial analysis
    
    PROMPT 2 - Human Perspective:
    "Given the financial analysis, how does this impact employees?"
    OUTPUT: Impact assessment
    
    PROMPT 3 - Ethical Perspective:
    "Considering both analyses, what are the ethical implications?"
    OUTPUT: Ethical evaluation
    
    PROMPT 4 - Comprehensive Conclusion:
    "Synthesize all three perspectives to provide a final recommendation"
    """
    return chain


def problem_solving_chain():
    """Chain for comprehensive problem solving"""
    chain = """
    STAGE 1 - Problem Definition:
    "What is the core problem here?"
    
    STAGE 2 - Root Cause Analysis:
    "Why does this problem exist? What are the root causes?"
    
    STAGE 3 - Solution Generation:
    "Given these root causes, what are possible solutions?"
    
    STAGE 4 - Solution Evaluation:
    "Evaluate each solution for feasibility, cost, and impact"
    
    STAGE 5 - Implementation Plan:
    "Create a step-by-step implementation plan for the best solution"
    
    STAGE 6 - Risk Mitigation:
    "What could go wrong? How do we mitigate these risks?"
    """
    return chain


def best_practices_chaining():
    """Best practices for context chaining"""
    practices = """
    BEST PRACTICES FOR CONTEXT CHAINING:
    
    1. Clear Hand-off
       - Explicitly reference previous output
       - Use placeholder like {PREVIOUS_OUTPUT}
       - Be specific about what part to use
    
    2. Preserve Context
       - Include summary of previous step
       - Remind the model of the chain's purpose
    
    3. Logical Progression
       - Each step should build naturally on the previous
       - Avoid jumping between unrelated tasks
    
    4. Quality Control
       - Check outputs at each stage
       - Don't pass flawed outputs down the chain
    
    5. Complexity Management
       - Keep individual prompts focused
       - Don't try to do too much in one step
    
    6. Variable Naming
       - Use clear naming: {ANALYSIS_RESULTS} instead of {OUTPUT}
       - Document what each variable represents
    """
    return practices


if __name__ == "__main__":
    print("=== Context Chaining Examples ===\n")
    print("1. Simple Chain:")
    print(simple_chain_example())
    print("\n2. Research to Summary Chain:")
    print(research_to_summary_chain())
    print("\n3. Information Extraction Chain:")
    print(information_extraction_chain())
    print("\n4. Multi-Perspective Chain:")
    print(multi_perspective_chain())
    print("\n5. Problem Solving Chain:")
    print(problem_solving_chain())
    print("\n6. Best Practices:")
    print(best_practices_chaining())
