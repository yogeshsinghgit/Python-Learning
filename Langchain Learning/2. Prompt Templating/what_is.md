## **Prompt Templates in LangChain**

### **1. What is a Prompt Template?**
A **PromptTemplate** helps structure the input for an LLM by defining placeholders for dynamic values. This ensures that the input format remains consistent, making interactions more predictable and reliable.

---

### **2. Installing Dependencies**
If you haven't already, install LangChain:
```bash
pip install langchain
```

---

### **3. Creating a Basic Prompt Template**
```python
from langchain.prompts import PromptTemplate

# Define a prompt template with placeholders
template = PromptTemplate(
    input_variables=["topic"], 
    template="Explain {topic} in simple terms."
)

# Format the template with actual values
formatted_prompt = template.format(topic="Artificial Intelligence")
print(formatted_prompt)
```
**🔹 Output:**
```
Explain Artificial Intelligence in simple terms.
```

---

### **4. Using Multiple Variables**
You can use multiple placeholders in the template:
```python
template = PromptTemplate(
    input_variables=["topic", "audience"], 
    template="Explain {topic} to a {audience}."
)

formatted_prompt = template.format(topic="Quantum Computing", audience="5-year-old")
print(formatted_prompt)
```
**🔹 Output:**
```
Explain Quantum Computing to a 5-year-old.
```

---

### **5. Using Prompt Templates with an LLM**
Now, let's use our prompt template with OpenAI's GPT model:
```python
from langchain.llms import OpenAI

# Initialize LLM
llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

# Generate response using formatted prompt
response = llm(template.format(topic="Blockchain", audience="beginner"))
print(response)
```

---

### **6. Few-Shot Prompting with Examples**
Few-shot prompting provides the model with examples to improve its responses:
```python
from langchain.prompts import FewShotPromptTemplate

# Example prompts and responses
examples = [
    {"question": "What is Python?", "answer": "Python is a programming language."},
    {"question": "What is an API?", "answer": "An API is a set of rules for communication between applications."}
]

# Template for formatting examples
example_template = PromptTemplate(
    input_variables=["question", "answer"],
    template="Q: {question}\nA: {answer}"
)

# Define the few-shot prompt
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="Here are some Q&A examples:\n",
    suffix="Q: {question}\nA:",
    input_variables=["question"]
)

# Generate a new prompt
formatted_prompt = few_shot_prompt.format(question="What is Machine Learning?")
print(formatted_prompt)
```
**🔹 Output:**
```
Here are some Q&A examples:
Q: What is Python?
A: Python is a programming language.

Q: What is an API?
A: An API is a set of rules for communication between applications.

Q: What is Machine Learning?
A:
```
(The LLM will now generate an appropriate answer.)

---

### **7. Using ChatPromptTemplate (For Chat Models)**
If you're using models like GPT-4, `ChatPromptTemplate` helps structure chat-based prompts.

```python
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# Define a system message (guides the model)
system_message = SystemMessagePromptTemplate.from_template(
    "You are an AI assistant that answers questions in a concise manner."
)

# Define a user message (actual input from user)
user_message = HumanMessagePromptTemplate.from_template("{question}")

# Create a chat prompt
chat_prompt = ChatPromptTemplate.from_messages([system_message, user_message])

# Format the chat prompt
formatted_chat_prompt = chat_prompt.format(question="What is LangChain?")
print(formatted_chat_prompt)
```

---

### **8. Dynamic Prompting with Functions**
You can dynamically generate prompts using Python functions.

```python
def generate_prompt(topic: str, audience: str):
    template = PromptTemplate(
        input_variables=["topic", "audience"],
        template="Explain {topic} to a {audience}."
    )
    return template.format(topic=topic, audience=audience)

print(generate_prompt("Neural Networks", "high school student"))
```
**🔹 Output:**
```
Explain Neural Networks to a high school student.
```
