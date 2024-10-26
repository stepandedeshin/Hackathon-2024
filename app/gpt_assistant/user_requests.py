import requests


def get_user_request(request_text: str):
    with open('data.txt', 'r', encoding = 'UTF-8') as data_text:
        data_string = data_text.readline()
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
                "text": f"Ты бот-помощник, который отвечает на вопросы, опираясь на этот текст: {data_string}"
            },
            {
                "role": "user",
                "text": request_text
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)

    return response.json()['result']['alternatives'][0]['message']['text']
