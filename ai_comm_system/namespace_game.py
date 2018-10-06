import socketio
import random

MOVE_CHOICES = {
    0: 'UP',
    1: 'RIGHT',
    2: 'DOWN',
    3: 'LEFT'
}


class GameNamespace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        print("connect ", sid)

    def on_disconnect(self, sid):
        print('disconnect ', sid)

    async def on_message(self, sid, data):
        print("message ", data)

        if data['key'] == 'state':
            print("state ", data['state'])

        if data['key'] in ['play', 'state']:
            selected_move = MOVE_CHOICES[random.randint(0, 3)]
            print("selected move ", selected_move)
            my_move = {
                'key': 'my_move',
                'choice': selected_move
            }
            await self.emit('message', my_move, namespace='/game')
        else:
            await self.emit('message', namespace='/game')