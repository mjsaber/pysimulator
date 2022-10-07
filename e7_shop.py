import sys
import time
import win32api
import win32con
import aircv as ac
from math import fabs
from PIL import ImageGrab
from win32gui import *
import atexit
import datetime
import os
from PIL import Image, ImageDraw, ImageFile
import numpy
import pytesseract
import cv2
import imagehash
import collections

windowHandleGame = 0
gameSize = ""
shuaXinCount = 0  # 刷新次数
useJewel = 0  # 使用钻石
useMoney = 0  # 使用金钱
shenmiCount = 0  # 神秘次数
shengyueCount = 0  # 圣约次数
sleepSize = 1.2  # 程序等待多长时间(秒)
threshold = 0.7  # 比较图片的阈值，影响精准度，取值在0到1之间
windowHandleName = "BlueStacks App Player"  # 模拟器窗口的名称
windowChilHandleName = "BlueStacks Android PluginAndroid"


def compare_image_with_hash(self, image_file1="images/desktop.jpg",
                            image_file2="images/desktopCompare.jpg", max_dif=7):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    hash_1 = None
    hash_2 = None
    with open(image_file1, 'rb') as fp:
        hash_1 = imagehash.average_hash(Image.open(fp))
        print(hash_1)
    with open(image_file2, 'rb') as fp:
        hash_2 = imagehash.average_hash(Image.open(fp))
        print(hash_2)
    dif = hash_1 - hash_2
    print(dif)
    if dif < 0:
        dif = -dif
    if dif <= max_dif:
        return True
    else:
        return False


def winfun(hwnd, lparam):
    global windowHandleGame
    s = GetWindowText(hwnd)
    if windowChilHandleName == s:
        windowHandleGame = hwnd
    return 1


@atexit.register
def endGame():
    f1 = open('res.txt', 'w')
    f1.write("时间:" + str(datetime.datetime.now()) + "\n")
    f1.write("刷新次数:" + str(shuaXinCount) + "\n")
    f1.write("使用钻石:" + str(useJewel) + "\n")
    f1.write("使用金钱:" + str(useMoney) + "\n")
    f1.write("神秘次数:" + str(shenmiCount) + "\n")
    f1.write("圣约次数:" + str(shengyueCount) + "\n")
    f1.write("...by Konvite")
    f1.close()


def compareShengyue(desktop, picture):
    yigoumaishengyue = ac.imread("images/yigoumaishengyue.png")
    useRes = ac.find_template(desktop, yigoumaishengyue, threshold)
    if useRes == None:
        return True
    res = ac.find_template(desktop, picture, threshold)
    if res == None:
        return False
    if useRes['confidence'] > res['confidence']:
        return False
    return True


def compareShenmi(desktop, picture):
    yigoumaishenmi = ac.imread("images/yishiyongshenmi.png")
    useRes = ac.find_template(desktop, yigoumaishenmi, threshold)
    if useRes == None:
        return True
    res = ac.find_template(desktop, picture, threshold)
    if res == None:
        return False
    if useRes['confidence'] > res['confidence']:
        return False
    return True


def comparePicture(desktop, picture):
    res = ac.find_template(desktop, picture, threshold)
    if res == None:
        return None
    clickSize = res['result']
    return [int(clickSize[0]), int(clickSize[1])]


def gameAutoStart():
    goumai = ac.imread("images/goumai.png")
    shenmi = ac.imread("images/shenmi.png")
    shengyue = ac.imread("images/shengyue.png")
    shuaxin = ac.imread("images/shuaxin.png")
    queren = ac.imread("images/queren.png")

    global shuaXinCount
    global useJewel
    global windowHandleName
    game = FindWindow(0, windowHandleName)
    ShowWindow(game, win32con.SW_SHOWNOACTIVATE)
    SetWindowPos(game, win32con.HWND_TOPMOST, 0, 0, 300, 300, win32con.SWP_SHOWWINDOW)
    time.sleep(sleepSize)
    game = FindWindow(0, windowHandleName)
    EnumChildWindows(game, winfun, None)
    global gameSize
    gameSize = GetWindowRect(windowHandleGame)

    jiequ_DeskTop(gameSize)

    desktop = ac.imread("images/desktop.jpg")

    autoBuy(desktop, goumai, shengyue, shenmi)
    endGame()

    while True:
        time.sleep(0.5)
        res = comparePicture(desktop, shuaxin)
        if res != None:
            windowClick(res)
            time.sleep(sleepSize)
            jiequ_DeskTopCompare(gameSize)
            while True:
                if compare_image_with_hash(None):
                    windowClick(res)
                    time.sleep(sleepSize)
                    jiequ_DeskTopCompare(gameSize)
                else:
                    break

            jiequ_DeskTop(gameSize)
            desktop = ac.imread("images/desktop.jpg")
            res = comparePicture(desktop, queren)
            if res != None:
                windowClick(res)
                time.sleep(sleepSize + 0.2)
                jiequ_DeskTopCompare(gameSize)
                while True:
                    if compare_image_with_hash(None):
                        windowClick(res)
                        time.sleep(sleepSize + 0.2)
                        jiequ_DeskTopCompare(gameSize)
                    else:
                        break
                shuaXinCount = shuaXinCount + 1
                useJewel = useJewel + 3
        jiequ_DeskTop(gameSize)
        desktop = ac.imread("images/desktop.jpg")
        autoBuy(desktop, goumai, shengyue, shenmi)
        endGame()


