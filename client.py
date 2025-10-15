from openai import OpenAI

# Initialize the client
client = OpenAI(api_key="")  # Replace with your actual API key

# Make a chat completion request
completion = client.chat.completions.create(
    model="gpt-4o-mini",  # or gpt-5 if available
    messages=[
        {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
        {"role": "user", "content": "What is coding?"}
    ]
)

# Print the assistant's reply
print(completion.choices[0].message.content)