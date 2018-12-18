import math

MIN_COUNT = 1
MAX_COUNT = 16
THRESHOLD_MAX_TILE = 512


async def apply(oracle, state, weight):
    result = await oracle.empty_cells(state)
    empty_cells_count = len(result.get('positions', []))

    if empty_cells_count <= 0.25 * MAX_COUNT and state['max_tile'][0] >= THRESHOLD_MAX_TILE:
        return -1 * (1 - _normalize(empty_cells_count)) * math.log(state['max_tile'][0]) * weight

    if empty_cells_count >= 0.50 * MAX_COUNT and state['max_tile'][0] >= THRESHOLD_MAX_TILE:
        return _normalize(empty_cells_count) * math.log(state['max_tile'][0]) * weight

    return weight


def _normalize(cell_count):
    return (cell_count - MIN_COUNT) / (MAX_COUNT - MIN_COUNT)
