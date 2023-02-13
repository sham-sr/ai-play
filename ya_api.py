import requests
import os
import json

# переводчик
def ya_translate(text,target_language='ru'):
    try:
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": f'Api-Key {os.getenv("YA_API_KEY")}'
                  }
        body = {
        "targetLanguageCode": target_language,
        "texts": text,
        "folderId": os.getenv("YA_FOLDER"),
        }
        response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                  json = body,
                                  headers = headers
                                )
        return json.loads(str(response.text))['translations'][0]['text']
    except:
        return None