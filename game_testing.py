from ai_utils import move_left

SCENARIOS_MOVE_LEFT = [
    {'entries': [0, 0, 0, 2], 'expected': [2, 0, 0, 0], 'score': 0},
    {'entries': [0, 0, 2, 0], 'expected': [2, 0, 0, 0], 'score': 0},
    {'entries': [0, 2, 0, 0], 'expected': [2, 0, 0, 0], 'score': 0},
    {'entries': [2, 0, 0, 0], 'expected': [2, 0, 0, 0], 'score': 0},
    {'entries': [0, 0, 2, 2], 'expected': [4, 0, 0, 0], 'score': 4},
    {'entries': [0, 2, 2, 0], 'expected': [4, 0, 0, 0], 'score': 4},
    {'entries': [2, 2, 0, 0], 'expected': [4, 0, 0, 0], 'score': 4},
    {'entries': [2, 0, 0, 2], 'expected': [4, 0, 0, 0], 'score': 4},
    {'entries': [2, 0, 2, 0], 'expected': [4, 0, 0, 0], 'score': 4},
    {'entries': [0, 2, 0, 2], 'expected': [4, 0, 0, 0], 'score': 4},
    {'entries': [0, 2, 2, 2], 'expected': [4, 2, 0, 0], 'score': 4},
    {'entries': [2, 0, 2, 2], 'expected': [4, 2, 0, 0], 'score': 4},
    {'entries': [2, 2, 0, 2], 'expected': [4, 2, 0, 0], 'score': 4},
    {'entries': [2, 2, 2, 0], 'expected': [4, 2, 0, 0], 'score': 4},
    {'entries': [2, 2, 2, 2], 'expected': [4, 4, 0, 0], 'score': 8},
    {'entries': [0, 0, 4, 2], 'expected': [4, 2, 0, 0], 'score': 0},
    {'entries': [0, 4, 2, 0], 'expected': [4, 2, 0, 0], 'score': 0},
    {'entries': [4, 2, 0, 0], 'expected': [4, 2, 0, 0], 'score': 0},
    {'entries': [0, 4, 0, 2], 'expected': [4, 2, 0, 0], 'score': 0},
    {'entries': [4, 0, 2, 0], 'expected': [4, 2, 0, 0], 'score': 0},
    {'entries': [0, 2, 4, 4], 'expected': [2, 8, 0, 0], 'score': 8},
    {'entries': [2, 0, 4, 4], 'expected': [2, 8, 0, 0], 'score': 8},
    {'entries': [2, 4, 0, 4], 'expected': [2, 8, 0, 0], 'score': 8},
    {'entries': [2, 4, 4, 0], 'expected': [2, 8, 0, 0], 'score': 8},
    {'entries': [0, 4, 4, 2], 'expected': [8, 2, 0, 0], 'score': 8},
    {'entries': [4, 0, 4, 2], 'expected': [8, 2, 0, 0], 'score': 8},
    {'entries': [4, 4, 0, 2], 'expected': [8, 2, 0, 0], 'score': 8},
    {'entries': [4, 4, 2, 0], 'expected': [8, 2, 0, 0], 'score': 8},
    {'entries': [4, 2, 0, 4], 'expected': [4, 2, 4, 0], 'score': 0},
    {'entries': [4, 2, 4, 0], 'expected': [4, 2, 4, 0], 'score': 0},
    {'entries': [4, 4, 4, 2], 'expected': [8, 4, 2, 0], 'score': 8},
    {'entries': [4, 4, 2, 4], 'expected': [8, 2, 4, 0], 'score': 8},
    {'entries': [4, 2, 4, 4], 'expected': [4, 2, 8, 0], 'score': 8},
    {'entries': [2, 4, 4, 4], 'expected': [2, 8, 4, 0], 'score': 8},
    {'entries': [4, 4, 2, 2], 'expected': [8, 4, 0, 0], 'score': 12},
    {'entries': [4, 2, 2, 4], 'expected': [4, 4, 4, 0], 'score': 4},
    {'entries': [4, 2, 4, 2], 'expected': [4, 2, 4, 2], 'score': 0}
]


def test_move():
    for scenario in SCENARIOS_MOVE_LEFT:
        actual = move_left(scenario['entries'])
        if actual[0] == scenario['expected'] and actual[1] == scenario['score']:
            print('##### test PASSED #####')
        else:
            print('##### test FAILED #####')
            print('\n----------------')
            print(scenario['entries'])
            print(scenario['expected'])
            print(actual[0])
            print(actual[1])
            print('----------------\n')


if __name__ == '__main__':
    test_move()
