# PythonTestCase
##RobotController python case使用说明：
1.    解压Controller.dmg
2.    将RobotController.app 拖进应用程序
3.    将安装包内的TestCases拷贝到文稿目录（/User/用户名/Documents）
4.    本机需要安装python2.7
5.    打开终端，找到python执行程序 cd /usr/lib 找到python2.7的位置
ls –al
如下：
python2.7 -> ../../System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7
前往目录System/Library/Frameworks/Python.framework/Versions/2.7，将python拷贝到文稿目录
6.    运行RobotController ,将CaseList拉到最底下，如果能看到case200，则环境配置成功，可以增加python case，Python case在TestCases文件夹内添加，命名规则Case+数字.py(C需要大写)
7.    添加完Case，重启app就能看到
关于python case
8.    Test Case编写必须有的部分：
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR+"/libpycmd.so"
needterms用例需要终端的数目
categories用例的类别
shortDesc用例描述，页面显示
detailDesc用例的详细描述
requires(必要时填写)操作系统要求，字符串从第0个开始，中间用“,”分开
run用例运行
ll= ctypes.cdll.LoadLibrary
lib = ll(path)
//调用sdk API 的方法
lib.ExeCmdCallBack(nTermIndex, "sdk API,param1,param2,…")
如第0个终端调用：int setChannelProfile (CHANNEL_PROFILE_TYPE profile)
lib.ExeCmdCallBack(0, "setChannelProfile,1")//1:broadcast 0:communication
9.    参数检测
//调用检测的方法
CounterGetTotal 获取一段时间内的某项参数的统计总数
GetSample      获取一段时间内某项参数的值
GetEarliestEvent  获取一段时间内某个事件发生的时间
例子：
（1）    lib.ExeCmdCallBack(nTermIndex, "CHECK, CounterGetTotal, interval, param,
comparesymbol, fthreshold ") //判断条件
如：lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20,
/data/videoEngine/data/Counters/iFrameSent0, >=, 3.0")//20s内的发送帧率大于等于3
（2）value=lib.ExeCmdCallBack(nTermIndex, "CHECK, GetSample, interval, param")
如width = lib.ExeCmdCallBack(0, "CHECK, GetSample, 10,
/data/videoEngine/data/States/iWidth0")//10内编码器的宽
(3) lib.ExeCmdCallBack(nTermIndex, "CHECK, GetEarliestEvent, interval, param, event, judgeInterval")
如：lib.ExeCmdCallBack(0, "CHECK, GetEarliestEvent, 10, /data/videoEngine/data/Events, setClientRole, 4.0")//10s内，前4s区间内有没有收到角色发生改变的事件

具体例子：
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes
import time
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR+"/libpycmd.so"
print path

def needterms():
return "1"
def requireos():
return "/os == \"Mac\""
def categories():
return "broadcast;sanity;video;single"
def shortDesc():
return "视频直播的sanity test (使用缺省设置)"
def detailDesc():
return "在单机上以主播方式加入频道，然后检验发送的视频帧率是否符合要求视频的参数都是缺省值"
def run():
ll= ctypes.cdll.LoadLibrary
lib = ll(path)
lib.ExeCmdCallBack(0, "setChannelProfile,1")
lib.ExeCmdCallBack(0, "setClientRole,1,nil")
lib.ExeCmdCallBack(0, "enableVideo")
lib.ExeCmdCallBack(0, "setupLocalVideo,2,-1")
lib.ExeCmdCallBack(0, "joinChannelByKey,nil,Test00001,nil,1")
i = lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 3.0")
lib.ExeCmdCallBack(0, "leaveChannel")
if i == 0:
return "0"
else:
return "-1"
