from aiohttp import web
from config import *
from middle import log

routes = web.RouteTableDef()

@routes.get(url_api('/test'))
@log
async def test(request):
    return web.Response(text="it's working!")

@routes.get('/dashboard/')
async def main(request):
    return tresponse(request,"dashboard.html",{"val":"tut value"})

@routes.get(url_api('/sets'))
@log
async def sets(request):
    sets = await get_sets(request.app['db'])
    return jresponse(sets ,200)

@routes.post(url_api('/sets'))
@log
async def put_set(request):
    jdata = await request.json()
    result = await request.app['db'].put_set(jdata)
    return jmresponse(upresult(result) ,200)

@routes.get(url_api('/dashboard_get_values'))
async def dashboard_get_values(request):
    response = await request.app['db'].dashboard_get_values()
    return jresponse(response, 200)
