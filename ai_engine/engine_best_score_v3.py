import copy
from ai_engine import AIEngine

MOVE_CHOICES = ['UP', 'RIGHT', 'DOWN', 'LEFT']


class BestScore(AIEngine):

    async def next_move(self, state):
        action_states = await self._states_for_all_possible_moves(state)
        print('action_scores ', [(action, state['score']) for action, state in action_states])

        max_action_scores = [(action, await self._find_max_score_from_all_possibilities(state, new_tile_value=4))
                             for action, state in action_states]
        print('min_action_scores ', [(action, int(new_score) - int(state['score']))
                                     for action, new_score in max_action_scores])
        max_action_score = max(max_action_scores, key=lambda a_s: a_s[1])
        print('max_action_score ', (max_action_score[0], max_action_score[1] - state['score']))
        return max_action_score[0]

    async def _execute_action(self, state, action):
        result = await self._oracle.play(state, action)
        return result['state']

    async def _find_min_score_from_all_possibilities(self, state, new_tile_value=2):
        result = await self._oracle.empty_cells(state)
        # print('==> before')
        # print_grid(state)
        # print('==> after')
        new_states = [BestScore._new_state(state, position, new_tile_value) for position in result.get('positions', [])]

        min_scores = []
        for new_state in new_states:
            action_states = await self._states_for_all_possible_moves(new_state)
            # print('action_scores with tile %s ' % new_tile_value, [(action, state['score'])
            #                                                        for action, state in action_states])
            if len(action_states) > 0:
                min_score_action = min(action_states, key=lambda a_s: a_s[1]['score'])
                min_scores.append(min_score_action[1]['score'])

        return min(min_scores) if len(min_scores) > 0 else 0

    async def _find_max_score_from_all_possibilities(self, state, new_tile_value=4):
        result = await self._oracle.empty_cells(state)
        # print('==> before')
        # print_grid(state)
        # print('==> after')
        new_states = [BestScore._new_state(state, position, new_tile_value) for position in result.get('positions', [])]

        max_scores = []
        for new_state in new_states:
            action_states = await self._states_for_all_possible_moves(new_state)
            # print('action_scores with tile %s ' % new_tile_value, [(action, state['score'])
            #                                                        for action, state in action_states])
            if len(action_states) > 0:
                max_score_action = min(action_states, key=lambda a_s: a_s[1]['score'])
                max_scores.append(max_score_action[1]['score'])

        return max(max_scores) if len(max_scores) > 0 else 0

    async def _states_for_all_possible_moves(self, state):
        result = await self._oracle.available_moves(state)
        move_choices = [option['action'] for option in result.get('moves', []) if option.get('available', False)]
        action_states = [(action, await self._execute_action(state, action)) for action in move_choices]
        return action_states

    @staticmethod
    def _new_state(state, new_tile_pos, new_tile_value=2):
        new_state = copy.deepcopy(state)
        row_num_to_update = new_tile_pos['x']
        col_num_to_update = new_tile_pos['y']
        new_state['grid']['cells'][row_num_to_update][col_num_to_update] = {
            'position': new_tile_pos,
            'value': new_tile_value
        }
        return new_state
