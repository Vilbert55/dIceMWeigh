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
@log
async def dashboard(request):
    return tresponse(request,"dashboard.html",{"key":"some value"})

@routes.get(url_api('/dashboard_get_values'))
@log
async def dashboard_get_values(request):
    dt = request.rel_url.query.get('dt')
    response = await request.app['db'].dashboard_get_values(dt)
    return jresponse(response, 200)

@routes.get('/report/worktime/')
@log
async def worktime(request):
    return tresponse(request,"report_worktime.html",{})

@routes.post(url_api('/get_values/report_worktime'))
@log
async def worktime_get_values(request):
    jdata = await request.json()
    response = await request.app['db'].worktime_get_values(jdata)
    return jresponse(response, 200)

@routes.get('/prods_list')
async def prods_list(request):
    return tresponse(request,"prods_list.html",{})

@routes.post(url_api('/prods_head_list'))
async def set_username(request):
    jdata = await request.json()
    response = await request.app['db'].get_prods_head_total(jdata)
    return jresponse(response, 200)

@routes.get(url_api('/prods'))
@log
async def prods(request):
    jdata = request.rel_url.query
    result = await request.app['db'].get_prods(jdata)
    return jresponse(result,200)

@routes.get('/plan')
async def prods_list(request):
    return tresponse(request,"plan.html",{})

