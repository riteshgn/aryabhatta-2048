from aiohttp import web


async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


def setup(app):
    app.router.add_static('/', '2048-AI')
    app.router.add_get('/', index)
