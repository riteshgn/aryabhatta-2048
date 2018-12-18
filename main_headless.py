import json
import statistics
import time

# from ai_engine.engine_best_score_v2 import BestScore as AIEngine
# from ai_engine.engine_best_score_with_depth import BestScoreWithDepth as AIEngine
from ai_engine.engine_expectimax_with_heur_v1 import Expectimax as AIEngine
from ai_oracle.oracle_python_impl import OraclePythonImpl as Oracle
from ai_oracle.game import Game
from ai_oracle.game_cache import Cache
from ai_utils import print_grid, random_initial_state


game_engine = AIEngine(Oracle())

GAME_SETTINGS = {
    'algorithm': 'Expectimax',
    # 'algorithm': 'BestScoreWithDepth',
    # 'algorithm': 'BestScore v2',
    'max_depth': 3,
    'heuristics_enabled': False,
    'number_of_simulations': 3
}


def create_initial_game_board():
    state = random_initial_state()
    # print_grid(state)
    return Game(state)


async def play_game(game_num):
    print('\t>>> Setting up the game board for game ', game_num)
    game = create_initial_game_board()
    print('\t>>> Starting game')

    try:
        while not game.is_game_over():
            # game.print_board()
            direction = await game_engine.next_move(game.state())
            # print('selected move ', direction)

            game.move(direction, add_random_tile=True)
    except:
        print('\t\t>>> Simulation Error')

    print('\n\t>>> Game is over!')
    print_grid(game.state())
    print('\n')

    return game.metrics()


async def simulate_games(number_of_games=1):
    print('>>> Starting simulations\n')

    scores = []
    max_tiles = []
    execution_times = []
    for index in range(0, number_of_games):
        t0 = time.time()
        metrics = await play_game(game_num=index+1)
        t1 = time.time()
        scores.append(metrics['score'])
        max_tiles.append(metrics['max_tile'])
        execution_times.append(t1 - t0)

    print('\n---------------------------')
    print('--- Summary Report      ---')
    print('---------------------------\n')

    print('games:              ', number_of_games)
    print('algorithm:          ', GAME_SETTINGS['algorithm'])
    print('max_depth:          ', GAME_SETTINGS['max_depth'])
    print('heuristics_enabled: ', GAME_SETTINGS['heuristics_enabled'])

    print('\n--- score stats         ---')
    print('min:   ', min(scores))
    print('max:   ', max(scores))
    print('mean:  ', statistics.mean(scores))
    print('median:', statistics.median(scores))
    print('sd:    ', statistics.stdev(scores))

    print('\n--- max tile stats      ---')
    print('min:   ', min(max_tiles))
    print('max:   ', max(max_tiles))
    print('mean:  ', statistics.mean(max_tiles))
    print('median:', statistics.median(max_tiles))
    print('sd:    ', statistics.stdev(max_tiles))

    print('\n--- execution time stats ---')
    print('min:   ', min(execution_times))
    print('max:   ', max(execution_times))
    print('mean:  ', statistics.mean(execution_times))
    print('median:', statistics.median(execution_times))
    print('sd:    ', statistics.stdev(execution_times))

    print('cache metrics: ', json.dumps(Cache().metrics()))


if __name__ == '__main__':
    import asyncio

    loop = asyncio.new_event_loop()
    loop.run_until_complete(simulate_games(GAME_SETTINGS['number_of_simulations']))
    loop.close()
