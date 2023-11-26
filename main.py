from openai import OpenAI

client = OpenAI()

# Methoden --------------------------------------------------------------------------------

# Function to get a response from OpenAI's Chat Completion API
def get_chat_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content


# Function to ask LLM to rate the output and reformulate the prompt
def rate_and_reformulate(messages):
    # Ask the LLM to rate the output
    messages.append({
        "role": "system",
        "content": "Please rate the quality of the previous completion on a scale from 1 to 10 and explain the rating."
    })

    # Get the rating
    rating_response = get_chat_response(messages)
    print(f"Rating: {rating_response}")

    # Ask the LLM to reformulate the prompt for a better output
    messages.append({
        "role": "system",
        "content": "Based on the rating, how would you reformulate the prompt for a better completion."
    })

    # Get the reformulated prompt
    reformulated_prompt_response = get_chat_response(messages)
    print(f"Reformulated Prompt: {reformulated_prompt_response}")

    return rating_response, reformulated_prompt_response

# Main --------------------------------------------------------------------------------

# Initial prompt
initial_prompt = "How can I manage my time during exam phase?"

# Initial message to the API
messages = [
    {"role": "user", "content": initial_prompt}
]

# Get the initial output
output = get_chat_response(messages)
messages.append({"role": "assistant", "content": output})

# Ask LLM to rate the output and suggest a reformulated prompt
rating, reformulated_prompt = rate_and_reformulate(messages)

print("----------------------------------------")
print("initial prompt: " + initial_prompt)
print("output: " + output)
print("rating: " + rating)
print("reformulated prompt: " + reformulated_prompt)

# Continue the conversation with the reformulated prompt if necessary
# This would involve adding the reformulated prompt to messages and getting a new output
# You could loop this process as needed
