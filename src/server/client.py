import socketio

# standard Python
sio = socketio.Client()
sio.connect('http://localhost:8000')

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def disconnect():
    print("I'm disconnected!")