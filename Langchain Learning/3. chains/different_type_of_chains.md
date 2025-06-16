# **🔹 LangChain Chains Explained: LLMChain, SequentialChain, RouterChain**  

LangChain provides different **chain types** to handle various use cases. Below is a detailed breakdown of the three most commonly used chains:

---

## **1️⃣ LLMChain: Simple Chain with LLM & Prompt Templates**
💡 **Basic single-step chain** that consists of:  
✅ **Prompt Template** → Injects dynamic inputs  
✅ **LLM Call** → Generates a response  

🔹 **When to Use?**  
- Simple **input → output** scenarios  
- Summarization, answering questions, single-step tasks  

### **🔹 Example: Using `LLMChain`**
```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-4")

# Create a prompt template
prompt = PromptTemplate.from_template("What are the top 3 key points about {topic}?")

# Create a simple LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

# Invoke the chain
response = chain.invoke({"topic": "Quantum Computing"})
print(response)
```
✅ **A single input (`topic`) generates structured output!**  

---

## **2️⃣ SequentialChain: Multi-Step Processing**
💡 **Handles multiple dependent steps** where output from one step **feeds into** the next.  

🔹 **When to Use?**  
- When an intermediate step is needed (e.g., extracting keywords before answering)  
- Multi-step reasoning or complex workflows  
- Chatbots requiring context retention  

### **🔹 Example: Using `SequentialChain`**
```python
from langchain.chains import SequentialChain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4")

# Step 1: Extract keywords from a topic
keyword_prompt = PromptTemplate.from_template("Extract three key concepts from {topic}.")
keyword_chain = LLMChain(llm=llm, prompt=keyword_prompt, output_key="keywords")

# Step 2: Generate a summary based on extracted keywords
summary_prompt = PromptTemplate.from_template(
    "Based on these keywords: {keywords}, summarize {topic}."
)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt, output_key="summary")

# Create a SequentialChain
chain = SequentialChain(
    chains=[keyword_chain, summary_chain], 
    input_variables=["topic"],
    output_variables=["summary"]
)

# Invoke the chain
response = chain.invoke({"topic": "Artificial Intelligence"})
print(response["summary"])
```
✅ **Automatically extracts keywords, then summarizes them!**  

---

### **🔹 What Does `output_key="keywords"` Mean in LangChain?**  

In LangChain, the `output_key` argument is used to **name the output of an LLMChain**, which is useful when working with **SequentialChain** (or other multi-step chains).  

---

### **💡 Why Use `output_key`?**
1. **Stores the output under a named key** (useful for passing outputs between chains).  
2. **Ensures clarity** when multiple chains are used together.  
3. **Prevents overwriting** when chaining multiple LLM calls.  

---

### **🔹 Example Explanation**
```python
# Step 1: Extract keywords from a topic
keyword_prompt = PromptTemplate.from_template("Extract three key concepts from {topic}.")
keyword_chain = LLMChain(llm=llm, prompt=keyword_prompt, output_key="keywords")
```
Here’s what happens:  
- The **prompt** asks the LLM to extract **three key concepts** from `{topic}`.  
- The output of this chain is **stored under the key `"keywords"`** instead of the default `"text"`.  
- This output is then **passed into the next chain** inside a `SequentialChain`.  

---

### **🔹 How `output_key` Works in `SequentialChain`**
```python
# Step 2: Generate a summary based on extracted keywords
summary_prompt = PromptTemplate.from_template(
    "Based on these keywords: {keywords}, summarize {topic}."
)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt, output_key="summary")

# Create a SequentialChain
chain = SequentialChain(
    chains=[keyword_chain, summary_chain], 
    input_variables=["topic"],  # Initial input to the first chain
    output_variables=["summary"]  # Final output key
)

# Invoke the chain
response = chain.invoke({"topic": "Artificial Intelligence"})
print(response["summary"])  # Access the final summary
```

### **🛠 How Data Flows**
1. **Step 1 (`keyword_chain`)**  
   - Input: `{"topic": "Artificial Intelligence"}`
   - Output: `{"keywords": "Machine Learning, Deep Learning, Neural Networks"}`  

2. **Step 2 (`summary_chain`)**  
   - Input: `{"keywords": "Machine Learning, Deep Learning, Neural Networks", "topic": "Artificial Intelligence"}`
   - Output: `{"summary": "AI is powered by Machine Learning, Deep Learning, and Neural Networks, which enable computers to learn and adapt."}`  

---

### **📝 Summary**
✅ `output_key="keywords"` → Stores extracted keywords under `"keywords"` key.  
✅ Useful in **SequentialChain** to **pass structured data** between steps.  
✅ Helps prevent overwriting when **multiple LLM calls** are chained together.  



## **3️⃣ RouterChain: Conditional Execution Based on Input**
💡 **Dynamically selects the best chain** based on the input type or category.  

🔹 **When to Use?**  
- When multiple processing strategies exist  
- If different prompts are needed for different topics  
- Routing questions to domain-specific experts  

### **🔹 Example: Using `RouterChain`**
```python
from langchain.chains import RouterChain, LLMChain
from langchain.chains.router import MultiPromptChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4")

# Define different prompt templates
science_prompt = PromptTemplate.from_template("Explain the science behind {topic}.")
history_prompt = PromptTemplate.from_template("Give a historical background of {topic}.")
generic_prompt = PromptTemplate.from_template("Provide general information about {topic}.")

# Create separate LLMChains
science_chain = LLMChain(llm=llm, prompt=science_prompt)
history_chain = LLMChain(llm=llm, prompt=history_prompt)
generic_chain = LLMChain(llm=llm, prompt=generic_prompt)

# Define router rules
router = RouterChain(
    prompt_chains={
        "science": science_chain,
        "history": history_chain,
        "general": generic_chain
    },
    default_chain=generic_chain  # Fallback if no rule matches
)

# Invoke the router with an input
response = router.invoke({"topic": "Relativity", "category": "science"})
print(response)
```
✅ **Dynamically chooses the best chain based on input category!**  

---

# **📌 Key Differences**
| Chain Type       | Use Case | Key Feature |
|-----------------|----------|-------------|
| **LLMChain** | Simple input → output task | Single prompt & LLM call |
| **SequentialChain** | Multi-step workflows | One step's output feeds into another |
| **RouterChain** | Choosing the best approach | Dynamic routing based on input |

---

## **🚀 Final Thoughts**
✅ **LLMChain** → Best for **simple single-step** tasks  
✅ **SequentialChain** → Best for **multi-step workflows**  
✅ **RouterChain** → Best for **conditional execution**  
