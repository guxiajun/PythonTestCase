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
    return "1483:视频：禁用远端视频 "
def detailDesc():
    return "Muteremote/Unmuteremote can successful"
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
    time.sleep(2)

    lib.ExeCmdCallBack(0,"muteAllRemoteVideoStreams,true")
    lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iRenderFrames_00000002, ==, 0.0")
    lib.ExeCmdCallBack(0, "muteAllRemoteVideoStreams,false")
    i=lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iRenderFrames_00000002, >=, 3.0")

    lib.ExeCmdCallBack(0, "leaveChannel")
    lib.ExeCmdCallBack(1, "leaveChannel")
    if i == 0:
        return "0"
    else:
        return "-1"
