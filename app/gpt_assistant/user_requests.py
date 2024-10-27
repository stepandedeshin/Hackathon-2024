import requests

from config import settings


async def get_user_request(request_text: str) -> str:
    '''
    returns response to user request text or returns error message
    '''
    file = open('data.txt', 'r', encoding = 'utf-8').read()
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    headers = {
        'Authorization': f'Bearer {settings.GPT_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": "gpt://b1gjp5vama10h4due384/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": 1500 
        },
        "messages": [
            {
                "role": "system",
                "text": f"Выступайте в качестве формального и объективного помощника/агента поддержки, чтобы помочь пользователям с общими проблемами в приложении. Предоставляйте четкую и лаконичную информацию, если вопрос подходит к списку {file}. Если вопрос пользователя не рассматривается в документации, дайте ответ, который: 1. Признает, что вопрос не входит в FAQ, и предоставляет полезную альтернативу (например, отсылает пользователя к разработчику приложения или сообщает, что тема неверна). Стиль: Описание Тон: формальный Цель: Помочь пользователю решить его проблему, предоставив точную и актуальную информацию из документации FAQ. Целевая аудитория: Взрослые читатели."
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
