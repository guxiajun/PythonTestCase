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
    return "视频直播的sanity test (使用缺省设置)"
def detailDesc():
    return "在单机上以主播方式加入频道，然后检验发送的视频帧率是否符合要求视频的参数都是缺省值"
def run():
    ll= ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0, "setChannelProfile,1")
    lib.ExeCmdCallBack(0, "setClientRole,1,nil")
    lib.ExeCmdCallBack(0, "enableVideo")
    lib.ExeCmdCallBack(0, "setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil,Test00001,nil,1")
    #lib.ExeCmdCallBack(termIndex, "CHECK, func, interval, param, minband, maxband");
    i = lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, 0.0, 0.0")
    if i == 0:
        return "0"
    else:
        return "-1"


