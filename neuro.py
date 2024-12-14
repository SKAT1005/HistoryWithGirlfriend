import os

import django
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, MixtralForCausalLM, LlamaTokenizer

from const import translater

tokenizer = LlamaTokenizer.from_pretrained('NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO', trust_remote_code=True)
model = MixtralForCausalLM.from_pretrained(
    "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_8bit=False,
    load_in_4bit=True,
    use_flash_attention_2=True
).to('cpu')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HistoryWithGirlfriend.settings')
django.setup()
print('done')

from app.models import Text



def generate_promt(user, history_message, prompt):
    prompt = translater(prompt, 'en')
    user.history_message.add(Text.objects.create(role='user', message=prompt))
    history = user.choose_history
    character = history.character
    model_prompt = f'Максимальная длина ответа не должна превышать 30 слов' \
                   f'Тебя зовут: {character.name}.' \
                   f'Твой характер: {character.personality}.' \
                   f'Придерживайся этой истории: {history.description}'
    messages = [
        {"role": "system",
         "content": translater(model_prompt, 'en')},
    ]
    for message in history_message:
        messages.append({"role": message.role, "content": message.message})
    input_text = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True)
    return input_text


def generate_text(user, prompt):
    inputs = generate_promt(user, list(user.history_message.all())[-6:], prompt)
    outputs = model.generate(inputs, max_new_tokens=50, temperature=0.6,
                             top_p=0.4, do_sample=True)
    text = tokenizer.decode(outputs[0]).split('\n')[-1].replace('<|im_end|>', '')
    user.history_message.add(Text.objects.create(role='assistant', message=text))
    if user.language != 'en':
        text = translater(text, user.language)
    return text
