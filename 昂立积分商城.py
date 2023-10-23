'''
cron: 50 */30 8-22 * * *
new Env('f昂立积分商城');
入口微信打开：#小程序://昂立积分商城/4rF8vR9m4i9Q06g或者搜索：昂立积分商城
tg频道地址：https://t.me/ymxzpd
tg频道群组:https://t.me/yangmaoxz
使用方法：
1.微信打开活动入口
2.抓包任意https://points-mall.henshihui.com的cookie中的PHPSESSID参数,
例如：Cookie: PHPSESSID=12345
12345就是cookie
3.青龙环境变量菜单，添加本脚本环境变量
填写变量参数时,为方便填写可以随意换行
名称 ：aljf
单个账户参数： [{'bei_zhu':'测试','cookie':'1234'}]
多个账户[{'bei_zhu':'测试','cookie':'1234'},{'bei_zhu':'测试','cookie':'1234'}]

或者在青龙环境变量配置文件中填写
填写变量参数时为方便填写可以随意换行
单个账户参数： export aljf="[{'bei_zhu':'测试','cookie':'1234'}]"
多个账户：export aljf="[
    {'bei_zhu':'测试','cookie':'1234'},
    {'bei_zhu':'测试','cookie':'1234'}
]"
参数说明与获取：
bei_zhu:备注随意填写
ck:打开活动入口，抓包获取
4.新用户注册奖励请手动领取
cron: 12 8 * * *
new Env('昂立积分商城');
'''
import os
import json
import time
import requests
#青龙默认推送，若要开启推送，请去除下方#号
#import notify
import random


def getEnv():
    env = os.getenv('aljf')
    if env == None:
        print('请检查变量参数是否填写')
        exit(0)
    try:
        env = json.loads(env.replace("'", '"').replace("\n", ""))
        return env
    except Exception as e:
        print('错误:', e)
        print('你填写的变量是:', env)
        print('请检查变量参数是否填写正确')
        exit(0)


class ALShop():
    def __init__(self, cg):
        self.heaers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8447',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wxf1438acf10b6cd3b/4/page-frame.html',
            'Cookie': f'PHPSESSID={cg["cookie"]}'
        }
        self.name = cg['bei_zhu']
        self.sec = requests.session()
        self.sec.headers = self.heaers

    def myInfo(self):
        u = 'https://points-mall.henshihui.com/index/personal-center/get-user-info?s_ver=1&applicationId=4066'
        r = self.sec.get(u)
        rj = r.json()
        if rj.get('return_code') != 'SUCCESS':
            print(rj)
            print('变量参数失效或者填写错误')
            self.pstr += '变量参数失效或者填写错误\n'
            return False
        self.balance = rj.get('return_msg').get('balance').get('2')
        return True
    def signDay(self):
        pm = 'activityId=5520&s_ver=1&applicationId=4066'
        u = 'https://points-mall.henshihui.com/activity/sign-h5/sign?' + pm
        r = self.sec.post(u, data=pm)
        # print(r.text)
        rj = r.json()
        if rj.get('return_code') == 'SUCCESS':
            print(f'签到成功获得{rj["return_msg"]["prize"]["pointsNum"]}橙长点')
        else:
            print(rj['return_msg'])

    def getTaskListAndDoTask(self):
        try:
            u = 'https://points-mall.henshihui.com/task/api/show-app-task?pageSize=10&s_ver=1&applicationId=4066'
            r = self.sec.get(u)
            rj = r.json()
            if rj.get('return_code') != 'SUCCESS':
                return False
            taskList = rj['return_msg']['taskContent']['content']['task']['taskList']
            time.sleep(random.randint(2, 5))
            specific_values = ['新用户注册','邀好友赚积分兑好礼']
            for item in taskList[:]:
                if item.get('taskName') in specific_values:
                    taskList.remove(item)
            for i in taskList:
                self.doTask(i)
        except Exception as e:
            print(e)
            print('任务列表获取异常')
            self.pstr+='任务列表获取异常\n'
    def doTask(self, info):
        print('-' * 20)
        print(f'做任务:', info['taskName'])
        try:
            for i in range(int(info['limit'])):
                pm = f'taskKey={info["taskKey"]}&activityId=1680160450650001&s_ver=1&applicationId=4066'
                u = 'https://points-mall.henshihui.com/task/api/report-task?' + pm
                r = self.sec.post(u, data=pm)
                if '已经完成' in r.text:
                    print('任务已经完成')
                    time.sleep(random.randint(2, 5))
                    break
                rj = r.json()
                if rj.get('return_code') == 'SUCCESS':
                    print(rj['return_msg']['msg'])
                else:
                    print(rj['return_msg'])
                time.sleep(random.randint(2, 5))
        except Exception as e:
            print(e)
            print('做任务异常')

    def main(self):
        global gpstr
        self.pstr = f'{self.name}\n'
        print('账号：',self.name)
        if self.myInfo():
            old = self.balance
            time.sleep(random.randint(1, 3))
            self.signDay()
            time.sleep(random.randint(1, 3))
            self.getTaskListAndDoTask()
            time.sleep(random.randint(1, 3))
            self.myInfo()
            new = self.balance
            total = int(new) - int(old)
            self.pstr+=f'橙长点:{self.balance}\n本次任务获取{total}橙长点\n'
            print(f'橙长点:{self.balance}\n本次任务获取{total}橙长点\n')
        gpstr+=f'{self.pstr}\n{"-"*20}\n'
if __name__ == '__main__':
    gpstr=''
    for cg in getEnv():
        print('=' * 30)
        api = ALShop(cg)
        api.main()
    # 青龙默认推送，若要开启推送，请去除下方#号
    #notify.send('昂立积分商城',gpstr)
