from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash" 
)

@tool
def ai_agent_tool(user_input: str) -> str:
    """AI Agent Tool using Google Gemini model to respond to user input."""
    messages = [
        SystemMessage(content="You are a helpful AI assistant."),
        HumanMessage(content=user_input)
    ]
    response = model(messages)
    return response.content


model_agent = model.bind_tools([ai_agent_tool]) 