import asyncio
import concurrent.futures
import requests

from ai_oracle import Oracle


class OracleApiClient(Oracle):

    def __init__(self, url='127.0.0.1', port=18080):
        self._api_url = 'http://%s:%s' % (url, port)
        self._thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)

    async def play(self, state, choice):
        response = await self._post_json_request('%s/oracle/play' % self._api_url,
                                                 json={'state': state, 'choice': choice})
        return response.json()

    async def empty_cells(self, state):
        response = await self._post_json_request('%s/oracle/empty_cells' % self._api_url,
                                                 json={'state': state})
        return response.json()

    async def available_moves(self, state):
        response = await self._post_json_request('%s/oracle/available_moves' % self._api_url,
                                                 json={'state': state})
        return response.json()

    async def _post_json_request(self, url, json):
        await asyncio.sleep(0.005)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._thread_pool, OracleApiClient._post_json_sync, url, json)

    @staticmethod
    def _post_json_sync(url, json):
        return requests.post(url, json=json)

