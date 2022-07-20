from aiohttp import web
import asyncio
import aiohttp_jinja2
import jinja2
import dbase
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet


from config import *
from main_routes import routes as m_routes

class PatchedEncryptedCookieStorage(EncryptedCookieStorage):
    def __init__(self, key, **kwargs):
        super().__init__(key, **kwargs)
        self._cookie_params["samesite"] = "none"
        self._cookie_params["path"] = "/"

if __name__ == '__main__':
    app = web.Application()
    fernet_key = fernet.Fernet.generate_key()
    f = fernet.Fernet(fernet_key)
    setup(app, PatchedEncryptedCookieStorage(f, httponly=True))
    #setup(app, EncryptedCookieStorage(f, httponly=True, samesite="None"))
    #loop = asyncio.get_event_loop()
    #db = loop.run_until_complete(dbase.setup_db())
    app['db'] = dbase.DB()
    app.add_routes(m_routes)
    app.router.add_static('/static', 'static')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    web.run_app(app,port=CONF['server']['port'])

