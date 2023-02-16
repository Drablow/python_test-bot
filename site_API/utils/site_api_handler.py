import json
import re
from typing import Dict

import requests
from aiogram import types


def _make_response(method: str, url: str, headers: Dict, params: Dict, timeout: int, success=200):
    """
    Выполнение HTTP-запроса к Hotels API (rapidapi.com) (Поиск локаций (городов)) и проверяем статус 200.
    """
    response = requests.request(method, url, headers=headers, params=params, timeout=timeout)

    status_code = response.status_code

    if status_code == success:
        return response

    return status_code


def _location_search(message: types.Message, url_dict: Dict, headers: Dict, lang: str, func=_make_response) -> Dict[
    str, str]:
    """
    Выполнение HTTP-запроса к Hotels API (rapidapi.com) (Поиск локаций (городов)).
    :param message: сообщение пользователя
    :return: словарь, содержащий сведения локаций (городов)
    """

    querystring = {"query": message.text, "locale": lang}
    response = func("GET", url_dict['city_url'], headers=headers, params=querystring, timeout=10)
    data = json.loads(response.text)

    city_dict = {', '.join((city['name'], re.findall('(\\w+)[\n<]', city['caption'] + '\n')[-1])): city['geoId']
                 for city in data['suggestions'][0]['entities']}
    return city_dict


def _hotel_search(data: Dict):
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {'currency': 'USD',
               'eapid': 1,
               'locale': 'ru_RU',
               'siteId': 300000001,
               'destination': {
                   'regionId': data.get('regionId')  # id из первого запроса
               },
               'checkInDate': {
                   'day': data.get('checkInDay'),
                   'month': data.get('checkInMonth'),
                   'year': data.get('checkInYear')
               },
               'checkOutDate': {
                   'day': data.get('checkOutDay'),
                   'month': data.get('checkOutMonth'),
                   'year': data.get('checkOutYear')
               },
               'rooms': [{'adults': data.get('adults')}],
               'resultsStartingIndex': 0,
               'resultsSize': 10,
               'sort': 'PRICE_LOW_TO_HIGH',
               "filters": {
                   "price": {
                       "max": data.get('max'),
                       "min": data.get('min')
                   }
               }
               }

    # payload = {
    #     "currency": "USD",
    #     "eapid": 1,
    #     "locale": "en_US",
    #     "siteId": 300000001,
    #     "destination": {"regionId": "3000"},
    #     "checkInDate": {
    #         "day": 10,
    #         "month": 10,
    #         "year": 2022
    #     },
    #     "checkOutDate": {
    #         "day": 15,
    #         "month": 10,
    #         "year": 2022
    #     },
    #     "rooms": [{"adults": 2}],
    #     "resultsStartingIndex": 0,
    #     "resultsSize": 200,
    #     "sort": "PRICE_LOW_TO_HIGH",
    #     "filters": {"price": {
    #         "max": 150,
    #         "min": 100
    #     }}
    # }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "56a3f34904msh1777fc4fdb5417dp1937d9jsnbcae13bb743d",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    data = json.loads(response.text)
    hotels_list = data['data']['propertySearch']['properties']

    if not hotels_list:
        return None, None


    print(f'Найдено {len(hotels_list)} отелей')
    for i in range(len(hotels_list)):
        print(hotels_list[i]['name'])


class SiteApiInterface():

    @staticmethod
    def get_location():
        return _location_search

    @staticmethod
    def get_hotel():
        return _hotel_search


if __name__ == "__main__":
    _make_response()
    _location_search()
    _hotel_search()

    SiteApiInterface()
