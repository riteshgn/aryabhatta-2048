from app import create_app, start_dev_server
from ai_comm_system.namespace_game import GameNamespace
from ai_engine.engine_random_moves import RandomMoves as AIEngine
from ai_oracle.oracle_api_client import OracleApiClient as Oracle

web_app, sio = create_app()

game_namespace = GameNamespace('/game', AIEngine(Oracle()))
sio.register_namespace(game_namespace)

if __name__ == '__main__':
    start_dev_server(web_app)
