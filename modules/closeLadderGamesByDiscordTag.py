import json
import requests

closeLadderUrl = "http://46.101.232.123:3002/api/ladder/cancel"

headers = {
    'Content-Type': 'application/json'
}

# Закрывает активную ладдерную встречу для игрока с переданным дискорд тегом
def closeLadderGamesByDiscordTag(discordTag):
    payload = json.dumps({
        "discord_id": discordTag
    })

    response = requests.request("POST", url=closeLadderUrl, headers=headers, data=payload)

    responseSerializeData = response.json()

    if responseSerializeData.get('STATUS') == 'SUCCESS':
        return responseSerializeData.get('MESSAGE')

    return "Ошибка при создании рейтинговой встречи"
