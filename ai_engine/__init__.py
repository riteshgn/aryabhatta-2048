
class AIEngine(object):
    def __init__(self, oracle):
        self._oracle = oracle

    async def next_move(self, state):
        raise NotImplementedError('you should be using a concrete implementation of the AI Engine')
