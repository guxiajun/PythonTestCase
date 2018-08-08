import os
import cv2
import struct
import math
import sys
import pytesseract
from ffmpy import FFmpeg
#streampath = '/Users/shlb/Downloads/2.3.0/0808/test_2s.mov'  #sys.argv[1]

width = 0
height = 0
startpx = 0
startpy= 0

def DelFile(path):
    ls = os.listdir(path)
    for i in range(0, len(ls)):
        c_path = os.path.join(path, ls[i])
        if os.path.isdir(c_path):
            DelFile(c_path)
            if os.path.exists(c_path):
                os.removedirs(c_path)
        else:
            os.remove(c_path)
    if os.path.exists(path) == True:
        os.removedirs(path)

def GetAudPow(pcmfile, samples):
    fVoiceEnergy = 0.0
    for k in range(0, int(samples)):
        audiodata = pcmfile.read(2)
        samples = int(samples) - len(audiodata)
        temp = struct.unpack('BB', audiodata)
        sampledata = struct.pack('BB', temp[1], temp[0])
        sampledat, = struct.unpack('h', sampledata)
        fVoiceEnergy += sampledat * sampledat
    fVoiceEnergy = float(fVoiceEnergy) / (480 * 32768.0 * 32768.0)
    if float(fVoiceEnergy) == 0.0:
        fAudPower = 127
    else:
        fAudPower = 10 * math.log10(fVoiceEnergy)
        if fAudPower > 0:
            fAudPower = 0
        if fAudPower < -127:
            fAudPower = -127
        fAudPower = -fAudPower
    return fAudPower

def SeperateAVsteam(inpath, outpath):
    ff = FFmpeg(inputs={inpath: None},
                outputs={outpath: '-f s16be -vn -ac 1 -ar 48000 -acodec pcm_s16be -y'})
    print(ff.cmd)
    ff.run()

def GetTickJpg(path, tick):
    timems = int(tick) % 1000
    times = float(float(tick) / 1000 % 60 + timems / 1000)
    timemin = int(tick) / 1000 / 60
    timeh = int(tick) / 1000 / 60 / 60
    snaptime = str(timeh) + ':' + str(timemin) + ':' + str(float(times))

    jpgpath = os.path.split(path)[0] + '/temp/jpg'
    isexist = os.path.exists(jpgpath)
    if isexist == False:
        os.mkdir(jpgpath)
    srcsnapfile = jpgpath + '/temp.jpg'
    dstsnapfile = jpgpath + '/' + str(tick) + '.jpg'
    param = '-ss ' + snaptime + ' -f image2 -vframes 1 -y'
    ff = FFmpeg(inputs={path: None},
                outputs={srcsnapfile: param})
    print(ff.cmd)
    ff.run()
    param = '-filter_complex crop=' + str(width) + ':' + str(height) + ':' \
            + str(startpx) + ':' + str(startpy) + ' -y'
    ff = FFmpeg(inputs={srcsnapfile: None},
                outputs={dstsnapfile: param})
    print(ff.cmd)
    ff.run()
    return dstsnapfile

def GetMedian(data):
    data = sorted(data)
    size = len(data)
    if size == 0:
        return 0
    if size % 2 == 0:
        median = (data[size // 2] + data[size // 2 - 1]) / 2
        data[0] = median
    if size % 2 == 1:
        median = data[(size - 1) // 2]
        data[0] = median
    return data[0]

def GetAvSyncInterval(path):
    temppath = os.path.split(path)[0] + '/temp'
    isexist = os.path.exists(temppath)
    if isexist == True:
        DelFile(temppath)
    os.mkdir(temppath)
    pcmpath = temppath + '/audio.pcm'
    SeperateAVsteam(path, pcmpath)
    pcmfile = open(pcmpath, 'rb+')
    pcmfile.seek(0, 2)
    size = pcmfile.tell()
    pcmfile.seek(0)
    count = -1
    LastPowerTime = 0
    dataset =[]
    while int(size) > 0:
        if size >= 480*2:
            fAudPow = GetAudPow(pcmfile, 480)
            count = count + 1
            size = size - 480*2
        else:
            break
        if int(fAudPow) < 30:
            print(fAudPow)
            powertime = count * 10
            if (powertime - LastPowerTime < 30) and (count != 0):
                LastPowerTime = powertime
                continue
            LastPowerTime = powertime
            if powertime >= 30:
                powertime = powertime - 30
            cropjpgfile = GetTickJpg(path, powertime)
            img = cv2.imread(cropjpgfile)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
            AsyFramesFile = temppath + '/temp.txt'
            text = pytesseract.image_to_string(dst)
            text = text.replace(' ', '')
            filedst = open(AsyFramesFile, 'a+')
            if text != '':
                print(text)
                if len(text.split(':', 2)) != 2:
                    continue
                text0 = text.split(':', 2)[0]
                text = text.split(':', 2)[1]
                if text.isdigit() != True or text0.isdigit() != True:
                    continue
                if int(text0) == 0 or int(text0) == 1:
                    if int(text0) == 1:
                        text = int(text) + 30
                    if int(text) >= 30 and int(text) <= 59:
                        text = 60 - int(text)
                        filedst.write(str(text) + '\n')
                        dataset.append(text)
                    elif int(text) < 30 and int(text) >= 0:
                        filedst.write(str(text) + '\n')
                        dataset.append(text)
    resultfile = os.path.split(path)[0] + '/result.txt'
    result_median = GetMedian(dataset)
    filemedian = open(resultfile, 'a+')
    param = str(os.path.split(path)) + ' median: '
    filemedian.write(param)
    filemedian.write(str(result_median) + '\n')
    DelFile(temppath)
    return result_median



if __name__ == "__main__":
    if len(sys.argv) >= 2:
        streampath = sys.argv[1]
    if len(sys.argv) == 6:
        width = sys.argv[2]
        height = sys.argv[3]
        startpx = sys.argv[4]
        startpy = sys.argv[5]
    file_extension = os.path.splitext(streampath)[1]
    if (file_extension == '.mov') or (file_extension == '.MOV') \
            or (file_extension == '.mp4') or (file_extension == '.MP4') \
            or (file_extension == '.flv') or (file_extension == '.FLV'):
        if len(sys.argv) != 6:
            cap = cv2.VideoCapture(streampath)
            streamheight = cv2.VideoCapture.get(cap, cv2.CAP_PROP_FRAME_HEIGHT)
            streamwidth = cv2.VideoCapture.get(cap, cv2.CAP_PROP_FRAME_WIDTH)
            if int(streamheight) == 720 and int(streamwidth) == 1280:
                width = 218
                height = 80
                startpx = 528
                startpy = 336
            elif int(streamheight) == 360 and int(streamwidth) == 640:
                width = 108
                height = 46
                startpx = 264
                startpy = 164
            cap.release()
        result = GetAvSyncInterval(streampath)
        print(str(result))







