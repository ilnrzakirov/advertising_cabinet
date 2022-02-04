import requests
from loguru import logger
import json
headers = {
    'X-ACCESS-KEY': "KEY",
    'X-SECRET-KEY': "KEY"
}
URL = 'https://api.bemob.com/v1/dictionaries/countries'

def country():
    response = requests.request("GET", URL, headers=headers)
    data = json.loads(response.text)
    return data
