# import os
# from langchain.llms import OpenAI

# os.environ['OPEN_API_KEY'] = "your_openai_api_key"

# # Initliaize the LLM
# llm = OpenAI(model_name='gpt-3.5-turbo', temperature=0.7)

# # model_name="gpt-3.5-turbo" → Specifies the model version.
# # temperature=0.7 → Controls creativity (lower = deterministic, higher = creative).

# # Generate text
# reponse = llm("what are the benifits of using langchain?")
# print(reponse)


from langchain_groq import ChatGroq
from loguru import logger

# for api key visit https://console.groq.com/api-keys

def basic_llm_call():

    try:
        logger.info("Initializing Groq LLM")
        # from groq import Groq
        # client = Groq(api_key="YOUR_KEY")
        # print(client.models.list())

        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key="",
            temperature=0.7
        )

        logger.info("Sending prompt to LLM")

        response = llm.invoke("What are the benefits of using LangChain?")

        logger.success(f"LLM Response: {response.content}")

    except Exception as e:
        logger.error(f"Error during LLM call: {e}")
        raise


if __name__ == "__main__":
    basic_llm_call()
