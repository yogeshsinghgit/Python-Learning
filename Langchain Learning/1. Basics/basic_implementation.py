import os
from langchain.llms import OpenAI

os.environ['OPEN_API_KEY'] = "your_openai_api_key"

# Initliaize the LLM
llm = OpenAI(model_name='gpt-3.5-turbo', temperature=0.7)

# model_name="gpt-3.5-turbo" → Specifies the model version.
# temperature=0.7 → Controls creativity (lower = deterministic, higher = creative).

# Generate text
reponse = llm("what are the benifits of using langchain?")
print(reponse)