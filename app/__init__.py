from aiohttp import web
from .routes import setup as setup_routers
from ai_comm_system import setup as setup_sio


def create_app():
    web_app = web.Application()
    sio = setup_sio(web_app)
    setup_routers(web_app)
    return web_app, sio


def start_dev_server(web_app):
    web.run_app(web_app)
