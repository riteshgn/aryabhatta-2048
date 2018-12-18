

async def apply(oracle, state, weight):
    if state['over']:
        return -1 * weight

    return 0
