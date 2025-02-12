import gradio as gr
import requests

API_URL = "http://api:8000/ask"

def format_response(data):
    response = ""
    
    # Краткий ответ
    response += f"**Краткий ответ:** {data['short_answer']}\n\n"
    
    # Подробный ответ с секциями
    for section in data["detailed_answer"]["sections"]:
        response += f"### {section['heading']}\n"
        response += f"{section['content']}\n\n"
        
        # Добавление списка, если он есть
        if "list" in section:
            for item in section["list"]:
                response += f"- {item}\n"
            response += "\n"
    
    # Проверка на отсутствие информации
    if data["missing_information"]["is_missing"]:
        response += f"⚠️ **Не хватает информации:** {data['missing_information']['details']}\n\n"
    
    # Источники
    response += "**Источники:**\n"
    for source in data["sources"]:
        response += f"- [{source['id']}]({source['url']})\n"

    return response


def query_llm(user_input):
    with requests.post(API_URL, json={"query": user_input}, stream=True) as response:
        partial_text = ""
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                partial_text += chunk.decode("utf-8")
                yield partial_text

with gr.Blocks(css_paths="style.css") as demo:
    gr.Markdown("# 💡 KnowledgeFlow")
    
    with gr.Row():
        user_input = gr.Textbox(label="Введите ваш запрос", placeholder="Например: Как работает GPT?")
    
    submit_btn = gr.Button("Спросить")
    output = gr.Markdown(label="Ответ")

    submit_btn.click(query_llm, inputs=user_input, outputs=output)

demo.launch(server_name="0.0.0.0", server_port=7860)