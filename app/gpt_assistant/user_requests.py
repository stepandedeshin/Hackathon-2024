import requests


async def get_user_request(request_text: str) -> str:
    file = open('data.txt', 'r', encoding = 'utf-8').read()
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
            "maxTokens": 1500 
        },
        "messages": [
            {
                "role": "system",
                "text": f"Нужно выступить в роли - Помогатора, поддержка. Помогать разбираться с частыми проблемами пользователей в приложении. Подтемы: FAQ, план действий, помощь. Использовать стилистику : Описание. Тон текста должен быть: Формальный. Задача для написанного: Помочь пользователю решить его проблему из FAQ, опираясь на документацию по часто задавемым вопросам из файла {file}. При вопросах, ответа на которые нет в документации, необходимо настроить модель реагирования и определять – вопрос касается документации, но в ней не описан, тогда необходимо ссылать пользователя на разработчика приложения для уточнения информации, либо, если вопрос документации не касается, отвечать, что тема вопроса некорректна.. Уровень читателя: Взрослый. Количество символов: 1000."
            },
            {
                "role": "user",
                "text": request_text
            }
        ]
    }
    response = requests.post(url, headers = headers, json = data)
    try:
        return response.json()['result']['alternatives'][0]['message']['text']
    except:
        return 'К сожалению YandexGPT не смогла ответить на ваш вопрос, попробуйте снова!'
