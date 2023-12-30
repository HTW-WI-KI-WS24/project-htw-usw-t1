from typing import Literal
from dataclasses import dataclass
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory
from langchain_core.messages import SystemMessage, HumanMessage

import langchain_helper as lch
import streamlit as st

st.set_page_config(layout="wide")


@dataclass
class Message:
    origin: Literal["USER", "AI"]
    message: str


def load_css():
    with open("static/styles.css") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)


def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "improved_history" not in st.session_state:
        st.session_state["improved_history"] = []
    if "gpt_history" not in st.session_state:
        llm = OpenAI()
        st.session_state["gpt_history"] = ConversationChain(
            llm=llm,
            memory=ConversationSummaryMemory(llm=llm)
        )


def generate_response():
    # Der ursprüngliche Benutzer-Prompt wird geholt.
    human_prompt = st.session_state["human_prompt"]

    # Der verbesserte Prompt wird basierend auf dem ursprünglichen Benutzer-Prompt erstellt.
    improved_prompt = improve_prompt(human_prompt)
    improved_prompt = improved_prompt.replace("Reformulated prompt:", "").strip()
    improved_prompt = improved_prompt.replace("Reformulated Prompt:", "").strip()

    # Benutzerpräferenzen werden geholt.
    preferences = st.session_state.get("preferences", {})

    # Der verbesserte Prompt wird basierend auf den Benutzerpräferenzen modifiziert.
    modified_prompt = modify_prompt_based_on_preferences(improved_prompt, preferences)

    # Eine Antwort wird basierend auf dem modifizierten Prompt generiert.
    gpt_improved_response = st.session_state["gpt_history"].run(modified_prompt)

    gpt_response = st.session_state["gpt_history"].run(human_prompt)

    # Die Nachrichten werden zu den Chat-Historien hinzugefügt.
    st.session_state["chat_history"].append(Message("USER", human_prompt))
    st.session_state["chat_history"].append(Message("AI", gpt_response))
    st.session_state["improved_history"].append(Message("USER", modified_prompt))
    st.session_state["improved_history"].append(Message("AI", gpt_improved_response))


def modify_prompt_based_on_preferences(prompt, preferences):
    # Example logic to modify prompt based on preferences
    # This needs to be tailored based on how the language model interprets these instructions

    if preferences:
        length_mod = f" [length: {preferences['length'].lower()}]"
        complexity_mod = f" [complexity: {preferences['complexity'].lower()}]"
        style_mod = f" [style: {preferences['style'].lower()}]"

        modified_prompt = prompt + length_mod + complexity_mod + style_mod
    else:
        modified_prompt = prompt

    return modified_prompt


def improve_prompt(user_prompt):
    improved_prompt = lch.improve_prompt(user_prompt)
    return improved_prompt


def response_to_shortened_prompt(shortened_prompt):
    response = lch.get_response(shortened_prompt)
    st.session_state["improved_history"].append(
        Message("AI", response)
    )


def delete_chat_history():
    for key in st.session_state.keys():
        del st.session_state[key]


def render_layout():
    with st.container():
        st.title("BetterPrompt ⭐")
        st.markdown("_A Prompt Optimizer by Tra My, Le and Andy_")
        st.markdown("Let BetterPrompt improve your prompt with a single click.")

        # Layout adjustments start here
        col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the ratio as needed
        with col1:
            with st.expander("Set Your Response Preferences", expanded=False):
                length_choice = st.selectbox(
                    'Preferred length of the answer:',
                    ('Short', 'Average', 'Long'),
                    index=1
                )
                complexity_choice = st.selectbox(
                    'Complexity level:',
                    ('Easy', 'Average', 'Complex'),
                    index=1
                )
                style_choice = st.selectbox(
                    'Tone or style of the response:',
                    ('Basic', 'Creative'),
                    index=0
                )

                if st.button('Set Preferences'):
                    st.session_state['preferences'] = {
                        'length': length_choice,
                        'complexity': complexity_choice,
                        'style': style_choice
                    }
                    st.success('Preferences updated!')
        # Layout adjustments end here

        with st.form("chat_form"):
            st.markdown("**Original Prompt**")
            columns = st.columns([12, 1])
            columns[0].text_input(
                "Enter your prompt",
                key="human_prompt",
                value=""
            )
            submit_button = columns[1].form_submit_button("Send")

        if submit_button:
            generate_response()

        if "chat_history" in st.session_state:
            with st.container():
                columns = st.columns(2)
                columns[0].button("Delete Chat History",
                                  on_click=delete_chat_history)
                if columns[1].button("Shorten improved Prompt"):
                    shortened_prompt = lch.shorten_prompt(st.session_state["improved_history"][0].message)
                    st.session_state["improved_history"].append(
                        Message("USER", shortened_prompt)
                    )
                    response_to_shortened_prompt(shortened_prompt)
            chat1, chat2 = st.columns(2)
            with chat1:
                st.markdown("Original Prompt: ")
                for message in st.session_state["chat_history"]:
                    message_length = len(message.message.split())
                    st.code(f"Length: {message_length}")
                    div = f"""
                    <div class="chat-row
                    {'' if message.origin == 'AI' else 'user_color'}">
                    {message.message}
                    </div>
                    """
                    st.markdown(div, unsafe_allow_html=True)

            with chat2:
                st.markdown("Improved Prompt:")
                for message in st.session_state["improved_history"]:
                    message_length = len(message.message.split())
                    st.code(f"Length: {message_length}")
                    div = f"""
                    <div class="chat-row
                    {'' if message.origin == 'AI' else 'user_color'}">
                    {message.message}
                    </div>
                    """
                    st.markdown(div, unsafe_allow_html=True)


load_css()
initialize_session_state()
render_layout()
