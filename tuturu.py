import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, time



def train(num):
    stations = {"авиа": "7702",
                "ильинская": "9202",
                "хрипань": "13802"
                }
    if num == 72:
        req = f'https://www.tutu.ru/rasp.php?st1={stations["авиа"]}&st2={stations["ильинская"]}'
    elif num == 73:
        req = f'https://www.tutu.ru/rasp.php?st1={stations["авиа"]}&st2={stations["хрипань"]}'
    elif num == 74:
        req = f'https://www.tutu.ru/rasp.php?st1={stations["ильинская"]}&st2={stations["авиа"]}'
    else:
        req = f'https://www.tutu.ru/rasp.php?st1={stations["хрипань"]}&st2={stations["авиа"]}'

    now_ = datetime.now()
    r = requests.get(req)
    bs = BeautifulSoup(r.text, "html.parser")
    bs = bs.findAll('a', class_="g-link desktop__depTimeLink__1NA_N")
    bs = [re.findall("\d\d:\d\d", str(i))[0] for i in bs]

    return [i for i in bs if now_.time() < time(int(i[:2]),int(i[3:]))]


