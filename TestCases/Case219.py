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
    return "broadcast;sanity;video"
def shortDesc():
    return "Can support the resolution can be "
def detailDesc():
    return "Check whether can support the resolution can be"
def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1")
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1")
    lib.ExeCmdCallBack(0,"setVideoProfile,43,false")#43:640*480 30 750
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00001,nil,1")


    lib.ExeCmdCallBack(1,"setChannelProfile,1")
    lib.ExeCmdCallBack(1,"setClientRole,1,nil")
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(1, "setVideoProfile,43,false")#43:640*480 30 750
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00001,nil,2")
    time.sleep(10)

    i = lib.ExeCmdCallBack(0, "CHECK, GetSample, 10, /data/videoEngine/data/States/iWidth0, ==, 640")
    j = lib.ExeCmdCallBack(0, "CHECK, GetSample, 10, /data/videoEngine/data/States/iHeight0, ==, 480")
    # if i != 0 or j != 0:
    #     return "0"
    # else:
    #     return "-1"

    k = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iWidth, ==, 640")
    q = lib.ExeCmdCallBack(1, "CHECK, GetSample, 10, /data/videoEngine/Renderer_00000001/States/iHeight, ==, 480")
    # if k != 0 or q != 0:
    #     return "0"
    # else:
    #     return "-1"

    lib.ExeCmdCallBack(0, "setVideoProfile,48,false")  # 48:848*480 30 930
    w = lib.ExeCmdCallBack(0, "CHECK, GetSample, 10, /data/videoEngine/data/States/iWidth0, ==, 848")
    h = lib.ExeCmdCallBack(0, "CHECK, GetSample, 10, /data/videoEngine/data/States/iHeight0, ==, 480")
    if w != 0 or h != 0:
        return "0"
    else:
        return "-1"

    lib.ExeCmdCallBack(0, "leaveChannel")
    lib.ExeCmdCallBack(1, "leaveChannel")

    #width = lib.ExeCmdCallBack(0, "CHECK, GetSample, 10, /data/videoEngine/data/States/iWidth0, ==, 848")

























