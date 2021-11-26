import logging
import yaml
import os
from aiohttp import web
from decimal import Decimal, ROUND_HALF_UP
import aiohttp_jinja2
import jinja2
from bson import json_util
import asyncio

DEFAULT_PORT = 20041
API_VERSION_DEFAULT = '1'
API_VERSION_1 = '1'

def _roundup(val,deep):
    real = "0"*deep
    return float( Decimal("%.4f" % val).quantize(Decimal("1."+real),rounding=ROUND_HALF_UP) )

def url_api(url,version=API_VERSION_DEFAULT):
    return f"/api/v{version}{url}"

def tresponse(request, template, data):
    #aiohttp_jinja2.setup(request.app, loader=jinja2.FileSystemLoader('templates'))
    return aiohttp_jinja2.render_template(template, request, data)

def jresponse(data, code=200):
    return web.json_response(data,status=code)

def jmresponse(data, code=200):
    return web.Response(text=json_util.dumps(data))

def upresult(result):
    res = {}
    for prop in ['modified_count','upserted_id','inserted_id']:
        if hasattr(result, prop):
            res[prop] = result.__getattribute__(prop)
    return res

async def get_sets(db):
    return await db.get_sets()


VERSION = "0.0.1"

# CONSTANTS
COOKIES     = "secret"
CONFIG_PATH = "config.yml"

DEFAULT_CONFIG = {
    'database':{
        "name": "IceMWeigh",
    },
    'server':{
        'port':DEFAULT_PORT
    },
    'log' : {
        "path_debug" : "log",
        "path_journal" : "log",
        "level": "DEBUG",
        "level_db": "WARNING"
    }
}


def read_config():
    if os.path.exists(CONFIG_PATH):
        config = yaml.load(open(CONFIG_PATH))
    else:
        config = {}
    for i,v in DEFAULT_CONFIG.items():
        if not i in config:
            config[i] = v
    return config

def init_logger(path, level, name):
    log = logging.getLogger(name)
    log.setLevel(level)
    fmt  = logging.Formatter('%(asctime)s,%(msecs)03d\t%(levelname)s\t%(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(path + "/" + name + ".log")
    handler.setLevel(level)
    handler.setFormatter(fmt)
    log.addHandler(handler)
    return log

CONF = read_config()
Logger = init_logger('log','INFO','journal')
Debug = init_logger('log','DEBUG','debug')


