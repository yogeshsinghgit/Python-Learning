# **📌 Summary of LLM Chains & Related Concepts in LangChain**  

This document consolidates all discussions on **LLM Chains, Pipe (`|`) Operator, Prompt Templates, and Token Cost Calculation** in LangChain.  

---

## **🔹 What are LLM Chains?**  
An **LLM Chain (`LLMChain`)** is a structured way to process inputs and outputs in LangChain. Instead of calling an LLM directly, LLMChains allow:  
✅ **Modularity** – Break down workflows into reusable components.  
✅ **Prompt Management** – Use **Prompt Templates** dynamically.  
✅ **Multi-Step Pipelines** – Chain multiple calls together.  
✅ **Memory Support** – Retain chat history across interactions.  

### **🔹 Why Not Call `llm(prompt)` Directly?**  
Although we can directly call an LLM like this:  
```python
llm("Explain Quantum Computing in simple terms.")
```
Using **LLMChains** provides **better structure, reusability, and debugging** for complex workflows.  

---

## **🔹 Pipe (`|`) Operator vs. LLMChain**  
LangChain **Expression Language (LCEL)** allows chaining operations using the `|` **pipe operator**, which is an alternative to `LLMChain`.

### ✅ **Advantages of Pipe (`|`) Operator**  
- **More Pythonic & Concise**  
- **Readable & Functional Approach**  
- **No Need to Manually Define Chains**  

### **🔹 Example: Using LLMChain**
```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4")

# Define a prompt template
prompt = PromptTemplate.from_template("Summarize {topic} in 3 bullet points.")

# Create an LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

# Invoke the chain
response = chain.invoke({"topic": "Quantum Computing"})
print(response)
```

### **🔹 Example: Using Pipe (`|`) Operator**
```python
chain = prompt | llm
response = chain.invoke({"topic": "Quantum Computing"})
print(response)
```
✅ **Same functionality, but cleaner syntax with the pipe operator!**  

---

## **🔹 Generating Structured Output (Pydantic Schema)**
LangChain can **enforce structured output** using a **Pydantic schema**, ensuring responses follow a specific format.

### **🔹 Example: Enforcing Structured Output**
```python
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

class SummarySchema(BaseModel):
    bullet_points: list[str]

llm = ChatOpenAI(model_name="gpt-4")

prompt = PromptTemplate.from_template("Summarize {topic} in 3 bullet points.")
structured_llm = llm.with_structured_output(SummarySchema)

# Using the pipe operator
chain = prompt | structured_llm
response = chain.invoke({"topic": "Artificial Intelligence"})

print(response)
```
🔹 **Ensures output follows the `SummarySchema` format**  
🔹 **Useful for JSON APIs, structured reports, or validation**  

---

## **🔹 Tracking Token Usage & Estimating Cost**
Since **LLM calls consume tokens**, we should track **input/output tokens** and estimate the cost.

### **🔹 `calculate_usage` Implementation**
```python
def calculate_usage(llm, raw_output):
    """
    Calculate the approximate cost of generating an LLM response.

    Args:
        llm: The LLM instance (must have model_name).
        raw_output: The response from the LLM (must include token usage).

    Returns:
        Dictionary containing input tokens, output tokens, total tokens, and cost in USD.
    """

    # Extract token usage details (if available)
    token_usage = raw_output.get("token_usage", {}) if isinstance(raw_output, dict) else {}

    input_tokens = token_usage.get("input_tokens", 0)
    output_tokens = token_usage.get("output_tokens", 0)
    total_tokens = input_tokens + output_tokens

    # Define pricing per 1,000 tokens (Update based on your LLM provider)
    pricing_per_1k = {
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    }

    # Get model pricing (default to GPT-4-turbo if unknown)
    model_name = getattr(llm, "model_name", "gpt-4-turbo").lower()
    pricing = pricing_per_1k.get(model_name, pricing_per_1k["gpt-4-turbo"])

    # Calculate cost
    cost = (input_tokens / 1000) * pricing["input"] + (output_tokens / 1000) * pricing["output"]

    return {
        "model": model_name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost_usd": round(cost, 6),
    }
```

### **🔹 Example Usage**
```python
raw_output = {
    "parsed": {"response": "This is an AI-generated response."},
    "token_usage": {
        "input_tokens": 50,
        "output_tokens": 150
    }
}

llm = ChatOpenAI(model_name="gpt-4")
usage_stats = calculate_usage(llm, raw_output)

print(usage_stats)
```

### **🔹 Example Output**
```json
{
    "model": "gpt-4",
    "input_tokens": 50,
    "output_tokens": 150,
    "total_tokens": 200,
    "cost_usd": 0.009
}
```
💡 **Cost Breakdown:**  
- **Input (50 tokens):** `(50 / 1000) * $0.03 = $0.0015`  
- **Output (150 tokens):** `(150 / 1000) * $0.06 = $0.009`  
- **Total Cost:** `$0.009`  

---

## **🔹 Putting It All Together: Full Example**
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel

# Define Pydantic schema
class SummarySchema(BaseModel):
    bullet_points: list[str]

# Function to generate structured output and track cost
async def generate_structured_output(llm, prompt_template, inputs, schema):
    prompt = PromptTemplate(
        template=prompt_template, input_variables=list(inputs.keys())
    )

    structured_llm = llm.with_structured_output(schema, include_raw=True)
    chain = prompt | structured_llm
    raw_output = chain.invoke(inputs)
    
    output = raw_output.get("parsed") if isinstance(raw_output, dict) else raw_output
    usage = calculate_usage(llm=llm, raw_output=raw_output)

    return output, usage

# Define LLM and inputs
llm = ChatOpenAI(model_name="gpt-4")
prompt_template = "Summarize {topic} in 3 bullet points."
inputs = {"topic": "Artificial Intelligence"}

# Call the function
structured_output, usage = await generate_structured_output(llm, prompt_template, inputs, SummarySchema)

print(structured_output)
print(usage)
```
---

## **📌 Key Takeaways**
✅ **LLMChain & Pipe (`|`) Operator** – Both enable structured LLM interactions.  
✅ **Prompt Templates** – Allow dynamic input injection.  
✅ **Structured Output (Pydantic)** – Ensures valid, structured responses.  
✅ **Token Usage Tracking** – Helps estimate API costs in real-time.  
✅ **End-to-End Workflow** – Combine everything into a **scalable, modular system**.  
