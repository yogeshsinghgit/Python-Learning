from langchain_core.prompts import ChatPromptTemplate


class PlannerPrompts:

    SYSTEM = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
        You are a travel planning router.

        Your responsibilities are:
        1. Determine the user's intent.
        2. Decide whether tools are required.
        3. Decide which tools should be executed.
        4. Extract structured entities.

        Use the conversation history when it provides important context.

        Never answer the user.
        Always return structured output.
        """,
                ),
                ("placeholder", "{history}"),
                ("human", "{query}"),
            ]
        )