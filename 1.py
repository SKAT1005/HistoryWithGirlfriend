from huggingface_hub import InferenceClient

client = InferenceClient(api_key="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")

messages = [
    {
        "role": 'system',
        "content": 'Ты нежная, застенчивая студентка, которая любит страсть в сексе'
    },
	{
		"role": "user",
		"content": "Что ты любишь в сексе?"
	}
]

completion = client.chat.completions.create(
    model="NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
	messages=messages,
	max_tokens=500
)

print(completion.choices[0].message.content)