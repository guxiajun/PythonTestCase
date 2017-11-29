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
    return "When all in landscape mode,check the view "
def detailDesc():
    return "Check when all in landscape mode,the video display"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1")#1直播 0通信
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")#1主播 2观众
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,1,-1")
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1")
    lib.ExeCmdCallBack(0,"setupRemoteVideo,3,2,-1")
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00001,nil,1")

    lib.ExeCmdCallBack(1,"setChannelProfile,1")
    lib.ExeCmdCallBack(1,"setClientRole,1,nil")
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(1, "setupRemoteVideo,3,2,-1")
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00001,nil,2")

    lib.ExeCmdCallBack(2,"setChannelProfile,1")
    lib.ExeCmdCallBack(2,"setClientRole,1,nil")
    lib.ExeCmdCallBack(2,"enableVideo")
    lib.ExeCmdCallBack(2,"setupLocalVideo,3,-1")
    lib.ExeCmdCallBack(2,"setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(2,"setupRemoteVideo,2,2,-1")
    lib.ExeCmdCallBack(2,"joinChannelByKey,nil,Test00001,nil,3")
    time.sleep(10)

    lib.ExeCmdCallBack(0,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSet0, >=, 3.0")
    lib.ExeCmdCallBack(1,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSet0, >=, 3.0")
    i = lib.ExeCmdCallBack(2,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSet0, >=, 3.0")

    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")
    lib.ExeCmdCallBack(2,"leaveChannel")

    if i == 0:
        return "0"
    else:
        return "-1"
