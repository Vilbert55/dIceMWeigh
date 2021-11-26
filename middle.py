import time
from config import *
from uuid import uuid4
import sys,traceback
from aiohttp import web 
import asyncio

HTTP_REQUEST = "RQ"
HTTP_RESPONSE  = "RS"


def log(handle):
    async def wrapper(*args, **kwargs):
        request = args[0]
        url, method,host = request.path, request.method,request.host
        uid = uuid4()
        username = ''
        Logger.info("%s: [%s][%s][%s]\t[%s]" % (HTTP_REQUEST, uid, host, method, url))
        try:
            tm0 = time.time()
            response = await handle(request)
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
