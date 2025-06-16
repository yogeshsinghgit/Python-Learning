# Using Multiple Variables..

from langchain.prompts import PromptTemplate

template = PromptTemplate(
    input_variables = ['topic', 'audience'],
    template= "Explain {topic} to a {audience}"
    )

formatted_prompt = template.format(topic="Quantum Computing", audience="5-year-old")
print(formatted_prompt)

# Now we can use this formatted prompt with our LLM Model