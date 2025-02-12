import openai
from config import (
    decision, 
    extraction, 
    TOGETHER_AI_API_KEY,
    GROQ_API_KEY)
from utils import ProviderNotFound, sync_stopwatch

providers = {
    "together": {
        "client": openai.OpenAI(
            api_key=TOGETHER_AI_API_KEY,
            base_url="https://api.together.xyz/v1"),
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
    },
    "groq":{
        "client": openai.OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"),
        "model": "llama-3.3-70b-versatile"
    }
}
client, model = providers['together'].values()

def set_client(provider: str):
    global client, model
    
    if provider not in providers:
        raise ProviderNotFound(f"""Провайдер "{provider}" не найден""")
    
    client, model = providers[provider].values()

def generate_completion(prompt):
    global client, model

    response = client.chat.completions.create(
        model=model,
        messages=prompt,
        max_tokens=None,
        temperature=0.7,
        top_p=0.7,
        stop=["<|eot_id|>","<|eom_id|>"],
        stream=False,
    )

    return response

def stream_completion(prompt):

    response = client.chat.completions.create(
        model=model,
        messages=prompt,
        max_tokens=None,
        temperature=0.7,
        top_p=0.7,
        stop=["<|eot_id|>","<|eom_id|>"],
        stream=True,
    )

    for chunk in response:
        choices = chunk.choices
        if choices:
            delta = chunk.choices[0].delta
            if delta:
                yield delta.content

# @sync_stopwatch(description='deciding how to answer')
def decide_how_to_answer(user_prompt):

    messages = [
        {
            "role": "system",
            "content": decision
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    response = generate_completion(messages)
    print(response)

    return response.choices[0].message.content

# @sync_stopwatch(description='extraction info')
def extract_info(relevant, query):

    context = '\n\n'.join([f"[Источник #{i}]({k})\n{v}" for i, (k, v) in enumerate(relevant.items(), start=1)])

    messages = [
        {
            "role": "system",
            "content": extraction.replace("$CONTEXT$", context)
        },
        {
            "role": "user",
            "content": query
        }
    ]
    
    response = stream_completion(messages)

    return response
