from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from typing import List, Tuple

llm = OpenAI(streaming=True)
chat_model = ChatOpenAI()

def improve_prompt(human_message):
    messages = [SystemMessage(
        content=f"Please refine the user's prompt, '{human_message}', by crafting a more detailed and specific query. "
                f"Expand on the core concept, adding personalized elements and hypothetical scenarios relevant to the "
                f"topic. These examples should cover various scenarios, preferences, or challenges pertinent to the "
                f"query. The aim is to create a context-rich and specific prompt, which thoroughly addresses the "
                f"user's needs without needing further clarification. Focus on enhancing the prompt itself without "
                f"providing a response to it. Return the enhanced, detailed prompt based on these guidelines."
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

# Define a class to manage reference examples
class ReferenceExamples:
    def __init__(self):
        self.good_examples = []
        self.bad_examples = []

    def add_example(self, example: str, quality: str):
        if quality == 'good':
            self.good_examples.append(example)
        elif quality == 'bad':
            self.bad_examples.append(example)
        else:
            raise ValueError("Quality must be 'good' or 'bad'.")

    def get_examples(self) -> Tuple[List[str], List[str]]:
        return self.good_examples, self.bad_examples

# Initialize the reference examples manager
ref_examples_manager = ReferenceExamples()

# Function to add a new reference example
def add_reference_example(example: str, quality: str):
    ref_examples_manager.add_example(example, quality)

# Function to retrieve reference examples
def get_reference_examples() -> Tuple[List[str], List[str]]:
    return ref_examples_manager.get_examples()

