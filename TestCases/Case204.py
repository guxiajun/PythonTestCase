#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    return "1482:视频：禁用本地视频"
def detailDesc():
    return "Mutelocal/Unmutelocal can successful"
def run():
    ll= ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0, "setChannelProfile,1")
    lib.ExeCmdCallBack(0, "setClientRole,1,nil")
    lib.ExeCmdCallBack(0, "enableVideo")
    lib.ExeCmdCallBack(0, "setupLocalVideo,2,-1")
    #lib.ExeCmdCallBack(0, "setLocalRenderMode,1")
    lib.ExeCmdCallBack(0, "setupRemoteVideo,2,2,-1")
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil,Test00001,nil,1")

    lib.ExeCmdCallBack(1, "setChannelProfile,1")
    lib.ExeCmdCallBack(1, "setClientRole,1,nil")
    lib.ExeCmdCallBack(1, "enableVideo")
    lib.ExeCmdCallBack(1, "setupLocalVideo,2,-1")
    # lib.ExeCmdCallBack(1, "setLocalRenderMode,3")
    lib.ExeCmdCallBack(1, "setupRemoteVideo,1,2,-1")#1显示远端指定的用户，2显示远端模式，-1新建窗口
    lib.ExeCmdCallBack(1, "joinChannelByKey,nil,Test00001,nil,2")
    time.sleep(3)

    lib.ExeCmdCallBack(0,"muteLocalVideoStream,true")
    lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, ==, 0.0")
    lib.ExeCmdCallBack(0, "muteLocalVideoStream,false")
    i=lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 3.0")

    lib.ExeCmdCallBack(0, "leaveChannel")
    lib.ExeCmdCallBack(1, "leaveChannel")
    #return "0"
    if i == 0:
        return "0"
    else:
        return "-1"