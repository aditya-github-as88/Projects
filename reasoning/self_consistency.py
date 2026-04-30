"""
Module: Self-Consistency Prompting
Description: Generating multiple reasoning paths and selecting the consistent answer
This improves accuracy by reducing reasoning errors through consensus
"""

def multi_path_math():
    """Math problem with multiple solution paths"""
    prompt = """
    Solve this problem in multiple ways to ensure accuracy.
    
    Problem: Calculate 25% of 80
    
    Method 1: Using decimals (multiply by 0.25)
    Method 2: Using fractions (multiply by 1/4)
    Method 3: Calculate 10% twice and multiply by 2.5
    
    Which answer appears consistently across methods?
    """
    return prompt


def reasoning_paths_analysis():
    """Analyze a question from multiple angles"""
    prompt = """
    Consider this question from different perspectives:
    
    Question: Is remote work better than office work?
    
    Perspective 1: From a productivity standpoint
    Perspective 2: From a collaboration and team culture standpoint
    Perspective 3: From an employee well-being standpoint
    
    Synthesize these perspectives to reach a nuanced conclusion.
    """
    return prompt


def text_interpretation():
    """Interpret text using multiple reading"""
    prompt = """
    Read this passage and interpret it in multiple ways:
    
    Passage: "The old man sat on the bench, watching the children play."
    
    Interpretation 1: Literal - describing a scene
    Interpretation 2: Emotional - what might he be feeling?
    Interpretation 3: Thematic - what bigger ideas does this suggest?
    
    Which interpretation feels most complete?
    """
    return prompt


def classification_consistency():
    """Classify something using multiple criteria"""
    prompt = """
    Classify this item using different classification systems:
    
    Item: A banana
    
    Classification 1: By botanical category
    Classification 2: By food group
    Classification 3: By color
    Classification 4: By texture
    
    Is there a consistent classification that holds across all systems?
    """
    return prompt


def validation_through_consistency():
    """Validate an answer through multiple checks"""
    prompt = """
    Verify this claim using multiple validation methods:
    
    Claim: "The population of Tokyo is over 35 million"
    
    Validation 1: Check if this makes sense given Japan's total population
    Validation 2: Compare with other major city populations
    Validation 3: Consider growth trends in metropolitan areas
    
    Does the claim hold up across different validation approaches?
    """
    return prompt


if __name__ == "__main__":
    print("=== Self-Consistency Prompting Examples ===\n")
    print("1. Multi-Path Math:")
    print(multi_path_math())
    print("\n2. Multiple Reasoning Paths:")
    print(reasoning_paths_analysis())
    print("\n3. Text Interpretation:")
    print(text_interpretation())
    print("\n4. Classification Consistency:")
    print(classification_consistency())
    print("\n5. Validation Through Consistency:")
    print(validation_through_consistency())
