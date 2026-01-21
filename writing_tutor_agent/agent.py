# Writing Tutor Agent - Main Entry Point
# Educational AI Writing Tutor for Children

from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
import os

# Import memory tools
from .tools import MEMORY_TOOLS

# Initialize LLM (Groq with tool-calling support)
llm = LiteLlm(
    model="groq/moonshotai/kimi-k2-instruct-0905",
    api_key=os.environ.get("GROQ_API_KEY")  
)


# Create the Writing Tutor Agent
root_agent = Agent(
    name="writing_tutor",
    model=llm,
    tools=MEMORY_TOOLS,
    instruction="""You are an AI writing tutor for children. Be CONCISE and encouraging.

WORKFLOW:
1. Check for past mistakes using get_past_mistakes(student_id, error_type)
2. Analyze the sentence and identify errors
3. Save new mistakes using save_mistake(student_id, mistake_type, details, sentence)
4. Provide corrected sentence and child-friendly tips

Use student_id="default-student" if not specified.

RESPONSE FORMAT:
📝 Errors found:
1. [Type]: "wrong" → "correct" - Brief tip
2. [Type]: "wrong" → "correct" - Brief tip

✅ Corrected: [Full corrected sentence]

💡 [Personalized tip if student has recurring errors]
"""
)

# For ADK CLI/Web
if __name__ == "__main__":
    from google.adk import Runner
    
    runner = Runner(agent=root_agent)
    
    # Test query
    user_input = "Check this sentence: I pley football"
    print(f"User: {user_input}")
    
    for event in runner.run(user_input):
        if hasattr(event, 'text') and event.text:
            print(f"Tutor: {event.text}")
