"""
Module: Flower Delivery AI Assistant System
Description: Multi-assistant system for a flower delivery business
Demonstrates: Role-based prompting, few-shot classification, system design, and routing

Architecture:
1. User Input → Classifier LLM → Route to appropriate assistant
2. Three specialized assistants handle different business functions:
   - Order Support Assistant: Customer issues, order status, payments
   - Floral Expert Assistant: Flower types, care, recommendations, seasonal info
   - Logistics & Operations Assistant: Driver routing, warehouse, delivery estimates

Techniques Used:
- Role-based system prompts with Jinja2 templates
- Few-shot classification with JSON examples
- Multi-turn conversation management
"""

from typing import Dict, List, Literal
from dataclasses import dataclass


@dataclass
class AssistantResponse:
    """Response from an assistant"""
    assistant_type: str
    response: str
    confidence: float


class FlowerDeliveryAssistantSystem:
    """Main system for routing and handling queries in flower delivery business"""
    
    def __init__(self):
        """Initialize the assistant system"""
        self.conversation_history: List[Dict] = []
        self.current_assistant = None
    
    # ==================== JINJA2 TEMPLATE PROMPTS ====================
    
    def get_classifier_prompt(self) -> str:
        """Classify user query to determine which assistant should handle it"""
        return """You are a classification system for a flower delivery business.
        
Analyze the user's query and classify it into ONE of these categories:

1. **Order Support** - Questions about:
   - Order status and tracking
   - Delivery delays and rescheduling
   - Bouquet customization or changes
   - Payment and billing issues
   - Returns or refunds
   - Delivery time windows

2. **Floral Expert** - Questions about:
   - Flower types and varieties
   - Care instructions for flowers
   - Bouquet recommendations
   - Seasonal flower availability
   - Flower meanings and symbolism
   - Storage or handling tips

3. **Logistics & Operations** - Questions about:
   - Driver routing or delivery location issues
   - Warehouse or inventory concerns
   - Delivery time estimates
   - Packaging guidelines
   - Bulk orders or corporate deliveries
   - Logistics constraints

Respond in JSON format:
{
    "category": "Order Support" | "Floral Expert" | "Logistics & Operations",
    "confidence": 0.0-1.0,
    "reasoning": "Brief explanation"
}"""
    
    def get_order_support_system_prompt(self) -> str:
        """System prompt for Order Support Assistant"""
        return """You are the Order Support Assistant for a flower delivery business.

**Your Role**: Handle all customer-facing order issues and inquiries.

**Key Responsibilities**:
- Track order status and delivery timelines
- Manage delivery changes and delays
- Handle payment and billing questions
- Process bouquet customizations
- Manage returns and refunds
- Escalate complex issues appropriately

**Guidelines**:
- Be empathetic about delivery delays
- Offer solutions (reschedule, discount, etc.)
- Explain policies clearly
- Maintain positive customer relationships
- Provide specific timelines when possible
- Apologize for inconveniences

**Tone**: Professional, empathetic, helpful, solution-oriented"""
    
    def get_floral_expert_system_prompt(self) -> str:
        """System prompt for Floral Expert Assistant"""
        return """You are the Floral Expert Assistant for a flower delivery business.

**Your Role**: Provide expert guidance on flowers, arrangements, and recommendations.

**Key Expertise**:
- Flower varieties, origins, and characteristics
- Seasonal availability and peak seasons
- Care instructions (watering, sunlight, temperature)
- Arrangement design principles
- Flower symbolism and meanings
- Storage and longevity tips
- Combinations that work well together

**Guidelines**:
- Provide detailed, practical advice
- Consider customer preferences (color, size, occasion)
- Suggest alternatives if flowers aren't available
- Explain care instructions clearly
- Recommend appropriate flowers for different occasions
- Share interesting floral facts

**Tone**: Knowledgeable, enthusiastic, educational, friendly"""
    
    def get_operations_system_prompt(self) -> str:
        """System prompt for Logistics & Operations Assistant"""
        return """You are the Logistics & Operations Assistant for a flower delivery business.

**Your Role**: Handle operational efficiency and logistical coordination.

**Key Responsibilities**:
- Manage driver routing and delivery coordination
- Handle warehouse inventory and fulfillment
- Provide delivery time estimates
- Ensure packaging guidelines are met
- Coordinate bulk and corporate orders
- Address operational constraints

**Guidelines**:
- Prioritize delivery efficiency
- Consider seasonal volume variations
- Provide accurate time estimates
- Flag packaging or handling concerns
- Suggest operational improvements
- Monitor quality standards

**Tone**: Professional, efficient, detail-oriented, practical"""
    
    # ==================== CLASSIFICATION LOGIC ====================
    
    def get_few_shot_classification_examples(self) -> str:
        """Few-shot examples for query classification"""
        return """
Examples:

User Query: "Can I change my delivery time for my bouquet order?"
Category: Order Support
Reasoning: Customer asking to modify existing order delivery

---

User Query: "What's the best way to keep my roses fresh longer?"
Category: Floral Expert
Reasoning: Question about flower care and longevity

---

User Query: "Our warehouse is running low on red roses. What's our supplier status?"
Category: Logistics & Operations
Reasoning: Internal inventory and supply chain question

---

User Query: "I ordered flowers 3 days ago and they haven't arrived yet. This is urgent!"
Category: Order Support
Reasoning: Delivery complaint requiring order investigation

---

User Query: "What flowers would work best for a spring wedding bouquet?"
Category: Floral Expert
Reasoning: Asking for flower recommendations and expertise

---

User Query: "Can we handle 50 deliveries in downtown by 5 PM today?"
Category: Logistics & Operations
Reasoning: Operational feasibility and routing question
"""
    
    def classify_query(self, user_query: str) -> Dict:
        """Classify query into appropriate category"""
        classification_prompt = f"""{self.get_classifier_prompt()}

{self.get_few_shot_classification_examples()}

User Query: "{user_query}"

Category:"""
        
        # In production, this would call the actual LLM
        # For now, return structure showing how it works
        return {
            "prompt": classification_prompt,
            "instructions": "Send this to classifier LLM to get category"
        }
    
    # ==================== ASSISTANT HANDLERS ====================
    
    def handle_order_support(self, user_query: str) -> AssistantResponse:
        """Handle query with Order Support Assistant"""
        system_prompt = self.get_order_support_system_prompt()
        
        # Add to history
        self._add_to_history("user", user_query)
        
        response_text = f"""[Order Support Response]
System: {system_prompt[:100]}...

Handling: {user_query}

Actions:
1. Check order status in database
2. Verify delivery address and timeline
3. Offer solutions if issues found
4. Process any necessary changes"""
        
        self._add_to_history("assistant", response_text)
        
        return AssistantResponse(
            assistant_type="Order Support",
            response=response_text,
            confidence=0.95
        )
    
    def handle_floral_expert(self, user_query: str) -> AssistantResponse:
        """Handle query with Floral Expert Assistant"""
        system_prompt = self.get_floral_expert_system_prompt()
        
        self._add_to_history("user", user_query)
        
        response_text = f"""[Floral Expert Response]
System: {system_prompt[:100]}...

Providing expert guidance on: {user_query}

Information:
1. Detailed flower characteristics
2. Care and maintenance instructions
3. Availability and seasonal information
4. Recommendations based on preferences"""
        
        self._add_to_history("assistant", response_text)
        
        return AssistantResponse(
            assistant_type="Floral Expert",
            response=response_text,
            confidence=0.95
        )
    
    def handle_operations(self, user_query: str) -> AssistantResponse:
        """Handle query with Logistics & Operations Assistant"""
        system_prompt = self.get_operations_system_prompt()
        
        self._add_to_history("user", user_query)
        
        response_text = f"""[Operations Response]
System: {system_prompt[:100]}...

Analyzing operational question: {user_query}

Actions:
1. Check warehouse inventory
2. Evaluate delivery routes
3. Calculate time estimates
4. Flag any constraints or issues"""
        
        self._add_to_history("assistant", response_text)
        
        return AssistantResponse(
            assistant_type="Logistics & Operations",
            response=response_text,
            confidence=0.95
        )
    
    # ==================== ROUTING LOGIC ====================
    
    def route_to_assistant(self, user_query: str, 
                          category: Literal["Order Support", "Floral Expert", "Logistics & Operations"]) -> AssistantResponse:
        """Route query to appropriate assistant based on category"""
        
        routing_map = {
            "Order Support": self.handle_order_support,
            "Floral Expert": self.handle_floral_expert,
            "Logistics & Operations": self.handle_operations
        }
        
        handler = routing_map.get(category)
        if handler:
            return handler(user_query)
        else:
            raise ValueError(f"Unknown category: {category}")
    
    def process_query(self, user_query: str) -> Dict:
        """Main entry point: Classify and route query"""
        print(f"\n{'='*60}")
        print(f"User Query: {user_query}")
        print(f"{'='*60}")
        
        # Step 1: Classify
        classification = self.classify_query(user_query)
        print(f"\n[STEP 1] Classification")
        print(f"Prompt generated to classify query...")
        
        # In production, we'd get actual classification here
        # For demo, we'll show the flow
        return {
            "original_query": user_query,
            "classification_prompt": classification["prompt"],
            "note": "In production, this would be sent to classifier LLM"
        }
    
    # ==================== CONVERSATION MANAGEMENT ====================
    
    def _add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_history
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []


