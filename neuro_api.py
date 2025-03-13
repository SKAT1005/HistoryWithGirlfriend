import os

import django
from huggingface_hub import InferenceClient

client = InferenceClient(api_key="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")

from const import translater

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HistoryWithGirlfriend.settings')
django.setup()

from app.models import Text

import base64
import time

import requests
import json

post_url = 'https://api.generativecore.ai/api/v3/tasks'

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Basic Z2VybF9oaXN0b3J5MTI6MWZhMzM1NTUxNmJhZTYzZDg4ZTA='
}


def image_to_base64(image_path):
    """
    Преобразует изображение из файла в строку base64.

    Args:
        image_path: Путь к файлу изображения.

    Returns:
        Строка base64, представляющая изображение, или None, если произошла ошибка.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string
    except Exception as e:
        print(f"Ошибка при преобразовании в base64: {e}")
        return None


def get_image(photo, prompt):
    photo = image_to_base64(photo)
    data = {
        "batchId": "1",
        "isFast": True,
        "payload": {
            "base64": False,
            "image": photo,
            "checkpoint": "juggernautXL_v9Rundiffusionphoto2.safetensors",
            "prompt": prompt,
            # 'styles': ['SAI Anime']
        },
        "type": "image-to-image"
    }
    response = requests.post(post_url, headers=headers, data=json.dumps(data))
    id = response.json()['id']
    while True:
        response = requests.get(f'https://api.generativecore.ai/api/v3/tasks/{id}', headers=headers)
        if response.json()['status'] == 'completed':
            photo_base64 = response.json()['results']['data']['images'][0]['url']
            break
        time.sleep(3)
    return photo_base64


def need_photo(history_message):
    model_prompt = """Проанализируй следующий текст. Если текст описывает:

•   **Смену одежды персонажа,**
•   **Переход персонажа в новую локацию,**
•   **Изменение позы персонажа,**

То извлеки и предоставь основное описание для создания фотографии, включающее: описание персонажа, одежды (если изменилась), локации и позы.

В противном случае, ответь: "НЕТ".

**Пример 1:**

**Текст:** Если вам удобнее переодеться в другой топ, *улыбается*, то я могу это сделать. Позвольте мне протянуть руку за спину и взять эту рубашку. Она более повседневная и свободного покроя, идеально подходит для непринужденной беседы на крыльце. *расстегивает и снимает с меня майку* Спасибо за предложение, надеюсь, это сделает нашу беседу более приятной. Если хотите, я с удовольствием узнаю больше о ваших интересах или даже расскажу несколько забавных историй. О чем бы мы могли поболтать?

**Промпт:** Улыбка, крыльцо, ясный день, рубашка свободного покроя."""
    messages = [
        {"role": "system", "content": translater(model_prompt, 'en')},
        {"role": 'user', "content": history_message.message}
    ]
    return messages


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
                   f'Давай ответы, длина которых не превышает 50 слов.'
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
    photo_input = need_photo(user.history_message.last())
    completion_photo = client.chat.completions.create(
        model="NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
        messages=photo_input,
        max_tokens=200)
    photo_prompt = completion_photo.choices[0].message.content
    if user.language != 'en':
        text = translater(text, user.language)

    if photo_prompt != 'NO':
        photo = get_image(user.history.photo, photo_prompt)
    else:
        photo = False
    return text, photo
