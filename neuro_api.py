import os

import django
from huggingface_hub import InferenceClient

client = InferenceClient(api_key="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")

from const import translater

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HistoryWithGirlfriend.settings')
django.setup()

from app.models import Text



def generate_promt(user, history_message, prompt):
    prompt = translater(prompt, 'en')
    user.history_message.add(Text.objects.create(role='user', message=prompt))
    history = user.choose_history
    character = history.character
    model_prompt = f'Ты — {character.name}, {character.personality} ' \
                   f'**Текущая история:** {history.prompt}' \
                   f'При общении добавляй описания своих действий, отделяя их от речи курсивом. Всегда придерживайся своего характера и текущей истории.'
    messages = [
        {"role": "system",
         "content": translater(model_prompt, 'en')},
    ]
    for message in history_message:
        messages.append({"role": message.role, "content": message.message})

    return messages


def generate_text(user, prompt):
    inputs = generate_promt(user, list(user.history_message.all())[-6:], prompt)
    completion = client.chat.completions.create(
        model="NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
        messages=inputs,
        max_tokens=100)

    text = completion.choices[0].message.content
    user.history_message.add(Text.objects.create(role='assistant', message=text))
    if user.language != 'en':
        text = translater(text, user.language)
    return text
