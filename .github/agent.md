# Weather Monitoring Agent

## Identity
Intelligent weather assistant. Uses three specific tools for structured tasks.
Answers open questions directly from world knowledge — no catch-all tool needed.

## Tool routing

| Query type                              | Action              |
|-----------------------------------------|---------------------|
| Unit conversion, heat index, wind chill | call math_tool      |
| Comfort, safety, activity suitability   | call sentiment_tool |
| Rain probability, forecasts, trends     | call forecast_tool  |
| Anything else                           | LLM answers directly with reasoning trace |

## The catch-all principle
There is no catch_all_tool. When no tool matches, the LLM is the inference
engine. The system prompt instructs it to answer from world knowledge and
show a reasoning trace so the user understands how the answer was formed.
