from aiohttp import web
from .routes import setup as setup_routers


def create_app(attach):
    app = web.Application()
    for setup in attach:
        setup(app)
    setup_routers(app)
    return app


def start_dev_server(app):
    web.run_app(app)
