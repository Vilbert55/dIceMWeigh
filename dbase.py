import motor.motor_asyncio
from bson import json_util
from datetime import datetime, timedelta
import requests
import subprocess

def curdt_mysql():
    return datetime.now().strftime(format="%Y-%m-%d")
def curtm_mysql():
    return datetime.now().strftime(format="%H:%M:%S")
def tm5m_mysql():
    tm = datetime.now() - timedelta(minutes=5)
    return tm.strftime(format="%H:%M:%S")
def tmh_mysql():
    tm = datetime.now() - timedelta(minutes=60)
    return tm.strftime(format="%H:%M:%S")
def percentage(part, whole):
    if not (part and whole):
        return 0.0
    return round(100.0 * part/whole, 2)

def setup_db():
    return motor.motor_asyncio.AsyncIOMotorClient().IceMWeigh

def run_cmd(cmd,timeout=300):
    try:
        r = subprocess.run(cmd, timeout = timeout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout=r.stdout.decode("utf8")
        stderr=r.stderr.decode("utf8")
        return r.returncode == 0,stdout,stderr
    except subprocess.TimeoutExpired:
        print("exception ",cmd)
        return False,"",""

def request_proxy(url,method,params):
    if method == 'get':
        return requests.get(url,params=params,timeout=30)
    else:
        return requests.post(url,json=params,timeout=30)

def ping(host):
    result,stdout,stderr = run_cmd(["ping","-c","1","-W","2",host],4)
    return result

def fsproxy(ip,_url,method,params={}):
    #ip = "localhost"  # заглушка для теста
    if not ping(ip):
        return 500,"not ping"
    url = "http://%s:20040%s" % (ip, _url)
    data = request_proxy(url,method,params)
    return data.status_code, data.json()


class DB:
    def __init__(self):
        self.db = setup_db()
        print(self.db)
        self.sets = {}
        self.prods = []
        self.prods_head = []
        self.reports_head = []

    async def inc_counters(self,field):
        # Автоинкремент
        r = await self.db.counters.find_one_and_update({"_id":field},  { "$inc" : { "value" : 1 } }, upsert = True)
        if r:
            return r["value"]
        else:
            return 1

    async def get_sets(self):
        # Получить все настройки
        self.sets = {}
        async for document in self.db.sets.find():
            self.sets[document['id']] = document['value'] 
        return self.sets
    
    async def put_set(self,item):
        # Записать настройку item {"id":id,"value":value}
        result =  await self.db.sets.replace_one({"id":item.get("id")}, item, upsert=True)
        if 'cur_good' == item.get('id'):
            # Записываем текущий товар в текущее взвешивание
            productid = item.get('value')
            good = await self._get_good({"id":productid})
            result = await self.upd_prods_head({'productid':productid,'article':good['vendor_code']})
        return result

    async def dashboard_get_values(self):
        data = {"weigh1":{},"weigh2":{}}
        for fs in data:
            code, json = fsproxy(fs, "/api/v1/report_head","get")
            if code != 200:
                data[fs]["status"] = "not_connect"
            else:
                data[fs] = json
                data[fs]["status"] = "inwork"
        return data
