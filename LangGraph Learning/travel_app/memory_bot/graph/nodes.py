from loguru import logger
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage
from langgraph.graph import MessagesState

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=""
    
)


def chatbot(state: MessagesState) -> MessagesState:
    logger.info("Invoking chatbot...")

    response: AIMessage = llm.invoke(state["messages"])

    logger.info("Chatbot response generated.")

    return {
        "messages": [response],
    }