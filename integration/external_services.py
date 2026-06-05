"""
External Services Integration

Integrating LangChain with databases, APIs, and other services.
Building complete systems with external dependencies.
"""

from typing import Dict, Any, List


def database_integration() -> None:
    """
    Example 1: Integrating with databases.
    Store and retrieve data from databases.
    """
    print("\n=== Example 1: Database Integration ===")
    
    databases = {
        "SQL (PostgreSQL, MySQL)": {
            "Use Case": "Structured data, complex queries",
            "Library": "sqlalchemy, psycopg2",
            "Example": "Store user data, transactions"
        },
        "NoSQL (MongoDB, etc.)": {
            "Use Case": "Flexible schema, document storage",
            "Library": "pymongo",
            "Example": "Store conversations, logs"
        },
        "Vector Database (Pinecone, Weaviate)": {
            "Use Case": "Semantic search, embeddings",
            "Library": "langchain.vectorstores",
            "Example": "RAG systems, similarity search"
        },
        "Cache (Redis)": {
            "Use Case": "Fast retrieval, caching",
            "Library": "redis",
            "Example": "Cache LLM responses"
        }
    }
    
    for db_type, details in databases.items():
        print(f"\n{db_type}:")
        for key, value in details.items():
            print(f"  {key}: {value}")


def api_integration() -> None:
    """
    Example 2: Integrating with external APIs.
    Call other web services.
    """
    print("\n=== Example 2: API Integration ===")
    
    print("API integration patterns:")
    print("\nWeather API Example:")
    print("""from langchain.tools import Tool
import requests

def get_weather(city: str) -> str:
    response = requests.get(f"https://api.weather.com/forecast?city={city}")
    return response.json()["forecast"]

weather_tool = Tool(
    name="Weather",
    func=get_weather,
    description="Get weather forecast for a city"
)
    """)


def search_integration() -> None:
    """
    Example 3: Integrating search capabilities.
    Web search, document search, etc.
    """
    print("\n=== Example 3: Search Integration ===")
    
    search_types = {
        "Web Search (Google, Bing)": "Search the internet for current information",
        "Document Search (Elasticsearch)": "Full-text search over documents",
        "Vector Search (Semantic)": "Find similar content by meaning",
        "Graph Search": "Query knowledge graphs"
    }
    
    print("\nSearch integration types:")
    for search_type, description in search_types.items():
        print(f"  {search_type}: {description}")


def authentication_and_security() -> None:
    """
    Example 4: Authentication for external services.
    Secure integration patterns.
    """
    print("\n=== Example 4: Authentication & Security ===")
    
    auth_methods = {
        "API Keys": "Store in environment variables",
        "OAuth": "Token-based authentication",
        "JWT": "Signed tokens",
        "Basic Auth": "Username/password (use HTTPS)",
        "Service Account": "Service-to-service auth"
    }
    
    print("\nAuthentication methods:")
    for method, description in auth_methods.items():
        print(f"  {method}: {description}")
    
    print("\nBest practices:")
    print("  - Never commit secrets to version control")
    print("  - Use environment variables or secret managers")
    print("  - Rotate credentials regularly")
    print("  - Use HTTPS for all communications")
    print("  - Validate SSL certificates")


def error_handling_and_retry() -> None:
    """
    Example 5: Error handling and retry logic.
    Robust integration patterns.
    """
    print("\n=== Example 5: Error Handling & Retry ===")
    
    print("Error handling patterns:")
    print("""import tenacity

@tenacity.retry(
    wait=tenacity.wait_exponential(),
    stop=tenacity.stop_after_attempt(3)
)
def call_external_api(data):
    try:
        response = api.call(data)
        return response
    except Timeout:
        logger.error("API timeout")
        raise
    except RateLimitError:
        logger.warning("Rate limited, retrying...")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    """)


def rate_limiting_and_caching() -> None:
    """
    Example 6: Managing rate limits and caching.
    Efficient service usage.
    """
    print("\n=== Example 6: Rate Limiting & Caching ===")
    
    strategies = {
        "Caching": [
            "Cache API responses",
            "Use Redis for distributed cache",
            "Implement TTL (time-to-live)",
            "Cache tokens and credentials"
        ],
        "Rate Limiting": [
            "Track API calls per time window",
            "Implement backoff strategies",
            "Use token buckets",
            "Queue requests"
        ],
        "Optimization": [
            "Batch requests when possible",
            "Use webhooks instead of polling",
            "Compress data",
            "Filter unnecessary data"
        ]
    }
    
    for strategy, tactics in strategies.items():
        print(f"\n{strategy}:")
        for tactic in tactics:
            print(f"  - {tactic}")


def monitoring_integration_health() -> None:
    """
    Example 7: Monitoring external service health.
    Keep systems running reliably.
    """
    print("\n=== Example 7: Health Monitoring ===")
    
    monitoring_aspects = {
        "Availability": "Is the service up?",
        "Latency": "How fast are responses?",
        "Error Rate": "How many requests fail?",
        "Data Accuracy": "Is returned data correct?",
        "Cost": "How much are we spending?"
    }
    
    print("\nMetrics to monitor:")
    for metric, description in monitoring_aspects.items():
        print(f"  {metric}: {description}")
    
    print("\nTools:")
    print("  - Prometheus for metrics")
    print("  - Grafana for dashboards")
    print("  - PagerDuty for alerting")
    print("  - DataDog for APM")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("External Services Integration")
    print("="*60)
    
    database_integration()
    api_integration()
    search_integration()
    authentication_and_security()
    error_handling_and_retry()
    rate_limiting_and_caching()
    monitoring_integration_health()