def windowClick(res):
    zzzs = win32api.MAKELONG(res[0], res[1])
    SendMessage(windowHandleGame, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    SendMessage(windowHandleGame, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, zzzs)
    time.sleep(0.05)
    SendMessage(windowHandleGame, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, zzzs)


def jiequ_DeskTop(gameSize):
    ImageGrab.grab([gameSize[0], gameSize[1], gameSize[2], gameSize[3]]).save("images/desktop.jpg")


def jiequ_DeskTopCompare(gameSize):
    ImageGrab.grab([gameSize[0], gameSize[1], gameSize[2], gameSize[3]]).save("images/desktopCompare.jpg")


def autoBuy(desktop, goumai, shengyue, shenmi):
    clickMouse(desktop, shengyue, shenmi, goumai, 4)
    time.sleep(sleepSize)
    point = win32api.MAKELONG(int(gameSize[2] / 2), -int(gameSize[3] / 1.3))
    pointEnd = win32api.MAKELONG(int(gameSize[2] / 1.5), 0)
    PostMessage(windowHandleGame, win32con.WM_MOUSEWHEEL, point, pointEnd)
    time.sleep(sleepSize + 0.5)
    jiequ_DeskTop(gameSize)
    desktop = ac.imread("images/desktop.jpg")
    clickMouse(desktop, shengyue, shenmi, goumai, 5)


def clickMouse(desktop, shengyue, shenmi, goumai, maxCount):
    global useMoney
    global shenmiCount
    global shengyueCount

    res = comparePicture(desktop, shenmi)
    if res != None:
        if compareShenmi(desktop, shenmi):
            shenmiCount = shenmiCount + 1
            useMoney = useMoney + 280000
            allRes = ac.find_all_template(desktop, goumai)
            clickMouse_GouMai(allRes, res, desktop, goumai, maxCount)
    res = comparePicture(desktop, shengyue)
    if res != None:
        if compareShengyue(desktop, shengyue):
            shengyueCount = shengyueCount + 1
            useMoney = useMoney + 184000
            allRes = ac.find_all_template(desktop, goumai)
            clickMouse_GouMai(allRes, res, desktop, goumai, maxCount)


def clickMouse_GouMai(allRes, res, desktop, goumai, maxCount):
    finalClickSize = []
    finalClickVal = 0
    allList = []
    if allRes != None:
        for index in range(len(allRes)):
            if index == maxCount:
                break
            if index == 0:
                clickSize = allRes[index]['result']
                finalClickSize = [int(clickSize[0]), int(clickSize[1])]
                finalClickVal = fabs(finalClickSize[1] - res[1])
                continue
            clickSize = allRes[index]['result']
            allList.append([int(clickSize[0]), int(clickSize[1])])
    for re in allList:
        val = fabs(re[1] - res[1])
        if val < finalClickVal:
            finalClickVal = val
            finalClickSize = re
    windowClick(finalClickSize)
    time.sleep(sleepSize)
    jiequ_DeskTopCompare(gameSize)
    while True:
        if compare_image_with_hash(None):
            windowClick(finalClickSize)
            time.sleep(sleepSize)
            jiequ_DeskTopCompare(gameSize)
        else:
            break

    jiequ_DeskTop(gameSize)
    desktop = ac.imread("images/desktop.jpg")
    res = ac.find_template(desktop, goumai, 0.7)
    clickSize = res['result']

    windowClick([int(clickSize[0]), int(clickSize[1])])
    time.sleep(sleepSize)
    jiequ_DeskTopCompare(gameSize)
    while True:
        if compare_image_with_hash(None):
            windowClick([int(clickSize[0]), int(clickSize[1])])
            time.sleep(sleepSize)
            jiequ_DeskTopCompare(gameSize)
        else:
            break


if __name__ == '__main__':
    gameAutoStart()
