from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class SwitchPrivate(QObject):
    def __init__(self, bn:QAbstractButton,  parent=None) -> None:
        super().__init__(parent)
        self.bn = bn
        self.pos = 0

        self.gradient = QLinearGradient()
        self.gradient.setSpread(QGradient.PadSpread)
        self.gradient.setCoordinateMode(QGradient.ObjectMode)
        self.gradient.setStart(0, 0)
        self.gradient.setFinalStop(0, 1)

        self.ani = QPropertyAnimation(self, b"position")
        self.ani.setStartValue(0)
        self.ani.setEndValue(1)
        self.ani.setDuration(200)
        self.ani.setEasingCurve(QEasingCurve.InOutExpo)
        self.ani.finished.connect(self.bn.update)

    def draw(self, painter: QPainter):
        r = self.bn.rect()
        margin = r.height()/10

        shadow = self.bn.palette().color(QPalette.Shadow)
        green = QColor(Qt.green)
        red = QColor(Qt.red)

        self.gradient.setColorAt(0, shadow.lighter(120))
        self.gradient.setColorAt(1, shadow.lighter(150))

        painter.setBrush(self.gradient)
        painter.drawRoundedRect(r, r.height()/2, r.height()/2)

        # draw inner rounded rect
        color, text =  (green, "ON") if self.bn.isChecked() else (red, "OFF")

        self.gradient.setColorAt(0, color.lighter(130))
        self.gradient.setColorAt(1, color.lighter(160))

        painter.setBrush(self.gradient)
        r1 = QRectF(r.width()*self.pos*(3/5) , margin, r.width()*(2/5), r.height() - 2*margin)

        m = r.height()/20
        painter.drawRoundedRect(r1.adjusted(m, m, -m, -m), r1.height()/3, r1.height()/3)
        painter.drawText(r1.adjusted(m, m, -m, -m), Qt.AlignCenter, text)


    @pyqtProperty(float)
    def position(self):
        return self.pos

    @position.setter
    def position(self, value):
        self.pos = value
        self.bn.update()

    def animate(self, checked):
        self.ani.setDirection(QPropertyAnimation.Forward if checked else QPropertyAnimation.Backward)
        self.ani.start()

class SwitchButton(QAbstractButton):
    def __init__(self):
        super().__init__()
        self.pri = SwitchPrivate(self)
        self.setCheckable(True)
        self.clicked.connect(self.pri.animate)

        font = self.font()
        font.setPixelSize(20)
        self.setFont(font)

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.pri.draw(painter)

    def resizeEvent(self, e: QResizeEvent) -> None:
        self.update()

    def sizeHint(self) -> QSize:
        return QSize(84, 42)


class Scene(QGraphicsScene):
    def __init__(self):
        super().__init__()

class View(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._scene = Scene()
        self.setScene(self._scene)
        self.setSceneRect(-100, -100, 200, 200)

        self.setInteractive(True)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)


    def drawForeground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setPen(QPen(Qt.red, 1, Qt.DotLine))
        painter.drawRect(self.sceneRect())

    def wheelEvent(self, e: QWheelEvent) -> None:
        super().wheelEvent(e)

        factor = 2.71827**(e.angleDelta().y()/360)
        ratio = self.transform().scale(factor, factor).mapRect(QRectF(0, 0, 1, 1)).width()

        if ratio < 0.1 or ratio > 5:
            return

        self.scale(factor, factor)

    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        def fitInView():
            self.fitInView(self.sceneRect())

        menu = QMenu()
        menu.addAction("fitInView", fitInView)
        menu.exec(e.globalPos())
        super().contextMenuEvent(e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)

        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)

        super().mouseReleaseEvent(e)