# ==================== SAMPLE QUERIES FOR TESTING ====================

SAMPLE_QUERIES = [
    "Can I change the delivery time for my bouquet?",
    "Which flowers last longest in hot weather?",
    "A driver is stuck in traffic—what should we update the customer about?",
    "My flowers arrived wilted. What can you do?",
    "What's the difference between garden roses and hybrid roses?",
    "Can we handle 50 deliveries tomorrow with our current staff?"
]


def run_tests():
    """Run the flower delivery assistant system with test queries"""
    print("\n" + "="*70)
    print("FLOWER DELIVERY AI ASSISTANT SYSTEM - TEST RUN")
    print("="*70)
    
    system = FlowerDeliveryAssistantSystem()
    
    print("\n[SYSTEM INITIALIZATION]")
    print("✓ Order Support Assistant loaded")
    print("✓ Floral Expert Assistant loaded")
    print("✓ Logistics & Operations Assistant loaded")
    print("✓ Query classification system ready")
    
    print("\n" + "-"*70)
    print("TESTING WITH SAMPLE CUSTOMER & STAFF QUERIES")
    print("-"*70)
    
    for i, query in enumerate(SAMPLE_QUERIES, 1):
        result = system.process_query(query)
        print(f"\nTest {i}: {query}")
        print(f"Classification Prompt Generated: Yes")
        print(f"Status: Ready for LLM classification")


