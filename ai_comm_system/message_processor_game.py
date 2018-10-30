from ai_engine.engine_random_moves import RandomMoves as AIEngine


class GameMessages(object):

    def __init__(self):
        self._ai_engine = AIEngine()

    def handle(self, data):
        print('\nmessage ', data)

        if data['key'] == 'play' and data['state']['over']:
            print('\nGame is over! Score: %s' % data['state']['score'])
            return {'respond': False}

        if data['key'] == 'play':
            print("state ", data['state'])

            selected_move = self._ai_engine.next_move(data['state'])
            print('selected move ', selected_move)

            my_move = {
                'key': 'my_move',
                'choice': selected_move
            }
            return {'respond': True, 'payload': my_move}

        return {'respond': False}
