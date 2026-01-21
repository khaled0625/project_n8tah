# Memory Layer - SuperMemory Integration
# Persistent student memory for tracking learning progress

import os
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from supermemory import Supermemory

# Load environment variables from .env
load_dotenv()

# Initialize SuperMemory client (uses SUPERMEMORY_API_KEY from environment)
client = Supermemory()


def add_student_memory(
    student_id: str,
    mistake_type: str,
    details: str,
    sentence: str,
) -> dict:
    """
    Store a student's mistake in memory for future reference.
    
    Args:
        student_id: Unique identifier for the student
        mistake_type: Type of error (spelling, grammar, punctuation, etc.)
        details: Description of the mistake (e.g., "pley -> play")
        sentence: The original sentence containing the error
    
    Returns:
        SuperMemory response with document ID
    """
    content = f"""
Student Mistake Record:
- Type: {mistake_type}
- Error: {details}
- Original Sentence: "{sentence}"
- Recorded: {datetime.now().isoformat()}

This helps track the student's learning patterns and recurring errors.
"""
    
    response = client.memories.add(
        content=content,
        container_tag=f"student-{student_id}",
        metadata={
            "type": mistake_type,
            "student_id": student_id,
            "timestamp": datetime.now().isoformat(),
        }
    )
    
    return {"success": True, "id": response.id if hasattr(response, 'id') else str(response)}


def search_student_history(
    student_id: str,
    query: str,
    limit: int = 5,
) -> list:
    """
    Search for relevant past mistakes in a student's history.
    
    Args:
        student_id: The student ID to search within
        query: What to search for (e.g., "spelling errors", "capitalization")
        limit: Maximum number of results to return
    
    Returns:
        List of relevant memories
    """
    response = client.search.memories(
        q=query,
        container_tag=f"student-{student_id}",
        limit=limit,
    )
    
    results = []
    if hasattr(response, 'results'):
        for item in response.results:
            results.append({
                "content": item.content if hasattr(item, 'content') else str(item),
                "score": item.score if hasattr(item, 'score') else None,
            })
    
    return results


def get_student_profile(student_id: str) -> dict:
    """
    Get an auto-generated profile showing the student's learning patterns.
    
    This uses SuperMemory's profile feature to analyze patterns across
    all stored memories for this student.
    
    Args:
        student_id: The student ID to get profile for
    
    Returns:
        Profile summary with common mistake patterns
    """
    try:
        response = client.profile(
            container_tag=f"student-{student_id}",
            q="What are this student's most common writing errors and areas for improvement?"
        )
        
        return {
            "student_id": student_id,
            "profile": response.profile if hasattr(response, 'profile') else str(response),
        }
    except Exception as e:
        return {
            "student_id": student_id,
            "profile": None,
            "error": str(e),
        }
