"""😈"""

__version__ = "0.2"

import threading


def ferenc():
    while True:
        print('Gyurcsány')


x = threading.Thread(target=ferenc)
x.start()
x.join()
