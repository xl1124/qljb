"""
Author: lindaye
Update:2023-09-26
57Box
活动入口：小程序
添加账号说明(青龙/本地)二选一
青龙: 青龙变量boxtoken 值{"mobile":"110","password":"120"} 一行一个(回车分割)
本地: 脚本内置ck方法ck_token = [{"mobile":"110","password":"120"},{"mobile":"110","password":"120"}]
cron: 12 9 * * *
new Env('57box');
"""
version = "0.0.1"
name = "57Box"
linxi_token = "boxtoken"
linxi_tips = '{"mobile":"110","password":"120"}'
import requests
import json
import os
import time
from multiprocessing import Pool

# 变量类型(本地/青龙)
Btype = "青龙"
# 抽鞋盒开关
Limit = True
# 小啄阅读域名(无法使用时请更换)
domain = 'https://www.57box.cn/app/index.php'
# 保持连接,重复利用
ss = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/47) uni-app',
}

def user_info(i,ck):
    data = {"mobile": ck['mobile'], "password": ck['password'], "password2": "","code": "","invite_uid": "0","source": "app"}
    result = requests.post(domain+"?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=login&m=greatriver_lottery_operation", headers=headers, data=data).json()
    if result['errno'] == 0:
        token = result['data']['token']
        data = {"m": "greatriver_lottery_operation","title": "",}
        result = requests.post(domain+f"?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=getuserinfo&&token={token}", headers=headers, data=data).json()
        if result['errno'] == 999:
            print(f"账号【{i+1}】{result['message']}")
        elif result['errno'] == 0:
            print(f"账号【{i+1}】账号:{result['data']['nickname']} 矿石余额:{result['data']['integral']}")
        else:
            print(f"账号【{i+1}】错误未知{result}")
    elif result['errno'] == 999:
        print(f"账号【{i+1}】登陆错误:{result['message']}")
    else:
        print(f"账号【{i+1}】错误未知:{result}")
          


def do_read(i,ck):
    data = {"mobile": ck['mobile'], "password": ck['password'], "password2": "","code": "","invite_uid": "0","source": "app"}
    result = requests.post(domain+"?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=login&m=greatriver_lottery_operation", headers=headers, data=data).json()
    if result['errno'] == 0:
        token = result['data']['token']
        task_list = {
            "看广告领矿石":{"id":"35","answer": ""},
            "进群密码":{"id":"26","answer": "669988"},
            "每日答题":{"id":"30","answer": "普通物品不可分解"}
        }
        for task in task_list:
            print(f"账号【{i+1}】开始任务-{task}")
            data = {"m": "greatriver_lottery_operation","id": task_list[task]['id'],"answer": task_list[task]['answer']}
            if task_list[task]['id'] == "35":
                for j in range(3):
                    result = ss.post(domain+ f"?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=uptaskinfo&&token={token}", headers=headers, data=data).json()
                    if result['errno'] == 999:
                        print(f"账号【{i+1}】任务失败:{task}第{j+1}次 {result['message']}")
                        break
                    elif result['errno'] == 0:
                        print(f"账号【{i+1}】任务成功:{task}第{j+1}次 {result['message']}")
                        time.sleep(5)
                    else:
                        print(f"账号【{i+1}】错误未知:{task}第{j+1}次 {result}")
                        break
            else:
                result = ss.post(domain+ f"?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=uptaskinfo&&token={token}", headers=headers, data=data).json()
                if result['errno'] == 999:
                    print(f"账号【{i+1}】任务失败:{task} {result['message']}")
                elif result['errno'] == 0:
                    print(f"账号【{i+1}】任务成功:{task} {result['message']}")
                else:
                    print(f"账号【{i+1}】错误未知:{task} {result}")
            time.sleep(3)
        if Limit:
            params = {
                "i": "2","t": "0","v": "1","from": "wxapp","c": "entry",
                "a": "wxapp","do": "openthebox","token": token,
                "m": "greatriver_lottery_operation",
                "box_id": "303","paytype": "1","answer": "","num": 1
            }
            result = ss.post(domain, headers=headers, data=params).json()
            if result['errno'] == 0:
                complete_prize_title = result['data']['prizes_data'][0]['complete_prize_title']
                prize_market_price = result['data']['prizes_data'][0]['prize_market_price']
                print(f"账号【{i+1}】任务成功:开鞋盒 {result['message']}-{complete_prize_title} 市场价:{prize_market_price}")
            elif result['errno'] == 999:
                print(f"账号【{i+1}】任务失败:开鞋盒 {result['message']}")
            else:
                print(f"账号【{i+1}】错误未知:开鞋盒 {result}")
        else:
            print(f"账号【{i+1}】开鞋盒: 此功能未启用!")
    elif result['errno'] == 999:
        print(f"账号【{i+1}】登陆错误:{result['message']}")
    else:
        print(f"账号【{i+1}】错误未知:{result}")


if __name__ == "__main__":
    print(f"""██╗     ██╗███╗   ██╗██╗  ██╗██╗      ███████╗███████╗██████╗  ██████╗ ██╗  ██╗
██║     ██║████╗  ██║╚██╗██╔╝██║      ██╔════╝╚════██║██╔══██╗██╔═══██╗╚██╗██╔╝
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗███████╗    ██╔╝██████╔╝██║   ██║ ╚███╔╝ 
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝╚════██║   ██╔╝ ██╔══██╗██║   ██║ ██╔██╗ 
███████╗██║██║ ╚████║██╔╝ ██╗██║      ███████║   ██║  ██████╔╝╚██████╔╝██╔╝ ██╗
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝      ╚══════╝   ╚═╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
    项目:{name}           BY-林夕          Verion: {version}(并发)
    Github仓库地址: https://github.com/linxi-520/LinxiPush
""")
    if Btype == "青龙":
        if os.getenv(linxi_token) == None:
            print(f'青龙变量异常: 请添加{linxi_token}变量示例:{linxi_tips} 确保一行一个')
            exit()
        # 变量CK列表
        ck_token = [json.loads(line) for line in os.getenv(linxi_token).splitlines()]
    else:
        # 本地CK列表
        ck_token = [
            # 这里填写本地变量
        ]
        if ck_token == []:
            print(f'本地变量异常: 请添加本地ck_token示例:{linxi_tips}')

    # 创建进程池
    with Pool() as pool:
        # 并发执行函数
        print("==================获取账号信息=================")
        pool.starmap(user_info, list(enumerate(ck_token)))
        print("==================开始执行任务=================")
        pool.starmap(do_read, list(enumerate(ck_token)))
        print("==================获取账号信息=================")
        pool.starmap(user_info, list(enumerate(ck_token)))


        # 关闭进程池
        pool.close()
        # 等待所有子进程执行完毕
        pool.join()

        # 关闭连接
        ss.close
        # 输出结果
        print(f"================[{name}V{version}]===============")
