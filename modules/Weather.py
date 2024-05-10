import json

from bs4 import BeautifulSoup
from curl_cffi import requests
from fuzzywuzzy import fuzz

from data.config import WEATHER_DEFAULT_CITY, WEATHER_URL


class Weather:
    def __init__(self):
        self.default_city = WEATHER_DEFAULT_CITY
        self.url = WEATHER_URL

    def get_info(self, city: str) -> str:
        try:
            response = requests.get(f"{self.url}/{city}", impersonate="chrome110")
            soup = BeautifulSoup(response.text, "html.parser")
            card = soup.find(
                "div",
                class_=["fact", "fact_prec_rain-low", "card", "card_size_big"]
            )
            info = card.find(
                "div",
                class_=["fact__temp-wrap"]
            )
            temp = info.find(
                "span",
                class_=["temp__value", "temp__value_with-unit"]
            ).text
            weather = info.find(
                "div",
                class_=["link__condition", "day-anchor i-bem"]
            ).text.lower()
            return f"За окном {temp}, {weather}"
        except AttributeError:
            return self.get_info(self.default_city)

    def validate_city(self, voice: str) -> str:
        validate_voice = voice.split(" ")[-1]
        rc = {'cmd': '', 'percent': 0}
        data = json.load(open("data/weather_city.json"))
        for ru, en in data.items():
            vrt = fuzz.ratio(validate_voice.lower(), ru.lower())
            if vrt > rc['percent']:
                rc['cmd'] = en.lower()
                rc['percent'] = vrt
        if rc['percent'] > 80:
            return rc['cmd']
        return self.default_city
