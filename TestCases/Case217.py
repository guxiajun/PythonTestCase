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
    return "进入频道后设置分辨率高于当前分辨率"
def detailDesc():
    return "进入频道后设置分辨率高于当前分辨率"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1")
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1")
    #lib.ExeCmdCallBack(0, "setVideoProfile,640，480")
    lib.ExeCmdCallBack(0,"setVideoProfileEx,640,480,15,500")
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00001,nil,1")

    lib.ExeCmdCallBack(1,"setChannelProfile,1")
    lib.ExeCmdCallBack(1,"setClientRole,1,nil")
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(1,"setVideoProfileEx,640,480,15,500")
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00001,nil,2")
    time.sleep(10)

    lib.ExeCmdCallBack(0,"setVideoProfileEx,848,480,30,930")
    lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=,20.0")
    lib.ExeCmdCallBack(0,"setVideoProfileEx,1920,1080,15,2080")
    i = lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=,10.0")

    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")

    if i == 0:
        return "0"
    else:
        return "-1"




























