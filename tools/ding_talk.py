import json
import urllib3
from config import config


def DingTalkSend(result):
    context = {
     "msgtype": "markdown",
     "markdown": {
         "title": "[gmc-http-test]自动化测试",
         "text": f"### gmc-http-test自动化测试结果\n>####  [查看测试报告]({result['url']}) \n>####  [查看构建地址]({result['jenkins_url']}) \n"
                 f"#### 测试结果：{result['result']}\n"
                 f"#### 通过用例：{result['pass']}\n"
                 f"#### 失败用例：{result['fail']}\n"
                 f"#### 跳过用例：{result['skip']}\n"
     },
     "at": {
          "atMobiles": [
              "15757115799"
          ],
          "isAtAll": False
      }
    }
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    jd = json.dumps(context)
    jd = bytes(jd, 'utf-8')
    ding_url = config.get_conf("dingding", "dingtalk_url")
    # 发送钉钉消息
    http.request('POST', ding_url, body=jd, headers={'Content-Type': 'application/json'})


if __name__ == "__main__":
    results = {'url': 'http://localhost:63342/gmc-http-test-master/reports/20210113171718.html', 'result': '测试通过',
              'jenkins_url': 'http://jenkins-gmc-dev.cfuture.shop/', 'pass': '1', 'fail': '0', 'skip': '0'}

    DingTalkSend(results)