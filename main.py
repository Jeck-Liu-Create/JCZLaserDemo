import os
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from core.laserMarker import JCZLaserMarker, Pen, Hatch
from core.constants import JCZError

from ui.UiMainWindow import Ui_MainWindow
from ui import ui

class RedLightThread(QThread):
    def __init__(self, laser, name="", showContour=True) -> None:
        super().__init__()
        self.name = name
        self.laser = laser
        self.showContour = showContour

        self._isRunning = False

    def start(self, priority=QThread.InheritPriority) -> None:
        self._isRunning = True
        super().start(priority)

    def quit(self) -> None:
        self._isRunning = False

    def run(self) -> None:
        while self._isRunning:
            self.laser.redLightMarkByEnt(self.name, self.showContour)
            self.msleep(1)

        self.quit()

class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("write by chenjie")

        QDir.setCurrent("./bin/")
        self.laser = JCZLaserMarker(os.path.abspath( "./MarkEzd.dll" ))
        self.laser.loadDLL()
        self.laser.sigError.connect(self.onError)

        # action
        self.actInit.triggered.connect(self.onInit)
        self.actLoadFile.triggered.connect(self.onLoad)
        self.actSaveFile.triggered.connect(self.onSave)
        self.actClose.triggered.connect(self.onClose)
        self.actDevConfig.triggered.connect(self.onDevConfig)

        # button
        self.BnGetEntName.clicked.connect(self.onGetEntName)
        self.BnGoto.clicked.connect(self.onGoto)
        self.BnGetEntSize.clicked.connect(self.onGetEntSize)
        self.BnMark.clicked.connect(self.onMark)
        self.BnRedLight.clicked.connect(self.onRedLight)
        self.BnDelete.clicked.connect(self.onDeleteEnt)
        self.BnChangeText.clicked.connect(self.onChangeText)
        self.BnMoveSize.clicked.connect(self.onMoveSize)
        self.BnRect.clicked.connect(self.onSetRect)

        #
        self.isOpen = False
        self.gview = ui.View()
        self.vlayGView.addWidget(self.gview)

        self.startTimer(500)

        self.redThread = RedLightThread(self.laser)

    def onSetRect(self):
        name = self.LeEntName.text()
        x = float(self.LeX_Move.text())
        y = float(self.LeY_Move.text())
        w = float(self.LeWMove.text())
        h = float(self.LeHMove.text())

        self.laser.addRect(x, y, w, h, name, 0, True)

    def onMoveSize(self):
        name = self.LeEntName.text()
        x = float(self.LeX_Move.text())
        y = float(self.LeY_Move.text())
        w = float(self.LeWMove.text())
        h = float(self.LeHMove.text())

        self.laser.setSizeAndMove(name, x, y, w, h)

    def onChangeText(self):
        name = self.LeEntName.text()
        newText = self.LeNewText.text()
        self.laser.changeTextByName(name, newText)

    def onDeleteEnt(self):
        name = self.LeEntName.text()
        self.laser.deleteEntByName(name)

    def onRedLight(self):
        name = self.LeEntName.text()
        self.redThread.name = name

        if self.redThread.isRunning():
            self.redThread.quit()
        else:
            self.redThread.start()

    def onMark(self):
        self.laser.markEntity(self.LeEntName.text())

    def onGetEntSize(self):
        name = self.LeEntName.text()
        r, z = self.laser.getEntSize(name)
        self.LbEntSize.setText(f"{r}, {z}")

    def onGoto(self):
        x, y = self.LeX.text(), self.LeY.text()
        self.laser.gotoPos(float(x), float(y))

    def onGetEntName(self):
        id = self.TeId.text()
        name = self.laser.getEntName(int(id))
        self.LbEntName.setText(name)

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        if self.isOpen == False : return

        ## img
        s = self.gview.sceneRect().size()
        img = self.laser.getPrevBitmap(s.width(), s.height())
        img = self.gview.scene().addPixmap(img)
        img.setPos(-200, -200)

        ## pos
        x, y = self.laser.getCurCoor()
        self.LbPos.setText(f"({x},{y})")

        ## is marking
        v = self.laser.isMarking()
        self.LbIsMarking.setText(str(v))

        ## speed
        v = self.laser.getFlySpeed()
        self.LbSpeed.setText(f"{v}")

        ## ent count
        v = self.laser.getEntityCount()
        self.LbEntCount.setText(f"{v}")

    def onError(self, methodName, e: JCZError):
        print("OnError:", [methodName, e.code, e.desc, e.solution])

    def onInit(self, _):
        self.isOpen = self.laser.initial(False)

    def onLoad(self):
        file = os.path.abspath("./AUTOSAVE.ezd")
        self.laser.loadEzdFile(file)

    def onSave(self):
        self.laser.saveEzdFile("./abc.ezd")

    def onClose(self):
        self.laser.close()
        self.isOpen = False

    def onDevConfig(self):
        # self.laser.setDeviceConfigWithAxis(True, True)

        # ps = np.array([
        #     [0,0],
        #     [20, 0],
        #     [20, 20],
        #     [0, 20],
        #     [0, 0]
        # ])

        # self.laser.addCurve(ps, "ps", 0, True)

        # hatch = self.laser.setHatchEntParam2(Hatch("T1"))
        pass
        # self.laser.hatchEnt("T1", "T2")

        # self.laser.setDeviceConfig()

        # v = self.laser.getFontRecord(0)
        # print(v)
        v = self.laser.getAllFonts()
        print(v)

app = QApplication([])
win  = MainWindow()
win.show()
app.exec()
