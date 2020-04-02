from typing import Dict, List, Union

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randint
import vk_api
import datetime
import data


class Bot:
    clouds = {'облако сережи': 'https://yadi.sk/d/zkdaamG-Ol-sjg',
              'облако': 'https://cloud.mail.ru/public/NAzt/FJpjdhFpZ',
              'облако мыкольникова': 'https://yadi.sk/d/IN37NgpLzhI1SA',
              }

    contacts = data.contacts

    contacts_2 = data.contacts_2

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
            keyboard.add_button('Облако Сережи', payload=6, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Облако Мыкольникова', payload=7, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Главное меню', payload=1, color=VkKeyboardColor.PRIMARY)

        elif payload == 10:
            n = 11
            for response in self.contacts.keys():
                keyboard.add_button(response, payload=n, color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                n += 1
            keyboard.add_button('Cледующая страница', payload=n, color=VkKeyboardColor.PRIMARY)

        elif payload == 20:
            n = 21
            for response in self.contacts_2.keys():
                keyboard.add_button(response, payload=n, color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                n += 1
            keyboard.add_button('Главное меню', payload=1, color=VkKeyboardColor.PRIMARY)


        elif payload == 4:
            print('Закрываем клаву')
            return keyboard.get_empty_keyboard()

        else:
            keyboard.add_button('Хочу облако', payload=2, color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('Расписание', payload=1, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Какая сейчас неделя', payload=8, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Контакты преподавателя', payload=10, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Закрыть быстрый ввод', payload=4, color=VkKeyboardColor.PRIMARY)

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
                # print('Текст сообщения: ' + str(event.obj.text))
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
                    print(
                        f'Текст сообщения: {response} ,от {sender_name["first_name"]} id: {sender_name["id"]}  {datetime.datetime.now()}')
                    first_name = str(sender_name['first_name'])

                    keyboard = self.create_keyboard(payload)
                    if response == 'start' or payload == 1:
                        self.send_message(peer_id=event.obj.peer_id,
                                          message='О чем ты хочешь узнать {0}?'.format(first_name), keyboard=keyboard)
                    elif payload == None:
                        pass
                    elif payload == 2:
                        self.send_message(peer_id=event.obj.peer_id,
                                          message='Какое облако вы хотите, {0}'.format(first_name), keyboard=keyboard)
                    elif 5 <= payload <= 7:
                        self.send_message(peer_id=event.obj.peer_id, message=self.clouds[response], keyboard=keyboard)
                    elif payload == 8:
                        self.send_message(peer_id=event.obj.peer_id, message=self.which_week_is_now(),
                                          keyboard=keyboard)
                    elif payload == 10:
                        self.send_message(peer_id=event.obj.peer_id,
                                          message='Чьи контакты вы хотите, {0}'.format(first_name), keyboard=keyboard)
                    elif 11 <= payload < 20:
                        self.send_message(peer_id=event.obj.peer_id, message=self.contacts[response], keyboard=keyboard)
                    elif 21 <= payload <= 28:
                        self.send_message(peer_id=event.obj.peer_id, message=self.contacts_2[response],
                                          keyboard=keyboard)
                    elif payload == 20:
                        self.send_message(peer_id=event.obj.peer_id,
                                          message='Cледующая страница, {0}'.format(first_name), keyboard=keyboard)

    def which_week_is_now(self):
        # Date = datetime.date(2020, 2, 8)
        # day_of_the_week = datetime.datetime.isocalendar(Date)[2]
        # numbrer_of_the_week = datetime.datetime.isocalendar(Date)[1]
        # print(Date)
        # print(day_of_the_week)
        # print(numbrer_of_the_week)
        Date = datetime.datetime.now()
        day_of_the_week = datetime.datetime.isocalendar(Date)[2]
        numbrer_of_the_week = datetime.datetime.isocalendar(Date)[1]
        numbrer_of_the_week -= 6
        print(Date)
        print(day_of_the_week)
        print(numbrer_of_the_week)
        if numbrer_of_the_week % 2 == 0:
            print('Знаменатель')
            return f'{numbrer_of_the_week} неделя, Знаменатель'
        else:
            print('Числитель')
            return f'{numbrer_of_the_week} неделя, Числитель'


start = Bot()
start.main_method()
