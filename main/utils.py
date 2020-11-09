import requests
import json

BASEURL = "https://www.wordsapi.com/mashape/words/"

def get_data(word):
    ENDPOINT = f"{word}?when=2020-11-06T03:35:03.282Z&encrypted=8cfdb18ae723929bea9707bfec58bdbcaeb02e0932f795b8"
    data = requests.get(BASEURL+ENDPOINT)
    result = json.loads(data.text).get("results")
    if result:
        return result[0]
    return

def get_field(field, data):
    if data:
        return data.get(field)