import copy
import math
import random

from ai_utils import cell_value, empty_cells, has_tile_matches, move_left, print_grid, max_tile
from .game_cache import Cache


MOVE_CHOICES = {'UP': 0, 'RIGHT': 1, 'DOWN': 2, 'LEFT': 3}
DEFAULT_INITIAL_STATE = {
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


class Game(object):
    def __init__(self, state=DEFAULT_INITIAL_STATE):
        self._current_state = copy.deepcopy(state)

    def state(self):
        return copy.deepcopy(self._current_state)

    def score(self):
        return self._current_state['score']

    def metrics(self):
        return {
            'max_tile': max_tile(self._current_state)[0],
            'score': self._current_state['score']
        }

    def is_game_over(self):
        positions = empty_cells(self._current_state)
        if len(positions) == 0:
            return has_tile_matches(self._current_state)

        return False

    def print_board(self):
        print_grid(self._current_state)

    def add_random_tile(self):
        cell_positions = empty_cells(self._current_state)
        if len(cell_positions) > 0:
            new_position_index = math.floor(random.random() * len(cell_positions))
            new_tile_position = cell_positions[new_position_index]
            self._current_state['grid']['cells'][new_tile_position['x']][new_tile_position['y']] = {
                'position': {
                    'x': new_tile_position['x'],
                    'y': new_tile_position['y']
                },
                'value': 2 if random.random() < 0.9 else 4
            }
        return self._current_state

    @staticmethod
    def _cache_key(entries, direction):
        prefix = 'U' if direction in ['UP', 'LEFT'] else 'D'
        return '{}_{}'.format(prefix, '|'.join([str(entry) for entry in entries]))

    @staticmethod
    def _get_from_cache(entries, direction):
        cache_entry = Cache().get(Game._cache_key(entries, direction))
        if cache_entry is not None:
            cache_value = [int(entry) for entry in cache_entry.split('|')]
            return cache_value[:-1], cache_value[-1]

        return None, None
        # prefix_transpose = 'D' if direction in ['UP', 'LEFT'] else 'U'

    @staticmethod
    def _add_to_cache(entries, direction, new_entries, total_value):
        transformation = [str(entry) for entry in new_entries]
        transformation.append(str(total_value))
        Cache().put(
            Game._cache_key(entries, direction),
            '|'.join(transformation)
        )

    @staticmethod
    def _left_move_from_cache(row):
        transformed_row, value_add = Game._get_from_cache(row, 'LEFT')

        if transformed_row is None or value_add is None:
            transformed_row, value_add = move_left(row)
            Game._add_to_cache(row, 'LEFT', transformed_row, value_add)

        return transformed_row, value_add
        # return move_left(row)

    def _move_up(self):
        new_state = self.state()
        original_cells = self._current_state['grid']['cells']

        for col_num in range(0, 4):
            row = [cell_value(original_cells[col_num][0]), cell_value(original_cells[col_num][1]),
                   cell_value(original_cells[col_num][2]), cell_value(original_cells[col_num][3])]
            transformed_row, value_add = Game._left_move_from_cache(row)

            new_entries = [None if value == 0 else {'position': {'x': col_num, 'y': index}, 'value': value}
                           for index, value in enumerate(transformed_row)]
            new_state['grid']['cells'][col_num][0] = new_entries[0]
            new_state['grid']['cells'][col_num][1] = new_entries[1]
            new_state['grid']['cells'][col_num][2] = new_entries[2]
            new_state['grid']['cells'][col_num][3] = new_entries[3]
            new_state['score'] = new_state['score'] + value_add

        return new_state

    def _move_down(self):
        new_state = self.state()
        original_cells = self._current_state['grid']['cells']

        for col_num in range(0, 4):
            row = [cell_value(original_cells[col_num][3]), cell_value(original_cells[col_num][2]),
                   cell_value(original_cells[col_num][1]), cell_value(original_cells[col_num][0])]
            transformed_row, value_add = Game._left_move_from_cache(row)

            new_entries = [None if value == 0 else {'position': {'x': col_num, 'y': index}, 'value': value}
                           for index, value in enumerate(transformed_row)]
            new_state['grid']['cells'][col_num][3] = new_entries[0]
            new_state['grid']['cells'][col_num][2] = new_entries[1]
            new_state['grid']['cells'][col_num][1] = new_entries[2]
            new_state['grid']['cells'][col_num][0] = new_entries[3]
            new_state['score'] = new_state['score'] + value_add

        return new_state

    def _move_left(self):
        new_state = self.state()
        original_cells = self._current_state['grid']['cells']

        for row_num in range(0, 4):
            row = [cell_value(original_cells[0][row_num]), cell_value(original_cells[1][row_num]),
                   cell_value(original_cells[2][row_num]), cell_value(original_cells[3][row_num])]
            transformed_row, value_add = Game._left_move_from_cache(row)

            new_entries = [None if value == 0 else {'position': {'x': index, 'y': row_num}, 'value': value}
                           for index, value in enumerate(transformed_row)]
            new_state['grid']['cells'][0][row_num] = new_entries[0]
            new_state['grid']['cells'][1][row_num] = new_entries[1]
            new_state['grid']['cells'][2][row_num] = new_entries[2]
            new_state['grid']['cells'][3][row_num] = new_entries[3]
            new_state['score'] = new_state['score'] + value_add

        return new_state

    def _move_right(self):
        new_state = self.state()
        original_cells = self._current_state['grid']['cells']

        for row_num in range(0, 4):
            row = [cell_value(original_cells[3][row_num]), cell_value(original_cells[2][row_num]),
                   cell_value(original_cells[1][row_num]), cell_value(original_cells[0][row_num])]
            transformed_row, value_add = Game._left_move_from_cache(row)

            new_entries = [None if value == 0 else {'position': {'x': index, 'y': row_num}, 'value': value}
                           for index, value in enumerate(transformed_row)]
            new_state['grid']['cells'][3][row_num] = new_entries[0]
            new_state['grid']['cells'][2][row_num] = new_entries[1]
            new_state['grid']['cells'][1][row_num] = new_entries[2]
            new_state['grid']['cells'][0][row_num] = new_entries[3]
            new_state['score'] = new_state['score'] + value_add

        return new_state

    def move(self, direction, add_random_tile=False):
        if direction == 'UP':
            new_state = self._move_up()

        elif direction == 'DOWN':
            new_state = self._move_down()

        elif direction == 'LEFT':
            new_state = self._move_left()

        elif direction == 'RIGHT':
            new_state = self._move_right()

        self._current_state = new_state
        self._current_state['over'] = self.is_game_over()
        if not self.is_game_over() and add_random_tile:
            self.add_random_tile()
        return self._current_state
