#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes
import time
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR+"/libpycmd.so"
print path

def needterms(): #two users
    return "2"
def categories():
    return "broadcast;sanity;video"
def shortDesc():
    return "（直播）大流切小流"
def detailDesc():
    return "设备A／B以主播方式进入频道，设备A申请切小流，查看设备A切小流情况"
def run():
    ll= ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0, "setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(0, "setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(0, "enableVideo")
    lib.ExeCmdCallBack(0, "setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0, "enableDualStreamMode,true") # True:双流，False:单流（默认）
    lib.ExeCmdCallBack(0, "setupRemoteVideo,2,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil,Test00201,nil,1") # uid:1

    lib.ExeCmdCallBack(1, "setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(1, "setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(1, "enableVideo")
    lib.ExeCmdCallBack(1, "setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(1, "enableDualStreamMode,true") # True:双流，False:单流（默认）
    lib.ExeCmdCallBack(1, "setupRemoteVideo,1,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(1, "joinChannelByKey,nil,Test00201,nil,2") # uid:2
    time.sleep(5)

    #切小流 （默认640*360）
    lib.ExeCmdCallBack(0, "setRemoteVideoStream,2,1") # 第一空:uid, 0:大流，1:小流
    time.sleep(15)

    #check
    width = lib.ExeCmdCallBack(0, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000002/States/iWidth")
    height = lib.ExeCmdCallBack(0, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000002/States/iHeight")

    # leaveChannel
    lib.ExeCmdCallBack(0, "leaveChannel")
    lib.ExeCmdCallBack(1, "leaveChannel")

    if width < 640 and height < 360:
        return "0"
    else:
        return "-1"



