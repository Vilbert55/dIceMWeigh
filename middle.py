from re import L
import time
from unicodedata import name
from config import *
from uuid import uuid4
import sys,traceback
from aiohttp import web 
import asyncio
import base64

HTTP_REQUEST = "RQ"
HTTP_RESPONSE  = "RS"

def get_auth(request):
    if not request.headers.get("Authorization") is None:
        atype, enc = request.headers.get('Authorization').strip().split(" ")
        if atype.lower() == 'basic':
            return True, (base64.b64decode(enc).decode('utf8').split(":"))
    username = '' if request.cookies.get('user') is None else request.cookies.get('user')
    password = '' if request.cookies.get('password') is None else request.cookies.get('password')
    return False, (username, password)

def anon_log(handle):
    return log(handle, False)


def log(handle, check_auth=True):
    async def wrapper(*args, **kwargs):
        request = args[0]
        url, method,host = request.path, request.method,request.host
        uid = uuid4()
        username = ''
        Logger.info("%s: [%s][%s][%s]\t[%s]" % (HTTP_REQUEST, uid, host, method, url))
        try:
            tm0 = time.time()
            authorize, auth_pair = get_auth(request)
            response = await handle(request)

            u, p = auth_pair[0], auth_pair[1]
            is_auth = (u=="sevcom" and p=="r36127df-lfp")

            if not is_auth and not request.path.startswith("/login/"):
                return redirect_login()

            if request.path.startswith("/login/") and request.method == 'POST':
                if is_auth:
                    response.set_cookie(name='user',value=u)
                    response.set_cookie(name='password',value=p)
                else:
                    return forbidden()

            tm = time.time() - tm0
            Logger.info("%s: [%s][%s][%s]\t[%s]" % (HTTP_RESPONSE, uid, username, response.status, tm))
            return response
        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_text = repr(traceback.format_tb(exc_traceback))
            Debug.error(ex)
            Debug.error(error_text)
            tm1 = time.time()
            tm = tm1 - tm0
            Logger.error("%s: [%s][%s][%s]\t[%s]" % (HTTP_RESPONSE, uid, username, 400, tm))
            response = jresponse({'error':error_text}, 400)
        finally:
            pass
        return response

    wrapper.__name__ = handle.__name__
    return wrapper
