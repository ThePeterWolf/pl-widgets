"""
PlProgressCircle - A circular progress bar widget for PySide6.

Author: Pierre-Lou Guilloré
License: MIT
"""

from PySide6 import QtWidgets, QtGui, QtCore
from .pl_style_mixin import PlStyleMixin


class PlProgressCircle(PlStyleMixin, QtWidgets.QWidget):
    """
    A circular progress indicator with customizable color, thickness, and central text.

    Properties:
        value (int): The progress value from 0 to 100.
        progressColor (QColor): The color of the progress arc.
        completeColor (QColor): The color when progress is 100%.
        backgroundColor (QColor): The background circle color.
        textColor (QColor): The text color inside the circle.
        
        lineWidth (int): The thickness of the circle lines.
        textVisible (bool): Whether to display the percent label.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._value = 0
        self._text_visible = True

        self._progressColor = QtGui.QColor("#e2a010")
        self._completeColor = QtGui.QColor("#2caf3e")
        self._backgroundColor = QtGui.QColor("#dcdde1")
        self._textColor = QtGui.QColor("#2f3640")
        self._textSize = 14
        self._lineWidth = 10

        self.setMinimumSize(40, 40)

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(120, 120)

    def paintEvent(self, _: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        size = min(width, height)
        margin = self.lineWidth / 2

        # Colors (from properties)
        bg_color = self.backgroundColor
        progress_color = self.progressColor if self._value < 100 else self.completeColor
        text_color = self.textColor

        # Arc geometry
        rect = QtCore.QRectF(margin, margin, size - 2 * margin, size - 2 * margin)

        # Draw background circle
        pen = QtGui.QPen(bg_color, self.lineWidth)
        painter.setPen(pen)
        painter.drawEllipse(rect)

        # Draw progress arc
        pen.setColor(progress_color)
        painter.setPen(pen)
        angle = int(360 * self._value / 100)
        painter.drawArc(rect, -90 * 16, -angle * 16)

        # Draw percentage text
        if self.textVisible:
            font = painter.font()
            font.setPointSize(self._textSize)
            painter.setFont(font)
            painter.setPen(QtGui.QPen(text_color))
            painter.drawText(QtCore.QRect(0, 0, size, size), QtCore.Qt.AlignCenter, f"{self._value}%")

    # --- Properties ---

    @QtCore.Property(int)
    def value(self) -> int:
        """Current progress value (0–100)."""
        return self._value

    @value.setter
    def value(self, val: int) -> None:
        self.setValue(val)

    def setValue(self, value: int) -> None:
        self._value = max(0, min(100, value))
        self.update()

    def getValue(self) -> int:
        return self._value

    def incrementValue(self, delta: int) -> None:
        self.setValue(self._value + delta)

    @QtCore.Property(bool)
    def textVisible(self) -> bool:
        """Whether the center percentage text is visible."""
        return self._text_visible

    @textVisible.setter
    def textVisible(self, visible: bool) -> None:
        self._text_visible = visible
        self.update()

    @QtCore.Property(int)
    def textSize(self) -> int:
        """Whether the center percentage text is visible."""
        return self._textSize

    @textSize.setter
    def textSize(self, size: int) -> None:
        self._textSize = size
        self.update()

    @QtCore.Property(QtGui.QColor)
    def progressColor(self) -> QtGui.QColor:
        return self._progressColor

    @progressColor.setter
    def progressColor(self, color: QtGui.QColor) -> None:
        self._progressColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def completeColor(self) -> QtGui.QColor:
        return self._completeColor

    @completeColor.setter
    def completeColor(self, color: QtGui.QColor) -> None:
        self._completeColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def backgroundColor(self) -> QtGui.QColor:
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, color: QtGui.QColor) -> None:
        self._backgroundColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def textColor(self) -> QtGui.QColor:
        return self._textColor

    @textColor.setter
    def textColor(self, color: QtGui.QColor) -> None:
        self._textColor = color
        self.update()

    @QtCore.Property(int)
    def lineWidth(self) -> int:
        return self._lineWidth

    @lineWidth.setter
    def lineWidth(self, value: int) -> None:
        self._lineWidth = value
        self.update()
