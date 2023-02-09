import os
import enum
import math
import types
import sys
import typing
import numpy as np
import numpy.ctypeslib as clib

import ctypes as C

from ctypes import wintypes
from functools import wraps
from PyQt5.QtCore import QObject, QSizeF
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWinExtras import QtWin

from .constants import JCZErrorList

I = C.c_int
D = C.c_double
B = C.c_bool

def str2bytes(s: str):
    return bytes(s, "utf-8")

def errorAutoProcess(ins, val):
    if val == 0:return
    fb = sys._getframe().f_back
    ins.sigError.emit(fb.f_code.co_name, JCZErrorList[val] )


class FontRecord(C.Structure):
    _fields_ = [("name", C.c_wchar*256), ("attr", wintypes.DWORD)]

class Rect:
    def __init__(self) -> None:
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

    def setBottomLeft(self, x, y):
        self.left = x
        self.bottom = y

    def setTopRight(self, x, y):
        self.right = x
        self.top = y

    def bottomLeft(self) -> typing.Tuple[float, float]:
        return (self.left, self.bottom)

    def bottomRight(self) -> typing.Tuple[float, float]:
        return (self.right, self.bottom)

    def topLeft(self) -> typing.Tuple[float, float]:
        return (self.left, self.top)

    def topRight(self) -> typing.Tuple[float, float]:
        return (self.right, self.top)

    def center(self) -> typing.Tuple[float, float]:
        s = self.size()
        return (self.left + s.width()/2, self.bottom + s.height()/2 )

    def size(self) -> QSizeF:
        return QSizeF(self.right - self.left, self.top - self.bottom)

    def __str__(self) -> str:
        x, y = self.bottomLeft()
        s = self.size()
        return f"{__class__.__name__}({x}, {y}, {s.width()} , {s.height()})"


class Decorator:
    def __init__(self, func):
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        instance : JCZLaserMarker
        instance = args[0]

        ret = self.__wrapped__(*args, **kwargs)
        instance.sigError.emit(JCZErrorList[ret])
        return None

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

class Pen:
    def __init__(self, penNo: int = 0, **kwargs) -> None:
        self.penNo = penNo
        self.markLoop = I(kwargs.get("markLoop", -1))
        self.markSpeed = D(kwargs.get("markSpeed", -1))
        self.powerRatio = D(kwargs.get("powerRatio", -1))
        self.current = D(kwargs.get("current", -1))
        self.freq = I(kwargs.get("freq", -1))
        self.pluseWidth = D(kwargs.get("pluseWidth", -1))
        self.startTC = I(kwargs.get("startTC", -1))
        self.laserOffTC = I(kwargs.get("laserOffTC", -1))
        self.endTC = I(kwargs.get("endTC", -1))
        self.polyTC = I(kwargs.get("polyTC", -1))
        self.jumpSpeed = D(kwargs.get("jumpSpeed", -1))
        self.jumpPosTC = I(kwargs.get("jumpPosTC", -1))
        self.jumpDistTC = I(kwargs.get("jumpDistTC", -1))
        self.endComp = D(kwargs.get("endComp", -1))
        self.accDist = D(kwargs.get("accDist", -1))
        self.pointTime = D(kwargs.get("pointTime", -1))
        self.plusePointMode = B(kwargs.get("plusePointMode", False))
        self.pluseNum = I(kwargs.get("pluseNum", -1))
        self.flySpeed = D(kwargs.get("flySpeed", -1))

    def asGetParam(self) -> tuple:
        F = C.byref

        return (
        self.penNo,
        F(self.markLoop),
        F(self.markSpeed),
        F(self.powerRatio),
        F(self.current),
        F(self.freq),
        F(self.pluseWidth),
        F(self.startTC),
        F(self.laserOffTC),
        F(self.endTC),
        F(self.polyTC),
        F(self.jumpSpeed),
        F(self.jumpPosTC),
        F(self.jumpDistTC),
        F(self.endComp),
        F(self.accDist),
        F(self.pointTime),
        F(self.plusePointMode),
        F(self.pluseNum),
        F(self.flySpeed)
        )

    def asSetParam(self) -> tuple:

        return (
        self.penNo,
        self.markLoop,
        self.markSpeed,
        self.powerRatio,
        self.current,
        self.freq,
        self.pluseWidth,
        self.startTC,
        self.laserOffTC,
        self.endTC,
        self.polyTC,
        self.jumpSpeed,
        self.jumpPosTC,
        self.jumpDistTC,
        self.endComp,
        self.accDist,
        self.pointTime,
        self.plusePointMode,
        self.pluseNum,
        self.flySpeed
        )


    def asValue(self) -> tuple:

        return (
        self.penNo,
        self.markLoop.value,
        self.markSpeed.value,
        self.powerRatio.value,
        self.current.value,
        self.freq.value,
        self.pluseWidth.value,
        self.startTC.value,
        self.laserOffTC.value,
        self.endTC.value,
        self.polyTC.value,
        self.jumpSpeed.value,
        self.jumpPosTC.value,
        self.jumpDistTC.value,
        self.endComp.value,
        self.accDist.value,
        self.pointTime.value,
        self.plusePointMode.value,
        self.pluseNum.value,
        self.flySpeed.value
        )

    def asDict(self) -> dict:
        d = {}
        for k, v in self.__dict__.items():
            if isinstance(k, str) and not k.startswith("_"):
                if isinstance(v, (int, str)):
                    d[k] = v
                else:
                    d[k] = v.value
        return d

    @classmethod
    def fromDict(cls, d: dict) -> "Pen":
        pen = Pen(**d)
        return pen

