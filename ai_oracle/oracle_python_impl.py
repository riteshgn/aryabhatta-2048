from ai_oracle import Oracle
from ai_oracle.game import Game
from ai_utils import empty_cells, minified_grid


class OraclePythonImpl(Oracle):

    async def play(self, state, choice):
        return {'state': Game(state).move(choice)}

    async def empty_cells(self, state):
        return {'positions': empty_cells(state)}

    async def available_moves(self, state):
        play_up = await self.play(state, 'UP')
        play_right = await self.play(state, 'RIGHT')
        play_down = await self.play(state, 'DOWN')
        play_left = await self.play(state, 'LEFT')
        minified_grid_original = minified_grid(state)

        return {
            "moves": [
                {"action": "UP", "available": minified_grid_original != minified_grid(play_up['state']), 'state': play_up['state']},
                {"action": "RIGHT", "available": minified_grid_original != minified_grid(play_right['state']), 'state': play_right['state']},
                {"action": "DOWN", "available": minified_grid_original != minified_grid(play_down['state']), 'state': play_down['state']},
                {"action": "LEFT", "available": minified_grid_original != minified_grid(play_left['state']), 'state': play_left['state']}
            ]
        }


async def _test_available_moves(oracle, state):
    print('\n-----------------------')
    actual_result = await oracle.available_moves(state)
    print(actual_result)

    expected_result = {
        "moves": [
            {"action": "UP", "available": True},
            {"action": "RIGHT", "available": False},
            {"action": "DOWN", "available": True},
            {"action": "LEFT", "available": True}
        ]
    }
    print('available_moves test result', actual_result == expected_result)
    print('-----------------------\n')
    pass


async def _test_empty_cells(oracle, state):
    print('\n-----------------------')
    actual_result = await oracle.empty_cells(state)
    print(actual_result)

    expected_result = {
        "positions": [
            {"x": 0, "y": 0},
            {"x": 0, "y": 1},
            {"x": 0, "y": 2},
            {"x": 1, "y": 0},
            {"x": 1, "y": 1},
            {"x": 1, "y": 2},
            {"x": 2, "y": 2}
        ]
    }
    print('empty_cells test result', actual_result == expected_result)
    print('-----------------------\n')


async def main():
    state = {
        "grid": {
            "size": 4,
            "cells": [
                [None, None, None, {"position": {"x": 0, "y": 3}, "value": 2}],
                [None, None, None, {"position": {"x": 1, "y": 3}, "value": 4}],
                [{"position": {"x": 2, "y": 0}, "value": 2}, {"position": {"x": 2, "y": 1}, "value": 2},
                 None, {"position": {"x": 2, "y": 3}, "value": 2}],
                [{"position": {"x": 3, "y": 0}, "value": 4}, {"position": {"x": 3, "y": 1}, "value": 4},
                 {"position": {"x": 3, "y": 2}, "value": 16}, {"position": {"x": 3, "y": 3}, "value": 4}]
            ]
        },
        "score": 36,
        "over": False
    }

    oracle = OraclePythonImpl()
    await _test_empty_cells(oracle, state)
    await _test_available_moves(oracle, state)


if __name__ == '__main__':
    import asyncio

    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()

