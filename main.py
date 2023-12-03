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
    human_prompt = st.session_state["human_prompt"]
    improved_prompt = improve_prompt(human_prompt)
    improved_prompt = improved_prompt.replace("Reformulated prompt:", "")
    improved_prompt = improved_prompt.replace("Reformulated Prompt:", "")
    gpt_response = st.session_state["gpt_history"].run(human_prompt)
    gpt_improved_response = st.session_state["gpt_history"].run(improved_prompt)
    st.session_state["chat_history"].append(
        Message("USER", human_prompt)
    )
    st.session_state["chat_history"].append(
        Message("AI", gpt_response)
    )
    st.session_state["improved_history"].append(
        Message("USER", improved_prompt)
    )
    st.session_state["improved_history"].append(
        Message("AI", gpt_improved_response)
    )

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

    with st.form("chat_form"):
        st.markdown("**Original Prompt**")
        columns = st.columns([12, 1])
        columns[0].text_input(
            placeholder="Enter your prompt",
            label="chat",
            label_visibility="collapsed",
            key="human_prompt",
            value="What are good computers to buy?"
        )
        submit_button = columns[1].form_submit_button(
            "Send",
            type="primary",
        )

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
                {"" if message.origin == "AI" else "user_color"}">
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
                {"" if message.origin == "AI" else "user_color"}">
                {message.message}
                </div>
                """
                st.markdown(div, unsafe_allow_html=True)

load_css()
initialize_session_state()
render_layout()
