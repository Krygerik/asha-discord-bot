import json
import requests

url = "http://46.101.232.123:3002/api/ladder/create"

headers = {
    'Content-Type': 'application/json'
}

# Запрос на создание турнирной встречи
def sendLadderPair(discordIds):
    payload = json.dumps({
        "discord_ids": discordIds
    })

    response = requests.request("POST", url, headers=headers, data=payload)

    responseSerializeData = response.json()

    if responseSerializeData.get('STATUS') == 'SUCCESS':
        return responseSerializeData.get('MESSAGE')

    return "Ошибка при создании рейтинговой встречи"
