import requests


async def get_data_request(filename: str):
    with open(filename, 'r', encoding = 'UTF-8') as data_text:
        data_string = data_text.read()
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    headers = {
        'Authorization': 'Bearer t1.9euelZqYjIyYnsaMy42PisjPmpnNyO3rnpWaz8iUi5GKzs2SkpCYyZ7NjJbl8_dMTA1H-e90VDBr_t3z9wx7Ckf573RUMGv-zef1656VmpDIk42KksqMk5adiZyZlomW7_zF656VmpDIk42KksqMk5adiZyZlomW.IJ_QGCIuY63zQIUebyPfTETEypm8kvaVuCaAaaPY6cQ7f3Z9PVesVDikA71bfMR3re4vQkiXEeFvUEVcKQjHCA',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": "gpt://b1gjp5vama10h4due384/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 2000
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
    response = requests.post(url, headers=headers, json=data)

    return response.json()['result']['alternatives'][0]['message']['text']