class Hatch:
    def __init__(self, name: str, **kw) -> None:
        self.name = name
        self.enableContour = B(kw.get("enableContour", True))
        self.paramIndex = I(kw.get("paramIndex", 1))
        self.enableHatch = I(kw.get("enableHatch", 1))
        self.contourFirst = B(kw.get("contourFirst", False))
        self.penNo = I(kw.get("penNo", 0))
        self.hatchType = I(kw.get("hatchType", 1))
        self.hatchAllCalc = B(kw.get("hatchAllCalc", False))
        self.hatchEdge = B(kw.get("hatchEdge", True))
        self.hatchAverageLine = B(kw.get("hatchAverageLine", False))
        self.hatchAngle = D(kw.get("hatchAngle", 0))
        self.hatchLineDist = D(kw.get("hatchLineDist", 0.03))
        self.hatchEdgeDist = D(kw.get("hatchEdgeDist", 0.1))
        self.hatchStartOffset = D(kw.get("hatchStartOffset", 0))
        self.hatchEndOffset = D(kw.get("hatchEndOffset", 0))
        self.hatchLineReduction = D(kw.get("hatchLineReduction", 0))
        self.hatchLoopDist = D(kw.get("hatchLoopDist", 0.5))
        self.edgeLoop = I(kw.get("edgeLoop", 0))
        self.hatchLoopRev = B(kw.get("hatchLoopRev", False))
        self.hatchAutoRotate = B(kw.get("hatchAutoRotate", False))
        self.hatchRotateAngle = D(kw.get("hatchRotateAngle", 10))
        self.hatchCrossMode = B(kw.get("hatchCrossMode", False))
        self.cycCount = I(kw.get("cycCount", 1))

    def asGetParam(self) -> tuple:
        RF = C.byref
        return (
            self.name,
            RF(self.enableContour),
            self.paramIndex,
            RF(self.enableHatch),
            RF(self.penNo),
            RF(self.hatchType),
            RF(self.hatchAllCalc),
            RF(self.hatchEdge),
            RF(self.hatchAverageLine),
            RF(self.hatchAngle),
            RF(self.hatchLineDist),
            RF(self.hatchEdgeDist),
            RF(self.hatchStartOffset),
            RF(self.hatchEndOffset),
            RF(self.hatchLineReduction),
            RF(self.hatchLoopDist),
            RF(self.edgeLoop),
            RF(self.hatchLoopRev),
            RF(self.hatchAutoRotate),
            RF(self.hatchRotateAngle)
        )

    def asGetParam2(self) -> tuple:
        RF = C.byref
        return (
            self.name,
            RF(self.enableContour),
            self.paramIndex,
            RF(self.enableHatch),
            RF(self.contourFirst),
            RF(self.penNo),
            RF(self.hatchType),
            RF(self.hatchAllCalc),
            RF(self.hatchEdge),
            RF(self.hatchAverageLine),
            RF(self.hatchAngle),
            RF(self.hatchLineDist),
            RF(self.hatchEdgeDist),
            RF(self.hatchStartOffset),
            RF(self.hatchEndOffset),
            RF(self.hatchLineReduction),
            RF(self.hatchLoopDist),
            RF(self.edgeLoop),
            RF(self.hatchLoopRev),
            RF(self.hatchAutoRotate),
            RF(self.hatchRotateAngle),
            RF(self.hatchCrossMode),
            RF(self.cycCount)
        )

    def asSetParam2(self) -> tuple:
        return (
            self.name,
            self.enableContour,
            self.paramIndex,
            self.enableHatch,
            self.contourFirst,
            self.penNo,
            self.hatchType,
            self.hatchAllCalc,
            self.hatchEdge,
            self.hatchAverageLine,
            self.hatchAngle,
            self.hatchLineDist,
            self.hatchEdgeDist,
            self.hatchStartOffset,
            self.hatchEndOffset,
            self.hatchLineReduction,
            self.hatchLoopDist,
            self.edgeLoop,
            self.hatchLoopRev,
            self.hatchAutoRotate,
            self.hatchRotateAngle,
            self.hatchCrossMode,
            self.cycCount
        )

    def asDict(self) -> dict:
        d = {}
        for k, v in self.__dict__.items():
            if isinstance(k, str) and not k.startswith("_"):
                if isinstance(v, (int, str)):
                    d[k] = v
                else:
                    d[k] = v.value
        return d

    @classmethod
    def fromDict(cls, d: dict) -> "Hatch":
        hatch = Hatch(**d)
        return hatch

