"""
@author: wakame-tech
"""

import socketio
import os
import time
import sys


# standard Python
sio = socketio.Client()


def mock():
    """
    """
    return {
        "score": 120,
        "falling":  {
            "type": "O",
            "pos": [3, 5]
        },
        "next": "J",
        "board": [
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000001",
            "0000003301",
            "0000033201",
            "0011112221",
        ],
        "isDead": False
    }


def prettify_board(res):
    """
    """
    t, pos = res['falling']['type'], res['falling']['pos']
    return '%s (%s, %s)\n%s' % (t, pos[0], pos[1], '\n'.join(res['board']))


@sio.event
def connect():
    print('connected')


@sio.event
def disconnect():
    print("disconnected")
    sys.exit(1)


def create_room(room_name):
    """
    """
    print('create room')
    sio.emit('request_create_room', {"room_name": room_name})


@sio.on('response_create_room')
def on_create_room(res):
    """
    """
    print('created')


def join_room(room_name):
    """
    """
    sio.emit('request_join_room', {"room_name": room_name})


@sio.on('response_join_room')
def on_join_room(res):
    print('joined')


def game_start(room_name):
    """
    """
    print('game start')
    sio.emit('request_game_start', {"room_name": room_name})


@sio.on('response_game_start')
def on_game_start(res):
    print('game started')


def game_end(room_name):
    """
    """
    print('game end')
    sio.emit('request_game_end', {"room_name": room_name})


@sio.on('response_game_end')
def on_game_end(res):
    """
    """
    print('game ended')
    sys.exit(0)


def move():
    """
    """
    sio.emit('request_move', mock())


@sio.on('response_board')
def on_board(res):
    """
    """
    print(prettify_board(res))

ENDPOINT = 'https://vendredi-noir.herokuapp.com'
# ENDPOINT = 'http://localhost:5000'

if __name__ == '__main__':
    sio.connect(ENDPOINT)

    room_name = 'AAA'

    if len(sys.argv) >= 2 and sys.argv[1] == 'join':
        join_room(room_name)
    else:
        create_room(room_name)

    time.sleep(10)

    game_start(room_name)

    i = 3
    while i > 0:
        time.sleep(2)
        i -= 1
        move()

    game_end(room_name)
