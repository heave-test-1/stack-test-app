import os
import threading
import time

import redis
from flask import Flask
from flask_mysqldb import MySQL


print('\n'.join([f'{k}: {v}' for k, v in sorted(os.environ.items())]))

app = Flask(__name__)
app.config['MYSQL_USER'] = os.getenv("DB_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
app.config['MYSQL_DB'] = os.getenv("DB_DATABASE")
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
count = 0


@app.route('/')
def hello_world():
    has_db = os.getenv("HAS_DB")
    if has_db:
        print("Testing DB access")
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT 1''')
            cursor.fetchall()

    has_redis = os.getenv("HAS_REDIS")
    if has_redis:
        print("Testing Redis access")
        r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=0)
        r.set('foo', 'bar')
        print(r.get('foo'))
    
    return f'I am {os.getenv("ENV")}'


def poll():
    global count
    while True:
        print(f"Polling: {count}")
        has_db = os.getenv("HAS_DB")
        if has_db:
            print("Testing DB access")
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute('''SELECT 1''')
                cursor.fetchall()

        has_redis = os.getenv("HAS_REDIS")
        if has_redis:
            print("Testing Redis access")
            r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=0)
            r.set('foo', 'bar')
            print(r.get('foo'))

        time.sleep(10)
        count += 1


if __name__ == '__main__':
    th = threading.Thread(target=poll)
    th.start()

    app.run(host="0.0.0.0", port=5000)
