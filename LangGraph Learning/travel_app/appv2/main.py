from langchain_core.messages import HumanMessage
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
            HumanMessage(
                content="Find hotels in Japan"
            )
        ]
    }
)

print(result["messages"][-1].content)