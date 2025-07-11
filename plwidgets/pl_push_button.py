from PySide6 import QtWidgets, QtCore, QtGui
from .pl_style_mixin import PlStyleMixin


class PlPushButton(PlStyleMixin, QtWidgets.QPushButton):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)

        # Style properties
        self._backgroundColor = QtGui.QColor("#3b3f45")
        self._hoverColor = self._backgroundColor.lighter(120)
        self._pressedColor = self._backgroundColor.darker(110)
        self._textColor = QtGui.QColor("#f0f0f0")
        self._borderColor = QtGui.QColor("#44484d")
        self._radius = 4

        self._hover = False
        self._pressed = False

        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setFont(QtGui.QFont("Segoe UI", 10))
        self.setMinimumHeight(28)
        self.setFlat(True)

        self.setAttribute(QtCore.Qt.WA_Hover)

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)
        radius = self._radius

        if self._pressed:
            bg = self._pressedColor
        elif self._hover:
            bg = self._hoverColor
        else:
            bg = self._backgroundColor

        painter.setPen(QtGui.QPen(self._borderColor, 1.2))
        painter.setBrush(bg)
        painter.drawRoundedRect(rect, radius, radius)

        painter.setPen(self._textColor)
        painter.drawText(rect, QtCore.Qt.AlignCenter, self.text())

    # === Style & Property Interface ===
    
    @QtCore.Property(QtGui.QColor)
    def backgroundColor(self):
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, color: QtGui.QColor):
        self._backgroundColor = color
        self._hoverColor = color.lighter(120)
        self._pressedColor = color.darker(110)
        self.update()

    @QtCore.Property(QtGui.QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, color: QtGui.QColor):
        self._textColor = color
        self.update()
