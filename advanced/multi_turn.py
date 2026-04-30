"""
Module: Multi-Turn Dialogue Prompting
Description: Building context and history across multiple prompt-response pairs
Maintaining conversation context for coherent multi-turn interactions
"""

def multi_turn_customer_support():
    """Multi-turn customer service conversation"""
    conversation = """
    System: You are a helpful customer support agent for an electronics retailer.
    
    Turn 1:
    Customer: "Hi, I'm having issues with my new laptop"
    Agent: "Hello! I'm sorry to hear you're having issues. 
            Can you please describe what problems you're experiencing?"
    
    Turn 2:
    Customer: "The battery drains very quickly, even when not in use"
    Agent: "Thank you for that information. How long have you had the laptop, 
            and when did this issue start?"
    
    Turn 3:
    Customer: "I bought it 2 weeks ago, and it started last week"
    Agent: "I understand. Let me help you troubleshoot. Have you tried..."
    """
    return conversation


def multi_turn_tutoring():
    """Multi-turn educational dialogue"""
    dialogue = """
    System: You are a patient math tutor helping a student understand algebra.
    
    Turn 1:
    Student: "I don't understand how to solve: 2x + 5 = 13"
    Tutor: "Great question! Let's break this down step by step.
            First, what do you think we need to do to isolate the 'x'?"
    
    Turn 2:
    Student: "Maybe subtract 5 from both sides?"
    Tutor: "Excellent! That's exactly right. What do you get when you do that?"
    
    Turn 3:
    Student: "2x = 8"
    Tutor: "Perfect! Now, what's the next step to find x?"
    
    Turn 4:
    Student: "Divide both sides by 2?"
    Tutor: "Yes! So x = 4. Great work!"
    """
    return dialogue


def multi_turn_planning_session():
    """Multi-turn project planning"""
    session = """
    System: You are a project manager helping plan a software project.
    Keep track of decisions and build on previous context.
    
    Turn 1:
    PM: "We need to plan a new mobile app. What should be our first step?"
    Dev: "We should define the core features and timeline"
    
    Turn 2:
    PM: "Good point. We've identified 5 core features. What's realistic for 3 months?"
    Dev: "With a team of 2, we can deliver 3 features, maybe 4 if they're straightforward"
    
    Turn 3:
    PM: "Okay, let's prioritize. Which features are most critical?"
    Dev: "User authentication, product catalog, and search are essential"
    
    Turn 4:
    PM: "Perfect. Let's plan for those three. When can we start?"
    """
    return session


def context_building_prompt():
    """Template for building context in multi-turn conversations"""
    template = """
    CONTEXT BUILDING STRATEGY:
    
    1. Initial Setup (Turn 1)
       - Establish the scenario
       - Define the role/character
       - Set expectations
    
    2. First Exchange (Turn 2-3)
       - Introduce the main topic
       - Gather initial information
       - Show understanding
    
    3. Deepening (Turn 4+)
       - Reference previous turns
       - Build on established context
       - Show progression
    
    4. Conclusion
       - Summarize decisions
       - Confirm next steps
       - Maintain consistency
    """
    return template


def maintaining_consistency():
    """Tips for consistency across turns"""
    tips = """
    MAINTAINING CONSISTENCY IN MULTI-TURN PROMPTS:
    
    1. Reference Previous Context
       - "As we discussed earlier..."
       - "Building on your point about..."
    
    2. Maintain Character
       - Keep the same persona throughout
       - Use consistent terminology
    
    3. Track Decisions
       - Note what was already decided
       - Avoid contradicting earlier statements
    
    4. Build Naturally
       - Let conversations progress logically
       - Don't jump topics abruptly
    
    5. Summarize Periodically
       - "So far we've established..."
       - "Just to confirm..."
    """
    return tips


if __name__ == "__main__":
    print("=== Multi-Turn Dialogue Prompting ===\n")
    print("1. Customer Support:")
    print(multi_turn_customer_support())
    print("\n2. Tutoring Session:")
    print(multi_turn_tutoring())
    print("\n3. Planning Session:")
    print(multi_turn_planning_session())
    print("\n4. Context Building Strategy:")
    print(context_building_prompt())
    print("\n5. Maintaining Consistency:")
    print(maintaining_consistency())
