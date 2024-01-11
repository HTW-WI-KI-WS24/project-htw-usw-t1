import streamlit as st
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI()

# Initialize session state variables if not already present
if 'response' not in st.session_state:
    st.session_state['response'] = None
if 'refined_response' not in st.session_state:
    st.session_state['refined_response'] = None
if 'current_response_for_evaluation' not in st.session_state:
    st.session_state['current_response_for_evaluation'] = None

# Main title and description
with st.container():
    st.title("BetterPrompt ⭐")
    st.markdown("A Prompt Optimizer by Tra My, Le and Andy")

# Sidebar: Evaluation Guidelines and Examples
with st.sidebar:
    st.header("How to Evaluate Responses")
    with st.expander("Evaluation Guidelines"):
        st.write("""
            - **Clarity**: Is the response easy to understand?
            - **Relevance**: Does it answer your question?
            - **Coherence**: Does the response make logical sense?
            - **Neutrality**: Is the response unbiased and factual?
        """)
    st.header("Response Examples")
    with st.expander("View Examples"):
        st.write("**Good Response Example**: Answers the question directly and clearly.")
        st.write("**Bad Response Example**: Off-topic or confusing and unclear.")

# Prompt Input and Response
st.header("Interact with the LLM")
st.markdown("Enter your prompt and receive a response. You can then refine the prompt for different types of responses.")

prompt = st.text_input("Your Prompt", "Enter your prompt here")

if st.button("Get Response"):
    response_obj = llm.invoke(prompt)
    st.session_state['response'] = response_obj.content if response_obj else "No response generated."
    st.session_state['refined_response'] = None
    st.session_state['current_response_for_evaluation'] = st.session_state['response']

if st.session_state['response']:
    st.subheader("LLM Response")
    st.write(st.session_state['response'])

    st.subheader("Refine Your Prompt")
    refine_option = st.selectbox("Select how you want the response to be refined:",
                                 ["Select an option", "More Simple", "More Complex", "Step by Step", "More Detailed", "More Concise", "very short"])

    if refine_option != "Select an option":
        refinement_request = (f"Please reformulate the following prompt, '{prompt}'. The reformulated prompt should "
                              f"include the instruction to the assistant to answer '{refine_option}'. Only return the "
                              f"refined prompt, which includes the instruction to answer in the specified way. Do not "
                              f"provide a response.")
        refined_prompt_obj = llm.invoke(refinement_request)
        refined_prompt = refined_prompt_obj.content if refined_prompt_obj else "No refined prompt generated."
        st.session_state['refined_response'] = llm.invoke(refined_prompt).content
        st.session_state['current_response_for_evaluation'] = st.session_state['refined_response']

if st.session_state['refined_response']:
    st.subheader("Refined LLM Response")
    st.write(st.session_state['refined_response'])

# Evaluation of Responses in Sidebar
st.sidebar.header("Evaluate the Responses")
current_response = st.session_state['current_response_for_evaluation'] if st.session_state['current_response_for_evaluation'] else "Awaiting response..."
st.sidebar.write(current_response)

rating = st.sidebar.selectbox("Rate this response:", ["Select a rating", "⭐️", "⭐️⭐️", "⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️⭐️"])
if rating != "Select a rating":
    st.sidebar.success("Thank you for your rating!")

detailed_feedback = st.sidebar.text_area("Provide detailed feedback (optional):")
if st.sidebar.button("Submit Feedback"):
    st.sidebar.success("Thank you for your detailed feedback!")
