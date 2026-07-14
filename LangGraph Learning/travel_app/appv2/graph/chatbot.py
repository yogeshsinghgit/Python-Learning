from langchain_groq import ChatGroq

from tools.travel_tools import (
    search_attractions,
    search_hotels,
)

GROQ_API_KEY = ""
llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            api_key=GROQ_API_KEY
        )


llm_with_tools = llm.bind_tools(
    [
        search_hotels,
        search_attractions,
    ]
)
