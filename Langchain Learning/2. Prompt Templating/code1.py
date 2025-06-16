from langchain.prompts import PromptTemplate

# Define a prompt template with placeholder
template = PromptTemplate(
    input_variables = ["topic"],
    template="Explain {topic} in simple terms."
    )

# Format the template with actual values
formatted_prompt = template.format(topic = "Python Programming Language")
print(formatted_prompt)