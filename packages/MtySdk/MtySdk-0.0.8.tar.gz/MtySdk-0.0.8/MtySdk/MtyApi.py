#coding=utf-8

from websocket import create_connection
import json
import csv
import datetime
import sys
import matplotlib.pyplot as plt
import requests

IP = "192.168.0.114"
WSPORT = "9999"
HTTPPORT = "9999"


class MtyAuth(object):
    """
    客户信息类
    """
    def __init__(self,user_name: str = "", password: str = ""):
        self.username=user_name;
        self.password=password;

class DataApi(object):

    def clearMath(self,filePath: str):
        """
        约定格式csv文件读取函数
        :param filePath:
        :return:
        """

        try:
            with open(filePath) as f:
                csvTemplete = csv.reader(f)
                header = next(csvTemplete)

                index = 0;
                list = [];

                for row in csvTemplete:
                    model = {
                        'datetime': datetime.datetime.strftime(datetime.datetime.fromtimestamp(int(row[1][0:10])),
                                                               '%Y-%m-%d %H:%M:%S'),
                        'datetimeNano': int(row[1][0:10]),
                        'open': row[2],
                        'high': row[3],
                        'low': row[4],
                        'close': float(row[5]),
                        'volume': row[6]
                    }
                    list.append(model)
                    index += 1;

                return list;
        except Exception as e:
            print("非约定格式的csv文件")
            sys.exit(0);

    def upload(self,symboname: str, username: str, password: str, mathlist: list):
        """
        数据上传功能
        :param symboname:       品种名称
        :param username:        用户名
        :param password:        密码
        :param mathlist:        数据列表
        :return:
        """
        param = {
            'datalist': mathlist,
            'symboname': symboname,
            'username': username,
            'password': password
        }
        header = {
            'Content-Type': 'application/json;charset=UTF-8'
        }

        url = "http://%s:%s/mtyj/regresstest/data/addlist" % (IP,HTTPPORT)

        response = requests.post(url, data=json.dumps(param),headers=header, timeout=60)
        print(response.status_code)
        print(response.text)


