from flask import Flask, request
import config
import psycopg2
import requests
import modules
import re


app = Flask(__name__)


def update_currency(cur):
    """
    write currencies to database
    return string of all available rates
    """
    result = False
    db_time = modules.time_currency(cur)
    if db_time is None:
        print('add_currency')
        dict_of_currency, time = get_all_rates()
        for name, value in dict_of_currency.items():
            db_value = int(modules.rounded(value, 2) * 100)
            modules.add_currency(name, db_value, cur, time)
        result = True

    elif modules.time_delta(db_time) > 600:
        print('update_currency')
        dict_of_currency, time = get_all_rates()
        for name, value in dict_of_currency.items():
            db_value = int(modules.rounded(value, 2) * 100)
            modules.update_currency(name, db_value, cur, time)
        result = True
    return result


def send_message(chat_id, text):
    method = "sendMessage"
    token = config.TELEGRAMBOT_KEY
    url = f'https://api.telegram.org/bot{token}/{method}'
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


def get_all_rates():
    access_key = config.EXCHANGERATE_KEY
    url = f"https://api.fastforex.io/fetch-all?api_key={access_key}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()['results'], response.json()['updated']


def get_currency_list(cur, command):
    print('get_currency_list')
    result = []
    cur.execute('SELECT name, value FROM usd_currency')
    row = cur.fetchone()
    while row is not None:
        result.append(f'{row[0]}: {row[1] / 100}\n')
        row = cur.fetchone()
    return result


def exchange(cur, command):
    pattern = r"(^/exchange\s+\$[0-9]+.+[A-Z]{3}$)|(^/exchange\s+[0-9]+\sUSD.+[A-Z]{3}$)"
    result = []
    print(command)
    if re.match(pattern, command):
        quantity = re.findall(r'[0-9]+', command)[0]
        name = re.findall(r'[A-Z]{3}$', command)[0]
        value = modules.get_currency_value(cur, name)
        result.append(f'${value * int(quantity)}\n')
    else:
        result.append("Incorrect pattern. Please use example:'/exchange $10 to CAD'")
    return result


def start(cur, command):
    return ['Welcome']


commands = {
    '/list': get_currency_list,
    '/lst': get_currency_list,
    '/exchange': exchange,
    '/start': start
}


@app.route('/', methods=["POST"])
def process():
    message_info = request.json.get('message', request.json.get('edited_message', {}))
    command_line = message_info.get('text')
    command_line = command_line.strip()
    command = command_line.split(' ')[0]
    if command in commands:
        conn = None
        try:
            conn = psycopg2.connect(config.DATABASE_URL)
            cur = conn.cursor()
            if update_currency(cur) is True:
                conn.commit()
            result = commands[command](cur=cur, command=command_line)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            result = str(error)
        finally:
            if conn is not None:
                conn.close()
    else:
        result = ['There is no such command.']

    chat_id = request.json['message']['chat']['id']
    send_message(chat_id=chat_id, text=''.join(result))
    return "True"


if __name__ == '__main__':
    app.run()
