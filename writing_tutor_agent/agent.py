# Writing Tutor Agent - Main Entry Point
# Educational AI Writing Tutor for Children

from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
import os

# Initialize LLM (Groq with tool-calling support)
llm = LiteLlm(
    model="groq/moonshotai/kimi-k2-instruct-0905",
    api_key=os.environ.get("GROQ_API_KEY")  
)



# Create the Writing Tutor Agent
root_agent = Agent(
    name="writing_tutor",
    model=llm,

    instruction="""You are an AI writing tutor. Be CONCISE.


RESPONSE FORMAT:
📝 Errors found:
1. [Type]: "wrong" → "correct" - Brief tip
2. [Type]: "wrong" → "correct" - Brief tip

✅ Corrected: [Full corrected sentence]

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
