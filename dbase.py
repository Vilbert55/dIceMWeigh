import motor.motor_asyncio
from bson import json_util
from datetime import datetime, timedelta
import requests
import subprocess
import time
from config import Debug

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
def list_get (l, idx, default):
  try:
    return l[idx]
  except IndexError:
    return default
def str2time(tmstr):
    if tmstr is None:
        tmstr = datetime.datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")
    if len(tmstr)==16:
        tmstr += ':00'
    return time.strptime(tmstr, "%Y-%m-%d %H:%M:%S")
def deltatimes(tm1,tm2):
    tm1 = tm1 if tm1 else time.strftime("%Y-%m-%d %H:%M:%S")
    tm2 = tm2 if tm2 else time.strftime("%Y-%m-%d %H:%M:%S")
    return time.mktime(str2time(tm2)) - time.mktime(str2time(tm1))
def seconds_to_hhmmss(seconds):
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    return int(hours), int(minutes), int(seconds)

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
        return result

    async def _get_report_head(self, fs, date=None):
        # Получить текущий отчёт или за определённую дату
        date = date or curdt_mysql()
        _filter = {"dttm":{ "$regex": ".*{}.*".format(date),"$options":"i" },"fs":{"$eq" : fs}}
        document = await self.db.reports_head.find_one(_filter)
        return document

    async def insert_or_update_report_head(self, item, fs, date=None):
        report_head = await self._get_report_head(fs, date)
        if report_head:
            await self.db.reports_head.update_one({"_id":report_head.get('_id')}, { '$set' : item }, upsert=True)
        else:
            await self.db.reports_head.insert_one(item)

    async def dashboard_get_values(self):
        Debug.info("begin get values for dashboard")
        data = {"weigh1":{},"weigh2":{},"weigh3":{}}
        for fs in data:
            try:
                code, json = fsproxy(fs, "/api/v1/report_head","get")
            except:
                code, json = 500, {}
            if code != 200:
                data_backup = await self._get_report_head(fs)
                if data_backup:
                    Debug.warning("dashboard_get_values: %s data_backup, response_code %s" % (fs, code))
                    data[fs] = data_backup
                    data[fs]["status"] = "data_backup"
                    del data[fs]["_id"]
                else:
                    Debug.warning("dashboard_get_values: %s no data" % fs)
                    data[fs]["status"] = "no_data"
            else:
                Debug.info("dashboard_get_values: %s response_code %s" % (fs, code))
                data[fs] = json
                data[fs]["status"] = "online"
                data[fs]["fs"] = fs
                data[fs]["dttm_data"] = curdt_mysql() + ' ' + curtm_mysql()
                del data[fs]["_id"]
                await self.insert_or_update_report_head(data[fs], fs)
        result = await self.merge_dashboard_values(data)
        return result

    async def merge_dashboard_values(self, data):
        # объединяем данные weigh1 и weigh3
        data["weigh1_backup"] = data["weigh1"]
        data["weigh3_backup"] = data["weigh3"]
        if data["weigh3"]["status"] != "no_data" and data["weigh1"]["status"] != "no_data":
            summ_fields = ["count", "weight", "count_h", "weight_brak", "total_fact", "count_pereves",
                "count_packages", "count_packages_v2", "count_packages_v3_h", "count_packages_v3"]
            for k in summ_fields:
                data["weigh1"][k] += data["weigh3"][k]
                data["weigh1"][k] = round(data["weigh1"][k], 2)
            for h2 in data["weigh3"]["prods_by_hours"]:
                for h in data["weigh1"]["prods_by_hours"]:
                    if h["hour"] == h2["hour"]:
                        h["prods_list"] += h2["prods_list"]
            data["weigh1"]["procent_brak"] = percentage(data["weigh1"]["weight_brak"], data["weigh1"]["weight"])
            data["weigh1"]["procent_pereves"] = percentage(data["weigh1"]["count_pereves"], data["weigh1"]["total_fact"])
            data["weigh1"]["procent_plan"] = percentage(data["weigh1"]["total_fact"], data["weigh1"]["total_plan"])

            if "no_data" in (data["weigh1"]["status"], data["weigh3"]["status"]):
                data["weigh1"]["status"] = "no_data"
            elif "data_backup" in (data["weigh1"]["status"], data["weigh3"]["status"]):
                data["weigh1"]["status"] = "data_backup"
            if "stop" in (data["weigh1"]["work_status"], data["weigh3"]["work_status"]):
                data["weigh1"]["work_status"] = "stop"
            data["weigh1"]["dttm_data"] = min(data["weigh3"]["dttm_data"], data["weigh1"]["dttm_data"])
        elif data["weigh3"]["status"] != "no_data" and data["weigh1"]["status"] == "no_data":
            data["weigh1"] = data["weigh3"]
                    
        del data["weigh3"]
        return data

    async def worktime_get_values(self, jdata):
        date, fs = jdata.get('date'), jdata.get('fs')
        report = await self._get_report_head(fs, date)
        if not report or not report.get('work_intervals'):
            return False
        result = {'intervals':[]}
        work_time = 0
        for interval in report['work_intervals']:
            item = {}
            item['tm1'] = list_get(interval, 0, 'нет данных')
            item['tm2'] = list_get(interval, 1, 'нет данных')
            if len(interval) == 2:
                worktime_seconds = deltatimes(interval[0],interval[1])
                hh,mm,ss = seconds_to_hhmmss(worktime_seconds)
                item['worktime_seconds'] = worktime_seconds
                item['worktime_str'] = "%s часов %s минут" % (hh,mm)
                work_time += worktime_seconds
            else:
                item['worktime_str'] = 'нет данных'
            (result['intervals']).append(item)
        hh,mm,ss = seconds_to_hhmmss(work_time)
        result['worktime_seconds'] = work_time
        result['worktime_str'] = "%s часов %s минут" % (hh,mm)
        return result
            
