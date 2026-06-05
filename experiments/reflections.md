# Experiment Reflections

Notes on what worked, what didn't, and lessons learned from experiments.

## Key Insights
- Prompt clarity matters more than model choice for many tasks.
- Few-shot examples consistently improved classification accuracy.
- Chain-of-thought prompts increased correctness on complex reasoning tasks.
- Structured output parsers reduced post-processing effort and improved reliability.
- Monitoring token usage is essential for cost management.

## Lessons Learned
- Start with a concise prompt and expand only when results are poor.
- Use memory sparingly in conversational agents to avoid token bloat.
- Validate JSON output with parsers and add fallback handling.
- Combine self-consistency with chain-of-thought for hard reasoning problems.
- Document each experiment clearly with metrics and observations.
