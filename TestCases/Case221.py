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
    return "(通信)调用setVideoProfileEX自定义接口，任意设置分辨率帧率码率后再加入频道，检测分辨率帧率码率是否正常发送"
def detailDesc():
    return "设备A/B在频道外均设置分辨率帧率码率后再以通信模式进入频道，分别检测设备A/B的分辨率帧率码率"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,0")# ﻿communication:0, broadcast:1
    #lib.ExeCmdCallBack(0,"setClientRole,1,nil")# ﻿host:1, audience:2
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1")# 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(0,"setVideoProfileEx,800,550,15,870")
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00001,nil,1")# uid:1

    lib.ExeCmdCallBack(1,"setChannelProfile,0")
    #lib.ExeCmdCallBack(1,"setClientRole,1,nil")
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(1,"setVideoProfileEx,380,380,15,650")
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00001,nil,2")
    time.sleep(15)

    #check 软编码器分辨率适配规则：宽/高均为4的倍数，(width+3)/4*4 (height+3)/4*4
    width1 = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iWidth")
    height1 = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iHeight")
    intent0 = (800 + 3) / 4 * 4
    intent1 = (550 + 3) / 4 * 4
    if intent0 < width1 or intent1 < height1:
        return "-1"
    result = lib.ExeCmdCallBack(0,"CHECK, Fps, 10, /data/videoEngine/data/Counters/iFrameSent0, >=, 5.0") #本地发送帧率
    if result != 0:
        return "-1"
    result2 = lib.ExeCmdCallBack(0,"CHECK, BitRate, 10, /data/videoEngine/data/Counters/iBytes0, >=, 600")
    if result2 != 0:
        return "-1"

    width2 = lib.ExeCmdCallBack(0, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000002/States/iWidth")
    height2 = lib.ExeCmdCallBack(0, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000002/States/iHeight")
    intent3 = (380 + 3) / 4 * 4
    intent4 = (380 + 3) / 4 * 4
    if intent3 < width2 or intent4 < height2:
        return "-1"
    result3 = lib.ExeCmdCallBack(1, "CHECK, Fps, 10, /data/videoEngine/data/Counters/iFrameSent0, >=, 3.0") #本地发送帧率
    if result3 != 0:
        return "-1"
    result4 = lib.ExeCmdCallBack(1, "CHECK, BitRate, 10, /data/videoEngine/data/Counters/iBytes0, >=, 260")

    #leaveChannel
    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")
    if result4 == 0:
        return "0"
    else:
        return "-1"