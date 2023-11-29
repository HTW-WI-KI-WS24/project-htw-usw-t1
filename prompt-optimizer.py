from openai import OpenAI

client = OpenAI()


def get_response(user_prompt):
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": user_prompt}],
        model="gpt-3.5-turbo-0613"
    )
    return response.choices[0].message.content


def rate_response(messages):
    messages.append({
        "role": "system",
        "content": "Please rate the quality of the previous completion on a scale from 1 to 10 and explain the rating."
    })

    rating = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo"
    )
    return rating.choices[0].message.content


def improve_prompt(messages):
    messages.append({
        "role": "system",
        "content": "Give an example prompt for the user, so he might get a better response!"
    })

    improved_prompt = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo"
    )
    return improved_prompt.choices[0].message.content


# Get user prompt
user_prompt = input("User prompt: ")

# Initialize Message History
messages = [
    {"role": "user", "content": user_prompt}
]

first_output = get_response(user_prompt)
print("First output ---------------------")
print(first_output)
messages.append({"role": "assistant", "content": first_output})

rating_first_output = rate_response(messages)
print("Rating ---------------------")
print(rating_first_output)
messages.append({"role": "assistant", "content": rating_first_output})

improved_prompt = improve_prompt(messages)
print("Improved prompt ---------------------")
print(improved_prompt)

