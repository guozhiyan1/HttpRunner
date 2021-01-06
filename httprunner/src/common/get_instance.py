import requests
import datetime
import time
import hmac
import base64
import urllib.request
import urllib.parse
from hashlib import sha1

class ENSApiTest(object):
    # 配置基本参数
    def __init__(self):
        self.get_enviroment()

    def get_enviroment(self):
        self.getregion_url = "http://11.239.177.110"
        self.ak = "lvzy"
        self.secret = "lvzy"
        print(self.getregion_url, self.secret, self.ak)

    # 生成签名
    def eternity_sign(self, requestmethod, para_dict, secret):
        # 遍历参数
        para = [(k, para_dict[k]) for k in sorted(para_dict.keys())]
        para = urllib.parse.urlencode(para).replace('+', '%20').replace('%27', '%22')  # 空格特殊
        para = urllib.parse.quote(para)
        # para = para.replace('=','%3D').replace('&','%26').replace('*','%2A')
        # para = para.replace('=','%3D').replace('&','%26').replace('*','%2A')
        para = requestmethod.upper() + '&' + '%2F' + '&' + para
        para = para.encode('utf-8')
        SECRET_KEY = secret + '&'
        SECRET_KEY = bytes(SECRET_KEY, encoding='utf-8')

        # 加密md5
        sign = hmac.new(SECRET_KEY, para, sha1).digest()
        sign = base64.b64encode(sign)
        sign = urllib.parse.quote(sign)
        sign = sign.replace('/', '%2F')
        return sign

    # 拼接URL参数
    def generateurl(self, parasd):
        ts = int(time.time()) - 1  # 生成当前时间
        ak = self.ak
        secret = self.secret
        parasd0 = {'ak': ak, 'ts': ts}

        url = parasd['url']
        method = parasd['method']
        parasd.pop('url')
        parasd.pop('method')

        parasdict = dict(parasd0, **parasd)
        sign = self.eternity_sign(method, parasdict, secret)
        url_other = ''
        for k, v in parasdict.items():
            if k == 'pdata':  ###这个地方需要改，post的请求body部分不能加到url中，现只针对下单暂时这样处理
                pass
            else:
                url_other = url_other + k + '=' + str(v) + '&'

        url = url + url_other + 'sign=' + sign
        return url

    # 发起GET请求
    def httpget(self, url):
        r = requests.get(url, timeout=10)
        result = r.json()
        return result

    #获取实例列表
    def get_instance(self):
        url = self.getregion_url + '/v1/instance?'
        parasd = {'method': 'get', 'url': url, 'employee_id': '2222', "page_size": 100, "order_by_params": '{\"created_at\": \"desc\"}'}
        url = self.generateurl(parasd)
        result = self.httpget(url)
        lists = [i['uuid'] for i in result['data']]
        return lists

if __name__ == '__main__':

    print("*"*50)
    n = ENSApiTest()
    newlist = n.get_instance()
    print(newlist)