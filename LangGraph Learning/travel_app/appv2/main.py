from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.messages import AIMessage
from pathlib import Path
from graph.builder import graph

# graph_visual = graph.get_graph()
# mermaid = graph_visual.draw_mermaid()

# # PNG bytes
# png = graph_visual.draw_mermaid_png()
# Path("graph.png").write_bytes(png)

result = graph.invoke(
    {
        "messages": [
            SystemMessage(
                content="""
                    You are a travel assistant.

                    Use the available tools whenever you need hotel or attraction information.

                    After receiving the tool results, produce the final answer.

                    Do NOT call the same tool again unless the user explicitly asks for new information.

                    If all required information is available, respond to the user and do not make additional tool calls.
                    """
           
            ),
            HumanMessage(
                content="Find hotels in Japan"
            )
        ]
    }
)



for index, message in enumerate(result["messages"]):
    if isinstance(message, AIMessage):
        print(f"\nAI Message {index}")
        print("Content:", message.content)
        print("Tool Calls:", message.tool_calls)