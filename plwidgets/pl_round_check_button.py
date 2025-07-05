"""
PlRoundCheckButton - A round, checkable button with minimal styling.

This widget creates a flat, pill-shaped toggle button with customizable
colors and a fully stylable API, including border, background, and text
colors for checked and unchecked states.

Author: Pierre-Lou Guilloré
License: MIT
"""

from PySide6 import QtWidgets, QtCore, QtGui
from .pl_style_mixin import PlStyleMixin


class PlRoundCheckButton(QtWidgets.QPushButton, PlStyleMixin):
    """
    A minimalistic checkable button with a rounded pill shape.

    - Transparent background by default
    - Colored border and text
    - Background filled when checked
    - Text turns dark when checked
    - Fully stylable via QSS or Python properties

    Properties
    ----------
    borderColor : QColor
        The color of the button border.
    textColor : QColor
        The text color when unchecked.
    checkedColor : QColor
        The background color when checked.
    checkedTextColor : QColor
        The text color when checked.
    """

    def __init__(self, text: str = "", parent: QtWidgets.QWidget = None):
        super().__init__(text, parent)

        self.setCheckable(True)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Medium))
        self.setMinimumSize(100, 50)
        self.setFlat(True)
        self.setAttribute(QtCore.Qt.WA_Hover)

        # Default colors
        self._borderColor = QtGui.QColor("#5683d1")
        self._textColor = QtGui.QColor("#5683d1")
        self._checkedColor = QtGui.QColor("#5683d1")
        self._checkedTextColor = QtGui.QColor("#2a2a2a")

        self._font = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Normal)
        self.setFont(self._font)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        self._resolveStyle()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)
        radius = rect.height() / 2

        # Background
        if self.isChecked():
            painter.setBrush(self._checkedColor)
        else:
            painter.setBrush(QtCore.Qt.transparent)

        # Border
        painter.setPen(QtGui.QPen(self._borderColor, 2))
        painter.drawRoundedRect(rect, radius, radius)

        # Text
        text_color = self._checkedTextColor if self.isChecked() else self._textColor

        font = QtGui.QFont(self._font)
        font.setBold(self.isChecked())
        painter.setFont(font)

        painter.setPen(text_color)
        painter.drawText(rect, QtCore.Qt.AlignCenter, self.text())

    def _resolveStyle(self):
        """Reads QSS custom properties and applies fallback colors."""
        self._borderColor = self.getColor("border-color", self._borderColor)
        self._textColor = self.getColor("text-color", self._textColor)
        self._checkedColor = self.getColor("checked-color", self._checkedColor)
        self._checkedTextColor = self.getColor("checked-text-color", self._checkedTextColor)

    # --- Properties ---

    @QtCore.Property(QtGui.QColor)
    def borderColor(self) -> QtGui.QColor:
        return self._borderColor

    @borderColor.setter
    def borderColor(self, color: QtGui.QColor):
        self._borderColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def textColor(self) -> QtGui.QColor:
        return self._textColor

    @textColor.setter
    def textColor(self, color: QtGui.QColor):
        self._textColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def checkedColor(self) -> QtGui.QColor:
        return self._checkedColor

    @checkedColor.setter
    def checkedColor(self, color: QtGui.QColor):
        self._checkedColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def checkedTextColor(self) -> QtGui.QColor:
        return self._checkedTextColor

    @checkedTextColor.setter
    def checkedTextColor(self, color: QtGui.QColor):
        self._checkedTextColor = color
        self.update()
