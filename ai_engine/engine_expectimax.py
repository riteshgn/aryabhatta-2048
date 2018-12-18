from ai_engine import AIEngine
from ai_utils import insert_tile, minified_grid

DEFAULT_MAX_DEPTH = 2


class Expectimax(AIEngine):

    async def next_move(self, state):
        selected_action = await expectimax(self._oracle, state)
        return selected_action[0]


async def expectimax(oracle, state, max_depth=DEFAULT_MAX_DEPTH, player=0):
    print('[level={depth}] [player={player}] grid={grid}'.format(
        depth=max_depth, player='AI' if player == 0 else 'Chance', grid=minified_grid(state)))

    if state['over'] or max_depth == 0:
        print('[level={depth}] [player={player}] score={score} game_over={game_over} '
              'max_depth_reached={max_depth_reached}'.format(depth=max_depth,
                                                             player='AI' if player == 0 else 'Chance',
                                                             score=state['score'], game_over=state['over'],
                                                             max_depth_reached=(max_depth == 0)))
        return None, state['score']

    available_moves = await oracle.available_moves(state)
    available_action_states = [(option['action'], option['state'])
                               for option in available_moves.get('moves', []) if option.get('available', False)]

    # main player i.e. AI
    if player == 0:
        action_plays = [(action, await expectimax(oracle, new_state, max_depth - 1, player=1))
                        for action, new_state in available_action_states]
        action_scores = [(action, play[1]) for action, play in action_plays]
        max_action_score = max(action_scores, key=lambda a_s: a_s[1])
        print('[level={depth}] [player={player}] max_score={score} for action={action}'.format(
            depth=max_depth, player='AI' if player == 0 else 'Chance',
            score=max_action_score[1], action=max_action_score[0]))
        return max_action_score

    # chance player i.e. either the 2 or 4 tile
    if player == 1:
        result = await oracle.empty_cells(state)
        new_states = \
            [insert_tile(state, position, new_tile_value=2) for position in result.get('positions', [])] + \
            [insert_tile(state, position, new_tile_value=4) for position in result.get('positions', [])]

        # Pr = (chance of 2 or 4) * (chance appearing in one of the empty cells) = 0.5 * (1/number of empty cells)
        probability = 0.5 / len(result)

        action_scores = [await expectimax(oracle, probable_state, max_depth, player=0) for probable_state in new_states]
        probable_action_scores = [(action, probability * score) for action, score in action_scores]
        min_action_score = min(probable_action_scores, key=lambda a_s: a_s[1])
        print('[level={depth}] [player={player}] min_score={score} for action={action}'.format(
            depth=max_depth, player='AI' if player == 0 else 'Chance',
            score=min_action_score[1], action=min_action_score[0]))
        return min_action_score


async def _execute_action(oracle, state, action):
    result = await oracle.play(state, action)
    return result['state']
