import ssl

from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/')
async def main(rq: web.Request):
    params = rq.query
    if not params:
        if rq.cookies.get('Authorised'):
            resp = web.HTTPFound('/success')
            return resp
        return web.HTTPFound('/?action=auth')
    if params.get('action'):
        action = params.get('action')
        if action == 'auth':
            with open('templates/auth.html', 'r') as f:
                page = f.read()
            return web.Response(body=page, content_type='text/html')
        if action == 'register':
            with open('templates/register.html', 'r') as f:
                page = f.read()
            return web.Response(body=page, content_type='text/html')
    return web.HTTPBadRequest()


@routes.get('/success')
async def success_page(rq: web.Request):
    if not rq.cookies.get('Authorised'):
        return web.HTTPUnauthorized()
    return web.Response(text='success')


def get_ssl_context():
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.load_cert_chain('cert.crt', 'key.pem')


app = web.Application()
app.add_routes(routes)
web.run_app(app, host='localhost', port=8080, ssl_context=get_ssl_context())
