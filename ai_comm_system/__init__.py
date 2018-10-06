import socketio
from .namespace_game import GameNamespace


def setup(app):
    sio = socketio.AsyncServer()
    sio.register_namespace(GameNamespace('/game'))
    sio.attach(app)
