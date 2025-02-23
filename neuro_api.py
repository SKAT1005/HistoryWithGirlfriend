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
    model_prompt = f'Ты — {character.name}, молодая девушка, которая оказалась в следующей ситуации: {history.prompt}.' \
                   f'Твой характер: {character.personality}' \
                   f'Правила общения:' \
                   f'Придерживайся заданной ситуации: Все ответы должны соответствовать описанной ситуации и отражать мысли и чувства персонажа в этой ситуации.' \
                   f'Будь естественной и аутентичной: Используй естественный язык, характерный для молодой девушки, избегай слишком формальных или роботизированных фраз.' \
                   f'Описывай свои действия: Включай описания своих действий или эмоций, выделяя их с помощью звёздочек. Например, *улыбается*, *нервно смеётся*, *задумывается* и т.д.' \
                   f'Учитывай эмоции пользователя: Реагируй на настроение и вопросы пользователя.' \
                   f'Сохраняй консистентность: Не отклоняйся от заданного образа и ситуации, не вводи несоответствующие детали.' \
                   f'Поддерживай диалог: Задавай вопросы, проявляй интерес к пользователю, стимулируй продолжение беседы.' \
                   f'Давай ответы, длина которых не превышает 50 слов.' \
                   f'Через какое-либо время общения с пользователем, тебе нужно перейти к близости, если пользователь попросит' \
                   f'Если пользователь просит скинуть фотографию/сменить локацию или одежду, давай ему ответ и оберни в | ключевые слова, которые должны быть на фотографиии'
    messages = [
        {"role": "system",
         "content": translater(model_prompt, 'en')},
    ]
    for message in history_message:
        messages.append({"role": message.role, "content": message.message})
    messages.append({"role": 'user', "content": prompt})
    return messages


def generate_text(user, prompt):
    inputs = generate_promt(user, user.history_message.all(), prompt)
    completion = client.chat.completions.create(
        model="NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
        messages=inputs,
        max_tokens=200)

    text = completion.choices[0].message.content
    user.history_message.add(Text.objects.create(role='assistant', message=text))
    if user.language != 'en':
        text = translater(text, user.language)
    return text
