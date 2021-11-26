from aiohttp import web
import asyncio
import aiohttp_jinja2
import jinja2
import dbase

from config import *
from main_routes import routes as m_routes

if __name__ == '__main__':
    app = web.Application()
    #loop = asyncio.get_event_loop()
    #db = loop.run_until_complete(dbase.setup_db())
    app['db'] = dbase.DB()
    app.add_routes(m_routes)
    app.router.add_static('/static', 'static')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    web.run_app(app,port=CONF['server']['port'])

