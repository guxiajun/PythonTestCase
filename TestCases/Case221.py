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
    return "communication;sanity;video"
def shortDesc():
    return "通信模式下，频道外使用setVideoProfileEX自定义设置分辨率帧率码率，加入频道"
def detailDesc():
    return "通信模式下，频道外使用setVideoProfileEX自定义设置分辨率帧率码率，加入频道"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,0")#通信
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1")
    lib.ExeCmdCallBack(0,"setVideoProfileEx,760,550,30,870")#640,480,15,500
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00001,nil,1")

    lib.ExeCmdCallBack(1,"setChannelProfile,0")
    lib.ExeCmdCallBack(1,"setClientRole,1,nil")
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(1,"setVideoProfileEx,640,480,30,750")
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00001,nil,2")
    time.sleep(10)

    i = lib.ExeCmdCallBack(0,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 15.0")#本地发送帧率
    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")
    if i == 0:
        return "0"
    else:
        return "-1"