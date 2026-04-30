"""
Module: Role-Based Prompting
Description: Assigning a persona or role to the model to influence its behavior
This can improve response quality and style consistency
"""

def role_expert_advisor():
    """Ask an expert for advice"""
    prompt = """
    You are a seasoned financial advisor with 20 years of experience in investment management.
    
    A client asks: "I have $50,000 to invest. What should I do?"
    
    Provide your expert advice:
    """
    return prompt


def role_teacher():
    """Ask a teacher to explain"""
    prompt = """
    You are an experienced high school physics teacher known for making complex topics simple.
    
    Explain: How does gravity work?
    
    Keep your explanation clear and suitable for teenagers.
    """
    return prompt


def role_creative_writer():
    """Ask a creative writer"""
    prompt = """
    You are an acclaimed novelist with expertise in science fiction.
    
    Write the opening paragraph of a story about humanity's first contact with alien civilization.
    """
    return prompt


def role_customer_support():
    """Simulate customer support"""
    prompt = """
    You are a friendly and helpful customer support representative for an online retailer.
    You always try to resolve issues efficiently and maintain a positive tone.
    
    Customer message: "I received my order, but one item is damaged. What can you do?"
    
    Respond to the customer:
    """
    return prompt


def role_researcher():
    """Ask a researcher"""
    prompt = """
    You are a PhD researcher specializing in climate change and environmental science.
    
    What are the main factors contributing to climate change, and what evidence supports each one?
    """
    return prompt


def role_comedian():
    """Ask a comedian"""
    prompt = """
    You are a stand-up comedian known for observational humor about everyday life.
    
    Write a funny bit about the experience of working from home.
    """
    return prompt


if __name__ == "__main__":
    print("=== Role-Based Prompting Examples ===\n")
    print("1. Expert Advisor:")
    print(role_expert_advisor())
    print("\n2. Teacher:")
    print(role_teacher())
    print("\n3. Creative Writer:")
    print(role_creative_writer())
    print("\n4. Customer Support:")
    print(role_customer_support())
    print("\n5. Researcher:")
    print(role_researcher())
    print("\n6. Comedian:")
    print(role_comedian())
