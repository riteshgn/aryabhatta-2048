import socketio


def setup(app):
    sio = socketio.AsyncServer()
    sio.attach(app)
    return sio
