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
    return "进入频道后分辨率不变设置帧率与码率"
def detailDesc():
    return "进入频道后分辨率不变设置帧率与码率"

def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0,"setChannelProfile,1")# 0通信 1直播
    lib.ExeCmdCallBack(0,"setClientRole,1,nil")# 1主播，2观众
    lib.ExeCmdCallBack(0,"enableVideo")
    lib.ExeCmdCallBack(0,"setupLocalVideo,2,-1")# 2:Fit
    lib.ExeCmdCallBack(0,"setupRemoteVideo,2,2,-1")#1显示远端指定的用户，2显示远端模式，-1新建窗口
    lib.ExeCmdCallBack(0, "setVideoProfileEx,640,480,15,500")
    lib.ExeCmdCallBack(0,"joinChannelByKey,nil,Test00001,nil,1")
    lib.ExeCmdCallBack(0,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=,13.0")

    lib.ExeCmdCallBack(1,"setChannelProfile,1")# 0通信 1直播
    lib.ExeCmdCallBack(1,"setClientRole,1,nil")# 1主播，2观众
    lib.ExeCmdCallBack(1,"enableVideo")
    lib.ExeCmdCallBack(1,"setupLocalVideo,2,-1")# 2:Fit
    lib.ExeCmdCallBack(1,"setupRemoteVideo,1,2,-1")#1显示远端指定的用户，2显示远端模式，-1新建窗口
    lib.ExeCmdCallBack(1, "setVideoProfileEx,640,480,15,500")
    lib.ExeCmdCallBack(1,"joinChannelByKey,nil,Test00001,nil,2")
    lib.ExeCmdCallBack(1,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=,13.0")
    time.sleep(10)

    #lib.ExeCmdCallBack(0, "setVideoProfileEx,640,480,30,2000")
    #lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=,25.0")

    chk_list = []
    for FrameRate in [15, 30, 60]:
        for BitRate in (50, 4781):
            cmd = "setVideoProfileEx, 640, 480, {0}, {1}".format(FrameRate, BitRate)
            print cmd
            lib.ExeCmdCallBack(0, cmd)
            time.sleep(5)
        if FrameRate ==15:
            result = lib.ExeCmdCallBack(0,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 13.0")
            chk_list.append(result)
        elif FrameRate ==30:
            result = lib.ExeCmdCallBack(0,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 20.0")
            chk_list.append(result)
        else:
            result = lib.ExeCmdCallBack(0,"CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, <=, 30.0")
            chk_list.append(result)

    if -1 in chk_list:
        return -1
    return 0






    #for num in range(50,4780):
    #    if 50<= num <= 900:
    #        lib.ExeCmdCallBack(0,"setVideoProfileEx,640,480,30,num")
    #        break
    #    elif 900< num <= 1800:
    #       lib.ExeCmdCallBack(0,"setVideoProfileEx,640,480,30,num")
    #           break
    #   elif 1800< num <= 2700:
    #       lib.ExeCmdCallBack(0,"setVideoProfileEx,640,480,30,num")
    #        break
    #    elif 2700< num <= 3600:
    #       lib.ExeCmdCallBack(0,"setVideoProfileEx,640,480,60,num")
    #        break
    #    elif 3600< num <= 4800:
    #        lib.ExeCmdCallBack(0,"setVideoProfileEx,640,480,60,num")
    #        break
    #    else:
    #        lib.ExeCmdCallBack(0,"setVideoProfileEx,640,480,60,num")
    #        break

        #time.sleep(10)
    #i = lib.ExeCmdCallBack(0, "CHECK, CounterGetTotal, 20, /data/videoEngine/data/Counters/iFrameSent0, >=, 20.0")

    lib.ExeCmdCallBack(0,"leaveChannel")
    lib.ExeCmdCallBack(1,"leaveChannel")

    #if i==0:
     #   return "0"
    #else:
       # return "-1"















