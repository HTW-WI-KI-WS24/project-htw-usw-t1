from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.schema import SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = OpenAI(streaming=True)
chat_model = ChatOpenAI()

def improve_prompt(human_message):
    messages = [SystemMessage(
        content=f"Please reformulate the user's prompt '{human_message}' by creating a detailed and comprehensive "
                f"query. Begin by expanding the core idea of the prompt into a more personalized and specific "
                f"request. Then, enrich the reformulated prompt by adding hypothetical examples relevant to the "
                f"topic. These examples should illustrate various scenarios, preferences, or challenges related to "
                f"the user's query. This approach should help in providing a context-rich, relatable, and specific "
                f"prompt, aiming to guide a response that comprehensively addresses the user's needs without "
                f"requiring further clarification on key aspects of their request."
                f" Please focus solely on enhancing and expanding the prompt itself. Do not provide a response or "
                f"answer to the reformulated prompt. Just return the newly crafted, detailed prompt based on the "
                f"instructions provided."
    )]
    improved_prompt = llm.invoke(messages)
    return improved_prompt

def shorten_prompt(human_message):
    messages = [SystemMessage(
        content=f"Please shorten the user's prompt '{human_message}' to a maximum of 50 words. The shortened prompt "
                f"should be a concise and clear request that is easy to understand and respond to. Please focus "
                f"solely on shortening the prompt itself. Do not provide a response or answer to the shortened "
                f"prompt. Just return the newly crafted, short prompt based on the instructions provided."
    )]
    shortened_prompt = llm.invoke(messages)
    return shortened_prompt

def get_response(prompt):
    response = llm.invoke(prompt)
    return response
