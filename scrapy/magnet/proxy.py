import sys
# from handledb import exec_sql
import socket
# import urllib2

# dbapi = "MySQLdb"
# kwargs = {'user': 'root', 'passwd': 'toor', 'db': 'ippool', 'host': 'localhost', 'use_unicode': True}


def counter(start_at=0):
    """
    功能: 计数
    用法: f=counter(i) print f() #i+1
    """

    count = [start_at]

    def incr():
        count[0] += 1
        return count[0]
    return incr


def use_proxy(browser, proxy, url):
    """Open browser with proxy"""
    # After visited transfer ip
    profile = browser.profile
    profile.set_preference('network.proxy.type', 1)  
    profile.set_preference('network.proxy.http', proxy[0])  
    profile.set_preference('network.proxy.http_port', int(proxy[1]))  
    profile.set_preference('permissions.default.image', 2)
    profile.update_preferences() 
    browser.profile = profile
    browser.get(url)
    browser.implicitly_wait(30)
    return browser


class Singleton(object):
    """ 单例模式 """
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance
    # def __new__(cls, *args, **kw):
    #     if cls._instance is None:
    #         cls._instance = object.__new__(cls, *args, **kw)
    #     return cls._instance


class GetIp(Singleton):
    def __init__(self):
        # sql = '''SELECT  `IP`,`PORT`,`TYPE`
        # FROM  `proxy`
        # WHERE `TYPE` REGEXP  'HTTP|HTTPS'
        # AND  `SPEED`<5 OR `SPEED` IS NULL
        # ORDER BY `proxy`.`TYPE` ASC
        # LIMIT 50 '''
        # self.result = exec_sql(sql, **kwargs)
        self.result = []
        with open('ip.txt', 'r') as f:
            for line in f.readlines():
                record = line.strip().split(' ')
                self.result.append(record)

    def get_ips(self):
        print(" Proxy getip 被执行 ")
        # http = [h[0:2] for h in self.result if h[2] == "HTTP" and self.judge_ip(h)]  # 取出所有http的ip及端号
        # https = [h[0:2] for h in self.result if h[2] == "HTTPS" and self.judge_ip(h)] # 取出所有https的ip及端号
        http = [h[0:2] for h in self.result if h[2] == "HTTP"]
        https = [h[0:2] for h in self.result if h[2] == "HTTPS"]
        print("Http: ", len(http), "Https: ", len(https))  # 打印输出
        return {"http": http, "https": https}  # 返回获取的ip及端号


        # @staticmethod
    # def del_ip(record):
    #     """
    #     删除没用的ip
    #     """
    #     sql = "delete from proxy where IP='%s' and PORT='%s'" % (record[0], record[1])
    #     print(sql)
    #     exec_sql(sql, **kwargs)
    #     print(record, " was deleted.")
"""
    def judge_ip(self, record):
        http_url = "http://www.baidu.com/"
        https_url = "https://www.alipay.com/"
        proxy_type = record[2].lower()
        url = http_url if proxy_type == "http" else https_url  # 根据协议类型确定访问哪个url
        proxy = "%s:%s" % (record[0], record[1])  # 代理ip地址及端口号
        try:
            req = urllib2.Request(url=url)  # 创建请求
            req.set_proxy(proxy, proxy_type)  # 在请求中添加代理
            response = urllib2.urlopen(req, timeout=30)  # 提交请求，带超时
        except Exception as e:
            print("申请错误:", e)
            # self.del_ip(record)  # 出问题就删除ip
            return False
        else:
            code = response.getcode()  # 根据返回码判断是否可用
            # if code >= 200 and code < 300:
            if 200 <= code < 300:
                print('有效的 proxy', record)
                return True
            else:
                print('无效的 proxy', record)
                # self.del_ip(record)
                return False
"""
