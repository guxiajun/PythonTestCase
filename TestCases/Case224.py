#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes #ctypes是加载C++动态库
import time
import os #os是调python包的接口路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR+"/libpycmd.so" #libpycmd.so是个动态库
print path

def needterms(): #one user
    return "1"
def categories(): #类别
    return "broadcast;sanity;video"
def shortDesc():
    return " (直播)StressTest：720p反复切摄像头5000次，查看摄像头是否卡死"
def detailDesc():
    return " 设备A直播模式进入频道，调用setVideoProfileEx接口，设置720p，然后反复切摄像头5000次，每切20次休息10s,查看摄像头是否卡死"
def run():
    ll= ctypes.cdll.LoadLibrary #这个是Python调用C++ DLL动态链接库的方法
    lib = ll(path)
    #备注：lib.ExeCmdCallBack是动态库里面python调C++的接口, 所以python调C++里面的接口就是通过ExeCmdCallBack接口调的，且只有这一个接口
    lib.ExeCmdCallBack(0, "setChannelProfile,1") #﻿ communication:0, broadcast:1
    lib.ExeCmdCallBack(0, "setClientRole,1,nil") #﻿ host:1, audience:2
    lib.ExeCmdCallBack(0, "enableVideo")
    lib.ExeCmdCallBack(0, "setupLocalVideo,2,-1") # Hidden:1, Fit:2
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil,Test00224,nil,1") # uid:1
    time.sleep(5)

    lib.ExeCmdCallBack(0, "setVideoProfileEx,1280,720,30,4096")

    for num in range(0,5000):
        if num%20 == 0:
            time.sleep(10)
        lib.ExeCmdCallBack(0, "switchCamera")
        time.sleep(0.2)
    #check，摄像头卡死后帧率和码率都会没有
    fps = lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 10, /data/videoEngine/data/Counters/iFrameSent0, >=, 10.0")

    #leaveChannel
    lib.ExeCmdCallBack(0, "leaveChannel")
    if fps == 0:
        return "0"
    else:
        return "-1"




