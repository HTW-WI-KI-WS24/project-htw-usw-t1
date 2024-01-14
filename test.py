import streamlit as st
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI()
st.set_page_config(layout="wide")

if 'responses' not in st.session_state:
    st.session_state['responses'] = []

with st.container():
    # Use HTML and CSS to center the title and markdown
    st.markdown("""
        <div style="text-align: center;">
            <h1>BetterPrompt ⭐</h1>
            <p>A Prompt Optimizer by Tra My, Le and Andy</p>
        </div>
        """, unsafe_allow_html=True)

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

st.header("Interact with the LLM")
st.markdown("Enter your prompt and receive a response.")
prompt = st.text_input("Enter your prompt here", value="", key="prompt")

if st.button("Get Response"):
    response_obj = llm.invoke(prompt)
    st.session_state['responses'].append({'prompt': prompt, 'response': response_obj.content, 'refinements': []})

for idx, item in enumerate(st.session_state['responses']):
    st.subheader(f"Response {idx + 1}")
    st.write(item['response'])
    rating_key = f'rating_{idx}'
    st.radio("Rate the response:", ["⭐️", "⭐️⭐️", "⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️⭐️"], key=rating_key)

    if idx == len(st.session_state['responses']) - 1:
        refine_option_key = f'refine_option_{idx}'
        refine_option = st.selectbox("Select how you want to refine the prompt:",
                                     ["Select an option", "More Simple", "More Complex", "Step by Step", "More Detailed", "More Concise", "Very short"],
                                     key=refine_option_key)
        if refine_option != "Select an option":
            refinement_instructions = item['refinements'] + [refine_option]
            refinement_request = " and ".join(refinement_instructions)
            prompt_refinement = f"Please reformulate the following prompt to be '{refinement_request}': {item['prompt']}"
            refined_prompt_obj = llm.invoke(prompt_refinement)
            print(refined_prompt_obj)
            refined_prompt = refined_prompt_obj.content if refined_prompt_obj else "No refined prompt generated."
            refined_response_obj = llm.invoke(refined_prompt)
            refined_response = refined_response_obj.content if refined_response_obj else "No response generated."
            st.session_state['responses'].append({'prompt': refined_prompt, 'response': refined_response, 'refinements': refinement_instructions})

if len(st.session_state['responses']) > 0:
    st.session_state['satisfied'] = st.checkbox("I am satisfied with this response", key='satisfied_check')
    if st.session_state['satisfied']:
        if st.button("Start with a new prompt"):
            st.session_state['responses'] = []
            st.session_state['satisfied'] = False
