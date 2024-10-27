import requests

from config import settings


async def get_data_request(filename: str) -> str:
    '''
    Forming a string of possible questions from given text file
    
    returns strng of possible requests or returns error message
    '''
    data_string = open(filename, 'r', encoding = 'utf-8').read()
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    headers = {
        'Authorization': f'Bearer {settings.GPT_API_TOKEN}',
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
                "text": "Ты - data scientist, тебе нужно делить входящий текст на множество вопросов, которые могут быть заданны к этому тексту, результатом твоей работы является текст пронумерованных вопросов"
            },
            {
                "role": "user",
                "text": f"Преобазуй {data_string} в список вопросов"
            }
        ]
    }
    response = requests.post(url, headers = headers, json = data)

    try:
        return response.json()['result']['alternatives'][0]['message']['text']
    except:
        return 'error'
