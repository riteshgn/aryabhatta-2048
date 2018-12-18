from ai_utils import cell_value


async def apply(oracle, state, weight):
    cells = state['grid']['cells']

    adjacent_matches = 0
    for col_num in range(0, 4):
        if cell_value(cells[col_num][0]) == cell_value(cells[col_num][1]):
            adjacent_matches = adjacent_matches + 1
        if cell_value(cells[col_num][1]) == cell_value(cells[col_num][2]):
            adjacent_matches = adjacent_matches + 1
        if cell_value(cells[col_num][2]) == cell_value(cells[col_num][3]):
            adjacent_matches = adjacent_matches + 1

    for row_num in range(0, 4):
        if cell_value(cells[0][row_num]) == cell_value(cells[1][row_num]):
            adjacent_matches = adjacent_matches + 1
        if cell_value(cells[1][row_num]) == cell_value(cells[2][row_num]):
            adjacent_matches = adjacent_matches + 1
        if cell_value(cells[2][row_num]) == cell_value(cells[3][row_num]):
            adjacent_matches = adjacent_matches + 1

    if adjacent_matches == 0:
        return -1 * weight
    return adjacent_matches * weight
