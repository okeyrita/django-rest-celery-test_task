import logging

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from test_task.celery import app

import xml.etree.ElementTree as ET
import requests
import json

URL = 'https://www.cbr-xml-daily.ru/daily.xml'
DATA_PATH = 'data/'
FILENAME = 'data.csv'
DATA_FILE = 'currency.txt'

LOGGER = logging.getLogger(__file__)


@app.task
def daily_request():

    r = requests.get(URL)

    with open(DATA_PATH+FILENAME, 'wb') as f:
        f.write(r.content)

    data = {}
    events = ("start",)
    for event, elem in ET.iterparse(DATA_PATH+FILENAME, events=events):
        if elem.tag == "Valute" and event == "start":
            if elem.get('ID') == 'R01239':
                data.update({
                    'EUR': elem.find('Value').text
                })
            elif elem.get('ID') == 'R01235':
                data.update({
                    'USD': elem.find('Value').text
                })

    with open(DATA_PATH+DATA_FILE, "w", encoding="utf-8") as filee:
        json.dump(data, filee)

    return True