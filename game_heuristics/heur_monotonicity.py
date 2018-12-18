

async def apply(oracle, state, weight):
    clockwise_top_edge = state['edges'][0][0] <= state['edges'][0][1] <= state['edges'][0][2] <= state['edges'][0][3]
    if clockwise_top_edge:
        return weight

    clockwise_right_edge = state['edges'][1][0] <= state['edges'][1][1] <= state['edges'][1][2] <= state['edges'][1][3]
    if clockwise_right_edge:
        return weight

    clockwise_bottom_edge = state['edges'][2][0] <= state['edges'][2][1] <= state['edges'][2][2] <= state['edges'][2][3]
    if clockwise_bottom_edge:
        return weight

    clockwise_left_edge = state['edges'][3][0] <= state['edges'][3][1] <= state['edges'][3][2] <= state['edges'][3][3]
    if clockwise_left_edge:
        return weight

    anti_clockwise_top_edge = state['edges'][0][0] >= state['edges'][0][1] >= state['edges'][0][2] >= state['edges'][0][3]
    if anti_clockwise_top_edge:
        return weight

    anti_clockwise_left_edge = state['edges'][3][0] >= state['edges'][3][1] >= state['edges'][3][2] >= state['edges'][3][3]
    if anti_clockwise_left_edge:
        return weight

    anti_clockwise_bottom_edge = state['edges'][2][0] >= state['edges'][2][1] >= state['edges'][2][2] >= state['edges'][2][3]
    if anti_clockwise_bottom_edge:
        return weight

    anti_clockwise_right_edge = state['edges'][1][0] >= state['edges'][1][1] >= state['edges'][1][2] >= state['edges'][1][3]
    if anti_clockwise_right_edge:
        return weight

    return 0



