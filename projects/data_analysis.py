"""
Module: Data Analysis
Description: Generate SQL queries, analyze datasets, create insights
Demonstrates prompting for data-driven tasks
"""


def sql_query_generation_prompt(question: str, schema: str) -> str:
    """Generate SQL query from natural language"""
    prompt = f"""
    Generate a SQL query to answer this question: {question}
    
    Database schema:
    {schema}
    
    Requirements:
    - Use correct SQL syntax
    - Only use tables and columns from the provided schema
    - Include appropriate WHERE, JOIN, or GROUP BY clauses as needed
    - Add comments explaining the query
    - Optimize for readability
    
    Provide:
    1. The SQL query
    2. Explanation of what it does
    3. Sample output description
    """
    return prompt


def data_interpretation_prompt(data: str, context: str = "") -> str:
    """Generate insights from data"""
    prompt = f"""
    Analyze this data and provide insights:
    
    {data}
    
    Context: {context}
    
    Provide:
    1. Key findings (most important patterns)
    2. Trends (changes over time or across groups)
    3. Outliers (unusual data points)
    4. Relationships (connections between variables)
    5. Recommendations (what to do with these insights)
    
    Be specific with numbers and percentages.
    Focus on actionable insights.
    """
    return prompt


def data_visualization_prompt(dataset_description: str, analysis_goal: str) -> str:
    """Generate recommendations for data visualization"""
    prompt = f"""
    Recommend visualizations for this dataset: {dataset_description}
    
    Goal of analysis: {analysis_goal}
    
    For each visualization, provide:
    1. Type (scatter plot, bar chart, line graph, etc.)
    2. What to plot (X and Y axes, colors, sizes)
    3. Why it's appropriate
    4. Insights it would show
    
    Recommend 3-4 visualizations that work together to tell the story of the data.
    """
    return prompt


def statistical_summary_prompt(data_description: str) -> str:
    """Generate statistical analysis prompts"""
    prompt = f"""
    Provide a statistical summary of this data: {data_description}
    
    Include:
    1. Descriptive Statistics
       - Mean, median, mode
       - Standard deviation
       - Range
    
    2. Distribution
       - Shape (normal, skewed, etc.)
       - Outliers
    
    3. Correlations
       - Relationships between variables
       - Strength of relationships
    
    4. Statistical Tests (if applicable)
       - Relevant tests for this type of data
       - Hypotheses to test
    
    5. Interpretation
       - What the statistics mean
       - Practical implications
    """
    return prompt


def comparative_analysis_prompt(data1: str, data2: str, comparison_aspect: str) -> str:
    """Generate comparison between datasets"""
    prompt = f"""
    Compare these two datasets on {comparison_aspect}:
    
    Dataset 1: {data1}
    Dataset 2: {data2}
    
    Analysis should include:
    1. Summary Statistics
       - Key metrics for each dataset
       - Side-by-side comparison
    
    2. Differences
       - Major differences
       - Why they might exist
    
    3. Similarities
       - What's consistent
       - What's comparable
    
    4. Implications
       - What this tells us
       - Practical meanings
    
    5. Visualizations
       - Best ways to show the comparison
    """
    return prompt


def anomaly_detection_prompt(dataset: str) -> str:
    """Generate anomaly detection analysis"""
    prompt = f"""
    Analyze this dataset for anomalies: {dataset}
    
    Identify:
    1. Outliers
       - Data points that deviate significantly
       - How far they deviate
    
    2. Unusual Patterns
       - Expected vs. unexpected trends
       - Seasonal patterns or breaks
    
    3. Data Quality Issues
       - Missing data
       - Suspicious values
       - Data entry errors
    
    4. Potential Causes
       - Why anomalies might exist
       - Are they errors or real phenomena?
    
    5. Recommendations
       - How to handle outliers
       - Whether to investigate further
    
    Use statistical methods to identify anomalies objectively.
    """
    return prompt


def predictive_analysis_prompt(historical_data: str, prediction_goal: str) -> str:
    """Generate predictive analysis recommendations"""
    prompt = f"""
    Based on this historical data: {historical_data}
    
    Make predictions about: {prediction_goal}
    
    Include:
    1. Trend Analysis
       - Historical trends
       - Direction of change
       - Rate of change
    
    2. Forecasting
       - Expected future values
       - Confidence level
       - Assumptions
    
    3. Factors Influencing Predictions
       - What variables matter most
       - External factors to consider
    
    4. Uncertainty
       - Range of possible outcomes
       - Risks to predictions
    
    5. Recommendations
       - Actions based on predictions
       - Monitoring strategies
    
    Be clear about limitations and assumptions.
    """
    return prompt


def data_quality_assessment():
    """Prompt for assessing data quality"""
    prompt = """
    For data quality assessment, evaluate:
    
    1. Completeness
       - Missing values
       - Coverage
    
    2. Accuracy
       - Correctness of values
       - Validation against sources
    
    3. Consistency
       - Uniformity across datasets
       - Standardization
    
    4. Validity
       - Values within acceptable range
       - Proper format
    
    5. Uniqueness
       - Duplicate records
       - Primary key violations
    
    6. Timeliness
       - Currency of data
       - Update frequency
    
    Provide: Overall quality score and improvement recommendations
    """
    return prompt


def business_intelligence_prompt(business_question: str, available_data: str) -> str:
    """Generate business intelligence analysis"""
    prompt = f"""
    Answer this business question: {business_question}
    
    Available data: {available_data}
    
    Analysis framework:
    1. Problem Understanding
       - What is being asked?
       - Why does it matter?
    
    2. Data Exploration
       - What data is relevant?
       - What's the data quality?
    
    3. Analysis
       - Calculate key metrics
       - Identify patterns
       - Find correlations
    
    4. Insights
       - What's the story in the data?
       - Key findings
    
    5. Recommendations
       - What should we do?
       - Action items
       - Expected impact
    
    6. Monitoring
       - What metrics to track
       - How often to review
    
    Make recommendations specific and actionable.
    """
    return prompt


if __name__ == "__main__":
    print("=== Data Analysis ===\n")
    print("1. SQL Query Generation:")
    schema = "Users (id, name, email), Orders (id, user_id, amount, date)"
    print(sql_query_generation_prompt("How much did each user spend total?", schema))
    print("\n2. Data Interpretation:")
    print(data_interpretation_prompt("Revenue increased 25% YoY", "E-commerce company"))
    print("\n3. Data Visualization:")
    print(data_visualization_prompt("Monthly sales from 2022-2024", "Identify growth trends"))
    print("\n4. Statistical Summary:")
    print(statistical_summary_prompt("Website traffic for 100 days"))
    print("\n5. Data Quality Assessment:")
    print(data_quality_assessment())
