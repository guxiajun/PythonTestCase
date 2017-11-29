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
    return "极大帧率显示"
def detailDesc():
    return "极大帧率显示"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1")# 0通信 1直播
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")# 1主播，2观众
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1")# 2:Fit
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1")#1显示远端指定的用户，2显示远端模式，-1新建窗口
    lib.ExeCmdCallBack(0, "setVideoProfileEx,640,360,40,400")
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00001,nil,1")
    lib.ExeCmdCallBack(0,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=,30.0")

    lib.ExeCmdCallBack(1,"setChannelProfile,1")# 0通信 1直播
    lib.ExeCmdCallBack(1,"setClientRole,1,nil")# 1主播，2观众
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1")# 2:Fit
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")#1显示远端指定的用户，2显示远端模式，-1新建窗口
    lib.ExeCmdCallBack(1, "setVideoProfileEx,640,360,40,400")
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00001,nil,2")
    lib.ExeCmdCallBack(1,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=,30.0")
    time.sleep(10)

    lib.ExeCmdCallBack(0, "setVideoProfileEx,640,360,60,400")
    i = lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=,50.0")

    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")

    if i==0:
        return "0"
    else:
        return "-1"
















