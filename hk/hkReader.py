from PyQt5.QtCore import QThread, QObject
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtGui import QImage

from typing import List, Tuple
from hk import *

class HKCaptureThread(QThread):
    sigCodes = Signal(QImage, list)
    def __init__(self, reader: 'HKReader'):
        super().__init__()
        self.reader = reader
        self.keep = False

    def stop(self):
        self.keep = False

    def run(self):
        self.keep = True
        while self.keep:
            if self.reader.isCaptured:
                pData = POINTER(c_ubyte)()
                pstFrameInfo = MV_CODEREADER_IMAGE_OUT_INFO_EX2()
                if self.reader.reader.CODEREADER_GetOneFrameTimeoutEx2(pData, pstFrameInfo, 500) == 0:
                    barcodeImgs = self.getImgAndCode(pData, pstFrameInfo)
                    if len(barcodeImgs) != 0:
                        self.sigCodes.emit(barcodeImgs[0], barcodeImgs[1])

            else:
                self.msleep(300)

    def getImgAndCode(self, pData, pstFrameInfo) -> List[Tuple[QImage, str]]:
        if pstFrameInfo.bIsGetCode == False: return []
        # if pstFrameInfo.enPixelType == MvCodeReaderGvspPixelType.PixelType_CodeReader_Gvsp_Jpeg:
        #     imgType = "JPG"
        # elif pstFrameInfo.enPixelType == MvCodeReaderGvspPixelType.PixelType_CodeReader_Gvsp_Mono8:
        #     imgType = "BMP"
        # else:
        #     imgType = ""

        buf = (c_ubyte*pstFrameInfo.nFrameLen)()
        memmove(buf, pData, pstFrameInfo.nFrameLen)
        img = QImage.fromData(buf)

        codes = []
        codeNum = pstFrameInfo.pstCodeListEx.contents.nCodeNum
        for i in range(codeNum):
            barcode = pstFrameInfo.pstCodeListEx.contents.stBcrInfoEx[i]
            codes.append(barcode.chCode.decode("utf-8"))

        return [img, codes]


class HKReader(QObject):
    #errors
    ErrOpen = 1
    ErrCapture = 2

    # signal
    sigError = Signal(int)
    sigCodes = Signal(QImage, list)
    def __init__(self, dllPath: str):
        super().__init__()
        # vars
        self.isOpened = False
        self.isCaptured = False
        self.devs = MV_CODEREADER_DEVICE_INFO_LIST()
        self.reader = MvCoderReaderCtrl(dllPath)

        # capture thread
        self.captureThread = HKCaptureThread(self)
        self.captureThread.sigCodes.connect(self.sigCodes)
        self.captureThread.start()

    def enumDevices(self):
        self.devs = MV_CODEREADER_DEVICE_INFO_LIST()
        self.reader.CODEREADER_EnumDevices(self.devs, MV_CODEREADER_GIGE_DEVICE)

    def openDevice(self, idx=0):
        if self.devs.deviceNum == 0:
            self.isOpened = False
            self.sigError.emit(__class__.ErrOpen)
            return

        self.reader.CODEREADER_CreateHandle(self.devs.deviceInfo(idx))
        ret = self.reader.CODEREADER_OpenDevice()
        self.isOpened = True  if ret == 0 else False
        if ret != 0: self.sigError.emit(__class__.ErrOpen)

    def closeDevice(self):
        self.reader.CODEREADER_CloseDevice()
        self.reader.CODEREADER_DestroyHandle()
        self.isOpened = False

    def startGrab(self):
        ret = self.reader.CODEREADER_StartGrabbing()
        if ret != 0:
            self.isCaptured = False
            self.sigError.emit(__class__.ErrCapture)
        else:
            self.isCaptured = True

    def stopGrab(self):
        self.reader.CODEREADER_StopGrabbing()
        self.isCaptured = False

    def setContinueTrigger(self):
        self.reader.set_continuous_trigger_mode()

    def setSingleTriggerBySoft(self):
        self.reader.set_single_trigger_mode()
        self.reader.set_trigger_source(MV_CODEREADER_TRIGGER_SOURCE.MV_CODEREADER_TRIGGER_SOURCE_SOFTWARE)

    def softTrigger(self):
        self.reader.trigger()
        self.isCaptured = True

