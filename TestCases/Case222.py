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
    return "两个主播互通，一方主播下麦成为观众后，另一方主播视频正常进行"
def detailDesc():
    return "两个主播互通，一方主播下麦成为观众后，另一方主播视频正常进行，主播和观众没有异常画面"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1")
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1")
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00001,nil,1")

    lib.ExeCmdCallBack(1,"setChannelProfile,1")
    lib.ExeCmdCallBack(1,"setClientRole,1,nil")
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00001,nil,2")
    time.sleep(10)

    lib.ExeCmdCallBack(0,"setClientRole,2,nil")
    j = lib.ExeCmdCallBack(0,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iRenderFrames_00000002, >=, 3.0")
    if j == -1:
        return "-1"
    i= lib.ExeCmdCallBack(1, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iRenderFrames_00000001, >=, 0.0")
    if i == 0:
        return "0"
    else:
        return "-1"