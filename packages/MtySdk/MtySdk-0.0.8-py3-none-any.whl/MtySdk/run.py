from MtyApi import *

# 使用员工账号连接系统
# api = MtyApi(auth=MtyAuth('account', 'password'))
# 按需求注册服务
# math = api.query_math('kq_m_shfe_au','2018-01-02','2018-01-04')
# print(math)

# 注册成功情况下消费服务
# while True:
#     result = api.get_math(math)
#     print(result)
#     if result is None :
#         api.close();
#         break
from MtyApi import *

#   上传文件本地地址
filePath   = 'E:\\CZCE.CF107P12600.csv';
#   品种名称
sysbolname = 'CZCE.CF107P12600';

#   数据清洗
dataApi = DataApi()
list = dataApi.clearMath(filePath)

#   数据上传
dataApi.upload(symboname=sysbolname,username='accountname',password='password',mathlist=list)