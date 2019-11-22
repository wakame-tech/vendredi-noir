#!/usr/bin/env python
from threading import Lock
import logging
from flask import Flask, session, request, copy_current_request_context, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

async_mode = None

l = logging.getLogger()
l.addHandler(logging.FileHandler("/dev/null"))
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")
# thread = None
# thread_lock = Lock()

# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         socketio.sleep(10)
#         count += 1
#         socketio.emit('my_response',
#                       {'data': 'Server generated event', 'count': count},
#                       namespace='/test')


# @app.route('/')
# def index():
#     return render_template('index.html', async_mode=socketio.async_mode)

# @socketio.on('join', namespace='/test')
# def join(message):
#     join_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'In rooms: ' + ', '.join(rooms()),
#           'count': session['receive_count']})


# @socketio.on('leave', namespace='/test')
# def leave(message):
#     leave_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'In rooms: ' + ', '.join(rooms()),
#           'count': session['receive_count']})


# @socketio.on('close_room', namespace='/test')
# def close(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
#                          'count': session['receive_count']},
#          room=message['room'])
#     close_room(message['room'])


# @socketio.on('my_room_event', namespace='/test')
# def send_room_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']},
#          room=message['room'])


# @socketio.on('disconnect_request', namespace='/test')
# def disconnect_request():
#     @copy_current_request_context
#     def can_disconnect():
#         disconnect()

#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'Disconnected!', 'count': session['receive_count']},
#          callback=can_disconnect)

def print_board(res):
    t, pos = res["falling"]["type"], res["falling"]["pos"]
    print('{} ({}, {})'.format(t, pos[0], pos[1]), end="\n\n")
    # for row in res["board"]:
    #     print(row)

def room_id(sid):
    return [r for r in rooms(sid) if r != sid][0]

@socketio.on('connect')
def on_connect():
    print('connected %s' % request.sid)
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         pass
            # thread
            # socketio.start_background_task(background_thread)

@socketio.on('request_create_room')
def on_create_room(req):
    room_name = req["room_name"]
    join_room(room_name)
    print('create room %s' % room_id(request.sid))
    emit('response_create_room', { "room_name": room_name }, room=room_name)

@socketio.on('request_join_room')
def on_create_room(req):
    room_name = req["room_name"]
    join_room(room_name)
    print('join %s to %s' % (request.sid, room_id(request.sid)))
    emit('response_join_room', { "room_name": room_name }, room=room_name)

@socketio.on('request_game_start')
def res(req):
    room_name = room_id(request.sid)
    print(room_id(request.sid))
    emit('response_game_start', {}, room=room_name)

@socketio.on('request_move')
def on_move(req):
    room_name = room_id(request.sid)
    print_board(req)
    emit('response_board', req, broadcast=True, room=room_name)

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
