import sys
import time
from client import api, connect, create_room, join_room, game_start, game_end, move

# ENDPOINT = 'https://vendredi-noir.herokuapp.com'
ENDPOINT = 'http://localhost:5000'

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
    return res
    # t, pos = res['falling']['type'], res['falling']['pos']
    # # return '%s (%s, %s)\n%s' % (t, pos[0], pos[1], '\n'.join(res['board']))
    # return '%s (%s, %s)' % (t, pos[0], pos[1])


"""
Event Handlers
"""
@api('connected')
def connected():
    print('[Connected]')


@api('disconnected')
def disconnected():
    print("[Disconnected]")
    sys.exit()


@api('room_created')
def room_created(res):
    print('created')


@api('room_joined')
def room_joined(res):
    print('joined')


@api('updated')
def update(res):
    print(prettify_board(res))


@api('game_started')
def game_started(res):
    print('game started')


@api('game_ended')
def game_ended(res):
    print('game ended')
    sys.exit()


"""
Usage:
# as host
python client_eexample.py
# as member
python client_eexample.py --join
"""
if __name__ == '__main__':
    connect(ENDPOINT)
    room_name = 'AAA'

    if len(sys.argv) >= 2 and sys.argv[1] == '--join':
        join_room(room_name)
    else:
        create_room(room_name)

    print('waiting 10s ...')
    time.sleep(10)

    game_start(room_name)

    i = 5
    while i > 0:
        i -= 1
        move(input())

    game_end(room_name)
