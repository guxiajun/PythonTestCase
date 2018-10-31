#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes
import time
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR+"/libpycmd.so"
print path

def needterms(): #two users
    return "2"
# def requireos():
#     return "/os == \"Mac\""
def categories():
    return "broadcast;sanity;video"
def shortDesc():
    return "（直播）renderMode由Fit->Hidden，退出频道再重进后，观察renderMode的显示模式以及对端帧率"
def detailDesc():
    return "设备A进入频道前设置renderMode为Fit；进入频道后，在频道内改renderMode为Hidden；退出频道后重进，观察renderMode的显示模式是否为Hidden模式以及对端是否有帧率"
def run():
    ll= ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0, "setChannelProfile,1") #﻿ communication:0, broadcast:1
    lib.ExeCmdCallBack(0, "setClientRole,1,nil") #﻿ host:1, audience:2
    lib.ExeCmdCallBack(0, "enableVideo")
    lib.ExeCmdCallBack(0, "setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0, "setLocalRenderMode,2") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0, "setupRemoteVideo,2,2,-1")  # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil,Test00200,nil,1") # uid:1
    time.sleep(2)
    lib.ExeCmdCallBack(0, "SnapShot") #快照
    time.sleep(3)

    lib.ExeCmdCallBack(1, "setChannelProfile,1")  # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(1, "setClientRole,1,nil")  # ﻿host:1, audience:2
    lib.ExeCmdCallBack(1, "enableVideo")
    lib.ExeCmdCallBack(1, "setupLocalVideo,2,-1")  # Hidden:1, Fit:2
    lib.ExeCmdCallBack(1, "setupRemoteVideo,1,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(1, "joinChannelByKey,nil,Test00200,nil,2") # uid:2
    time.sleep(5)

    #改变RenderMode
    lib.ExeCmdCallBack(0, "setLocalRenderMode,1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0, "SnapShot")
    time.sleep(3)
    lib.ExeCmdCallBack(0, "leaveChannel")
    time.sleep(3)
    lib.ExeCmdCallBack(0, "setupRemoteVideo,2,2,-1")# 在进入频道前需要再次调用对端，对端才会生效
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil,Test00200,nil,1")
    lib.ExeCmdCallBack(0, "SnapShot")
    time.sleep(5)

    #check send fps and render fps
    result = lib.ExeCmdCallBack(0, "CHECK, Fps, 10, /data/videoEngine/data/Counters/iFrameSent0, >=,4.0")
    if result != 0:
        return "-1"
    result2 = lib.ExeCmdCallBack(0, "CHECK, Fps, 10, /data/videoEngine/data/Counters/iRenderFrames_00000002, >=,3.0")#若对端卡住是没有帧率的

    #leaveChannel
    lib.ExeCmdCallBack(0, "leaveChannel")
    if result2 == 0:
        return "2"
    else:
        return "-1"



