"""
Module: Chatbot Demo
Description: Build a conversational AI assistant using multiple prompt techniques
Demonstrates multi-turn conversation, context management, and prompt optimization
"""

from typing import List, Dict


class ConversationalBot:
    """A chatbot that uses effective prompting techniques"""
    
    def __init__(self, system_role: str = "helpful assistant"):
        """Initialize bot with a system role"""
        self.system_role = system_role
        self.conversation_history: List[Dict] = []
        self.context = ""
    
    def build_system_prompt(self) -> str:
        """Build the system prompt for the bot"""
        return f"""You are a {self.system_role}. 
Your goal is to be helpful, harmless, and honest.
Be concise but informative.
If you don't know something, admit it rather than guessing."""
    
    def add_to_history(self, role: str, content: str):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def get_conversation_context(self) -> str:
        """Generate context from conversation history"""
        summary = f"Conversation has {len(self.conversation_history)} messages so far.\n"
        if self.conversation_history:
            summary += "Recent messages:\n"
            for msg in self.conversation_history[-4:]:  # Last 4 messages
                summary += f"- {msg['role']}: {msg['content'][:100]}...\n"
        return summary
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate response"""
        # Add user message to history
        self.add_to_history("user", user_input)
        
        # This would be called with actual API in production
        response = self.generate_response()
        
        # Add bot response to history
        self.add_to_history("assistant", response)
        
        return response
    
    def generate_response(self) -> str:
        """Generate bot response (placeholder)"""
        return "This would be the bot's response from the API"


def customer_service_bot_example():
    """Example of a customer service chatbot"""
    bot = ConversationalBot("customer service representative")
    
    dialogue = """
    SYSTEM PROMPT:
    You are a friendly customer service representative for an online retailer.
    You help resolve issues quickly and maintain a positive tone.
    Always be empathetic and offer solutions.
    
    USER: I received a damaged item. What can I do?
    BOT: I'm sorry to hear your item arrived damaged! That's not the experience we want you to have.
         Here's what we can do:
         1. Replace it at no cost
         2. Process a full refund
         3. Offer a discount on your next purchase
         
         Which option would work best for you?
    
    USER: Can you replace it?
    BOT: Of course! I can arrange that right away.
         - I'll send a prepaid shipping label so you can return the damaged item
         - Once we receive it, we'll ship your replacement immediately
         - Most replacements arrive within 3-5 business days
         
         Does that work for you?
    """
    return dialogue


def educational_tutor_example():
    """Example of an educational chatbot"""
    tutor_system = """
    SYSTEM PROMPT:
    You are a patient, encouraging math tutor.
    Your goal is to help students understand concepts, not just get answers.
    Ask guiding questions to help them think through problems.
    Celebrate progress and correct mistakes gently.
    
    TONE: Friendly, supportive, encouraging
    """
    
    dialogue = """
    USER: I don't understand fractions
    
    TUTOR: No problem! Let's break it down together.
           A fraction is just a way to show parts of a whole.
           
           Imagine you have a pizza cut into 8 slices.
           If you eat 3 slices, you've eaten 3/8 of the pizza.
           
           Try this: If a chocolate bar has 10 pieces and you eat 4,
           what fraction did you eat?
    
    USER: Um... 4/10?
    
    TUTOR: Exactly right! You've got it! 🎉
           That's 4 out of 10 pieces.
           
           You can also simplify it to 2/5 (we divide both numbers by 2).
           But 4/10 is correct!
           
           Want to try another one?
    """
    return dialogue


def technical_support_bot():
    """Example of technical support chatbot"""
    system = """
    You are a technical support specialist.
    Use troubleshooting techniques:
    1. Clarify the problem
    2. Check recent changes
    3. Try basic fixes first
    4. Escalate if needed
    
    Be technical but clear.
    Provide step-by-step instructions.
    """
    
    example = """
    USER: My laptop won't turn on
    
    BOT: Let's troubleshoot this. I'll ask a few questions first:
         1. When you press the power button, do you see any lights or hear any sounds?
         2. Is the laptop plugged in or on battery?
         3. When did this last work?
    
    USER: No lights or sounds. It's plugged in. Worked fine yesterday.
    
    BOT: Let's try some basic fixes:
         1. Check if the power adapter is fully plugged in at both ends
         2. Try a different power outlet
         3. Hold the power button for 30 seconds
         4. Wait 2 minutes and try again
         
         Let me know if any of these work.
    """
    return example


def multi_turn_conversation_structure():
    """Template for structuring multi-turn conversations"""
    structure = """
    MULTI-TURN CONVERSATION STRUCTURE:
    
    Turn 1: Introduction
    - Greet user
    - Explain what you can help with
    - Ask clarifying question
    
    Turn 2-3: Problem Identification
    - Gather information about the issue
    - Understand context
    - Ask follow-up questions if needed
    
    Turn 4-5: Solution/Assistance
    - Provide relevant help
    - Check for understanding
    - Offer next steps
    
    Turn 6: Conclusion
    - Summarize what was discussed
    - Confirm satisfaction
    - Offer further assistance
    
    KEY PRINCIPLES:
    - Remember what was said earlier
    - Build on previous context
    - Show empathy and understanding
    - Be clear and concise
    - Use conversational language
    """
    return structure


def prompt_optimization_for_bots():
    """Tips for optimizing prompts in chatbots"""
    tips = """
    PROMPT OPTIMIZATION FOR CHATBOTS:
    
    1. Clear System Role
       Good: "You are a helpful coding assistant"
       Better: "You are an experienced Python developer helping beginners learn Python"
    
    2. Behavioral Guidelines
       Include: tone, approach, what to do if you don't know
       Example: "Be encouraging. If unsure, ask for clarification."
    
    3. Output Format
       Specify: length, structure, format
       Example: "Respond in 1-2 paragraphs. Use bullet points for lists."
    
    4. Context Management
       - Include relevant conversation history
       - Reference previous topics
       - Maintain consistency in knowledge
    
    5. Constraint Setting
       - What topics to discuss or avoid
       - Appropriate tone/language
       - When to escalate
    
    6. Few-Shot Examples
       Include examples of good responses
       Helps model understand expected behavior
    """
    return tips


if __name__ == "__main__":
    print("=== Chatbot Demo ===\n")
    print("1. Customer Service Bot:")
    print(customer_service_bot_example())
    print("\n2. Educational Tutor:")
    print(educational_tutor_example())
    print("\n3. Technical Support Bot:")
    print(technical_support_bot())
    print("\n4. Multi-Turn Structure:")
    print(multi_turn_conversation_structure())
    print("\n5. Optimization Tips:")
    print(prompt_optimization_for_bots())
