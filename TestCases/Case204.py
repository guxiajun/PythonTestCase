#!/usr/bin/env python
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
    return "（直播）检测Mute/Unmute LocalVideoStream接口的有效性"
def detailDesc():
    return "设备A／B，设备A检测Mute/Unmute LocalVideoStream接口的有效性"
def run():
    ll= ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0, "setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(0, "setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(0, "enableVideo")
    lib.ExeCmdCallBack(0, "setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0, "setupRemoteVideo,2,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil,Test00204,nil,1") # uid:1

    lib.ExeCmdCallBack(1, "setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(1, "setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(1, "enableVideo")
    lib.ExeCmdCallBack(1, "setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(1, "setupRemoteVideo,1,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(1, "joinChannelByKey,nil,Test00204,nil,2") # uid:2
    time.sleep(3)

    #暂停本地视频流
    lib.ExeCmdCallBack(0,"muteLocalVideoStream,true") # True: 不发送本地视频流,False: 发送本地视频流
    result = lib.ExeCmdCallBack(0, "CHECK, Fps, 20, /data/videoEngine/data/Counters/iFrameSent0, ==,0.0")
    if result != 0:
        return "-1"

    #发送本地视频流
    lib.ExeCmdCallBack(0, "muteLocalVideoStream,false")
    resutl2=lib.ExeCmdCallBack(0, "CHECK, Fps, 20, /data/videoEngine/data/Counters/iFrameSent0, >=,3.0")

    #leaveChannel
    lib.ExeCmdCallBack(0, "leaveChannel")
    lib.ExeCmdCallBack(1, "leaveChannel")
    if resutl2 == 0:
        return "0"
    else:
        return "-1"