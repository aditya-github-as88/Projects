"""
Module: Chain of Thought Prompting
Description: Encouraging the model to show its reasoning step-by-step
This improves accuracy on complex reasoning tasks
"""

def math_chain_of_thought():
    """Math problem with step-by-step reasoning"""
    prompt = """
    Let's think through this step by step.
    
    Problem: If each notebook costs $3 and I buy 5 notebooks, and I pay with a $20 bill, how much change do I get?
    
    Step 1: Calculate the total cost of notebooks
    Step 2: Calculate the change from the $20 bill
    Step 3: Provide the final answer
    """
    return prompt


def logic_chain_of_thought():
    """Logic puzzle with reasoning"""
    prompt = """
    Think through this problem step by step.
    
    Problem: Alice, Bob, and Charlie went to a store. Alice bought apples, Bob bought bananas, and Charlie bought cherries.
    - Each person spent a different amount
    - Alice spent less than Charlie
    - Bob spent more than Alice
    
    Can you determine who spent the most? Explain your reasoning.
    """
    return prompt


def decision_making_chain_of_thought():
    """Decision making with reasoning"""
    prompt = """
    Let's break down this decision logically.
    
    Situation: I'm choosing between two job offers. Job A pays $80,000 and has 2 weeks vacation, but requires 60-hour work weeks. 
    Job B pays $70,000 with 4 weeks vacation, and requires 40-hour work weeks.
    
    Consider:
    - Financial impact
    - Work-life balance
    - Career growth potential
    - Personal wellbeing
    
    Which job should I choose and why?
    """
    return prompt


def reading_comprehension_cot():
    """Comprehension with reasoning"""
    prompt = """
    Read this passage and answer the question using step-by-step thinking.
    
    Passage: "In the 1920s, jazz music emerged as a cultural force in America. 
    Born from a blend of African-American musical traditions and European influences, 
    it became the soundtrack of the Jazz Age."
    
    Question: What cultural factors contributed to the emergence of jazz?
    
    Think step by step:
    1. Identify the cultural origins mentioned
    2. List the influences described
    3. Connect them to explain the emergence
    """
    return prompt


def problem_solving_cot():
    """Problem solving with explicit reasoning"""
    prompt = """
    Work through this problem with clear reasoning steps.
    
    Problem: A store has twice as many apples as oranges. 
    If there are 12 more apples than oranges, how many of each fruit does the store have?
    
    Let me work through this:
    Step 1: Define variables
    Step 2: Set up equations based on the information
    Step 3: Solve the equations
    Step 4: Verify the answer
    """
    return prompt


if __name__ == "__main__":
    print("=== Chain of Thought Prompting Examples ===\n")
    print("1. Math Problem:")
    print(math_chain_of_thought())
    print("\n2. Logic Puzzle:")
    print(logic_chain_of_thought())
    print("\n3. Decision Making:")
    print(decision_making_chain_of_thought())
    print("\n4. Reading Comprehension:")
    print(reading_comprehension_cot())
    print("\n5. Problem Solving:")
    print(problem_solving_cot())
