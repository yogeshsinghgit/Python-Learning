from loguru import logger
from langchain_core.messages import HumanMessage

from graph.builder import graph

config = {
    "configurable": {
        "thread_id": "chat-1",
    }
}

logger.info("Memory Chatbot Started")
logger.info("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        logger.info("Goodbye!")
        break

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_input),
            ]
        },
        config=config,
    )

    ai_message = result["messages"][-1]

    print(f"\nAI: {ai_message.content}\n")