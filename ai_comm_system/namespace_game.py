import socketio
from .message_processor_game import GameMessages


class GameNamespace(socketio.AsyncNamespace):

    def __init__(self, namespace):
        super(GameNamespace, self).__init__(namespace)
        self._game_messages = GameMessages()

    def on_connect(self, sid, environ):
        print("client connected to game namespace ", sid)

    def on_disconnect(self, sid):
        print('client disconnected from game namespace ', sid)

    async def on_message(self, sid, data):
        result = self._game_messages.handle(data)

        if result.get('respond', False):
            await self.emit('message', result.get('payload', None), namespace='/game')
