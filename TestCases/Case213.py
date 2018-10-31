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
    return "（直播）检测640*480,设置为30帧的极大帧率情况"
def detailDesc():
    return "设备A/B以主播方式进入频道，设备A调用setVideoProfileEx接口，分辨率和码率保持不变改变帧率，查看帧率爬升情况"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(0,"setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(0, "setVideoProfileEx,640,480,10,1000")
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00213,nil,1") # uid:1

    lib.ExeCmdCallBack(1,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(1,"setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00213,nil,2") # uid:2
    time.sleep(10)
    result = lib.ExeCmdCallBack(0, "CHECK, Fps, 10, /data/videoEngine/data/Counters/iFrameSent0, >=, 5.0")
    if result != 0:
        return "-1"

    #调用setVideoProfileEx接口
    lib.ExeCmdCallBack(0, "setVideoProfileEx,640,480,30,1000")
    time.sleep(3)
    result2 = lib.ExeCmdCallBack(0, "CHECK, Fps, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 25.0")

    #leaveChannel
    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")
    if result2 == 0:
        return "0"
    else:
        return "-1"
















