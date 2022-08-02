import os
import threading
import time

from flask import Flask

app = Flask(__name__)
count = 0
print('\n'.join([f'{k}: {v}' for k, v in sorted(os.environ.items())]))


@app.route('/')
def hello_world():
    return f'I am {os.getenv("ENV")}'


def poll():
    global count
    while True:
        print(f"Polling: {count}")
        has_db = os.getenv("HAS_DB")
        if has_db:
            print("Testing DB access")

        has_redis = os.getenv("HAS_REDIS")
        if has_redis:
            print("Testing Redis access")

        time.sleep(10)
        count += 1


if __name__ == '__main__':
    th = threading.Thread(target=poll)
    th.start()

    app.run()