class JCZLaserMarker(QObject):
    sigError = Signal(str, enum.Enum)
    def __init__(self, dllPath: str):
        super().__init__()
        self.dll = None
        self.ezdFile = ""
        self.dllPath = os.path.abspath(dllPath)
        self.dllDir = os.path.dirname(dllPath)

    def loadDLL(self) -> bool:
        try:
            self.dll = C.windll.LoadLibrary(self.dllPath)
        except OSError as e:
            return False
        else:
            return True

    def initial(self, isTestMode: bool) -> bool:
        """初始化 lmc1 控制卡
        :param bool isTestMode: 是否测试模式
        """
        ret = self.dll.lmc1_Initial2(self.dllDir, B(isTestMode) )
        errorAutoProcess(self, ret)

        return True if ret == 0 else False


    def close(self):
        ret =  self.dll.lmc1_Close()
        errorAutoProcess(self, ret)

    def setDeviceConfig(self):
        """调用设置设备参数的对话框

        调用 lmc1_SetDevCfg 会自动弹出设备参数设置对话框，用户可以设置设
        备参数。
        """
        ret =  self.dll.lmc1_SetDevCfg()
        errorAutoProcess(self, ret)

    def setDeviceConfigWithAxis(self, showAxis0: bool = True, showAxis1: bool = True):
        """调用设置设备参数的对话框

        调用 lmc1_SetDevCfg2 会自动弹出设备参数设置对话框，可设置扩展轴
        界面是否显示，用户可以设置设备参数。

        :param bool showAxis0: 扩展轴 0 的界面是否显示, defaults to True
        :param bool showAxis1: 扩展轴 1 的界面是否显, defaults to True
        """
        ret = self.dll.lmc1_SetDevCfg2(B(showAxis0), B(showAxis1))
        errorAutoProcess(self, ret)

    def setRotateMoveParam(self, moveX: float, moveY: float, centerX: float, centerY: float, rotateAngle: float):
        """设置旋转变换参数

        在程序中调用 lmc1_SetRotateMoveParam 来设置旋转变换参数，使数据
        库中所有对象在加工时绕指定中心旋转,然后移动指定距离。不影响数
        据的显示,只是加工时才对对象进行旋转。

        :param float moveX: X 方向移动距离
        :param float moveY: Y 方向移动距离
        :param float centerX: 旋转中心 x 坐标
        :param float centerY: 旋转中心 y 坐标
        :param float rotateAngle: 旋转角度
        """

        ret = self.dll.lmc1_SetRotateMoveParam(D(moveX), D(moveY), D(centerX), D(centerY), D(math.radians(rotateAngle)))
        errorAutoProcess(self, ret)

    def mark(self, flyMark: bool):
        """标刻当前数据库里的所有数据

        在使用 lmc1_LoadEzdFile 载入 ezd 文件后即可以使用此函数开始打标
        加工，此函数一直等待设备加工完毕后，或者用户停止才返回。即函
        数结束表示加工结束

        :param bool flyMark: 使能飞行打标
        """
        ret =  self.dll.lmc1_Mark(B(flyMark))
        errorAutoProcess(self, ret)

    def getCardSN(self) -> int:
        """得到当前卡序号

        当前板卡拨码开关设置的序号
        """
        sn = C.c_int(-1)
        ret = self.dll.lmc1_GetCardSN(C.byref(sn))

        errorAutoProcess(self, ret)

        return sn.value

    def loadEzdFile(self, filePath: str):
        """打开指定的 ezd 文件，并清除当前数据库中的所有对象。

        在程序中一般用此函数来打开一个用户建立 ezd 模板文件，这样用户就不
        需要在程序中设置加工参数，因为模板中的加工参数会自动导入。

        :param str filePath: 文件路径
        """
        self.ezdFile = filePath
        ret =  self.dll.lmc1_LoadEzdFile(filePath)
        errorAutoProcess(self, ret)

    def saveEzdFile(self, filePath: str):
        """保存当前数据库里所有对象到指定 ezd 文件里 。

        :param str filePath: 文件路径
        """
        ret = self.dll.lmc1_SaveEntLibToFile(filePath)
        errorAutoProcess(self, ret)


    def getPrevBitmap(self, width: int, height: int) -> QPixmap:
        """得到当前数据库里的所有对象的预览图像

        :param int width: 需要生成的图像的像素宽度
        :param int height: 需要生成的图像的像素高度
        """
        self.dll.lmc1_GetPrevBitmap2.restype = wintypes.HBITMAP
        handle =  self.dll.lmc1_GetPrevBitmap2(int(width), int(height))

        return QtWin.fromHBITMAP(handle)

    def getPrevBitmapWithParam(self, width: int, height: int, ox: float, oy: float, scale: float) -> QPixmap:
        self.dll.lmc1_GetPrevBitmap3.restype = wintypes.HBITMAP

        handle = self.dll.lmc1_GetPrevBitmap3(width, height, D(ox), D(oy), D(scale) )
        return QtWin.fromHBITMAP(handle)


    def getPrevBitmapByName(self, objName: str, width: int, height: int) -> QPixmap:
        """得到当前数据库里的指定对象数据的预览图像

        在程序中调用 lmc1_ GetPrevBitmapByName2 得到当前数据库里指定对
        象的预览图像指针，可以用于更新界面显示。

        :param str objName: 对象名称
        :param int width: 需要生成的图像的像素宽度
        :param int height: 需要生成的图像的像素高度
        """
        handle =  self.dll.lmc1_GetPrevBitmapByName2(objName, width, height)
        return QtWin.fromHBITMAP(handle)


    def getLastMarkTime(self):
        """获取上次加工所耗时间

        使用此接口在未重新给板卡上电的情况下可以读取最近一次标刻所用时间
        """

        hour, min, sec, miliSec = C.c_int(-1), C.c_int(-1), C.c_int(-1), C.c_int(-1)
        ret =  self.dll.lmc1_GetMarkTime(C.byref(hour), C.byref(min), C.byref(sec), C.byref(miliSec))

        errorAutoProcess(self, ret)
        return hour.value, min.value, sec.value, miliSec.value


    def markEntity(self, entName: str):
        """标刻当前数据库里的指定名称的对象。

        在使用 lmc1_LoadEzdFile 载入 ezd 文件后即可以使用此函数开始打标加
        工，此函数一直等待设备加工完毕后，或者用户停止才返回。即函数
        结束表示加工结束。

        :param str entName: 对象名称
        """
        ret =  self.dll.lmc1_MarkEntity(entName)

        errorAutoProcess(self, ret)


    def markFlyByStartSignal(self):
        """飞行标刻当前数据库里的所有数据。
        """

        ret = self.dll.lmc1_MarkFlyByStartSignal()
        errorAutoProcess(self, ret)


    def markEntityFly(self, entName: str):
        """飞行标刻当前数据库里的指定名称的对象

        :param str entName: 对象名称
        """
        ret =  self.dll.lmc1_MarkEntityFly(entName)
        errorAutoProcess(self, ret)

    def isMarking(self)-> bool:
        """判断卡正在处于工作状态
        """
        self.dll.lmc1_IsMarking.restype = C.c_bool

        ret = self.dll.lmc1_IsMarking()
        return ret

    def stopMark(self):
        ret = self.dll.lmc1_StopMark()
        errorAutoProcess(self, ret)

    def cancelMark(self):
        self.dll.lmc1_CancelMark()

    def redLightMark(self):
        """标刻一次红光显示框

        预览一次全部对象的打标范围
        """
        ret = self.dll.lmc1_RedLightMark()
        errorAutoProcess(self, ret)

    def redLightMarkContour(self):
        """红光预览当前数据库里面所有数据轮廓一次。

        预览一次全部对象的打标范围。
        """

        ret = self.dll.lmc1_RedLightMarkContour()
        errorAutoProcess(self, ret)

    def redLightMarkByEnt(self, entName: str, showContour: bool):
        """ 红光预览当前数据库里面指定对象。

        :param str entName: 名称
        :param bool showContour: 显示的是否是轮廓
        """
        ret =  self.dll.lmc1_RedLightMarkByEnt(entName, B(showContour) )
        errorAutoProcess(self, ret)

    def getFlySpeed(self) -> float:
        """获取当前的飞行速度。
        """
        speed = C.c_double(-1)
        ret = self.dll.lmc1_GetFlySpeed(C.byref(speed))
        errorAutoProcess(self, ret)

        return speed.value

    def gotoPos(self, x:float, y: float):
        """控制振镜直接运动到指定坐标

        :param float x: x pos
        :param float y: y pos
        """
        ret = self.dll.lmc1_GotoPos(D(x), D(y))
        errorAutoProcess(self, ret)

    def getCurCoor(self) -> typing.Tuple[float, float]:
        x,y = C.c_double(-1), C.c_double(-1)
        ret =  self.dll.lmc1_GetCurCoor(C.byref(x), C.byref(y))
        errorAutoProcess(self, ret)

        return x.value, y.value

    def markLine(self, x1: float, y1: float, x2: float, y2: float, pen: int):
        ret = self.dll.lmc1_MarkLine(D(x1), D(y1), D(x2), D(y2), pen)
        errorAutoProcess(self, ret)

    def markPoint(self, x: float, y: float, delay: float, pen: int):
        ret = self.dll.lmc1_MarkPoint(D(x), D(y), D(delay), pen)
        errorAutoProcess(self, ret)

    def markMultiPoints(self, points, jumpSpeed: float, laserOnTimeMs: float):
        pass

    def mirrorEnt(self, entName: str, centerX: float, centerY: float, mirrorX: bool, mirrorY: bool):
        ret =  self.dll.lmc1_MirrorEnt(entName, D(centerX), D(centerY), B(mirrorX), B(mirrorY))
        errorAutoProcess(self, ret)

    def rotateEnt(self, entName: str, centerX: float, centerY: float, angle: float):
        ret = self.dll.lmc1_RotateEnt(entName, D(centerX), D(centerY), D(math.radians(angle)) )
        errorAutoProcess(self, ret)

    def moveEnt(self, entName: str, moveX: float, moveY: float):
        r, _ = self.getEntSize(entName)
        x0, y0 = r.bottomLeft()
        ret = self.dll.lmc1_MoveEnt(entName, D(-x0 + moveX), D(-y0 + moveY) )
        errorAutoProcess(self, ret)

    def moveEntRelative(self, entName: str, moveX: float, moveY: float):
        ret = self.dll.lmc1_MoveEnt(entName, D( moveX), D( moveY) )
        errorAutoProcess(self, ret)

    def getEntSize(self, entName: str) -> typing.Tuple[Rect, float]:
        minX, minY, maxX, maxY, Z = D(-1), D(-1), D(-1), D(-1), D(-1)

        RF = C.byref
        ret = self.dll.lmc1_GetEntSize(entName, RF(minX), RF(minY), RF(maxX), RF(maxY), RF(Z))
        errorAutoProcess(self, ret)

        rect = Rect()
        rect.setBottomLeft(minX.value, minY.value)
        rect.setTopRight(maxX.value, maxY.value)

        return rect, Z.value

    def setSizeAndMove(self, name: str, x: float, y: float, w: float, h: float, delta=0.1):
        abs = math.fabs
        n = 0
        while True:
            r, _ = self.getEntSize(name)
            cx, cy = r.center()
            x0, y0 = r.bottomLeft()
            w0, h0 = r.size().width(), r.size().height()

            if n > 50: break

            if abs(x0 - x) < delta and abs(y0 - y) < delta and abs(w0 - w) < delta  and abs(h0 - h) < delta:
                break
            else:
                self.scaleEnt(name, cx, cy, w/w0, h/h0 )
                self.moveEnt(name, x, y)
                n += 1



    def scaleEnt(self, entName: str, cx: float, cy: float, sx: float, sy: float):
        ret = self.dll.lmc1_ScaleEnt(entName, D(cx), D(cy), D(sx), D(sy) )
        errorAutoProcess(self, ret)

    def getEntityCount(self) -> int:
        return self.dll.lmc1_GetEntityCount()

    def changeEntName(self, entName: str, newName: str):
        ret = self.dll.lmc1_ChangeEntName(entName, newName)
        errorAutoProcess(self, ret)

    def reverseAllEnt(self):
        ret = self.dll.lmc1_ReverseAllEntOrder()
        errorAutoProcess(self, ret)

    def moveEntAfter(self, ent: int, goalEnt: int):
        ret = self.dll.lmc1_MoveEntityAfter(ent, goalEnt)
        errorAutoProcess(self, ret)

    def moveEntBefore(self, ent: int, goalEnt: int):
        ret = self.dll.lmc1_MoveEntityBefore(ent, goalEnt)
        errorAutoProcess(self, ret)

    def copyEnt(self, ent: str, newEnt: str):
        ret = self.dll.lmc1_CopyEnt(ent, newEnt)
        errorAutoProcess(self, ret)

    def getEntName(self, entIdx: int) -> str:
        enName = C.create_unicode_buffer(256)
        ret = self.dll.lmc1_GetEntityName(entIdx, enName)
        errorAutoProcess(self, ret)

        return enName.value

    def setEntName(self, entIdx:int, entName: str):
        ret = self.dll.lmc1_SetEntityName(entIdx, entName)
        errorAutoProcess(self, ret)

    def readPort(self):
        v = wintypes.WORD(-1)
        ret = self.dll.lmc1_ReadPort(C.byref(v))
        errorAutoProcess(self, ret)

        return v.value

    def laserOn(self, on: bool):
        ret = self.dll.lmc1_LaserOn(B(on))
        errorAutoProcess(self, ret)

    def changeTextByName(self, entName:str, text: str):
        ret = self.dll.lmc1_ChangeTextByName(entName, text)
        errorAutoProcess(self, ret)

    def getTextByName(self, entName: str) -> str:
        text = C.create_unicode_buffer(256)
        ret = self.dll.lmc1_GetTextByName(entName, text)
        errorAutoProcess(self, ret)

        return text.value

    def clearAllEnt(self):
        ret = self.dll.lmc1_ClearEntLib()
        errorAutoProcess(self, ret)

    def deleteEntByName(self, entName: str):
        ret = self.dll.lmc1_DeleteEnt(entName)
        errorAutoProcess(self, ret)

    def addText(self, text: str, name: str, x: float, y: float,
        z: float, align: int, angle: float, pen: int, hatch: bool):

        ret = self.dll.lmc1_AddTextToLib(text, name, D(x), D(y),
        D(z), align, D(math.radians(angle)), pen, B(hatch))

        errorAutoProcess(self, ret)

    def addCurve(self, points: np.ndarray, name: str, pen: int, hatch: bool):
        self.dll.lmc1_AddCurveToLib.argtypes = (clib.ndpointer(np.double, 2), I, C.c_wchar_p, I, B )
        num = points.size//2

        points = points.reshape((-1,2)).astype(np.double)
        ret = self.dll.lmc1_AddCurveToLib(points, num, name, pen, hatch)
        errorAutoProcess(self, ret)

    def addRect(self, x: float, y: float, w: float, h: float, name: str, pen: int, hatch: bool):
        points = np.array([
            [0, 0],
            [w, 0],
            [w, h],
            [0, h],
            [0, 0]
        ])

        self.addCurve(points, name, pen, hatch)
        self.moveEnt(name, x, y)

    def getFontRecordCount(self) -> int:
        num = C.c_int(-1)
        ret = self.dll.lmc1_GetFontRecordCount(C.byref(num))
        errorAutoProcess(self, ret)

        return num.value

    def getPenNumberFromEnt(self, name: str) -> int:
        n = self.dll.lmc1_GetPenNumberFromEnt(name)
        return n

    def getPenParam(self, pen: Pen) -> Pen:
        ret = self.dll.lmc1_GetPenParam(*pen.asGetParam())
        errorAutoProcess(self, ret)

        return pen

    def setPenParam(self, pen: Pen):
        ret = self.dll.lmc1_SetPenParam(*pen.asSetParam())
        errorAutoProcess(self, ret)

    def getHatchEntParam(self, hatch: Hatch) -> Hatch:
        ret = self.dll.lmc1_GetHatchEntParam(*hatch.asGetParam())
        errorAutoProcess(self, ret)

        return hatch

    def getHatchEntParam2(self, hatch: Hatch) -> Hatch:
        ret = self.dll.lmc1_GetHatchEntParam2(*hatch.asGetParam2())
        errorAutoProcess(self, ret)

        return hatch

    def setHatchEntParam2(self, hatch: Hatch):
        ret = self.dll.lmc1_SetHatchEntParam2(*hatch.asSetParam2())
        errorAutoProcess(self, ret)

    def hatchEnt(self, entName: str, newName: str):
        ret = self.dll.lmc1_HatchEnt(entName, newName)
        errorAutoProcess(self, ret)

    # def getAllFontRecord(self) -> typing.Tuple[int, FontRecord]:
    #     num = C.c_int(-1)
    #     self.dll.lmc1_GetAllFontRecord.restype = C.POINTER(FontRecord)
    #     v = self.dll.lmc1_GetAllFontRecord(C.byref(num))

    #     return num.value, v.contents

    def getFontRecordCount(self) -> int:
        count = C.c_int(-1)
        ret = self.dll.lmc1_GetFontRecordCount(C.byref(count))
        errorAutoProcess(self, ret)
        return count.value

    def getFontRecord(self, idx: int) -> typing.Tuple[int, str, int]:
        idx = C.c_int(idx)
        name, attr = C.c_wchar_p("0")  , wintypes.DWORD(-1)
        RF = C.byref
        ret = self.dll.lmc1_GetFontRecord(idx, name, RF(attr))
        errorAutoProcess(self, ret)

        return idx.value, name.value, attr.value


    def getAllFonts(self) ->  typing.List[typing.Tuple[str, int]]:
        count = self.getFontRecordCount()

        ls = []
        for i in range(count):
            idx, name, attr = self.getFontRecord(i)
            ls.append((name, attr))

        return ls
