import random

from ai_engine import AIEngine
from ai_utils import print_grid


MOVE_CHOICES = {
    0: 'UP',
    1: 'RIGHT',
    2: 'DOWN',
    3: 'LEFT'
}


class RandomMoves(AIEngine):

    async def next_move(self, state):
        cells = await self._oracle.available_cells(state)
        print('available cells: ', cells)

        selected_move = MOVE_CHOICES[random.randint(0, 3)]

        expected_outcome = await self._oracle.play(state, selected_move)
        print('expected grid after move', selected_move)
        print_grid(expected_outcome['state'])

        return selected_move

