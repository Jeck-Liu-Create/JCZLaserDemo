import os
import json
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from core.laserMarker import JCZLaserMarker, Pen, Hatch
from core.constants import JCZError

from ui.UiLaser import Ui_Laser


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


class Window(Ui_Laser, QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("LaserDemo")

        QDir.setCurrent("./bin/")
        self.laser = JCZLaserMarker(os.path.abspath( "./MarkEzd.dll" ))
        self.laser.loadDLL()
        self.laser.sigError.connect(self.onError)

        self.isOpen = False
        self.startTimer(500)
        self.redThread = RedLightThread(self.laser)

        # bind signal
        self.bnOpen.clicked.connect(self.onOpen)
        self.bnSave.clicked.connect(self.onSave)
        self.bnInit.clicked.connect(self.onInit)
        self.bnClose.clicked.connect(self.onClose)
        self.bnSetting.clicked.connect(self.onDevConfig)

        self.bnMirrorMove.clicked.connect(self.onMirrorMove)

        self.bnEntMark.clicked.connect(self.onMark)
        self.bnEntRedLight.clicked.connect(self.onRedLight)
        self.bnEntChangeText.clicked.connect(self.onChangeText)
        self.bnEntMove.clicked.connect(self.onMove)
        self.bnEntMoveSet.clicked.connect(self.onMoveSet)
        self.bnEntGetHatch.clicked.connect(self.onGetHatch)
        self.bnEntSetHatch.clicked.connect(self.onSetHatch)
        self.bnEntSetPen.clicked.connect(self.onSetPen)
        self.bnEntGetPen.clicked.connect(self.onGetPen)

            # comboBox
        self.cbEnt.textActivated.connect(self.onCombo)

    def onError(self, methodName, e: JCZError):
        print("OnError:", [methodName, e.code, e.desc, e.solution])

    def onCombo(self, name):
        rect,z = self.laser.getEntSize(name)
        self.lbEntRect.setText(f"{rect}")

    def onOpen(self):
        if not self.isOpen: return
        file, _ = QFileDialog.getOpenFileName(filter="Ezd File (*.ezd)")
        if file:
            self.laser.loadEzdFile(file)

            n = self.laser.getEntityCount()
            for i in range(n):
                name = self.laser.getEntName(i)
                self.cbEnt.addItem(name)

    def onSave(self):
        self.laser.saveEzdFile(self.laser.ezdFile)

    def onInit(self):
        self.isOpen = self.laser.initial(False)

    def onClose(self):
        self.isOpen = False
        self.laser.close()

    def onDevConfig(self):
        self.laser.setDeviceConfig()

    def onMirrorMove(self):
        x, y = self.leMirrorX.text(), self.leMirrorY.text()
        self.laser.gotoPos(float(x), float(y))

    def onMark(self):
        name = self.cbEnt.currentText()
        self.laser.markEntity(name)

    def onRedLight(self):
        name = self.cbEnt.currentText()
        self.redThread.name = name
        if self.redThread.isRunning():
            self.redThread.quit()
        else:
            self.redThread.start()

    def onChangeText(self):
        name = self.cbEnt.currentText()
        newText = self.leEntText.text()
        self.laser.changeTextByName(name, newText)

    def onMove(self):
        name = self.cbEnt.currentText()
        x, y = self.leEntX.text(), self.leEntY.text()
        self.laser.moveEnt(name, float(x), float(y))

    def onMoveSet(self):
        name = self.cbEnt.currentText()
        x, y = self.leEntX.text(), self.leEntY.text()
        w, h = self.leEntW.text(), self.leEntH.text()
        self.laser.setSizeAndMove(name, float(x), float(y), float(w), float(h))

    def onGetHatch(self):
        name = self.cbEnt.currentText()
        hatch = self.laser.getHatchEntParam2(Hatch(name))
        self.tePara.setText(json.dumps(hatch.asDict(), indent=4))

    def onGetPen(self):
        name = self.cbEnt.currentText()
        n = self.laser.getPenNumberFromEnt(name)
        pen = self.laser.getPenParam(Pen(n))
        self.tePara.setText(json.dumps(pen.asDict(), indent=4))

    def onSetHatch(self):
        hatchDict = json.loads(self.tePara.toPlainText())
        self.laser.setHatchEntParam2(Hatch.fromDict(hatchDict))

    def onSetPen(self):
        penDict = json.loads(self.tePara.toPlainText())
        self.laser.setPenParam(Pen.fromDict(penDict))

    def timerEvent(self, e: 'QTimerEvent') -> None:
        if self.isOpen == False : return

        ## img
        s = self.gvPreview.sceneRect().size()
        img = self.laser.getPrevBitmap(s.width(), s.height())
        img = self.gvPreview.scene().addPixmap(img)
        img.setPos(-200, -200)

        ## pos
        x, y = self.laser.getCurCoor()
        self.lbPos.setText(f"({x},{y})")

        ## is marking
        v = self.laser.isMarking()
        self.lsMarking.setText(str(v))

        ## speed
        v = self.laser.getFlySpeed()
        self.lbSpeed.setText(f"{v}")

        ## ent count
        v = self.laser.getEntityCount()
        self.lbCount.setText(f"{v}")

        # ent Rect
        name = self.cbEnt.currentText()
        rect,z = self.laser.getEntSize(name)
        self.lbEntRect.setText(f"{rect}")

        # last markTime
        hour, min, sec, miliSec = self.laser.getLastMarkTime()
        self.lbMarkTime.setText(f"{hour}:{min}:{sec}.{miliSec}")


app = QApplication([])
win  = Window()
win.show()
app.exec()
