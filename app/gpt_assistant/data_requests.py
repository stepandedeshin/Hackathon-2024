import requests


async def get_data_request(filename: str) -> str:
    '''
    Forming a string of possible questions from given text file
    
    returns strng of possible requests or returns error message
    '''
    data_string = open(filename, 'r', encoding = 'utf-8').read()
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
