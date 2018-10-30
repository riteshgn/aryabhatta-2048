import random
from ai_engine import AIEngine


MOVE_CHOICES = {
    0: 'UP',
    1: 'RIGHT',
    2: 'DOWN',
    3: 'LEFT'
}


class RandomMoves(AIEngine):

    def next_move(self, state):
        return MOVE_CHOICES[random.randint(0, 3)]

