import os
import openai
from api import send_message

openai.api_key = os.getenv('OPENAI_API_KEY')


def generate_output(prompt):
    print(f"Generating output for {prompt}")
    return openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ).choices[0].text


def on_msg_received(msg, matches):
    chat_id = msg["chat"]["id"]
    prompt = matches.group(1)

    output = generate_output(prompt)
    print(f"Sending output {output}")

    send_message(chat_id, output)
