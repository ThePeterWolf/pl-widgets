# pl_slider.py

"""
PLSlider - A custom horizontal slider with circular thumb for PySide6.

This widget allows smooth value selection with optional step behavior
and customizable styling through QSS.

Author: Pierre-Lou Guilloré
License: MIT
"""

from PySide6 import QtWidgets, QtCore, QtGui
from .pl_style_mixin import PlStyleMixin


class PLSlider(PlStyleMixin, QtWidgets.QWidget):
    """
    A custom slider with a circle thumb and support for stylesheets and steps.

    Signals:
        valueChanged(int): Emitted when the slider value changes.

    Properties:
        value (int): The current slider value.
        minimum (int): Minimum slider value.
        maximum (int): Maximum slider value.
        backgroundColor (QColor): Color of the track.
        thumbColor (QColor): Color of the slider thumb.
    """

    valueChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(24)
        self.setMinimumWidth(100)

        self._margin = 6
        self._radius = 8
        self._minimum = 0
        self._maximum = 100
        self._value = 20

        self._step_enabled = False
        self._step_size = 1

        self._dragging = False

        self._backgroundColor = QtGui.QColor("#7d7e82")
        self._thumbColor = QtGui.QColor("#5683d1")

    # --- Public API ---
    def enableStep(self, step_size: int):
        """
        Enable stepped movement of the slider.
        """
        self._step_enabled = True
        self._step_size = max(1, step_size)
        self.setValue(self._value)

    def setRange(self, minimum: int, maximum: int):
        self._minimum = minimum
        self._maximum = maximum
        self.update()

    def setValue(self, value: int):
        value = max(self._minimum, min(self._maximum, value))
        if self._step_enabled:
            value = self._minimum + round((value - self._minimum) / self._step_size) * self._step_size
        if value != self._value:
            self._value = value
            self.valueChanged.emit(self._value)
            self.update()

    def value(self) -> int:
        return self._value

    # --- Mouse Events ---
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            self._dragging = True
            self._updateValueFromPosition(event.position().x())

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self._dragging:
            self._updateValueFromPosition(event.position().x())

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        self._dragging = False

    def _updateValueFromPosition(self, x: float):
        usable_width = self.width() - 2 * (self._margin + self._radius)
        x = min(max(x - (self._margin + self._radius), 0), usable_width)
        ratio = x / usable_width
        value = self._minimum + int(ratio * (self._maximum - self._minimum))
        self.setValue(value)

    # --- Painting ---
    def paintEvent(self, _: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect().adjusted(self._margin + self._radius, 0, -self._margin - self._radius, 0)
        center_y = rect.center().y()
        groove_height = 4

        # Track
        groove_rect = QtCore.QRectF(
            rect.left(), center_y - groove_height / 2,
            rect.width(), groove_height
        )
        bg_color = self.property("backgroundColor") or self._backgroundColor
        painter.setBrush(bg_color)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(groove_rect, 2, 2)

        # Thumb
        ratio = (self._value - self._minimum) / (self._maximum - self._minimum)
        pointer_x = rect.left() + ratio * rect.width()
        thumb_color = self.property("thumbColor") or self._thumbColor

        painter.setBrush(thumb_color)
        painter.drawEllipse(QtCore.QPointF(pointer_x, self.height() / 2), self._radius, self._radius)

    # --- QSS Properties ---
    @QtCore.Property(QtGui.QColor)
    def backgroundColor(self) -> QtGui.QColor:
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, color: QtGui.QColor):
        self._backgroundColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def thumbColor(self) -> QtGui.QColor:
        return self._thumbColor

    @thumbColor.setter
    def thumbColor(self, color: QtGui.QColor):
        self._thumbColor = color
        self.update()

    @QtCore.Property(int)
    def minimum(self) -> int:
        return self._minimum

    @minimum.setter
    def minimum(self, value: int):
        self._minimum = value
        self.update()

    @QtCore.Property(int)
    def maximum(self) -> int:
        return self._maximum

    @maximum.setter
    def maximum(self, value: int):
        self._maximum = value
        self.update()

    @QtCore.Property(int)
    def value_(self) -> int:
        return self._value

    @value_.setter
    def value_(self, val: int):
        self.setValue(val)
