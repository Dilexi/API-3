import os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse

import requests
from requests.exceptions import HTTPError


API_URL = 'https://api-ssl.bitly.com/v4/'
def shorten_link(token, url):
    bitly_url = "{}shorten".format(API_URL)
    params = {
        "long_url": url
    }
    headers = {
        "Authorization": "Bearer {}".format(token)
    }
    response = requests.post(
        bitly_url,
        json=params,
        headers=headers)
    response.raise_for_status()
    return response.json()["link"]


def count_clicks(token, link):
    bitly_url = "{0}bitlinks/{1}/clicks/summary".format(API_URL, link)
    params = {
        "unit": "month",
        "units": "-1"
    }
    headers = {
        "Authorization": "Bearer {}".format(token)
    }
    response = requests.get(
        bitly_url,
        params=params,
        headers=headers
    )
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, url):
    bitly_url = "{0}bitlinks/{1}".format(API_URL, url)
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.get(bitly_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    bitly_token = os.getenv('bitly_token')
    parser = argparse.ArgumentParser(description="Наша программа \
    поможет вам сократить ссылку, или посчитать колличество кликов, \
    по уже сокращенной ссылке. Для того, чтобы получить \
    коллличество кликов, вставьте --url ссылку, у которой \
    необходимо выполнить подсчет кликов.")
    parser.add_argument("--url", help="Введите ссылку")
    args = parser.parse_args()
    parsed_url = urlparse(args.url)


    
    url_without_protocol = f"{parsed_url.netloc}{parsed_url.path}"

    if parsed_url.scheme:
        url_with_protocol = args.url
    else:
        url_with_protocol = f"https://{args.url}"

    if is_bitlink(bitly_token, url_without_protocol):
        try:
            print(count_clicks(bitly_token, url_without_protocol))
        except HTTPError as error:
            print("Ошибка при подсчете кликов", error)
    else:
        try:
            print(shorten_link(bitly_token, url_with_protocol))
        except HTTPError as error:
            print("Неправильная ссылка: ", error)


if __name__ == "__main__":
    main()
