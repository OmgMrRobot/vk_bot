from typing import Dict, List, Union

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randint
import vk_api
import datetime
import data
import time
from weather import Weather
import tuturu


class Bot:
    clouds = {
        'облако': 'https://cloud.mail.ru/public/NAzt/FJpjdhFpZ',
        'облако мыкольникова': 'https://yadi.sk/d/IN37NgpLzhI1SA',
    }

    contacts = data.contacts
    contacts_2 = data.contacts_2
    contacts_3 = data.contacts_3
    bot_name = ['bot', 'хлам', 'start', 'xlam', 'бот', 'старт', 'дуц']

    def __init__(self):
        self.token = data.token
        self.group_id = data.group_id
        self.vk_session = vk_api.VkApi(token=self.token)
        self.session_api = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, self.group_id)

    def create_keyboard(self, payload):
        keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

        if payload == 2:
            keyboard.add_button('Облако', payload=5, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            # keyboard.add_button('Облако Сережи', payload=6, color=VkKeyboardColor.PRIMARY)
            # keyboard.add_line()
            keyboard.add_button('Облако Мыкольникова', payload=7, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Главное меню', payload=1, color=VkKeyboardColor.PRIMARY)

        elif payload == 10:
            n = 11
            for response in self.contacts.keys():
                keyboard.add_button(response.title(), payload=n, color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                n += 1
            keyboard.add_button('Cледующая страница', payload=n, color=VkKeyboardColor.PRIMARY)

        elif payload == 20:
            n = 21
            for response in self.contacts_2.keys():
                keyboard.add_button(response.title(), payload=n, color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                n += 1
            keyboard.add_button('Cледующая страница', payload=n, color=VkKeyboardColor.PRIMARY)

        elif payload == 30:
            n = 31
            for response in self.contacts_3.keys():
                keyboard.add_button(response.title(), payload=n, color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                n += 1
            keyboard.add_button('Главное меню', payload=1, color=VkKeyboardColor.PRIMARY)

        elif payload == 71:
            keyboard.add_button('Авиа -> Ильинская', payload=72, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Авиа -> Хрипань', payload=73, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Ильинская -> Авиа', payload=74, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Хрипань -> Авиа', payload=75, color=VkKeyboardColor.PRIMARY)




        elif payload == 4:
            return keyboard.get_empty_keyboard()

        else:
            keyboard.add_button('Хочу облако', payload=2, color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('Погода', payload=3, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Расписание на сегодня', payload=70, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Какая сейчас неделя', payload=8, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Контакты преподавателя', payload=10, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Электрички', payload=71, color=VkKeyboardColor.PRIMARY)
            # keyboard.add_line()
            # keyboard.add_button('Закрыть быстрый ввод', payload=4, color=VkKeyboardColor.PRIMARY)

        return keyboard.get_keyboard()

    def send_message(self, peer_id, message=None, attachment=None, keyboard=None, payload=None):
        self.session_api.messages.send(peer_id=peer_id, message=message, random_id=randint(-2147483648, +2147483648),
                                       attachment=attachment, keyboard=keyboard, payload=payload)

    def if_response_contain_name(self, response):
        if response.rfind('[club193592175|@xlam__bot]') != -1:
            response = response[27:]
        return response

    def main_method(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.obj.payload != None:
                    payload = int(event.obj.payload)
                else:
                    payload = None

                response = self.if_response_contain_name(event.obj.text.lower())
                if not event.obj.from_me:

                    sender_name = list(filter(lambda name: name['id'] == event.obj.from_id, [name for name in
                                                                                             self.session_api.messages.getConversationMembers(
                                                                                                 peer_id=event.obj.peer_id,
                                                                                                 fields='profiles')[
                                                                                                 'profiles']]))[0]

                    first_name = str(sender_name['first_name'])

                    keyboard = self.create_keyboard(payload)
                    if response in self.bot_name or payload == 1:
                        self.send_message(peer_id=event.obj.peer_id,
                                          message='О чем ты хочешь узнать {0}?'.format(first_name), keyboard=keyboard)
                    elif payload == 3:
                        weather = Weather()
                        self.send_message(peer_id=event.obj.peer_id,
                                          message=weather.get_currency_weather(), keyboard=keyboard)
                    elif payload == 2:
                        self.send_message(peer_id=event.obj.peer_id,
                                          message='Какое облако вы хотите, {0}'.format(first_name), keyboard=keyboard)
                    elif 5 <= payload <= 7:
                        self.send_message(peer_id=event.obj.peer_id, message=self.clouds[response], keyboard=keyboard)
                    elif payload == 8:
                        self.send_message(peer_id=event.obj.peer_id, message=self.which_week_is_now()[0],
                                          keyboard=keyboard)
                    elif payload == 10:
                        self.send_message(peer_id=event.obj.peer_id,
                                          message='Чьи контакты вы хотите, {0}'.format(first_name), keyboard=keyboard)
                    elif 11 <= payload < 20:
                        self.send_message(peer_id=event.obj.peer_id, message=self.contacts[response], keyboard=keyboard)
                    elif 21 <= payload < 30:
                        self.send_message(peer_id=event.obj.peer_id, message=self.contacts_2[response],
                                          keyboard=keyboard)
                    elif 31 <= payload <= 32:
                        self.send_message(peer_id=event.obj.peer_id, message=self.contacts_3[response],
                                          keyboard=keyboard)
                    elif payload == 20 or payload == 30:
                        self.send_message(peer_id=event.obj.peer_id,
                                          message='Cледующая страница, {0}'.format(first_name), keyboard=keyboard)
                    elif payload == 70:
                        self.send_message(peer_id=event.obj.peer_id, message=self.which_week_is_now()[1],
                                          keyboard=keyboard)
                    elif payload == 71:
                        self.send_message(peer_id=event.obj.peer_id, message='Выбери страница, {0}'.format(first_name),
                                          keyboard=keyboard)
                    elif payload == 72:
                        self.send_message(peer_id=event.obj.peer_id,
                                          message=f"Следующие электрички {' '.join(tuturu.train(72)[:2])}",
                                          keyboard=keyboard)
                    elif payload == 73:
                        self.send_message(peer_id=event.obj.peer_id,
                                          message=f"Следующие электрички {' '.join(tuturu.train(73)[:2])}",
                                          keyboard=keyboard)
                    elif payload == 74:
                        self.send_message(peer_id=event.obj.peer_id,
                                          message=f"Следующие электрички {' '.join(tuturu.train(74)[:2])}",
                                          keyboard=keyboard)
                    elif payload == 75:
                        self.send_message(peer_id=event.obj.peer_id,
                                          message=f"Следующие электрички {' '.join(tuturu.train(75)[:2])}",
                                          keyboard=keyboard)

    def which_week_is_now(self):
        Date = datetime.datetime.now()
        numbrer_of_the_week = datetime.datetime.isocalendar(Date)[1]
        if numbrer_of_the_week > 34:
            numbrer_of_the_week -= 35
        else:
            numbrer_of_the_week -= 6
        if numbrer_of_the_week % 2 == 0:
            return [f'{numbrer_of_the_week} неделя, Знаменатель',
                    data.time_table[2][datetime.datetime.isoweekday(Date)]]
        else:
            return [f'{numbrer_of_the_week} неделя, Числитель', data.time_table[1][datetime.datetime.isoweekday(Date)]]


while True:
    start = Bot()

    try:
        start.main_method()
    except KeyboardInterrupt:
        break
    except:
        del start
        time.sleep(10)
