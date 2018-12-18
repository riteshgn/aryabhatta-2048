from ai_utils import Singleton


class Oracle(metaclass=Singleton):

    async def play(self, state, choice):
        raise NotImplementedError('you should be using a concrete implementation of the Oracle')

    async def empty_cells(self, state):
        raise NotImplementedError('you should be using a concrete implementation of the Oracle')

    async def available_moves(self, state):
        raise NotImplementedError('you should be using a concrete implementation of the Oracle')
