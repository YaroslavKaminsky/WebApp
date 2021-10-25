from datetime import datetime, timezone, timedelta
import psycopg2
import config


def rounded(number: float, precision: int):
    number = int(number * 10 ** (precision+1))
    if number % 10 < 5:
        result = int(number / 10) / (10 ** precision)
    else:
        result = (int(number / 10) + 1) / (10 ** precision)
    return result


def time_delta(time):
    tzinfo = timezone(timedelta(hours=0.0))
    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    time = time.replace(tzinfo=tzinfo)
    current_time = datetime.now(tzinfo)
    delta = (current_time - time).total_seconds()
    return delta


def time_currency(cur):
    cur.execute("SELECT time_stamp FROM usd_currency WHERE name = 'AED'")
    return cur.fetchone()[0]


def update_currency(name, value, cur, time):
    cur.execute("UPDATE usd_currency SET value = %s, time_stamp = %s WHERE name = %s", (value, time, name,))


def add_currency(name, value, cur, time):
    cur.execute("INSERT INTO usd_currency (name, value, time_stamp) VALUES (%s, %s, %s)", (name, value, time))


def get_currency_value(cur, name):
    print('get_currency_value')
    cur.execute("SELECT value FROM usd_currency WHERE name = %s ORDER BY id DESC", (name, ))
    value = cur.fetchone()[0] / 100
    return value


def clean_db():
    conn = psycopg2.connect(config.DATABASE_URL)
    cur = conn.cursor()
    cur.execute('delete from usd_currency where id > 0')
    conn.commit()
    cur.close()
    conn.close()





