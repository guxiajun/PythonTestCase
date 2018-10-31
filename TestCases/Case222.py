#!usr/bin python
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
    return "设备A/B两个主播互通，其中设备A下麦成为观众后，检测设备A/B的帧率发送情况"
def detailDesc():
    return "设备A/B两个主播互通，其中设备A下麦成为观众后，设备A则不发送帧率只接收，设备B正常发送帧率视频正常进行，查看主播和观众没有异常画面"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1")# ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")# ﻿host:1, audience:2
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1")# 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00001,nil,1")# uid:1

    lib.ExeCmdCallBack(1,"setChannelProfile,1")
    lib.ExeCmdCallBack(1,"setClientRole,1,nil")
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00001,nil,2")
    time.sleep(3)
    lib.ExeCmdCallBack(0,"SnapShot")
    time.sleep(10)

    lib.ExeCmdCallBack(0,"setClientRole,2,nil")
    time.sleep(2)
    lib.ExeCmdCallBack(0, "SnapShot")
    lib.ExeCmdCallBack(0,"CHECK, Fps, 10, /data/videoEngine/data/Counters/iFrameSent0, ==, 0.0")




    j = lib.ExeCmdCallBack(0,"CHECK, Fps, 20, /data/videoEngine/data/Counters/iRenderFrames_00000002, >=, 3.0")
    if j == -1:
        return "-1"

    if i == 0:
        return "0"
    else:
        return "-1"