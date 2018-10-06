from aiohttp import web
import socketio

from ai_comm_system.namespace_game import GameNamespace


async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

sio = socketio.AsyncServer()
sio.register_namespace(GameNamespace('/game'))

app = web.Application()
sio.attach(app)

app.router.add_static('/', '2048-AI')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)
