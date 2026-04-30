"""
Module: Quiz Generator
Description: Generate quizzes, flashcards, and assessment materials
Demonstrates prompt engineering for educational content creation
"""

from typing import List, Dict


def multiple_choice_quiz_prompt(topic: str, num_questions: int = 5) -> str:
    """Generate a prompt to create multiple choice questions"""
    prompt = f"""
    Create {num_questions} multiple choice questions about {topic}.
    
    For each question:
    1. Question (clear and specific)
    2. Option A
    3. Option B
    4. Option C
    5. Option D
    6. Correct answer (A, B, C, or D)
    7. Explanation (why this is correct)
    
    Make questions progressively harder (easy to difficult).
    Avoid trick questions.
    Ensure all options are plausible but distinct.
    """
    return prompt


def flashcard_generator_prompt(subject: str, num_cards: int = 10) -> str:
    """Generate flashcards for a subject"""
    prompt = f"""
    Create {num_cards} flashcards for studying {subject}.
    
    Format for each card:
    FRONT (Question/Concept): [A clear, concise question or term]
    BACK (Answer): [The answer, explanation, or definition]
    
    Requirements:
    - Each flashcard should cover one concept
    - Front side should be short (one sentence max)
    - Back side should include definition and key details
    - Include mnemonics where helpful
    - Progress from basic to complex concepts
    """
    return prompt


def quiz_with_explanations(topic: str, difficulty: str = "medium") -> str:
    """Generate quiz with detailed explanations"""
    prompt = f"""
    Create a {difficulty}-difficulty quiz about {topic}.
    Include 3 questions.
    
    For each question:
    1. Question
    2. Multiple choice options (A, B, C, D)
    3. Correct answer
    4. Detailed explanation (2-3 sentences)
    5. Common mistakes to avoid
    6. Related concepts to study
    
    Difficulty levels:
    - easy: foundational concepts
    - medium: understanding and application
    - hard: analysis and synthesis
    """
    return prompt


def adaptive_quiz_prompt(current_level: str, correct_answers: int, 
                        incorrect_answers: int) -> str:
    """Generate adaptive quiz based on student performance"""
    accuracy = correct_answers / (correct_answers + incorrect_answers) if (correct_answers + incorrect_answers) > 0 else 0
    
    prompt = f"""
    Create the next quiz question for a student.
    
    Student Profile:
    - Current level: {current_level}
    - Accuracy: {accuracy:.1%}
    - Correct answers: {correct_answers}
    - Incorrect answers: {incorrect_answers}
    
    Based on performance:
    """
    
    if accuracy > 0.8:
        prompt += """
        - The student is doing well
        - Increase difficulty
        - Ask about more complex applications
        """
    elif accuracy < 0.5:
        prompt += """
        - The student is struggling
        - Reduce difficulty
        - Focus on fundamental concepts
        - Consider adding context/examples
        """
    else:
        prompt += """
        - The student is making progress
        - Maintain current difficulty
        - Mix review and new concepts
        """
    
    return prompt


def assessment_rubric_generator(skill: str, proficiency_levels: int = 4) -> str:
    """Generate a rubric for assessing student work"""
    prompt = f"""
    Create a {proficiency_levels}-level rubric for assessing {skill}.
    
    Include:
    1. Criteria (what to evaluate)
    2. Performance levels for each criterion
    3. Point values
    4. Examples of work at each level
    
    Format:
    
    SKILL: {skill}
    
    CRITERION 1: [Name of what to evaluate]
    Level 1: [Description of poor work] - X points
    Level 2: [Description of adequate work] - X points
    Level 3: [Description of good work] - X points
    Level 4: [Description of excellent work] - X points
    """
    return prompt


def study_guide_generator(topic: str, grade_level: str = "high school") -> str:
    """Generate a comprehensive study guide"""
    prompt = f"""
    Create a study guide for {topic} at the {grade_level} level.
    
    Include:
    1. Key Terms (with definitions)
    2. Main Concepts (2-3 paragraphs explaining core ideas)
    3. Important Facts (bulleted list)
    4. Common Misconceptions (what students get wrong)
    5. Practice Problems (with answers)
    6. Study Tips (how to prepare for an exam)
    7. Connections (how this relates to other topics)
    
    Keep language clear and age-appropriate.
    Include examples where helpful.
    """
    return prompt


def question_difficulty_classifier(question: str) -> str:
    """Classify question difficulty level"""
    prompt = f"""
    Classify the difficulty of this question: "{question}"
    
    Levels:
    1. Recall (remembering facts)
    2. Understanding (explaining concepts)
    3. Application (using knowledge)
    4. Analysis (breaking down and examining)
    5. Synthesis (combining ideas)
    6. Evaluation (making judgments)
    
    Provide:
    - Difficulty level number and name
    - Reasoning
    - What type of cognitive skill is required
    """
    return prompt


def quiz_format_examples():
    """Examples of different quiz formats"""
    examples = """
    QUIZ FORMAT EXAMPLES:
    
    1. MULTIPLE CHOICE
       Question: What is X?
       A) Option A
       B) Option B (correct)
       C) Option C
       D) Option D
    
    2. TRUE/FALSE
       Statement: X is true
       Answer: True/False
    
    3. SHORT ANSWER
       Question: Explain X
       Answer: [Space for student response]
    
    4. MATCHING
       Match concepts with definitions
    
    5. FILL IN THE BLANK
       X is a __________ 
       Answer: [term]
    
    6. ESSAY
       Question: Discuss X
       Evaluation: Based on rubric
    
    7. PROBLEM SOLVING
       Solve: [Math/logic problem]
       Answer: [Solution with work shown]
    """
    return examples


if __name__ == "__main__":
    print("=== Quiz Generator ===\n")
    print("1. Multiple Choice Quiz Prompt:")
    print(multiple_choice_quiz_prompt("Python Programming", 3))
    print("\n2. Flashcard Generator:")
    print(flashcard_generator_prompt("Biology", 5))
    print("\n3. Quiz with Explanations:")
    print(quiz_with_explanations("World History", "medium"))
    print("\n4. Adaptive Quiz:")
    print(adaptive_quiz_prompt("intermediate", 15, 5))
    print("\n5. Assessment Rubric:")
    print(assessment_rubric_generator("Essay Writing", 4))
    print("\n6. Study Guide Generator:")
    print(study_guide_generator("Photosynthesis", "high school"))
    print("\n7. Format Examples:")
    print(quiz_format_examples())
