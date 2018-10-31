#!uer/bin python
# -*- coding: utf-8 -*-

import ctypes
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR+"/libpycmd.so"
print path

def needterms():
    return "2"
def categories():
    return "broadcast;sanity;video"
def shortDesc():
    return "（直播）StressTest:检测主播和观众进入相同频道1小时后，观众退出频道，查看是否出现crash"
def detailDesc():
    return "设备A/B，设备A以主播方式进入频道，设备B以观众方式进入相同频道，1小时后，设备B退出频道，查看是否出现crash"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(0,"setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00211,nil,1") # uid:1

    lib.ExeCmdCallBack(1,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(1,"setClientRole,2,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")# 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00211,nil,2") # uid:2

    #设置1h
    lib.ExeCmdCallBack(0,"CHECK, CounterGetTotal, 600, /data/videoEngine/data/Counters/iFrameSent0, >=,3.0")
    lib.ExeCmdCallBack(1,"leaveChannel")
    time.sleep(2)

    #check
    result = lib.ExeCmdCallBack(0,"CHECK, CounterGetTotal, 10, /data/videoEngine/data/Counters/iFrameSent0, >=,3.0")

    #leaveChannel
    lib.ExeCmdCallBack(0,"leaveChannel")
    #lib.ExeCmdCallBack(1,"leaveChannel")
    if result == 0:
        return "0"
    else:
        return "-1"
















