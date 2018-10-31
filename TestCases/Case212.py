#!usr/bin/ python
# -*- coding: utf-8 -*-

import ctypes
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR+"/libpycmd.so"
print path

def needterms():
    return "3"
def categories():
    return "broadcast;sanity,video"
def shortDesc():
    return "（直播）检测3主播本地渲染模式及发送和接收帧率情况"
def detailDesc():
    return "设备A/B/C进入频道前设置本地渲染模式，设备A设置为Hidden，设备B为Fit，设备C为Adaptive，均以主播方式进入频道，检测三台设备的本地渲染模式及发送和接收帧率情况"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(0,"setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,1,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(0,"setupRemoteVideo,3,2,-1")
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00212,nil,1") # uid:1

    lib.ExeCmdCallBack(1,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(1,"setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(1, "setupRemoteVideo,3,2,-1")
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00212,nil,2")# uid:2

    lib.ExeCmdCallBack(2,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(2,"setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(2,"enableVideo")
    lib.ExeCmdCallBack(2,"setupLocalVideo,3,-1") # Hidden:1, Fit:2 Adaptive:3
    lib.ExeCmdCallBack(2,"setupRemoteVideo,1,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(2,"setupRemoteVideo,2,2,-1")
    lib.ExeCmdCallBack(2,"joinChannelByKey,nil,Test00212,nil,3")# uid:3
    time.sleep(20)

    #check
    lib.ExeCmdCallBack(0, "SnapShot")
    time.sleep(5)
    lib.ExeCmdCallBack(1, "SnapShot")
    time.sleep(5)
    lib.ExeCmdCallBack(2, "SnapShot")
    time.sleep(5)

    result = lib.ExeCmdCallBack(0,"CHECK, Fps, 10, /data/videoEngine/data/Counters/iFrameSent0, >=, 4.0")
    if result != 0:
        return "-1"
    result2 = lib.ExeCmdCallBack(0,"CHECK, Fps, 10, /data/videoEngine/data/Counters/iRenderFrames_00000002, >=, 3.0")
    result3 = lib.ExeCmdCallBack(0,"CHECK, Fps, 10, /data/videoEngine/data/Counters/iRenderFrames_00000003, >=, 3.0")
    if result2 != 0 and result3 != 0:
        return "-1"

    result4 = lib.ExeCmdCallBack(1,"CHECK, Fps, 10, /data/videoEngine/data/Counters/iFrameSent0, >=, 4.0")
    if result4 != 0:
        return "-1"
    result5 = lib.ExeCmdCallBack(1,"CHECK, Fps, 10, /data/videoEngine/data/Counters/iRenderFrames_00000001, >=, 3.0")
    result6 = lib.ExeCmdCallBack(1,"CHECK, Fps, 10, /data/videoEngine/data/Counters/iRenderFrames_00000003, >=, 3.0")
    if result5 != 0 and result6 != 0:
        return "-1"

    result7 = lib.ExeCmdCallBack(2,"CHECK, Fps, 10, /data/videoEngine/data/Counters/iFrameSent0, >=, 4.0")
    if result7 != 0:
        return "-1"
    result8 = lib.ExeCmdCallBack(2,"CHECK, Fps, 10, /data/videoEngine/data/Counters/iRenderFrames_00000001, >=, 3.0")
    result9 = lib.ExeCmdCallBack(2,"CHECK, Fps, 10, /data/videoEngine/data/Counters/iRenderFrames_00000002, >=, 3.0")

    #leaveChannel
    lib.ExeCmdCallBack(0, "leaveChannel")
    lib.ExeCmdCallBack(1, "leaveChannel")
    lib.ExeCmdCallBack(2, "leaveChannel")
    if result8 == 0 and result9 == 0:
        return "2"
    else:
        return "-1"
