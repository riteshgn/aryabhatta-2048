import requests

from ai_oracle import Oracle


class OracleApiClient(Oracle):

    def __init__(self, url='127.0.0.1', port=18080):
        self._api_url = 'http://%s:%s' % (url, port)

    async def play(self, state, choice):
        response = requests.post('%s/oracle/play' % self._api_url, json={'state': state, 'choice': choice})
        return response.json()

    async def available_cells(self, state):
        response = requests.post('%s/oracle/available_cells' % self._api_url, json={'state': state})
        return response.json()



