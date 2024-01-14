import streamlit as st
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI()
st.set_page_config(layout="wide")

if 'responses' not in st.session_state:
    st.session_state['responses'] = []
if 'input_disabled' not in st.session_state:
    st.session_state['input_disabled'] = False
if 'satisfied' not in st.session_state:
    st.session_state['satisfied'] = False
if 'reset_input' not in st.session_state:
    st.session_state['reset_input'] = False
if 'response_history' not in st.session_state:
    st.session_state['response_history'] = []

with st.container():
    st.title("BetterPrompt ⭐")
    st.markdown("A Prompt Optimizer by Tra My, Le and Andy")

st.header("Interact with the LLM")
st.markdown("Enter your prompt and receive a response.")
prompt = st.text_input("Enter your prompt here", value="", key="prompt")

if st.button("Get Response"):
    response_obj = llm.invoke(prompt)
    st.session_state['responses'].append(
        {'prompt': prompt, 'response': response_obj.content, 'ratings': {}, 'refinements': []})

for idx, item in enumerate(st.session_state['responses']):
    st.subheader(f"Interaction {idx + 1}")

    st.write("Prompt:")
    st.write(item['prompt'])
    response_length = str(len(item['response'].split()))
    st.write("Response:" + " (words: " + response_length + ")")
    st.write(item['response'])

    if 'ratings' not in item or not all(key in item['ratings'] for key in ['length', 'complexity', 'tone']):
        item['ratings'] = {'length': 3  , 'complexity': 3, 'tone': 3}

    rating_length_key = f'rating_length_{idx}'
    rating_complexity_key = f'rating_complexity_{idx}'
    rating_tone_key = f'rating_tone_{idx}'

    st.header("Rate the Response")
    st.subheader("Length (1 = Too Short, 5 = Too Long)")
    item['ratings']['length'] = st.slider("length", 1, 5, value=item['ratings']['length'], key=rating_length_key)
    st.subheader("Complexity (1 = Too Simple, 5 = Too Complex)")
    item['ratings']['complexity'] = st.slider("complexity", 1, 5, value=item['ratings']['complexity'],
                                              key=rating_complexity_key)
    st.subheader("Tone (1 = Too Casual, 5 = Too Formal)")
    item['ratings']['tone'] = st.slider("tone", 1, 5, value=item['ratings']['tone'], key=rating_tone_key)

    if idx == len(st.session_state['responses']) - 1:
        st.header("Refine the Prompt")
        action_word_option_key = f'action_word_option_{idx}'
        action_word_option = st.selectbox("Select the task you want to perform:",
                                          ["Select an option", "Give", "Generate", "Analyze", "Explain",
                                           "Write an email", "Write an essay", "Write a story"],
                                          key=action_word_option_key)
        format_option_key = f'format_option_{idx}'
        format_option = st.selectbox("Select how you want to refine the prompt:",
                                     ["Select an option", "step by step", "in detail", "in a few sentences",
                                      "in a few paragraphs", "concise", "long"],
                                     key=format_option_key)
        tone_option_key = f'tone_option_{idx}'
        tone_option = st.selectbox("Select the tone you want to use:",
                                   ["Select an option", "formal", "informal", "casual", "neutral"],
                                   key=tone_option_key)
        persona_option_key = f'persona_option_{idx}'
        persona_option = st.text_input("Enter the persona you want to use:", value="", key=persona_option_key)

        length_rating = item['ratings']['length']
        complexity_rating = item['ratings']['complexity']
        tone_rating = item['ratings']['tone']

        complexity = ""

        if length_rating == 1:
            response_length = int(response_length)*2.5
        elif length_rating == 2:
            response_length = int(response_length)*1.5
        elif length_rating == 3:
            response_length = int(response_length)
        elif length_rating == 4:
            response_length = int(response_length)*0.75
        else:
            response_length = int(response_length)*0.5

        if response_length % 2 != 0:
            response_length += 0.5

        if complexity_rating == 1:
            complexity = "complex"
        elif complexity_rating == 2:
            complexity = "complicated"
        elif complexity_rating == 3:
            complexity = "average"
        elif complexity_rating == 4:
            complexity = "simple"
        else:
            complexity = "very simple"

        if tone_rating == 1:
            tone = "very formal"
        elif tone_rating == 2:
            tone = "formal"
        elif tone_rating == 3:
            tone = "neutral"
        elif tone_rating == 4:
            tone = "casual"
        else:
            tone = "very casual"

        if st.button("Generate Response with Refinements", key=f'generate_response_{idx}'):
            refinements = [refinement for refinement in [action_word_option, format_option, tone_option, persona_option]
                           if refinement != "Select an option"]
            refinement_instructions = " and ".join(refinements)
            prompt_refinement = (f"Please reformulate the following prompt to be '{refinement_instructions}': "
                                 f"{item['prompt']}. The reformulated prompt should include an instruction to the "
                                 f"assistant to respond at around {str(response_length)} words. Furthermore the "
                                 f"prompt should include an instruction to the assistant to respond in a {complexity} "
                                 f"manner and in a {tone} tone."
                                 f"Furthermore just respond the reformulated prompt.")

            print(prompt_refinement)

            refined_prompt_obj = llm.invoke(prompt_refinement)
            print(refined_prompt_obj.content)
            refined_response_obj = llm.invoke(refined_prompt_obj.content)

            print(refined_response_obj.content)
            refined_response = refined_response_obj.content if refined_response_obj else "No response generated."

            st.session_state['responses'].append(
                {'prompt': refined_prompt_obj.content, 'response': refined_response_obj.content,
                 'refinements': refinements})

            print(response_length)

# Modification starts from the Satisfaction and Reset checks
if st.button("I am satisfied with the latest response", key='satisfaction'):
    # Store the last response in the response history
    if st.session_state['responses']:
        last_response = st.session_state['responses'][-1]
        st.session_state['response_history'].append(last_response)

    # Clear the chat history
    st.session_state['responses'] = []

    st.session_state['satisfied'] = True
    st.session_state['reset_input'] = True

if st.button("Start over with a new prompt", key='reset_app'):
    st.session_state['responses'] = []
    st.session_state['input_disabled'] = False
    st.session_state['satisfied'] = False
    st.session_state['reset_input'] = False

if st.session_state['reset_input']:
    st.session_state['reset_input'] = False

# Displaying the response history in the sidebar
st.sidebar.header("Response History")
for idx, history_item in enumerate(st.session_state['response_history']):
    st.sidebar.subheader(f"History {idx + 1}")
    st.sidebar.text(history_item['response'][:100] + '...')  # Display first 100 characters of the response
    # Display the ratings if they are available
    if 'ratings' in history_item:
        ratings = history_item['ratings']
        st.sidebar.text(f"Length: {ratings['length']}, Complexity: {ratings['complexity']}, Tone: {ratings['tone']}")