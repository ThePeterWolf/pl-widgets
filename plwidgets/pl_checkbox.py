# pl_slide_checkbox.py

"""
PlCheckBox - A custom toggle switch widget for PySide6.

This widget provides a sleek animated ON/OFF slider that can be used
as a replacement for a standard checkbox or toggle in PySide6 applications.

Author: Pierre-Lou Guilloré
License: MIT
"""

from PySide6 import QtWidgets, QtCore, QtGui
from .pl_style_mixin import PlStyleMixin


class PlCheckBox(PlStyleMixin, QtWidgets.QWidget):
    """
    A custom animated checkbox styled as a sliding toggle switch.

    Signals:
        toggled(bool): Emitted when the checked state changes.

    Properties:
        checked (bool): Indicates whether the switch is checked.
        bgColor (QColor): Background color of the switch.
        handleColor (QColor): Color of the sliding handle.
    """

    toggled = QtCore.Signal(bool)

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """
        Initialize the PlCheckBox widget.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.setFixedSize(60, 30)

        self._checked = False
        self._handle_position = 2

        self._backgroundColor = QtGui.QColor("#7d7e82")
        self._checkedBackgroundColor = QtGui.QColor("#5683d1")
        self._handleColor = QtGui.QColor("#bbbcbe")
        self._checkedHandleColor = QtGui.QColor("#9fb7e0")

        self._animation = QtCore.QPropertyAnimation(self, b"handle_position", self)
        self._animation.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self._animation.setDuration(200)

        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setProperty("checked", self._checked)

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(60, 30)

    def minimumSizeHint(self) -> QtCore.QSize:
        return self.sizeHint()

    def paintEvent(self, _: QtGui.QPaintEvent) -> None:
        """
        Handle the paint event to draw the toggle switch.
        """
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        bg_color = self.property("backgroundColor") or self._backgroundColor if not self.checked else self._checkedBackgroundColor
        handle_color = self.property("handleColor") or self._handleColor if not self.checked else self._checkedHandleColor

        rect = self.rect()
        border_radius = rect.height() / 2

        # Draw background
        painter.setBrush(bg_color)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(rect, border_radius, border_radius)

        # Draw handle
        handle_size = rect.height() - 4
        handle_rect = QtCore.QRectF(self._handle_position, 2, handle_size, handle_size)

        painter.setBrush(handle_color)
        painter.drawEllipse(handle_rect)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.toggle()
        self.setFocus()
        super().mousePressEvent(event)

    def toggle(self) -> None:
        self.setChecked(not self._checked)

    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, checked: bool) -> None:
        if self._checked == checked:
            return
        self._checked = checked
        self.setProperty("checked", self._checked)
        self.style().unpolish(self)
        self.style().polish(self)
        self._animate()
        self.toggled.emit(self._checked)

    def _animate(self) -> None:
        start = self._handle_position
        end = self.width() - self.height() + 2 if self._checked else 2
        self._animation.stop()
        self._animation.setStartValue(start)
        self._animation.setEndValue(end)
        self._animation.start()

    def _get_handle_position(self) -> int:
        return self._handle_position

    def _set_handle_position(self, pos: int) -> None:
        self._handle_position = pos
        self.update()

    handle_position = QtCore.Property(int, _get_handle_position, _set_handle_position)

    @QtCore.Property(bool)
    def checked(self) -> bool:
        return self._checked

    @checked.setter
    def checked(self, value: bool) -> None:
        self.setChecked(value)

    @QtCore.Property(QtGui.QColor)
    def backgroundColor(self) -> QtGui.QColor:
        """QColor: The background color of the switch."""
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, color: QtGui.QColor) -> None:
        self._backgroundColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def handleColor(self) -> QtGui.QColor:
        """QColor: The handle color of the switch."""
        return self._handleColor

    @handleColor.setter
    def handleColor(self, color: QtGui.QColor) -> None:
        self._handleColor = color
        self.update()