def show_system_architecture():
    """Display the system architecture and how it works"""
    print("\n" + "="*70)
    print("FLOWER DELIVERY ASSISTANT - SYSTEM ARCHITECTURE")
    print("="*70)
    
    architecture = """
    FLOW DIAGRAM:
    
    User Input
       ↓
    Classifier LLM (Determine category with few-shot examples)
       ↓
    ┌──────────────────────────────────────────┐
    │                                          │
    ↓                 ↓                        ↓
    
Order Support    Floral Expert      Logistics & Operations
Assistant        Assistant          Assistant
├─ Order Status   ├─ Flower Types    ├─ Driver Routing
├─ Delivery       ├─ Care Guides     ├─ Warehouse Mgmt
├─ Payments       ├─ Combos          ├─ Time Estimates
├─ Changes        └─ Seasonal        └─ Packaging
└─ Returns           Availability
       ↓                 ↓                        ↓
    ┌──────────────────────────────────────────┐
    │            Provide Response               │
    └──────────────────────────────────────────┘
                      ↓
                  User Response
    
    KEY TECHNIQUES USED:
    1. Role-based System Prompts - Each assistant has defined expertise
    2. Few-shot Classification - Examples help classify queries accurately
    3. JSON Structured Output - Consistent classification format
    4. Jinja2 Templates - System prompts defined as templates
    5. Multi-turn Conversation - History maintained per assistant
    6. Routing Logic - Smart query distribution
    """
    
    print(architecture)


def show_implementation_guide():
    """Show how to implement this with real LLM"""
    print("\n" + "="*70)
    print("IMPLEMENTATION GUIDE FOR PRODUCTION")
    print("="*70)
    
    guide = """
    TO USE WITH REAL LLM (Groq, OpenAI, etc.):
    
    1. CLASSIFIER STEP:
       - Send get_classifier_prompt() + user query to LLM
       - Parse JSON response to get category
       - Extract confidence level for fallback handling
    
    2. ROUTING:
       - Use category to determine which handler to call
       - Maintain assistant-specific conversation history
       - Pass conversation history to each LLM call
    
    3. ASSISTANT RESPONSE:
       - Use appropriate system prompt (Jinja2 template)
       - Include conversation history
       - Stream or batch response based on needs
    
    4. EXAMPLE CODE:
    
    system = FlowerDeliveryAssistantSystem()
    user_input = "Can I change my delivery time?"
    
    # Classify
    classification_prompt = system.get_classifier_prompt()
    category = llm(classification_prompt + user_input)
    
    # Route and handle
    response = system.route_to_assistant(user_input, category)
    
    5. ERROR HANDLING:
       - If confidence < 0.7, ask user to clarify
       - If classification fails, ask: "Is this about [Order/Flowers/Delivery]?"
       - Escalate to human if assistant can't resolve
    
    6. CONVERSATION PERSISTENCE:
       - Save conversation history to database
       - Use conversation_history for context
       - Allow users to switch assistants mid-conversation
    """
    
    print(guide)


if __name__ == "__main__":
    # Show system architecture
    show_system_architecture()
    
    # Run tests
    run_tests()
    
    # Show implementation guide
    show_implementation_guide()
    
    # Show one detailed example
    print("\n" + "="*70)
    print("DETAILED EXAMPLE: ORDER SUPPORT SYSTEM PROMPT")
    print("="*70)
    system = FlowerDeliveryAssistantSystem()
    print(system.get_order_support_system_prompt())
