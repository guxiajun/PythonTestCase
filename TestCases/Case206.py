#!usr/bin/env python
#-*- coding: utf-8 -*-

import ctypes
import time
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR+"/libpycmd.so"
print path

def needterms():
    return "2";
def categories():
    return "broadcast;sanity;video"
def shortDesc():
    return "One-to-one normal live video"
def detailDesc():
    return "Check whether one to one live video normal"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1")
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")#1主播，2观众
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0, "setupLocalVideo,2,-1")#2:Fit
    # lib.ExeCmdCallBack(0, "setLocalRenderMode,1")#1:Hidden 2:Fit 3:Adaptive
    lib.ExeCmdCallBack(0, "setupRemoteVideo,2,2,-1") # 2显示远端指定的用户，2显示远端模式，-1新建窗口
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil,Test00001,nil,1")

    lib.ExeCmdCallBack(1, "setChannelProfile,1")
    lib.ExeCmdCallBack(1, "setClientRole,1,nil")
    lib.ExeCmdCallBack(1, "enableVideo")
    lib.ExeCmdCallBack(1, "setupLocalVideo,2,-1")
    # lib.ExeCmdCallBack(1, "setLocalRenderMode,3")
    lib.ExeCmdCallBack(1, "setupRemoteVideo,1,2,-1")  # 1显示远端指定的用户，2显示远端模式，-1新建窗口
    lib.ExeCmdCallBack(1, "joinChannelByKey,nil,Test00001,nil,2")
    time.sleep(5)

    i=lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 10, /data/videoEngine/data/Counters/iRenderFrames_00000002, >=, 2.0")
    j=lib.ExeCmdCallBack(1, "CHECK, CounterGetTotal, 10, /data/videoEngine/data/Counters/iRenderFrames_00000001, >=, 2.0")
    lib.ExeCmdCallBack(0, "leaveChannel")
    lib.ExeCmdCallBack(1, "leaveChannel")
    if i != 0 or j != 0:
        return "-1"
    else:
        return "0"
