#!/use/bin/python3
# -*- coding: utf-8 -*-


import random
import requests
import json
import datetime
import time
import sqlite3

import user_agent


# CONFIG LOCATION
v_conf = 'config.json'
v_database = 'socks5.db'


# GET NOW 
def get_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# GET TIMESTAMP INT
def get_timestamp(dt):
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    return int(timestamp)


# GET CONFIG
def get_config():
    with open(v_conf, "r") as f:
        return json.load(f)

# GET RANDOM UserAgent
def get_randua():
    return random.choice(user_agent.vListUserAgent)

# GET RANDOM IP ADDRESS
def get_randip():
    a = str(random.randint(0, 255))
    b = str(random.randint(0, 255))
    c = str(random.randint(0, 255))
    d = str(random.randint(0, 255))
    xIP = a + '.' + b + '.' + c + '.' + d
    return xIP

# GET RANDOM PORT
def get_randport():
    return random.choice(range(1,65536))


# GET URL RESPONSE THROUGH SOCK5 PROXY
def checkSocks5Status(aURL, aIP, aPort, aUA, aTimeout):
    try:
        rHeader = {"User-Agent": aUA}
        vProxy = 'socks5://%s:%s' % (aIP, str(aPort))
        rProxies = {'http': vProxy, 'https': vProxy}
        res = requests.get(url = aURL, headers = rHeader, proxies = rProxies, timeout = aTimeout)
        print("    + RSP %d <-- %s" % (res.status_code, aURL))
        if res.status_code == 200:
            print("    + checkSocks5Status OKAY")
            return 'Y'
        else:
            print("    + checkSocks5Status UNKNOWN")
            return 'N'
    except Exception as e:
        print("    + checkSocks5Status TIMEOUT")
#        print(e)
        return 'N'

# RUN SQL TO INSERT/UPDATE DATA
def run_SQL(aDB, aSQL):
    try:
        conn = sqlite3.connect(aDB)
        csr = conn.cursor()
        csr.execute(aSQL)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def rungogogo():
    aIP = get_randip()      # 随机生成一个IP
    aPort = get_randport()  # 随机生成一个端口Port
    aUA = get_randua()      # 随机获取一个浏览器的UA
    print("+ IP: %s" % aIP)
    print("  + USERAGENT:%s" % aUA)
    conf = get_config()     # 获取配置文件的信息
    checkSocks5URL = conf.get("CheckURL")    # 获取配置文件中 用于检测socks5可用性的网址
    checkPorts = conf.get("CheckPorts")    # 获取配置文件中 固定会检测的端口列表
    checkPorts.append(aPort)

#   逐一对当前IP 需要检测的端口 进行检测
    for aSeqPort in checkPorts:
        print("    + CHECK PORT: %d" % aSeqPort)
#   检测socks5的状态
        vResponseStatus = checkSocks5Status(aURL = checkSocks5URL, aIP = aIP, aPort = aSeqPort, aUA = aUA, aTimeout = 6)

#   时间的信息
        vNow = get_now()
        vNowTS = get_timestamp(vNow)
        print("    + TIME FMT %s   TIMESTAMP %d" % (vNow,vNowTS))

        iSQL = "insert into socks5 (ip, port) values('%s', %d) " % (aIP, aSeqPort)
        uSQL = "update socks5 set itime = '%s', itimestamp = %d, status = '%s' where ip = '%s' and port = %d" % (vNow, vNowTS, vResponseStatus, aIP, aSeqPort)
        print(iSQL)
        print(uSQL)

#   检测的结果数据 入库
        run_SQL(aDB = v_database, aSQL = iSQL)
        run_SQL(aDB = v_database, aSQL = uSQL)
    

if __name__ == '__main__':
#    rungogogo()
    for i in range(100000000):
        rungogogo()