class MtyApi(object):
    """
    API类
    """
    def __init__(self,auth: MtyAuth=""):
        """
        初始化通信管道
        :param auth:
        """
        self.IP = IP
        self.WSPORT = WSPORT
        self.HTTPPORT = HTTPPORT
        self.ws = create_connection("ws://%s:%s/mtyj/regres/%s/%s/" %(self.IP,self.WSPORT,auth.username,auth.password))
        createresult = self.ws.recv()
        print(createresult)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    def is_having(self):
        """
        队列是否还有数据
        :return:
        """
        param = {
            'function': 'ishaving'
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        result = json.loads(result)
        if (result['code'] == 200):
            return result['result']

    def query_math(self,name: str,starttime: str=None , endtime: str=None):
        """
        # 申请消费队列的消息
        ;param name:         名称
        :param starttime:   开始时间
        :param endtime:     结束时间
        :return:
        """
        param={
            'function':'registerserver',
            'name':name,
            'startDate':starttime,
            'endData':endtime
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        result = json.loads(result)
        if (result['code'] == 0):
            print(result['msg'])
            return;
        if (result['code'] == 200):
            result['name']=name
            result['testplanid']=result['result']
            return result

        self.close();
        return None;

    def get_math(self,math):

        if math is None: return;

        """
        队列消费数据
        :param order:
        :return:
        """
        param = {
            'function': 'queryqueue',
            'name':math['name']
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        result = json.loads(result)
        return result;

    def closeposition(self,math,result,statu,price:float,volume:int):

        if statu != 'BUY' and statu!= 'SELL':
            print("statu必须是 SELL 或 BUY")
            return;

        symbol = math['name']
        if symbol is None:
            print("品种名称未填写");
            return;

        testplanid = math['testplanid']
        if testplanid is None:
            print("不符合规则的使用")
            return;

        datetime = result['datetime']
        if datetime is None:
            print("不符合规则的使用")
            return;

        if price is None:
            print("请填写报价");
            return

        if volume is None:
            print("请填写手数")
            return

        param = {
            'function': 'closeposition',
            'statu': statu,
            'symbol': symbol,
            'testplanid': testplanid,
            'datetime': datetime,
            'price': price,
            'volume': volume
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        print(result)

    def openoptions(self,math,result,statu,price:float,volume:int):

        if statu != 'BUY' and statu!= 'SELL':
            print("statu必须是 SELL 或 BUY")
            return;

        symbol = math['name']
        if symbol is None:
            print("品种名称未填写");
            return;

        testplanid = math['testplanid']
        if testplanid is None:
            print("不符合规则的使用")
            return;

        datetime = result['datetime']
        if datetime is None:
            print("不符合规则的使用")
            return;

        if price is None:
            print("请填写报价");
            return

        if volume is None:
            print("请填写手数")
            return

        param = {
            'function': 'openposition',
            'statu': statu,
            'symbol': symbol,
            'testplanid': testplanid,
            'datetime': datetime,
            'price':price,
            'volume':volume
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        print(result)

    def incomeline(self,testPlanId):

        param = {
            'function': 'earnings',
            'testPlanId': testPlanId
        }
        self.ws.send(json.dumps(param))

    def incomelineresult(self):
        result = self.ws.recv()
        return result;

    def queryEarnestMoney(self, volume:int,symboname:str,price:float,direction:str,fururePrice:float):
        """
        获取期货交易保证金
        :param volume:      手数
        :param symboname:   期货名称
        :param price:       期货价格
        :param direction:   买卖方向（BUY | SELL)
        :param fururePrice: 非必填，查询期权保证金时需要输入对应期期货的价格
        :return:
        """

        if volume is None:
            print("手数未设置")
            return
        if symboname is None:
            print("名称未设置")
            return
        if direction is None:
            print("买卖方向未设置")
            return
        if direction != 'BUY' and direction != 'SELL' :
            print("买卖方向只允许BUY,SELL")
            return;
        if price is None:
            print("期货价格未设置")
            return;

        url = "http://%s:%s/mtyj/regresstest/historydata/earnestMoney?volume=%s&symboname=%s&price=%s&direction=%s" % (
            self.IP,self.HTTPPORT,volume, symboname, price, direction)
        if fururePrice is not None:
            url = url + "&fururePrice=%s" %fururePrice;

        response = requests.get(url);
        if response.status_code == 200:
            return json.loads(response.text)['result'];
        else:
            return print(json.loads(response.text)['msg']);


    def queryServiceCharge(self,volume: int, symboname: str, direction: str, currentPrice: float):
        """
        获取交易手续费
        :param volume:      手数
        :param symboname:   期货名称
        :param direction:   多空方向 （OPEN | CLOSE | TODAYCLOSE）
        :param currentPrice: 期货价格
        :return:
        """
        if volume is None :
            print("手数未设置")
            return
        if symboname is None:
            print("名称未设置")
            return
        if direction is None:
            print("开平标志未设置")
            return
        if direction != 'CLOSE' and direction != 'OPEN' and direction != 'CLOSETODAY':
            print("开平标志只允许OPEN,CLOSE,TODAYCLOSE")
            return
        if currentPrice is None:
            print("期货价格未设置")
            return;

        url = "http://%s:%s/mtyj/regresstest/historydata/serviceCharge?volume=%s&symboname=%s&direction=%s&price=%s" % (
        self.IP,self.HTTPPORT,volume, symboname, direction, currentPrice)
        response = requests.get(url);
        if response.status_code == 200:
            return json.loads(response.text)['result'];
        else:
            return print(json.loads(response.text)['msg']);

    def close(self):
        self.ws.close();

def showline(code):
    # 使用员工账号连接系统
    api = MtyApi(auth=MtyAuth('credi', 'admin123'))

    # 2. 查询资金
    api.incomeline(code);

    # 开窗
    plt.ion()
    # 开窗
    plt.figure(1)
    # x轴
    t_list = []
    # 实时价格
    result_list = []
    # 实时收益
    result_list2 = []

    while True:
        try:

            result = api.incomelineresult()
            if result is '':
                api.close();
                while True:
                    plt.pause(10)  # 暂停0,1秒

            result = json.loads(result)
            print(result)

            t_list.append(result['datetime'])  # x轴
            # result_list.append(result['close'])
            result_list2.append(result['income'])

            # plt.plot(t_list, result_list, color='red', marker='*', linestyle='-', label='A')
            plt.plot(t_list, result_list2, color='blue', marker='*', linestyle='-', label='B')

            plt.pause(0.1)  # 暂停0,1秒

        except:
            api.close();
            t_list.clear()
            result_list2.clear()
            result_list.clear()
            plt.clf()  # 清理窗体数据
            break
            pass