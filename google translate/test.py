import requests
from ggtranslate import translate_url
import json

if __name__ == "__main__":
    url = translate_url('你好世界', to_language='en')
    rep = requests.get(url)

    js = json.loads(rep.text)
    print(js[0][0][1], ' => ', js[0][0][0])

