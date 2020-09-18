
import requests
import json
import data

class Weather():
    key = data.keyowm
    w = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q=Moscow,ru&appid={key}')

    def kelvin_to_celsius(self, temp):
        return str(int(temp) - 273)

    def get_currency_weather(self):
        w = json.loads(self.w.text)
        return f'Погода сейчас: {w["weather"][0]["main"]}\nТемпература: {self.kelvin_to_celsius(w["main"]["temp"])}\nОщущается как {self.kelvin_to_celsius(w["main"]["feels_like"])} \nВлажность: {w["main"]["humidity"]}'

if __name__ == '__main__':
    w = Weather()
    print(w.get_currency_weather())
