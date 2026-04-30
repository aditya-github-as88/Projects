"""
Module: Creative Writer
Description: Generate creative content - stories, poetry, character development
Demonstrates prompting for creative and imaginative tasks
"""


def short_story_prompt(genre: str, setting: str, word_count: int = 500) -> str:
    """Generate a prompt for a short story"""
    prompt = f"""
    Write a {genre} short story set in {setting}.
    
    Requirements:
    - Length: Approximately {word_count} words
    - Include: Engaging characters, clear conflict, resolution
    - Use: Descriptive language and dialogue
    - Structure: Beginning (setup), Middle (rising action), End (resolution)
    
    Story should be:
    - Original and creative
    - Emotionally engaging
    - Well-paced
    
    Begin writing the story:
    """
    return prompt


def poetry_prompt(style: str, theme: str, line_count: int = 12) -> str:
    """Generate a prompt for poetry"""
    prompt = f"""
    Write a {style} poem about {theme}.
    
    Requirements:
    - Style: {style} (consider rhyme scheme, meter, tone)
    - Lines: Approximately {line_count} lines
    - Theme: {theme}
    
    Elements to include:
    - Vivid imagery
    - Emotional resonance
    - Figurative language (metaphors, similes)
    - Rhythm and flow
    
    The poem should make the reader feel something.
    """
    return prompt


def character_development_prompt(story_context: str) -> str:
    """Generate a prompt for developing characters"""
    prompt = f"""
    Develop a compelling character for this story: {story_context}
    
    Include:
    1. Basic Information
       - Name
       - Age
       - Physical appearance
       - Background
    
    2. Personality
       - Key traits
       - Strengths
       - Weaknesses/flaws
       - Motivations
    
    3. Story Role
       - Main character, antagonist, or supporting
       - How they drive the plot
       - Relationship to other characters
    
    4. Development Arc
       - Where they start
       - Key changes/growth
       - Where they end
    
    5. Voice/Speech Patterns
       - How they talk
       - Unique expressions
       - Education level reflected in speech
    
    Make the character realistic and relatable.
    """
    return prompt


def dialogue_writing_prompt(scene: str, tone: str = "natural") -> str:
    """Generate a prompt for writing dialogue"""
    prompt = f"""
    Write realistic, engaging dialogue for this scene: {scene}
    
    Tone: {tone}
    
    Guidelines:
    - Dialogue should sound natural, not formal (unless character requires it)
    - Each character should have a distinct voice
    - Include action beats to show emotion
    - Avoid exposition dumps (characters don't explain everything)
    - Use contractions and informal speech
    - Show conflict or tension when appropriate
    
    Format:
    "Quoted speech," character name said/replied/asked.
    They showed emotion through action.
    "More dialogue," they continued.
    
    Begin the dialogue:
    """
    return prompt


def world_building_prompt(genre: str, setting: str) -> str:
    """Generate a prompt for world building"""
    prompt = f"""
    Build a detailed world for a {genre} story set in {setting}.
    
    Include:
    1. Geography
       - Physical layout
       - Climate
       - Notable locations
    
    2. Society
       - Government/power structure
       - Social hierarchy
       - Culture and customs
       - Technology level
    
    3. Rules of this World
       - Natural laws (if fantasy/sci-fi)
       - Magic system (if applicable)
       - Constraints and limitations
    
    4. History
       - Key historical events
       - How the world became what it is
       - Relevant backstory
    
    5. Conflict/Tension
       - What problems exist in this world?
       - What drives the story?
    
    Make it feel real and lived-in.
    Include sensory details.
    """
    return prompt


def writing_improvement_prompt(text: str, aspect: str = "overall") -> str:
    """Generate a prompt for improving writing"""
    prompt = f"""
    Analyze and improve this writing:
    
    "{text}"
    
    Focus on: {aspect}
    
    Aspects to consider:
    - Clarity: Is it easy to understand?
    - Flow: Does it read smoothly?
    - Vivid language: Are descriptions engaging?
    - Show vs Tell: Does it show action/emotion?
    - Pacing: Is the rhythm right?
    - Grammar: Is it correct?
    - Word choice: Are word choices effective?
    
    Provide:
    1. Specific feedback on strengths
    2. Areas for improvement
    3. Revised version with explanations of changes
    """
    return prompt


def creative_constraints_generator(genre: str, num_constraints: int = 5) -> str:
    """Generate creative constraints for writing"""
    prompt = f"""
    Generate {num_constraints} interesting creative writing constraints for a {genre} writer.
    
    Constraints should be:
    - Challenging but doable
    - Specific and clear
    - Encouraging creative problem-solving
    - Varied (different aspects of writing)
    
    Examples of constraint types:
    - Length limits (e.g., exactly 100 words)
    - Content requirements (e.g., must include dialogue)
    - Style requirements (e.g., present tense)
    - Word restrictions (e.g., can't use adjectives)
    - Structure requirements (e.g., starts and ends same way)
    
    Format each as:
    [Number]. [Constraint name]: [Clear description]
    """
    return prompt


def story_ideas_prompt(genre: str, num_ideas: int = 5) -> str:
    """Generate story ideas"""
    prompt = f"""
    Generate {num_ideas} unique story ideas for the {genre} genre.
    
    For each idea, include:
    - Catchy title
    - One-sentence premise
    - Main character
    - Central conflict
    - Potential twist or surprise
    - Why it would be compelling
    
    Make sure ideas are:
    - Original and interesting
    - Feasible to write
    - Emotionally engaging
    """
    return prompt


if __name__ == "__main__":
    print("=== Creative Writer ===\n")
    print("1. Short Story Prompt:")
    print(short_story_prompt("mystery", "small coastal town", 800))
    print("\n2. Poetry Prompt:")
    print(poetry_prompt("haiku", "autumn leaves", 3))
    print("\n3. Character Development:")
    print(character_development_prompt("A heist story set in modern-day Tokyo"))
    print("\n4. Dialogue Writing:")
    print(dialogue_writing_prompt("Two old friends reuniting after 10 years", "emotional"))
    print("\n5. World Building:")
    print(world_building_prompt("fantasy", "a medieval kingdom"))
    print("\n6. Writing Improvement:")
    print(writing_improvement_prompt("The cat was fast.", "vivid language"))
    print("\n7. Creative Constraints:")
    print(creative_constraints_generator("science fiction", 4))
    print("\n8. Story Ideas:")
    print(story_ideas_prompt("romantic comedy", 3))
