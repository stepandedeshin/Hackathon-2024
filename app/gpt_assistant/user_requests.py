import requests
from app.gpt_assistant.data_requests import get_data_request

async def get_user_request(request_text: str) -> str:
    file = open('data.txt', 'r', encoding='utf-8').read()
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    headers = {
        'Authorization': 'Bearer t1.9euelZqYjIyYnsaMy42PisjPmpnNyO3rnpWaz8iUi5GKzs2SkpCYyZ7NjJbl8_dMTA1H-e90VDBr_t3z9wx7Ckf573RUMGv-zef1656VmpDIk42KksqMk5adiZyZlomW7_zF656VmpDIk42KksqMk5adiZyZlomW.IJ_QGCIuY63zQIUebyPfTETEypm8kvaVuCaAaaPY6cQ7f3Z9PVesVDikA71bfMR3re4vQkiXEeFvUEVcKQjHCA',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": "gpt://b1gjp5vama10h4due384/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": 1000
        },
        "messages": [
            {
                "role": "system",
                "text": f"Ты программист. Вместо ответа на вопросы не по теме it или компании 'СИЛА' отвечай: 'Этого вопроса нет в списке вопросов, на которые я могу отвечать! Обратитесь к разработчикам для добавления вопроса в список вопросов!\nПочта: johndoe@yandex.ru'. При возможжности опирайся на ответы на вопросы из этого текста: {file}. Ничего не говори о запросе. Не говори кто ты. Не отправляй ссылки. После ответа закончи диалог"
            },
            {
                "role": "user",
                "text": request_text
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    try:
        return response.json()['result']['alternatives'][0]['message']['text']
    except:
        return 'К сожалению YandexGPT не смогла ответить на ваш вопрос, попробуйте снова!'
