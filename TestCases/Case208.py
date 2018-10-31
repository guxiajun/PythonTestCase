#!usr/bin/env python
#-*- coding: utf-8 -*-

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
    return "（直播）检测setVideoProfileEX私有接口的有效性，查看分辨率／帧率／码率爬升情况"
def detailDesc():
    return "设备A/B以主播方式进入频道，其中设备A在进入频道前先设置较低的videoProfile，进入频道后，设备A调用setVideoProfileEX私有接口并设置videoProfile，查看分辨率／帧率／码率爬升情况"
def run():
    ll= ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0, "setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(0, "setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(0, "enableVideo")
    lib.ExeCmdCallBack(0, "setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0, "setupRemoteVideo,2,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(0,"setVideoProfile,10,false")#10表示:180p,320*180  15  140
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil,test00208,nil,1") # uid:1
    #i = lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 2.0")

    lib.ExeCmdCallBack(1, "setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(1, "setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(1, "enableVideo")
    lib.ExeCmdCallBack(1, "setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(1, "setupRemoteVideo,1,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    #lib.ExeCmdCallBack(1,"setVideoProfile,20,false")  # 20表示:320X240  15  200
    lib.ExeCmdCallBack(1, "joinChannelByKey,nil,test00208,nil,2") # uid:2

    #调用私有接口
    lib.ExeCmdCallBack(0, "setVideoProfile,-1,false")#离开setVideoProfile之前需要关闭窗口
    lib.ExeCmdCallBack(0, "setVideoProfileEx,800,560,15,1200")
    time.sleep(20)

    #check
    result = lib.ExeCmdCallBack(0, "CHECK, Fps, 20, /data/videoEngine/data/Counters/iFrameSent0, >=,5.0")
    if result != 0:
        return "-1"
    width = lib.ExeCmdCallBack(1, "CHECK, GetSample, 20, /data/videoEngine/Renderer_00000001/States/iWidth")
    height = lib.ExeCmdCallBack(1, "CHECK, GetSample, 20, /data/videoEngine/Renderer_00000001/States/iHeight")
    if width != 800 or height != 560:
        return "-1"
    result2 = lib.ExeCmdCallBack(0, "CHECK, BitRate, 20, /data/videoEngine/data/Counters/iBytes0, >=,800")

    #leaveChannel
    lib.ExeCmdCallBack(0, "leaveChannel")
    lib.ExeCmdCallBack(1, "leaveChannel")
    if result2 == 0:
        return "0"
    else:
        return "-1"
