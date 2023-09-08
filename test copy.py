import os
import openai

messages = [
    {"role": "user", "content": "hello"}
]

chat = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=100
)

print(chat.choices[0].message.content)