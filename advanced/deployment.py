"""
Deployment of LangChain Apps

Getting LangChain applications into production.
Scaling, monitoring, and maintaining in production.
"""

from typing import List, Dict


def deployment_approaches() -> None:
    """
    Example 1: Different deployment approaches.
    Various ways to host LangChain applications.
    """
    print("\n=== Example 1: Deployment Approaches ===")
    
    approaches = {
        "REST API": {
            "Framework": "FastAPI, Flask",
            "Advantages": "Simple, language-agnostic",
            "Use Case": "Standard web services"
        },
        "Serverless": {
            "Platform": "AWS Lambda, Google Cloud Functions",
            "Advantages": "Pay-per-use, auto-scaling",
            "Use Case": "Variable load, cost-sensitive"
        },
        "Containerized": {
            "Platform": "Docker, Kubernetes",
            "Advantages": "Reproducible, scalable",
            "Use Case": "Enterprise, complex setups"
        },
        "Embedded": {
            "Platform": "SDK integration",
            "Advantages": "No external dependencies",
            "Use Case": "Desktop, mobile apps"
        }
    }
    
    for approach, details in approaches.items():
        print(f"\n{approach}:")
        for key, value in details.items():
            print(f"  {key}: {value}")


def api_deployment() -> None:
    """
    Example 2: Deploying as REST API.
    Using FastAPI as example.
    """
    print("\n=== Example 2: REST API Deployment ===")
    
    code = '''from fastapi import FastAPI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

app = FastAPI()

# Initialize chain
llm = OpenAI(api_key="...")
prompt = PromptTemplate(...)
chain = LLMChain(llm=llm, prompt=prompt)

@app.post("/predict")
def predict(input_text: str):
    result = chain.invoke({"input": input_text})
    return {"output": result["text"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    '''
    
    print(code)


def scaling_considerations() -> None:
    """
    Example 3: Scaling LangChain applications.
    Handling increased load.
    """
    print("\n=== Example 3: Scaling Strategies ===")
    
    strategies = {
        "Horizontal Scaling": [
            "Deploy multiple instances",
            "Use load balancer",
            "Stateless design",
            "Shared cache/database"
        ],
        "Vertical Scaling": [
            "Increase instance resources",
            "Better CPU/GPU",
            "More memory",
            "Faster storage"
        ],
        "Optimization": [
            "Cache responses",
            "Batch requests",
            "Use cheaper models for simple queries",
            "Optimize prompts for tokens"
        ],
        "Monitoring": [
            "Track response time",
            "Monitor token usage",
            "Alert on errors",
            "Log requests for analysis"
        ]
    }
    
    for strategy, tactics in strategies.items():
        print(f"\n{strategy}:")
        for tactic in tactics:
            print(f"  - {tactic}")


def cost_optimization() -> None:
    """
    Example 4: Optimizing costs.
    Reducing API and operational expenses.
    """
    print("\n=== Example 4: Cost Optimization ===")
    
    techniques = {
        "Model Selection": "Use cheaper models when appropriate",
        "Prompt Optimization": "Minimize tokens in prompts",
        "Caching": "Cache common requests",
        "Batching": "Group requests together",
        "Rate Limiting": "Prevent excessive usage",
        "Monitoring": "Track and control costs",
        "Open Source": "Use free models for some tasks",
        "Async Processing": "Don't block on API calls"
    }
    
    print("\nCost reduction techniques:")
    for technique, description in techniques.items():
        print(f"  {technique}: {description}")


def security_best_practices() -> None:
    """
    Example 5: Security in production.
    Protecting data and APIs.
    """
    print("\n=== Example 5: Security Best Practices ===")
    
    practices = {
        "API Security": [
            "Use authentication (API keys, OAuth)",
            "Rate limiting",
            "Input validation",
            "Output filtering"
        ],
        "Data Protection": [
            "Encrypt sensitive data",
            "Use HTTPS",
            "Don't log sensitive info",
            "Comply with regulations (GDPR, etc.)"
        ],
        "Model Security": [
            "Prevent prompt injection",
            "Validate model outputs",
            "Monitor for abuse",
            "Version control models"
        ],
        "Infrastructure": [
            "Use private networks",
            "Implement firewalls",
            "Backup data",
            "Disaster recovery plan"
        ]
    }
    
    for category, practices_list in practices.items():
        print(f"\n{category}:")
        for practice in practices_list:
            print(f"  ✓ {practice}")


def monitoring_alerting() -> None:
    """
    Example 6: Monitoring and alerting in production.
    Staying aware of system health.
    """
    print("\n=== Example 6: Monitoring and Alerting ===")
    
    metrics_to_monitor = {
        "Performance": ["Response time", "Throughput", "Error rate"],
        "Resources": ["CPU usage", "Memory", "Token usage"],
        "Business": ["API calls count", "Cost", "User satisfaction"],
        "Model": ["Accuracy", "Latency", "Hallucination rate"]
    }
    
    print("\nKey metrics to monitor:")
    for category, metrics in metrics_to_monitor.items():
        print(f"\n{category}:")
        for metric in metrics:
            print(f"  - {metric}")
    
    print("\nPopular monitoring tools:")
    print("  - Datadog")
    print("  - New Relic")
    print("  - CloudWatch")
    print("  - Prometheus")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Deployment of LangChain Apps")
    print("="*60)
    
    deployment_approaches()
    api_deployment()
    scaling_considerations()
    cost_optimization()
    security_best_practices()
    monitoring_alerting()