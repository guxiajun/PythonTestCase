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
    return  "MAC用户看本地视频和远端视频"
def detailDesc():
    return "通信模式，MAC用户看本地视频和远端视频"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,0")
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1")
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00001,nil,1")

    lib.ExeCmdCallBack(1,"setChannelProfile,0")
    lib.ExeCmdCallBack(1,"setClientRole,1,nil")
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,1,-1")
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00001,nil,2")
    time.sleep(5)

    i = lib.ExeCmdCallBack(0,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 3.0")
    if i == -1:
        return "-1"
    j = lib.ExeCmdCallBack(1,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 3.0")
    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")
    if j == 0:
        return "0"
    else:
        return "-1"



