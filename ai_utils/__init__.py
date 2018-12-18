import copy
import operator
from functools import reduce
import random
import math


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def print_grid(state, digits_in_max_score=4):
    grid = state['grid']['cells']
    grid_transpose = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

    total_chars_with_spacing = digits_in_max_score + 2
    grid_to_print = ['|'.join([' %s ' % str(cell.get('value', 0)).zfill(digits_in_max_score)
                               if cell is not None else ' ' * total_chars_with_spacing for cell in row])
                     for row in grid_transpose]
    border = ' %s' % (' '.join(['%s' % '-' * total_chars_with_spacing] * digits_in_max_score))
    cell_separator = '|'

    print(border)
    for row in grid_to_print:
        print('%s%s%s' % (cell_separator, row, cell_separator))
        print(border)

    print('score: ', state['score'])


def minified_grid(state):
    grid = state['grid']['cells']
    grid_transpose = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

    return ' | '.join([' '.join([str(cell.get('value', 0)) if cell is not None else '*' for cell in row])
                       for row in grid_transpose])


def insert_tile(state, new_tile_pos, new_tile_value):
    new_state = copy.deepcopy(state)
    row_num_to_update = new_tile_pos['x']
    col_num_to_update = new_tile_pos['y']
    new_state['grid']['cells'][row_num_to_update][col_num_to_update] = {
        'position': new_tile_pos,
        'value': new_tile_value
    }
    return new_state


def max_tile(state):
    all_tile_values = reduce(operator.concat,
                             [[(0, None) if cell is None else
                               (cell.get('value', 0), [cell['position']['x'], cell['position']['y']])
                               for cell in row] for row in state['grid']['cells']], [])
    return max(all_tile_values, key=lambda score_pos: score_pos[0])


def edges(state):
    def __extract_value(cell): return 0 if cell is None else cell.get('value', 0)

    rows = state['grid']['cells']
    top = [__extract_value(cell) for cell in [rows[0][0], rows[1][0], rows[2][0], rows[3][0]]]
    right = [__extract_value(cell) for cell in rows[3]]
    bottom = [__extract_value(cell) for cell in [rows[3][3], rows[2][3], rows[1][3], rows[0][3]]]
    left = [__extract_value(cell) for cell in [rows[0][3], rows[0][2], rows[0][1], rows[0][0]]]
    return top, right, bottom, left


def enhance_game_state(state):
    state['max_tile'] = max_tile(state)
    state['edges'] = edges(state)
    return state


def cell_value(cell):
    if cell is None:
        return 0

    return cell.get('value', 0)


def empty_cells(state):
    return reduce(operator.concat, [[{'x': i, 'y': j} for j, cell in enumerate(row) if cell is None]
                                    for i, row in enumerate(state['grid']['cells'])], [])


def has_tile_matches(state):
    cells = state['grid']['cells']

    for col_num in range(0, 4):
        if (cell_value(cells[col_num][0]) == cell_value(cells[col_num][1])
                or cell_value(cells[col_num][1]) == cell_value(cells[col_num][2])
                or cell_value(cells[col_num][2]) == cell_value(cells[col_num][3])):
            return True

    for row_num in range(0, 4):
        if (cell_value(cells[0][row_num]) == cell_value(cells[1][row_num])
                or cell_value(cells[1][row_num]) == cell_value(cells[2][row_num])
                or cell_value(cells[2][row_num]) == cell_value(cells[3][row_num])):
            return True

    return False


def move_left(row):
    # print('input', row)

    # base case - less than one element in the array
    if len(row) <= 1:
        # print('returning1 ', row)
        return row, 0

    # first element is zero - shift the entries to left by 1
    if row[0] == 0:
        temp = move_left(row[1:])
        result = temp[0] + [0], temp[1]
        # print('returning2 ', result)
        return result

    # first element is equal to second element
    #   - double first element value, remove second element and shift further entries to left by 1
    if row[0] == row[1]:
        temp = move_left(row[2:])
        result = [(row[0] * 2)] + temp[0] + [0], temp[1] + (row[0] * 2)
        # print('returning3 ', result)
        return result

    # check if empty slots next to first element
    #   - identify empty slots
    #   - need to shift until first non-empty slot is next to first element
    num_of_shifts = 0
    for i in range(1, len(row)):
        if row[i] == 0:
            num_of_shifts = num_of_shifts + 1
        else:
            break

    # apart from first entry all entries are empty
    #   - nothing to do here
    if num_of_shifts == len(row) - 1:
        # print('returning4; only empty slots so nothing to do', row)
        return row, 0

    # put first non-empty element next to first element and move_left
    if num_of_shifts > 0:
        new_row = row[num_of_shifts+1:] + [0]*num_of_shifts
        new_row.insert(0, row[0])
        result = move_left(new_row)
        # print('returning5; move left on this new row', new_row, result)
        return result

    # move left on rest of the array
    temp = move_left(row[1:])
    result = [row[0]] + temp[0], temp[1]
    # print('returning6; move left on rest of the array', result)
    return result


def random_initial_state():
    blank_state = {
        "grid": {
            "size": 4,
            "cells": [
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None],
            ]
        },
        "score": 0,
        "over": False
    }

    tile1 = randome_tile()
    tile2 = randome_tile()
    while (tile1['position']['x'] == tile2['position']['x']
           and tile1['position']['y'] == tile2['position']['y']):
        tile2 = randome_tile()

    blank_state['grid']['cells'][tile1['position']['x']][tile1['position']['y']] = tile1
    blank_state['grid']['cells'][tile2['position']['x']][tile2['position']['y']] = tile2

    return blank_state


def randome_tile():
    return {
        'position': {
            'x': math.floor(random.random() * 3),
            'y': math.floor(random.random() * 3)
        },
        'value': 2 if random.random() < 0.9 else 4
    }
