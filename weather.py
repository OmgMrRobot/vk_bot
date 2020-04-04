from bs4 import BeautifulSoup
import requests


class Weather():
    web_weather = "https://yandex.ru/search/?text=%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0&&lr=213"
    headers = {
        'user-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}

    # что ты браузер не думал, что мы бот

    def get_currency_weather(self):
        full_page = requests.get(self.web_weather, headers=self.headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        temperature = soup.findAll('div', {"class": "weather-forecast__current-temp"})
        weather_type = soup.findAll('div', {"class": "weather-forecast__current-details"})

        temperature = temperature[0].text
        weather_type = weather_type[0].text

        # сначала пишется тег, затем слассы соответсвтвующие

        for i in range(0, len(weather_type)):
            if weather_type[i].isdigit():
                break

        return f'Погода сейчас: {weather_type[:i]} {temperature} ' # достаем знаначение
