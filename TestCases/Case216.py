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
def requireos():
    return "/os == \"iOS\" || /os == \"Android\" || /os == \"Mac\""
def categories():
    return "broadcast;sanity;video"
def shortDesc():
    return "默认分辨率进入频道后，分辨率保持不变，设置帧率与码率，查看帧率和码率的变化情况"
def detailDesc():
    return "设备A/B以主播方式，默认分辨率进入频道，设备A保持分辨率不变,设置帧率与码率,查看帧率和码率的变化情况"

def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")  # ﻿host:1, audience:2
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    #lib.ExeCmdCallBack(0, "setVideoProfile,43,false")#43:640*480 30 750
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00216,nil,1") # uid:1

    lib.ExeCmdCallBack(1,"setChannelProfile,1") # ﻿communication:0, broadcast:1
    lib.ExeCmdCallBack(1,"setClientRole,1,nil")  # ﻿host:1, audience:2
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1") # 显示远端指定的用户／显示远端模式／新建窗口-1
    #lib.ExeCmdCallBack(1, "setVideoProfile,43,false")#43:640*480 30 750
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00216,nil,2") # uid:2
    time.sleep(10)

    #check 设置帧率和码率
    result = 0
    for FrameRate in [10, 20, 30]:
        for BitRate in (50,950,1850,2750,3650,4500):
            cmd = "setVideoProfileEx, 640, 480, {0}, {1}".format(FrameRate, BitRate)
            print cmd
            lib.ExeCmdCallBack(0, cmd)
            time.sleep(5)
        if FrameRate ==10:
            result = lib.ExeCmdCallBack(0,"CHECK, Fps, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 3.0")
            lib.ExeCmdCallBack(0, "CHECK, BitRate, 10, /data/videoEngine/data/Counters/iBytes0, >=, ")




        elif FrameRate ==20:
            result = lib.ExeCmdCallBack(0,"CHECK, Fps, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 15.0")
            bytes1 = lib.ExeCmdCallBack(0, "CHECK, Fps, 10, /data/videoEngine/data/Counters/iBytes0")
            BitRate1 = 1000.0 * bytes1 / 8 / 1024  # 8bit=1byte
            if result == -1 or BitRate1 == -1:
                return "-1"
        else:
            result = lib.ExeCmdCallBack(0,"CHECK, Fps, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 25.0")
            bytes2 = lib.ExeCmdCallBack(0, "CHECK, BitRate, 10, /data/videoEngine/data/Counters/iBytes0")
            BitRate2 = 1000.0 * bytes2 / 8 / 1024  # 8bit=1byte
            if result == -1 or BitRate2 == -1:
                return "-1"
    #leaveChannel
    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")

    #return "0"

















