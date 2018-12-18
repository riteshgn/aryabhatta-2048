from ai_engine import AIEngine

MOVE_CHOICES = ['UP', 'RIGHT', 'DOWN', 'LEFT']


class BestScore(AIEngine):

    async def next_move(self, state):
        result = await self._oracle.available_moves(state)
        move_choices = [option['action'] for option in result.get('moves', []) if option.get('available', False)]
        print('available actions', move_choices)

        scores = [(action, await self._fetch_score(state, action)) for action in move_choices]
        print(scores)

        action_score = max(scores, key=lambda a_s: a_s[1])
        selected_action = action_score[0]

        return selected_action

    async def _fetch_score(self, state, move):
        result = await self._oracle.play(state, move)
        return result['state']['score']
