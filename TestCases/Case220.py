#usr/bin python
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
    return "communication;sanity;video"#COMMUNICATION
def shortDesc():
    return "禁用视频后再启用能看到画面"
def detailDesc():
    return "禁用视频后再启用能看到画面(muteRemoteVideoStream)"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,0")# 0通信 1直播
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")# 1主播，2观众
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1")# 2:Fit
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1")#1显示远端指定的用户，2显示远端模式，-1新建窗口
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00001,nil,1")

    lib.ExeCmdCallBack(1,"setChannelProfile,0")
    lib.ExeCmdCallBack(1,"setClientRole,1,nil")
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00001,nil,2")
    time.sleep(10)

    lib.ExeCmdCallBack(0,"muteRemoteVideoStream,2,true")#暂停指定用户视频流
    j = lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iRenderFrames_00000002, ==, 0.0")
    if j == -1:
        return "-1"
    lib.ExeCmdCallBack(0,"muteRemoteVideoStream,2,false")
    i = lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iRenderFrames_00000002, >=, 3.0")
    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")
    if i == 0:
        return "0"
    else:
        return "-1"























