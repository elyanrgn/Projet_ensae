from huggingface_hub import InferenceClient

client = InferenceClient(api_key="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")

messages = [
    {
        "role": "user",
        "content": "You are a football analyst. Your goal is to predict the impact of news on the future performance of a player. To do so rate on a scale from -1 to 1 the title of the article. Where 1 is a strong postive impact and -1 the opposite. Title : 'Mbappe perds l'usage de ses jambes'?",
    }
]

stream = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    messages=messages,
    max_tokens=500,
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")
