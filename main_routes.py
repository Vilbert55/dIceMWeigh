from aiohttp import web
from config import *
from middle import log

routes = web.RouteTableDef()

@routes.get(url_api('/test'))
@log
async def test(request):
    return web.Response(text="it's working!")

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

@routes.get('/dashboard/')
async def dashboard(request):
    return tresponse(request,"dashboard.html",{"key":"some value"})

@routes.get(url_api('/dashboard_get_values'))
async def dashboard_get_values(request):
    response = await request.app['db'].dashboard_get_values()
    return jresponse(response, 200)

@routes.get('/report/worktime/')
async def worktime(request):
    return tresponse(request,"report_worktime.html",{})

@routes.post(url_api('/get_values/report_worktime'))
async def worktime_get_values(request):
    jdata = await request.json()
    response = await request.app['db'].worktime_get_values(jdata)
    return jresponse(response, 200)