import argparse
import os

import requests
from dotenv import load_dotenv


def shorten_link(token, user_input_url):
    link = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {"Authorization": "Bearer " + token}
    payload = {"long_url": user_input_url}
    response = requests.post(link, json=payload, headers=headers)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(token, bitlink):
    url_clicks = (f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary')
    headers = {"Authorization": "Bearer " + token}
    params = {'unit': 'day', 'units': '-1'}
    response = requests.get(url_clicks, params=params, headers=headers)
    response.raise_for_status()
    clicks = response.json()['total_clicks']
    return clicks


def main():
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser(description='Сокращаем ссылку через Bitly.com')
    parser.add_argument('user_input_url', help='Введите ссылку')
    args = parser.parse_args()
    user_input_url = args.user_input_url
    try:
        if user_input_url.startswith('bit.ly'):
            print('Кликов по ссылке:', count_clicks(token, user_input_url))
            return count_clicks(token, user_input_url)
        else:
            print('Короткая ссылка:', shorten_link(token, user_input_url))
            return shorten_link(token, user_input_url)
    except requests.exceptions.HTTPError as error:
        print(f'\nНеверная ссылка!\nОшибка\n{error}.')


if __name__ == '__main__':
    main()
