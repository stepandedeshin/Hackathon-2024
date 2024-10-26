import requests


async def get_user_request(request_text: str) -> str:
    file = open('data.txt', 'r', encoding='utf-8').read()
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    headers = {
        'Authorization': 'Bearer t1.9euelZrNk4-bzJWUyJvLm8_MicaOnO3rnpWaz8iUi5GKzs2SkpCYyZ7NjJbl8_c8WgpH-e9TAGRZ_N3z93wICEf571MAZFn8zef1656VmpqNmZqTz8yWncyVy8qKx4yP7_zF656VmpqNmZqTz8yWncyVy8qKx4yP.h_scoUHRbGOxzzNt2tzxu3u9a6L5F0hqcrSTtE6IpC9tKCCvG8PICQCP0-hnEoJfuI3CwsBZWCRiol1wTFVjAg',
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
