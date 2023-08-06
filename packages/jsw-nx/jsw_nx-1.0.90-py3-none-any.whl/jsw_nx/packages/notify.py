import requests

BASE_URL = 'https://api.day.app'


def notify(**kwargs):
    title = kwargs.get('title')
    icon = kwargs.get('icon')
    body = kwargs.get('body')
    sound = kwargs.get('sound')
    bark_key = kwargs.get('bark_key') or process.env.get('BARK_SDK_KEY')
    dict_args = {title, icon, body, sound}
    api_url = f'{BASE_URL}/{bark_key}'
    return requests.post(api_url, json=dict_args)
