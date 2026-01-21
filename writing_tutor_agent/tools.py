# ADK Function Tools - Memory Integration
# Wrappers for SuperMemory functions to use with Google ADK

from typing import Optional
from .memory import add_student_memory, search_student_history, get_student_profile


def save_mistake(
    student_id: str,
    mistake_type: str,
    details: str,
    sentence: str,
) -> str:
    """
    Save a student's writing mistake to memory for future reference.
    Use this after identifying errors to track the student's learning progress.
    
    Args:
        student_id: The student's unique identifier
        mistake_type: Type of error (spelling, grammar, punctuation, capitalization)
        details: Description of the mistake (e.g., "pley -> play")  
        sentence: The original sentence containing the error
    
    Returns:
        Confirmation message
    """
    try:
        result = add_student_memory(student_id, mistake_type, details, sentence)
        return f"✅ Saved {mistake_type} mistake for student {student_id}"
    except Exception as e:
        return f"❌ Could not save mistake: {str(e)}"


def get_past_mistakes(
    student_id: str,
    error_type: str = "writing errors",
) -> str:
    """
    Retrieve a student's past similar mistakes from memory.
    Use this to check if the student has made similar errors before.
    
    Args:
        student_id: The student's unique identifier
        error_type: What type of errors to search for (e.g., "spelling", "grammar")
    
    Returns:
        Summary of past similar mistakes or "No history found"
    """
    try:
        results = search_student_history(student_id, error_type, limit=3)
        
        if not results:
            return f"No previous {error_type} found for this student."
        
        output = f"📚 Found {len(results)} similar past mistakes:\n"
        for i, item in enumerate(results, 1):
            content = item.get("content", "")[:200]  # Truncate long content
            output += f"{i}. {content}...\n"
        
        return output
    except Exception as e:
        return f"Could not retrieve history: {str(e)}"


def get_learning_profile(student_id: str) -> str:
    """
    Get an AI-generated summary of the student's learning patterns.
    Use this to understand the student's strengths and areas for improvement.
    
    Args:
        student_id: The student's unique identifier
    
    Returns:
        Profile summary showing common mistake patterns
    """
    try:
        result = get_student_profile(student_id)
        
        if result.get("error"):
            return f"Could not generate profile: {result['error']}"
        
        profile = result.get("profile", "No profile data available yet.")
        return f"📊 Student Profile for {student_id}:\n{profile}"
    except Exception as e:
        return f"Could not generate profile: {str(e)}"


# Export tools as a list for easy agent integration
MEMORY_TOOLS = [
    save_mistake,
    get_past_mistakes,
    get_learning_profile,
]
