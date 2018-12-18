import math

CORNER_POSITIONS = [[0, 0], [0, 3], [3, 0], [3, 3]]
CENTRAL_POSITIONS = [[1, 1], [2, 1], [2, 2], [1, 2]]

GRADE = {
    'awesome': 1,
    'meh': 0,
    'disastrous': -1
}


async def apply(oracle, state, weight):
    # state['max_tile'] = (<value_int>, [<grid_x_pos>, <grid_y_pos>])
    max_tile_value, max_tile_position = state['max_tile']

    if max_tile_position in CORNER_POSITIONS:
        return GRADE['awesome'] * math.log(max_tile_value) * weight

    if max_tile_position in CENTRAL_POSITIONS:
        return GRADE['disastrous'] * math.log(max_tile_value) * weight

    return GRADE['meh'] * weight
