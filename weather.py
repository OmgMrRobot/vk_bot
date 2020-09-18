from pyowm import OWM

class Weather():
    key = 'effd2d0dea281ac4073dc1bd354964d1'
    owm = OWM(f'{key}')  # You MUST provide a valid API key

    def get_currency_weather(self):
        mgr = self.owm.weather_manager()
        observation = mgr.weather_at_place('Moscow, RU')
        w = observation.weather
        return f'Погода сейчас: {w.status}\nТемпература: {w.temperature("celsius")["temp"]}\nОщущается как {w.temperature("celsius")["feels_like"]}\nВлажность: {w.humidity}'  # достаем знаначение

if __name__ == '__main__':
    w = Weather()
    print(w.get_currency_weather())
