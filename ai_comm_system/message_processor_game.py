from ai_utils import print_grid


class GameMessages(object):

    def __init__(self, engine):
        self._ai_engine = engine

    async def handle(self, data):
        print('\nmessage ', data)

        if data['key'] == 'play' and data['state']['over']:
            print_grid(data['state'])
            print('\nGame is over! Score: %s' % data['state']['score'])
            return {'respond': False}

        if data['key'] == 'play':
            print_grid(data['state'])

            selected_move = await self._ai_engine.next_move(data['state'])
            print('selected move ', selected_move)

            my_move = {
                'key': 'game_my_move',
                'choice': selected_move
            }
            return {'respond': True, 'payload': my_move}

        return {'respond': False}

