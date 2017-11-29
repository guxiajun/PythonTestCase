#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes
import time
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR+"/libpycmd.so"
print path

def needterms():
    return "1";
def categories():
    return "broadcast;sanity;video;single"
def shortDesc():
    return "Hidden and adaptive mode whether work "
def detailDesc():
    return "Check hidden and adaptive mode whether work"
def run():
    ll= ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0, "setChannelProfile,1")
    lib.ExeCmdCallBack(0, "setClientRole,1,nil")
    lib.ExeCmdCallBack(0, "enableVideo")
    lib.ExeCmdCallBack(0, "setupLocalVideo,1,-1")
    lib.ExeCmdCallBack(0, "setLocalRenderMode,1")
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil,Test00001,nil,1")
    time.sleep(10)
    lib.ExeCmdCallBack(0, "leaveChannel")

    lib.ExeCmdCallBack(0, "setChannelProfile,1")
    lib.ExeCmdCallBack(0, "setClientRole,1,nil")
    lib.ExeCmdCallBack(0, "enableVideo")
    lib.ExeCmdCallBack(0, "setupLocalVideo,3,-1")
    lib.ExeCmdCallBack(0, "setLocalRenderMode,3")
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil,Test00001,nil,1")
    time.sleep(10)
    #lib.ExeCmdCallBack(termIndex, "CHECK, func, interval, param, minband, maxband");
    #i = lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, 0.0, 0.0")
    #获取这个 / data / videoEngine / data / Counters / iFrameSent0在20s内的帧数累加
    lib.ExeCmdCallBack(0, "leaveChannel")
    return "0"
