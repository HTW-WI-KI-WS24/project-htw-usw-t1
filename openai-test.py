from openai import OpenAI

client = OpenAI()

# Initialize conversation with a system message
messages = [{"role": "system", "content": "You are a helpful assistant."}]

while True:
    user_text = input("User: ")

    # Add the user message to the conversation history
    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        max_tokens=1000
    )

    assistant_response = response.choices[0].message.content
    print(f"\nSystem: {assistant_response}\n")

    # Add grandmas message to the conversation history
    messages.append({"role": "assistant", "content": assistant_response})
