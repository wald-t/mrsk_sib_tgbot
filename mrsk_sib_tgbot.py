import json
import urllib.request
import requests


class API:
    def __init__(self, link):
        self.api_url = link

    def get(self):
        data = json.loads(urllib.request.urlopen(self.api_url).read().decode('utf-8'))
        return data


class File:
    def __init__(self, fileName):
        self.name = fileName

    def read(self):
        fileData = []
        file = open(self.name, 'r')
        for line in file:
            fileData.append(line)
        file.close()
        return fileData

    def add(self, line):
        file = open(self.name, 'a')
        file.write(line)
        file.close()


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


db = 'text.txt'
config = json.loads(File('config.json').read()[0])
api_url = config.get('api_url')
data = API(api_url).get()
bot = BotHandler(config.get("tg_token"))
users_id = config.get("users_id")

if len(data) > 0:
    file_data = File(db).read()

    for index in data:
        line = ('{"home":"' + index.get('home') + '", "date_start":"' + index.get(
            'date_start') + '", "date_finish":"' + index.get('date_finish') + '"}')
        if not any(line in s for s in file_data):
            File(db).add(line + '\n')
            for user in users_id:
                bot.send_message(user, 'Ожибается отключение электричества по ул. Чапаева в домах: ' + index.get(
                    'home') + '\nНачало отключения: ' + index.get('date_start') +
                                 '\nКонец отключения: ' + index.get('date_finish'))
