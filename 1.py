import datetime
import time

from huggingface_hub import InferenceClient
import io
from PIL import Image
import base64
# 'stabilityai/stable-diffusion-xl-base-1.0' 'anthienlong/enhanceaiteam_uncensored' 'aifeifei798/flux-lora-uncensored' 'prashanth970/flux-lora-uncensored'
# enhanceaiteam/Flux-Uncensored-V2
n = ['aifeifei798/flux-lora-uncensored']

client = InferenceClient(api_key="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")

def generate_image(prompt, model_name):
    """Generates an image based on a text prompt using a Hugging Face model.

    Args:
        prompt: The text prompt describing the image you want to generate.
        model_name: The name of the Hugging Face model to use.

    Returns:
        A PIL Image object, or None if there was an error.
    """
    try:
        print('Начинаю генерацию')
        response = client.text_to_image(prompt=prompt, model=model_name)
        print(response)
        return response
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


if __name__ == "__main__":
    prompt = 'Anime style. nude girl in the park'
    l = 1
    for i in n:
        name = i.split('/')[1]
        stat = datetime.datetime.now().timestamp()
        generated_image = generate_image(prompt, model_name=i)
        if generated_image:
            generated_image.save(f"result/{l}.png") # Сохраняем изображение
            generated_image.show()
        else:
             print("Failed to generate image.")
        end = datetime.datetime.now().timestamp() - stat
        print(f'{l}/{len(n)}', end)
        l += 1