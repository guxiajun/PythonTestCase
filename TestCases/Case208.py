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
    return "频道内调用setVideoProfileEX私有接口设置分辨率"
def detailDesc():
    return "直播频道内调用setVideoProfileEX私有接口设置分辨率"
def run():
    ll= ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1")
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1")
    lib.ExeCmdCallBack(0,"setVideoProfile,20,true")#20表示:320X240  15  200
    lib.ExeCmdCallBack(0,"joinChannelVideoByKey,nil,test00001,nil,1")

    lib.ExeCmdCallBack(1,"setChannelProfile,1")
    lib.ExeCmdCallBack(1,"setClientRole,1,nil")
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(1,"joinChannelVideoByKey,nil,test00001,nil,2")
    time.sleep(5)
    lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSet0, >=, 3.0")

    lib.ExeCmdCallBack(0,"setVideoProfile,-1,false")#离开之前的设置
    lib.ExeCmdCallBack(0,"setVideoProfileEx,640,360,15,400")
    i=lib.ExeCmdCallBack(0,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSet0, >=, 3.0")

    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")

    if i ==0:
        return "0"
    else:
        return "-1"