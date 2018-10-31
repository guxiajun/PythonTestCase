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
#def requireos():
#    return "/os == \"iOS\" || /os == \"Android\""
def categories():
    return "broadcast;sanity;video"
def shortDesc():
    return "（直播）进入频道后设置分辨率高于当前分辨率，查看分辨率是否能达到设置的值以及帧率的发送情况"
def detailDesc():
    return "设备A/B以主播方式进入频道，设备A设置分辨率高于当前分辨率，查看分辨率是否能达到设置的值以及帧率的发送情况"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(0,"setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    #lib.ExeCmdCallBack(0, "setVideoProfile,640，480")
    lib.ExeCmdCallBack(0,"setVideoProfileEx,640,480,15,500")
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00217,nil,1") # uid:1

    lib.ExeCmdCallBack(1,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(1,"setClientRole,1,nil") # ﻿host:1, audience:2
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    lib.ExeCmdCallBack(1,"setVideoProfileEx,640,480,15,500")
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00217,nil,2") # uid:2
    time.sleep(10)

    # 848 * 480
    lib.ExeCmdCallBack(0,"setVideoProfileEx,848,480,15,2000")
    width1 = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iWidth")
    height1 = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iHeight")
    if width1 != 848 or height1 != 480:
        return "-1"
    time.sleep(3)
    result = lib.ExeCmdCallBack(0, "CHECK, Fps, 10, /data/videoEngine/data/Counters/iFrameSent0, >=,5.0")
    if result != 0:
        return "-1"

    # 1280 * 720
    lib.ExeCmdCallBack(0,"setVideoProfileEx,1280,720,15,2000")
    width2 = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iWidth")
    height2 = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iHeight")
    if width2 != 1280 or height2 != 720:
        return "-1"
    time.sleep(3)
    result2 = lib.ExeCmdCallBack(0, "CHECK, Fps, 10, /data/videoEngine/data/Counters/iFrameSent0, >=,8.0")
    if result2 != 0:
        return "-1"

    #leaveChannel
    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")
    if result2 == 0:
        return "0"
    else:
        return "-1"




























