from openai import OpenAI

client = OpenAI()


def generate_output_with_turbo(prompt):
    """
    This function sends the prompt to the OpenAI API using the gpt-3.5-turbo model and retrieves the output.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def evaluate_and_reformulate_with_davinci(messages):
    messages.append({
        "role": "system",
        "content": "Please rate the quality of the previous completion on a scale from 1 to 10 and explain the rating."
    })
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    rating_response = response.choices[0].message.content

    # Ask the LLM to reformulate the prompt for a better output
    messages.append({
        "role": "system",
        "content": "Based on the rating, how would you reformulate the user input for a better completion."
    })

    response2 = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    # Get the reformulated prompt
    reformulated_prompt_response = response2.choices[0].message.content
    print(f"Reformulated Prompt: {reformulated_prompt_response}")

    return rating_response, reformulated_prompt_response


# Example usage:
original_prompt = "Paint the sky in the colours of your emotions."

# Initial message to the API
messages = [
    {"role": "user", "content": original_prompt}
]

generated_output = generate_output_with_turbo(original_prompt)
messages.append({"role": "assistant", "content": generated_output})

rating, reformulated_prompt = evaluate_and_reformulate_with_davinci(messages)

print("----------------------------------------")
print("initial prompt: " + original_prompt)
print("output: " + generated_output)
print("rating: " + rating)
print("reformulated prompt: " + reformulated_prompt)

# The response from the LLM should contain the evaluation and any suggested reformulations.
