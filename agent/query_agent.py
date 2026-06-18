
import os
import openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()

from langchain_community.agent_toolkits import load_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


### Load LLM
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)



### Tool to Do a Web Search

from serpapi.google_search import GoogleSearch

serp_api_key = os.environ["SERPAPI_API_KEY"]

def do_web_search(query):
    """
    Perform a Google web search using SerpAPI and return a simplified list
    of the top organic search results.
    """

    # Parameters for the search query
    params = {
        "q": query,                     # Search query string
        "num": 1,                       # Number of results to fetch (top 1 result here)
        "google_domain": "google.com",  # Google domain to use for the search
        "api_key": serp_api_key         # Your SerpAPI key for authentication
    }

    # Initialize the GoogleSearch object with the parameters
    search = GoogleSearch(params)

    # Execute the search and get the full results as a Python dictionary
    results = search.get_dict()

    # Extract only essential fields from the organic search results
    slim_result = []
    for r in results.get("organic_results", []):
        slim_result.append(
            {
                "title": r.get("title"),       # Title of the search result page
                "link": r.get("link"),         # Direct URL to the page
                "source": r.get("source"),     # Source site or domain (if provided)
                "date": r.get("date"),         # Publish or announcement date (if available)
                "snippet": r.get("snippet"),   # Short text snippet/preview from the page
            }
        )

    # Return the simplified list of result dictionaries
    return slim_result


# Create the tool to pass to an agent
from langchain_core.tools import Tool
web_search_tool = Tool(
    name="web_search_tool",
    description="""Perform web search for the given input query.\
    The input should always be a string representing a query to search on web or internet, \
    and this function will always return a list of json object with the web search results. """,
    func = do_web_search,
)


### Tool to make a Weather API call

from langchain_community.utilities import OpenWeatherMapAPIWrapper
weather = OpenWeatherMapAPIWrapper()

# Create the tool to pass to an agent
from langchain_core.tools import Tool
weather_tool = Tool(
    name="weather_tool",
    description="""Get the weather details for the given city.\
    The input should always be a string representing the city name, \
    and this function will always return a json format response with weather details. """,
    func = weather.run,
)



### Load tools
tools = [web_search_tool, weather_tool]


### Initialize the agent
agent = create_agent(llm, tools=tools)


from langfuse.langchain import CallbackHandler
langfuse_handler = CallbackHandler()


### Run a sample query
from langchain_core.messages import HumanMessage

# input = {"messages": [HumanMessage(content="When was iPhone 17 launched")]}
query = "How is the weather in Hyderabad? What are the popular places to visit in Hyderabad?"
input = {"messages": [HumanMessage(content=query)]}

#response = agent.invoke(input)

response = agent.invoke(
    input,
    config={
        "callbacks": [langfuse_handler],
        "run_name": "Agent_Query"
        }
    )

print(f"Input query: {query}")
print(f"Agent Response:\n{response['messages'][-1].content}")
