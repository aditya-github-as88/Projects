"""
Module: Evaluation Metrics
Description: Scoring and evaluating prompt quality across different dimensions
Methods for measuring prompt effectiveness
"""

def relevance_scoring():
    """Evaluate relevance of responses"""
    guide = """
    RELEVANCE SCORING (1-10 scale)
    
    Definition: How well does the response address the specific question/task?
    
    10 - Highly Relevant
        Perfect match to the question, addresses all aspects
    
    7-9 - Very Relevant
        Directly addresses the question with minor deviations
    
    5-6 - Somewhat Relevant
        Addresses main question but includes tangential information
    
    3-4 - Partially Relevant
        Only partially addresses the question
    
    1-2 - Not Relevant
        Doesn't address the question or completely off-topic
    
    EXAMPLE:
    Question: "What is Python?"
    Response: "Python is a high-level programming language..."
    Score: 10 (Direct answer to the question)
    """
    return guide


def coherence_scoring():
    """Evaluate logical flow and coherence"""
    guide = """
    COHERENCE SCORING (1-10 scale)
    
    Definition: Does the response flow logically with clear connections between ideas?
    
    10 - Highly Coherent
        Ideas flow perfectly, clear transitions, logical progression
    
    7-9 - Very Coherent
        Clear structure, mostly smooth transitions
    
    5-6 - Somewhat Coherent
        Some logical flow but occasional jumps between ideas
    
    3-4 - Partially Coherent
        Difficult to follow, weak connections between ideas
    
    1-2 - Incoherent
        Random ideas, no logical flow
    
    Evaluation Tips:
    - Look for clear paragraph structure
    - Check for logical transitions between ideas
    - Verify ideas build upon each other
    """
    return guide


def creativity_scoring():
    """Evaluate originality and creativity"""
    guide = """
    CREATIVITY SCORING (1-10 scale)
    
    Definition: How original and imaginative is the response?
    
    10 - Highly Creative
        Novel ideas, unique perspective, engaging and original
    
    7-9 - Very Creative
        Some original elements, mostly interesting approach
    
    5-6 - Moderately Creative
        Some creative elements but somewhat predictable
    
    3-4 - Minimally Creative
        Standard response with few original elements
    
    1-2 - Not Creative
        Completely generic, clichéd, no original thinking
    
    Assessment Criteria:
    - Use of unexpected examples
    - Novel connections between concepts
    - Original phrasing vs. clichés
    - Depth of thinking beyond surface level
    """
    return guide


def factual_accuracy_scoring():
    """Evaluate factual correctness"""
    guide = """
    FACTUAL ACCURACY SCORING (1-10 scale)
    
    Definition: How factually correct is the information provided?
    
    10 - Completely Accurate
        All facts verified as correct
    
    7-9 - Highly Accurate
        Minimal or trivial errors
    
    5-6 - Mostly Accurate
        Some significant errors but core information is correct
    
    3-4 - Partially Accurate
        Multiple errors, significantly affects understanding
    
    1-2 - Inaccurate
        Mostly or entirely incorrect
    
    Verification Methods:
    - Check against reliable sources
    - Verify dates and statistics
    - Confirm definitions and terminology
    - Cross-reference with authoritative sources
    """
    return guide


def composite_scoring_system():
    """Create a composite score from multiple dimensions"""
    system = """
    COMPOSITE EVALUATION SYSTEM
    
    Dimensions and Weights:
    - Relevance (25%): Does it answer the question?
    - Accuracy (25%): Is the information correct?
    - Clarity (20%): Is it easy to understand?
    - Completeness (15%): Does it cover necessary aspects?
    - Coherence (15%): Is it well-organized?
    
    Calculation:
    Score = (Relevance × 0.25) + (Accuracy × 0.25) + (Clarity × 0.20) 
          + (Completeness × 0.15) + (Coherence × 0.15)
    
    Example:
    Relevance: 9 × 0.25 = 2.25
    Accuracy: 8 × 0.25 = 2.00
    Clarity: 9 × 0.20 = 1.80
    Completeness: 8 × 0.15 = 1.20
    Coherence: 9 × 0.15 = 1.35
    ─────────────────────────────
    TOTAL SCORE: 8.6/10
    
    Interpretation:
    8.5-10.0: Excellent response
    7.5-8.4: Good response
    6.5-7.4: Adequate response
    5.0-6.4: Acceptable response
    Below 5.0: Poor response
    """
    return system


def evaluation_rubric():
    """Complete evaluation rubric template"""
    rubric = """
    COMPREHENSIVE EVALUATION RUBRIC
    
    TASK: [Specify the task]
    INPUT: [What was given to the model]
    EXPECTED OUTPUT: [What we wanted]
    ACTUAL OUTPUT: [What the model produced]
    
    ┌─────────────────┬────────┬──────────────────────────┐
    │ Dimension       │ Score  │ Notes                    │
    ├─────────────────┼────────┼──────────────────────────┤
    │ Relevance       │  /10   │                          │
    │ Accuracy        │  /10   │                          │
    │ Clarity         │  /10   │                          │
    │ Completeness    │  /10   │                          │
    │ Coherence       │  /10   │                          │
    └─────────────────┴────────┴──────────────────────────┘
    
    Overall Score: ___/50 ➜ ___/10 (average)
    
    Strengths:
    - [What the response did well]
    
    Areas for Improvement:
    - [What could be better]
    
    Suggested Prompt Revision:
    - [How to improve the prompt for better results]
    """
    return rubric


if __name__ == "__main__":
    print("=== Evaluation Metrics ===\n")
    print("1. Relevance Scoring:")
    print(relevance_scoring())
    print("\n2. Coherence Scoring:")
    print(coherence_scoring())
    print("\n3. Creativity Scoring:")
    print(creativity_scoring())
    print("\n4. Factual Accuracy Scoring:")
    print(factual_accuracy_scoring())
    print("\n5. Composite Scoring System:")
    print(composite_scoring_system())
    print("\n6. Evaluation Rubric:")
    print(evaluation_rubric())
