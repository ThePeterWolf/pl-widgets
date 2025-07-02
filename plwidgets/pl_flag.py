from PySide6 import QtWidgets, QtCore, QtGui


class PLFlag(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)

        self._title_height = 24
        self._radius = 4
        self._topColor = QtGui.QColor("#2c2f33")
        self._bottomColor = QtGui.QColor("#2c2f33")
        self._borderColor = QtGui.QColor("#44484d")
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setMinimumHeight(60)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect()
        half_height = self._title_height

        radius = self._radius

        # --- Partie haute (arrondi en haut seulement)
        top_rect = QtCore.QRect(0, 0, rect.width(), half_height)
        top_path = QtGui.QPainterPath()
        top_path.moveTo(0, half_height)
        top_path.lineTo(0, radius)
        top_path.quadTo(0, 0, radius, 0)
        top_path.lineTo(rect.width() - radius, 0)
        top_path.quadTo(rect.width(), 0, rect.width(), radius)
        top_path.lineTo(rect.width(), half_height)
        top_path.closeSubpath()

        painter.setBrush(self._topColor)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawPath(top_path)

        # bottom_rect = QtCore.QRect(0, half_height, rect.width(), rect.height() - half_height)
        # bottom_path = QtGui.QPainterPath()
        # bottom_path.moveTo(0, half_height)
        # bottom_path.lineTo(0, rect.height() - radius)
        # bottom_path.quadTo(0, rect.height(), radius, rect.height())
        # bottom_path.lineTo(rect.width() - radius, rect.height())
        # bottom_path.quadTo(rect.width(), rect.height(), rect.width(), rect.height() - radius)
        # bottom_path.lineTo(rect.width(), half_height)
        # bottom_path.closeSubpath()

        # painter.setBrush(self._bottomColor)
        # painter.drawPath(bottom_path)

        pen = QtGui.QPen(self._borderColor)
        pen.setWidth(1)
        painter.setPen(pen)

        painter.setBrush(QtCore.Qt.NoBrush)
        global_rect = self.rect()
        global_rect.adjust(1, 1, -1, -1)
        painter.drawRoundedRect(global_rect, self._radius, self._radius)

        painter.end()




