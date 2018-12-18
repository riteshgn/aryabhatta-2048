import copy
from ai_engine import AIEngine

from ai_utils import print_grid, insert_tile

MOVE_CHOICES = ['UP', 'RIGHT', 'DOWN', 'LEFT']


class BestScoreWithDepth(AIEngine):

    def __init__(self, oracle, depth=2):
        super(BestScoreWithDepth, self).__init__(oracle)
        self._depth = depth

    async def next_move(self, state):
        selected_action = await self._next_move_at_depth(state, self._depth)
        return selected_action[0]

    async def _next_move_at_depth(self, state, depth):
        result = await self._oracle.available_moves(state)
        actions = [option['action'] for option in result.get('moves', []) if option.get('available', False)]
        min_scores = [await self._find_min_score(action, state, depth) for action in actions]

        selected_action = max(min_scores, key=lambda a_s: a_s[1]['score'])
        # print('[depth: {}] [NMAD] selected_action: {}, score: {}'.format(
        #     depth, selected_action[0], selected_action[1]['score']))
        return selected_action

    async def _find_min_score(self, action, state, depth):
        new_state = await self._execute_action(state, action)

        result = await self._oracle.empty_cells(new_state)
        options = [await self._find_min_score_at_depth(insert_tile(new_state, position, new_tile_value=2), depth)
                   for position in result.get('positions', [])]

        selected_action = min(options, key=lambda a_s: a_s[1]['score'])
        # print('[depth: {}] [FMS] selected_action: {}, score: {}'.format(
        #     depth, selected_action[0], selected_action[1]['score']))
        return selected_action

    async def _find_min_score_at_depth(self, state, depth):
        if depth == 1:
            selected_action = await self._select_move(
                state, pick_one=lambda xs: min(xs, key=lambda a_s: a_s[1]['score']))
            # print('[depth: {}] [FMSAD] selected_action: {}, score: {}'.format(
            #     depth, selected_action[0], selected_action[1]['score']))
            return selected_action

        selected_action = await self._next_move_at_depth(state, depth=depth - 1)
        # print('[depth: {}] [FMSAD] selected_action: {}, score: {}'.format(
        #     depth, selected_action[0], selected_action[1]['score']))
        return selected_action

    async def _select_move(self, state, pick_one):
        result = await self._oracle.available_moves(state)
        actions = [option['action'] for option in result.get('moves', []) if option.get('available', False)]
        action_states = [(action, await self._execute_action(state, action)) for action in actions]
        return pick_one(action_states)

    async def _execute_action(self, state, action):
        result = await self._oracle.play(state, action)
        return result['state']
