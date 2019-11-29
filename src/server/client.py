"""
@author: wakame-tech
"""

import socketio
import os
import time
import sys

sio = socketio.Client()

handlers = {}


def api(event):
    """
    Event Handler of API
    """
    def registerhandler(handler):
        handlers[event] = handler
        return handler
    return registerhandler


@sio.event
def on_connect():
    if 'connected' in handlers:
        handlers['connected']()


@sio.event
def on_disconnect():
    if 'disconnected' in handlers:
        handlers['disconnected']()


@sio.on('response_create_room')
def on_create_room(res):
    if 'room_created' in handlers:
        handlers['room_created'](res)


@sio.on('response_join_room')
def on_join_room(res):
    if 'room_joined' in handlers:
        handlers['room_joined'](res)


@sio.on('response_game_start')
def on_game_start(res):
    if 'game_started' in handlers:
        handlers['game_started'](res)


@sio.on('response_game_end')
def on_game_end(res):
    if 'game_ended' in handlers:
        handlers['game_ended'](res)


@sio.on('response_board')
def on_board(res):
    if 'updated' in handlers:
        handlers['updated'](res)

def connect(endpoint):
    sio.connect(endpoint)

def create_room(room_name):
    """
    """
    print('[Create] %s' % room_name)
    sio.emit('request_create_room', {"room_name": room_name})


def join_room(room_name):
    """
    """
    print('[Join] to %s' % room_name)
    sio.emit('request_join_room', {"room_name": room_name})


def game_start(room_name):
    """
    """
    print('[Game Start]')
    sio.emit('request_game_start', {"room_name": room_name})


def game_end(room_name):
    """
    """
    print('[Game End]')
    sio.emit('request_game_end', {"room_name": room_name})


def move(req):
    """
    """
    print('[Update]')
    sio.emit('request_move', req)
