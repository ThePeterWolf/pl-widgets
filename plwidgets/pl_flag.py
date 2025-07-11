"""
PlFlag - A container widget with a styled header area using PySide6.

This widget displays a titled header with customizable alignment and colors,
and allows you to insert arbitrary layouts/content in the body.

Author: Pierre-Lou Guilloré
License: MIT
"""

from PySide6 import QtWidgets, QtCore, QtGui
from .pl_style_mixin import PlStyleMixin


class PlFlag(PlStyleMixin, QtWidgets.QWidget):
    """
    A titled box widget with a painted header and layout container.

    Properties:
        title (str): The label shown in the top flag area.
        topColor (QColor): Color of the top header.
        bottomColor (QColor): Background of the full widget (not used in default painting).
        borderColor (QColor): Border color around the flag.
        radius (int): Corner radius of the flag.
        labelAlignment (Qt.Alignment): Alignment of the text in the header.
    """

    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)

        self._title = title

        # Style properties
        self._radius = 4
        self._title_height = 24
        self._topColor = QtGui.QColor("#2c2f33")
        self._bottomColor = QtGui.QColor("#2c2f33")
        self._borderColor = QtGui.QColor("#44484d")
        self._alignment = QtCore.Qt.AlignCenter

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(10, self._title_height + 10, 10, 10)
        super().setLayout(self._layout)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect()
        half_height = self._title_height
        radius = self._radius

        # Draw top rounded header
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

        # Outer border
        painter.setBrush(QtCore.Qt.NoBrush)
        pen = QtGui.QPen(self._borderColor)
        pen.setWidth(1)
        painter.setPen(pen)
        border_rect = rect.adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(border_rect, radius, radius)

        # Draw header title
        painter.setPen(QtGui.QColor("white"))
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)

        text_rect = QtCore.QRectF(0, 0, rect.width(), half_height)
        if self._alignment == QtCore.Qt.AlignLeft:
            text_rect.adjust(10, 4, -10, 0)

        painter.drawText(text_rect, self._alignment, self._title)

        painter.end()

    def _clear_layout(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.layout():
                self._clear_layout(item.layout())
                item.layout().deleteLater()
            elif item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
            else:
                del item
                
    def setLayout(self, layout: QtWidgets.QLayout):
        self._clear_layout
        self._layout.addLayout(layout)

    def setLabelAlignment(self, alignment: QtCore.Qt.AlignmentFlag):
        self._alignment = alignment
        self.update()

    # === Style & Property Interface ===

    @QtCore.Property(str)
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.update()

    @QtCore.Property(QtGui.QColor)
    def topColor(self):
        return self._topColor

    @topColor.setter
    def topColor(self, color):
        self._topColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def bottomColor(self):
        return self._bottomColor

    @bottomColor.setter
    def bottomColor(self, color):
        self._bottomColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def borderColor(self):
        return self._borderColor

    @borderColor.setter
    def borderColor(self, color):
        self._borderColor = color
        self.update()

    @QtCore.Property(int)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self.update()

    @QtCore.Property(QtCore.Qt.Alignment)
    def labelAlignment(self):
        return self._alignment

    @labelAlignment.setter
    def labelAlignment(self, alignment):
        self._alignment = alignment
        self.update()
