Your Markdown is mostly correct conceptually, but **LangChain v0.2+ / v0.3 introduced some changes**:

Key updates needed:

1. Use **`langchain_core.prompts`** instead of `langchain.prompts`
2. **`OpenAI` completion model example is outdated**
3. Use **chat models + `.invoke()`**
4. `ChatPromptTemplate.format()` should be **`format_messages()`**
5. Prefer **LCEL (`prompt | llm`) pipelines**
6. Update dependency installs

Below is a **cleaned and modernized version of your MD file** that aligns with **current LangChain best practices**.

---

# Fixed & Updated Markdown (Modern LangChain)

````md
## Prompt Templates in LangChain

### 1. What is a Prompt Template?

A **PromptTemplate** helps structure the input for an LLM by defining placeholders for dynamic values.  
This ensures the prompt format remains consistent and reusable.

Prompt templates are commonly used for:

- Summarization
- Extraction
- Classification
- RAG pipelines

---

# 2. Installing Dependencies

Install LangChain:

```bash
pip install langchain langchain-core
````

If using Groq models:

```bash
pip install langchain-groq
```

---

# 3. Creating a Basic Prompt Template

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Explain {topic} in simple terms."
)

formatted_prompt = template.format(topic="Artificial Intelligence")

print(formatted_prompt)
```

### Output

```
Explain Artificial Intelligence in simple terms.
```

---

# 4. Using Multiple Variables

Prompt templates can contain multiple variables.

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Explain {topic} to a {audience}."
)

formatted_prompt = template.format(
    topic="Quantum Computing",
    audience="5-year-old"
)

print(formatted_prompt)
```

### Output

```
Explain Quantum Computing to a 5-year-old.
```

---

# 5. Using Prompt Templates with an LLM

Modern LangChain uses **Chat Models + invoke()**.

Example using **Groq**.

```python
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key="YOUR_API_KEY"
)

prompt = PromptTemplate.from_template(
    "Explain {topic} to a {audience}."
)

formatted_prompt = prompt.format(
    topic="Blockchain",
    audience="beginner"
)

response = llm.invoke(formatted_prompt)

print(response.content)
```

---

# 6. Few-Shot Prompting with Examples

Few-shot prompting provides examples to guide the model's response.

```python
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

examples = [
    {"question": "What is Python?", "answer": "Python is a programming language."},
    {"question": "What is an API?", "answer": "An API allows communication between applications."}
]

example_prompt = PromptTemplate.from_template(
    "Q: {question}\nA: {answer}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Here are some Q&A examples:\n",
    suffix="Q: {question}\nA:",
    input_variables=["question"]
)

formatted_prompt = few_shot_prompt.format(
    question="What is Machine Learning?"
)

print(formatted_prompt)
```

### Output

```
Here are some Q&A examples:

Q: What is Python?
A: Python is a programming language.

Q: What is an API?
A: An API allows communication between applications.

Q: What is Machine Learning?
A:
```

The LLM will generate the final answer.

---

# 7. Using ChatPromptTemplate (For Chat Models)

Chat models expect **messages instead of a single prompt string**.

LangChain provides **ChatPromptTemplate** for this.

```python
from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant that answers questions concisely."),
    ("human", "{question}")
])

messages = chat_prompt.format_messages(
    question="What is LangChain?"
)

print(messages)
```

### Output

```
[
 SystemMessage(content='You are an AI assistant that answers questions concisely.'),
 HumanMessage(content='What is LangChain?')
]
```

These message objects are sent to the LLM.

---

# 8. Using ChatPromptTemplate with an LLM

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key="YOUR_API_KEY"
)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI teacher."),
    ("human", "Explain {topic} to a {audience}")
])

messages = chat_prompt.format_messages(
    topic="Neural Networks",
    audience="beginner"
)

response = llm.invoke(messages)

print(response.content)
```

---

# 9. Dynamic Prompt Generation

You can generate prompts dynamically using Python functions.

```python
from langchain_core.prompts import PromptTemplate

def generate_prompt(topic: str, audience: str):

    template = PromptTemplate.from_template(
        "Explain {topic} to a {audience}."
    )

    return template.format(
        topic=topic,
        audience=audience
    )


print(generate_prompt("Neural Networks", "high school student"))
```

### Output

```
Explain Neural Networks to a high school student.
```

---

# Summary

| Component             | Purpose                            |
| --------------------- | ---------------------------------- |
| PromptTemplate        | Create reusable prompt structures  |
| FewShotPromptTemplate | Provide examples to guide LLM      |
| ChatPromptTemplate    | Structure prompts for chat models  |
| format()              | Convert template → string          |
| format_messages()     | Convert template → message objects |

Prompt templates are a **core building block** for:

* RAG systems
* AI agents
* extraction pipelines
* chatbots

```

