import json
import time

from ai_engine import AIEngine
from ai_utils import insert_tile, enhance_game_state
from game_heuristics import heur_empty_cells, heur_max_tile_position, heur_monotonicity, heur_losing_penalty, heur_matching_tiles

DEFAULT_MAX_DEPTH = 4
MOVE_CHOICES = ['UP', 'RIGHT', 'DOWN', 'LEFT']

PROBABILITY_NEW_TILE_2 = 0.9
PROBABILITY_NEW_TILE_4 = 1 - PROBABILITY_NEW_TILE_2


class Expectimax(AIEngine):

    async def next_move(self, state):
        t0 = time.time()
        game_state = enhance_game_state(state)
        selected_action = await expectimax(self._oracle, game_state)
        t1 = time.time()
        print('time elapsed:', (t1-t0))
        return selected_action[0]


async def apply_heuristics(oracle, state):
    # tuple (heur_function, weight)
    heuristics = [
        (heur_empty_cells, 10),
        (heur_max_tile_position, 5),
        # (heur_monotonicity, 10),
        (heur_matching_tiles, 25),
        (heur_losing_penalty, 50)
    ]

    if len(heuristics) == 0:
        return state['score']

    heur_scores = sum([await heuristic.apply(oracle, state, weight) for heuristic, weight in heuristics])
    return state['score'] + heur_scores


async def expectimax(oracle, state, max_depth=DEFAULT_MAX_DEPTH, player=0):
    # print('[level={depth}] [player={player}] grid={grid}'.format(
    #     depth=max_depth, player='AI' if player == 0 else 'Chance', grid=minified_grid(state)))

    if state['over'] or max_depth == 0:
        # print('[level={depth}] [player={player}] score={score} game_over={game_over} '
        #       'max_depth_reached={max_depth_reached}'.format(depth=max_depth,
        #                                                      player='AI' if player == 0 else 'Chance',
        #                                                      score=state['score'], game_over=state['over'],
        #                                                      max_depth_reached=(max_depth == 0)))
        return None, await apply_heuristics(oracle, state)

    available_moves = await oracle.available_moves(state)
    available_action_states = [(option['action'], option['state'])
                               for option in available_moves.get('moves', []) if option.get('available', False)]

    if len(available_action_states) == 0:
        # print('[level={depth}] [player={player}] score={score} no further actions possible'
        #       .format(depth=max_depth,
        #               player='AI' if player == 0 else 'Chance',
        #               score=state['score']))
        return None, await apply_heuristics(oracle, state)

    # main player i.e. AI
    if player == 0:
        action_plays = [(action, await expectimax(oracle, enhance_game_state(new_state), max_depth - 1, player=1))
                        for action, new_state in available_action_states]
        action_scores = [(action, play[1]) for action, play in action_plays]
        max_action_score = max(action_scores, key=lambda a_s: a_s[1])
        # print('[level={depth}] [player={player}] max_score={score} for action={action}'.format(
        #     depth=max_depth, player='AI' if player == 0 else 'Chance',
        #     score=max_action_score[1], action=max_action_score[0]))
        return max_action_score

    # chance player i.e. either the 2 or 4 tile
    if player == 1:
        result = await oracle.empty_cells(state)
        new_states = \
            [(insert_tile(state, position, new_tile_value=2), PROBABILITY_NEW_TILE_2) for position in result.get('positions', [])] + \
            [(insert_tile(state, position, new_tile_value=4), PROBABILITY_NEW_TILE_4) for position in result.get('positions', [])]

        action_scores = [(await expectimax(oracle, probable_state, max_depth, player=0), probability) for probable_state, probability in new_states]
        probable_action_scores = [(action, probability * score) for (action, score), probability in action_scores]
        min_action_score = min(probable_action_scores, key=lambda a_s: a_s[1])
        # print('[level={depth}] [player={player}] min_score={score} for action={action}'.format(
        #     depth=max_depth, player='AI' if player == 0 else 'Chance',
        #     score=min_action_score[1], action=min_action_score[0]))
        return min_action_score


async def _execute_action(oracle, state, action):
    result = await oracle.play(state, action)
    return enhance_game_state(result['state'])
