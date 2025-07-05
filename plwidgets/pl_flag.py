from PySide6 import QtWidgets, QtCore, QtGui


class PLFlag(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)

        self._title_height = 24
        self._title = title
        self._radius = 4
        self._topColor = QtGui.QColor("#2c2f33")
        self._bottomColor = QtGui.QColor("#2c2f33")
        self._borderColor = QtGui.QColor("#44484d")
        self._alignment = QtCore.Qt.AlignCenter
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setMinimumHeight(60)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(10, 10, 10, 10)
        self._layout.addSpacerItem(QtWidgets.QSpacerItem(0, self._title_height))
        super().setLayout(self._layout)

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

        pen = QtGui.QPen(self._borderColor)
        pen.setWidth(1)
        painter.setPen(pen)

        painter.setBrush(QtCore.Qt.NoBrush)
        global_rect = self.rect()
        global_rect.adjust(1, 1, -1, -1)
        painter.drawRoundedRect(global_rect, self._radius, self._radius)

        # Draw centered title
        painter.setPen(QtGui.QColor("white"))
        font = painter.font()
        # font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)
        text_rect = QtCore.QRectF(0, 0, rect.width(), half_height)
        
        if self._alignment == QtCore.Qt.AlignLeft:
            text_rect.adjust(10, 4, -10, 0)
        
        painter.drawText(text_rect, self._alignment, self._title)

        painter.end()

    def setLayout(self, layout):
        self._layout.addLayout(layout)

    def setLabelAlignement(self, alignement: QtCore.Qt.AlignmentFlag):

        self._alignment = alignement
        
        self.update()


