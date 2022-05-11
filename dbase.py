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
def dttm_plus_tm(dttm, sec):
    # возвращает дату и время на sec секунд позднее dttm
    dttm_tmformat = datetime.strptime(dttm, '%Y-%m-%d %H:%M:%S')
    return (dttm_tmformat+timedelta(seconds=sec)).strftime(format="%Y-%m-%d %H:%M:%S")
def list_get (l, idx, default=None):
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
    try:
        if not ping(ip):
            return 500,{}
        url = "http://%s:20040%s" % (ip, _url)
        data = request_proxy(url,method,params)
    except:
        return 500, {}
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
        _filter = {"dt":{"$eq" : date},"fs":{"$eq" : fs}}
        document = await self.db.reports_head.find_one(_filter)
        return document

    async def _get_reports_head(self, fs, dt1, dt2):
        # получить список отчётов за интервал
        _filter = {"dt": {"$gte": dt1, "$lte": dt2}, "fs":{"$eq" : fs}}
        document = await self.db.reports_head.find(_filter).sort("dt").to_list(length=100)
        return document

    async def insert_or_update_report_head(self, item, fs, date):
        dt = curdt_mysql() if date in ["", None] else date
        Debug.info("start insert_or_update_report_head cnt fs:%s date:%s" % (fs,dt))
        await self.db.reports_head.delete_many({"dt":{"$eq" : dt}, "fs":{"$eq" : fs}})
        counter = await self.inc_counters("report_head_id")
        item["_id"] = counter
        await self.db.reports_head.insert_one(item)
        Debug.info("replaced reports_head fs:%s date:%s" % (fs, dt))

    async def upd_report_head(self, report):
        Debug.info("start upd report")

        report["count_packages_v2_brak"] = 0
        report["count_packages_v3_brak"] = 0
        report["count_packages_v4_brak"] = 0
        report["count_packages_v2_pereves"] = 0
        report["count_packages_v3_pereves"] = 0
        report["count_packages_v4_pereves"] = 0
        report["weight_pereves"] = 0
        report["count_packages_v2_norma"] = 0
        report["count_packages_v3_norma"] = 0
        report["count_packages_v4_norma"] = 0
        report["count_packages_v4"] = 0
        report["weight_norma"] = 0
        report["total_fact"] = 0
        report["total_plan"] = 0
        report["allprods"] = []
        report["prods_by_hours"] = sorted(report["prods_by_hours"], key=lambda x: x["hour"])

        for g in report["goods"]:
            report["goods"][g]["fact_v4"] = 0
            report["goods"][g]["fact"] = 0
            report["total_plan"] += report["goods"][g]["plan"]
        for i in report["prods_by_hours"]:
            for j in i["prods_list"]:
                report["allprods"].append(j)
                if j["status"] == "Брак":
                    report["count_packages_v2_brak"] += j["pack_qtt_v2"]
                    report["count_packages_v3_brak"] += j["pack_qtt_v3"]
                    report["count_packages_v4_brak"] += j.get("pack_qtt_v4",1)
                if j["status"] == "Перевес":
                    report["count_packages_v2_pereves"] += j["pack_qtt_v2"]
                    report["count_packages_v3_pereves"] += j["pack_qtt_v3"]
                    report["count_packages_v4_pereves"] += j.get("pack_qtt_v4",1)
                    report["count_packages_v4"] += j.get("pack_qtt_v4",1)
                    report["weight_pereves"] += j["weight_prod"]
                if j["status"] == "Норма":
                    report["count_packages_v2_norma"] += j["pack_qtt_v2"]
                    report["count_packages_v3_norma"] += j["pack_qtt_v3"]
                    report["count_packages_v4_norma"] += j.get("pack_qtt_v4",1)
                    report["count_packages_v4"] += j.get("pack_qtt_v4",1)
                    report["weight_norma"] += j["weight_prod"]

                if j["status"] != "Брак":
                    report["total_fact"] += 1
                    if j["id"] in report["goods"]:
                        report["goods"][j["id"]]["fact_v4"] += j.get("pack_qtt_v4",1)
                        report["goods"][j["id"]]["fact"] += 1
                    else:
                        report["goods"][j["id"]] = {
                            "article": j["article"],
                            "name": j["article"],
                            "plan": 0,
                            "fact": 1,
                            "fact_v4": j.get("pack_qtt_v4",1),
                        }

        report["procent_pereves"] = percentage(report["count_packages_v4_pereves"],\
            report["count_packages_v4"]+report["count_packages_v4_brak"])
        report["procent_brak"] = percentage(report["count_packages_v4_brak"],\
            report["count_packages_v4"]+report["count_packages_v4_brak"])
        if report.get("_id"):
            del report["_id"]
        Debug.info("end upd report")
        return report

    async def dashboard_get_values(self, dt):
        Debug.info("begin get values for dashboard")
        data = {"weigh1":{},"weigh2":{},"weigh3":{}}
        for fs in data:
            code, json = 500, {}
            if not dt:
                code, json = fsproxy(fs, "/api/v1/report_head","get")
            if code != 200:
                json = await self._get_report_head(fs, dt)
                if json:
                    if not dt:
                        Debug.warning("dashboard_get_values: %s data_backup, response_code %s" % (fs, code))
                    data[fs]["status"] = "data_backup"
                elif dt:
                    url = "/api/v1/report_head?date=%s" % dt
                    code, json = fsproxy(fs, url,"get")
            if json:
                Debug.info("dashboard_get_values: %s response_code %s" % (fs, code))
                data[fs] = await self.upd_report_head(json)
                data[fs]["fs"] = fs
                data[fs]["status"] = "data_backup"
                if not dt:
                    if code == 200:
                        data[fs]["status"] = "online"
                        data[fs]["dttm_data"] = curdt_mysql() + ' ' + curtm_mysql()
                else:
                    data[fs]["dttm_data"] = json["dt"]
                if code == 200:
                    await self.insert_or_update_report_head(data[fs], fs, dt)
                if data[fs].get("_id"):
                    del data[fs]["_id"]
            else:
                data[fs]["status"] = "no_data"                    

        result = await self.merge_dashboard_values(data)
        return result

    async def merge_dashboard_values(self, data):
        # объединяем данные weigh1 и weigh3
        data["weigh1_backup"] = data["weigh1"]
        data["weigh3_backup"] = data["weigh3"]

        if data["weigh3"]["status"] != "no_data" and data["weigh1"]["status"] != "no_data":
            summ_fields = ["count", "weight", "count_h", "weight_brak", "total_fact", "count_pereves",
                "count_packages", "count_packages_v2", "count_packages_v3_h", "count_packages_v3", "count_packages_v4",
                "count_packages_v2_brak", "count_packages_v3_brak", "count_packages_v4_brak",
                "count_packages_v2_pereves", "count_packages_v3_pereves", "count_packages_v4_pereves",
                "weight_pereves", "count_packages_v2_norma", "count_packages_v3_norma", "count_packages_v4_norma",
                "weight_norma", "allprods"]

            for k in summ_fields:
                if not data["weigh1"].get(k):
                    data["weigh1"][k] = 0
                if data["weigh3"].get(k):
                    data["weigh1"][k] += data["weigh3"][k]
                if k != "allprods":
                    data["weigh1"][k] = round(data["weigh1"][k], 2)
            for h2 in data["weigh3"]["prods_by_hours"]:
                for h in data["weigh1"]["prods_by_hours"]:
                    if h["hour"] == h2["hour"]:
                        h["prods_list"] += h2["prods_list"]
            for g2 in data["weigh3"]["goods"]:
                if g2 in data["weigh1"]["goods"]:
                    data["weigh1"]["goods"][g2]["fact"] += data["weigh3"]["goods"][g2]["fact"]
                    data["weigh1"]["goods"][g2]["fact_v4"] += data["weigh3"]["goods"][g2]["fact_v4"]
                else:
                    data["weigh1"]["goods"][g2] = data["weigh3"]["goods"][g2]

            data["weigh1"]["procent_brak"] = percentage(data["weigh1"]["count_packages_v4_brak"],\
                data["weigh1"]["count_packages_v4_brak"] + data["weigh1"]["count_packages_v4"])
            data["weigh1"]["procent_pereves"] = percentage(data["weigh1"]["count_packages_v4_pereves"],\
                data["weigh1"]["count_packages_v4_pereves"] + data["weigh1"]["count_packages_v4"])
            data["weigh1"]["procent_plan"] = percentage(data["weigh1"]["total_fact"], data["weigh1"]["total_plan"])
            if "no_data" in (data["weigh1"]["status"], data["weigh3"]["status"]):
                data["weigh1"]["status"] = "no_data"
            elif "data_backup" in (data["weigh1"]["status"], data["weigh3"]["status"]):
                data["weigh1"]["status"] = "data_backup"
            if "stop" in (data["weigh1"]["work_status"], data["weigh3"]["work_status"]):
                data["weigh1"]["work_status"] = "stop"
            data["weigh1"]["dttm_data"] = min(data["weigh3"]["dttm_data"], data["weigh1"]["dttm_data"])
        elif data["weigh3"]["status"] != "no_data" and data["weigh1"]["status"] == "no_data":
            data["weigh3"]["status"] = "no_data"
            data["weigh1"] = data["weigh3"]
                    
        del data["weigh3"]
        return data

    async def worktime_get_values(self, jdata):
        date1, date2, fs = jdata.get('date1'), jdata.get('date2'), jdata.get('fs')
        reports = await self._get_reports_head(fs, date1, date2)
        result = {'intervals':[]}
        work_time = 0
        count_packages_v4 = 0
        count_packages_v4_brak = 0
        for report in reports:
            report = await self.upd_report_head(report)
            if not report.get("allprods"):
                continue
            for pr in report.get("allprods"):
                pr["in_intervals"] = False
            if report['work_intervals'] and report["allprods"][0]["dttm"] < report['work_intervals'][0][0]:
                firts_tm1 = report["allprods"][0]["dttm"]
                first_tm2 = dttm_plus_tm( report['work_intervals'][0][0], -1)
                report['work_intervals'] = [[firts_tm1, first_tm2]] + report['work_intervals']
            if not report['work_intervals']:
                firts_tm1 = report["allprods"][0]["dttm"]
                first_tm2 = report["allprods"][-1]["dttm"]
                report['work_intervals'] = [[firts_tm1,first_tm2]]
            for interval in report['work_intervals']:
                item = {"count_packages_v4": 0, "count_packages_v4_brak": 0}
                item['tm1'] = list_get(interval, 0)
                item['tm2'] = list_get(interval, 1, report["allprods"][-1]["dttm"])
                if item['tm1'][:10] < date1 or item['tm2'][:10] > date2:
                    continue

                worktime_seconds = deltatimes(item['tm1'],item['tm2']) or 1
                hh,mm,ss = seconds_to_hhmmss(worktime_seconds)
                item['worktime_seconds'] = worktime_seconds
                item['worktime_str'] = "%s часов %s минут" % (hh,mm)
                work_time += worktime_seconds

                for prod in report["allprods"]: 
                    if prod["dttm"] >= item['tm1'] and prod["dttm"] <= item['tm2']:

                        prod["in_intervals"] = True
                        if prod["status"] != "Брак":
                            count_packages_v4 += prod.get("pack_qtt_v4",1)
                            item["count_packages_v4"] += prod.get("pack_qtt_v4",1)
                        else:
                            count_packages_v4_brak += prod.get("pack_qtt_v4",1)
                            item["count_packages_v4_brak"] += prod.get("pack_qtt_v4",1)

                if item["count_packages_v4_brak"] or item["count_packages_v4"]:
                    total_cnt = item["count_packages_v4"] + item["count_packages_v4_brak"]
                    item["performance"] = round(item["count_packages_v4"]/(worktime_seconds/3600),2)
                    item["percent_brak"] = percentage(item["count_packages_v4_brak"],total_cnt)
                    (result['intervals']).append(item)

        if not work_time:
            return None

        miss_prods = list(filter(lambda x: x["in_intervals"] == False, report["allprods"]))
        if miss_prods:
            index, max_value = max(enumerate(result['intervals']), key=lambda i: i[1]["count_packages_v4"])
        for prod in miss_prods:
            if prod["status"] != "Брак":
                count_packages_v4 += prod.get("pack_qtt_v4",1)
                result['intervals'][index]["count_packages_v4"] += prod.get("pack_qtt_v4",1)
            else:
                count_packages_v4_brak += prod.get("pack_qtt_v4",1)
                result['intervals'][index]["count_packages_v4_brak"] += prod.get("pack_qtt_v4",1)

        hh,mm,ss = seconds_to_hhmmss(work_time)
        result['worktime_seconds'] = work_time
        result['worktime_str'] = "%s часов %s минут" % (hh,mm)
        result['count_packages_v4'] = count_packages_v4
        hours = work_time / 3600
        result['performanse'] = round(count_packages_v4/hours, 2)
        total_cnt = count_packages_v4_brak + count_packages_v4
        result['count_packages_v4_brak'] = count_packages_v4_brak
        result['percent_brak'] = percentage(count_packages_v4_brak,total_cnt)
        return result
            
    async def get_prods_head_total(self, jdata):
        code, json = fsproxy(jdata["fs"], "/api/v1/prods_head_list", "post")
        return json

    async def get_prods(self, jdata):
        code, json = fsproxy(jdata["fs"], "/api/v1/prods", "get", {"head_id": jdata["head_id"]})
        return json


