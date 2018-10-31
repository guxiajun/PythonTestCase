#!uer/bin python
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
    return "（直播）帧率／码率保持不变，检测分辨率先升后降"
def detailDesc():
    return "设备A/B以主播方式进入频道，设备A设置分辨率先升后降，检测分辨率升降情况"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(0,"setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(0, "setVideoProfileEx,640,480,15,1000")
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00214,nil,1") # uid:1

    lib.ExeCmdCallBack(1,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(1,"setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00214,nil,2") # uid:2
    time.sleep(5)

    #check
    width = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iWidth")
    height = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iHeight")
    if width != 640 or height != 480:
        return "-1"

    #分辨率先升后降
    lib.ExeCmdCallBack(0, "setVideoProfileEx,1280,720,15,1000")
    width1 = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iWidth")
    height1 = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iHeight")
    if width1 != 1280 or height1 != 720:
        return "-1"
    time.sleep(3)
    lib.ExeCmdCallBack(0, "setVideoProfileEx,320,180,15,1000")
    time.sleep(6)
    width2 = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iWidth")
    height2 = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iHeight")

    #leaveChannel
    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")
    if width2 == 320 and height2 == 180:
        return "0"
    else:
        return "-1"
















