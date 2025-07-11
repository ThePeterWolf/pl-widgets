"""
PlTabWidget - A custom tab bar with fully painted tabs using PySide6.

This widget mimics a tab system with a custom-painted header and integrates
a QStackedLayout for showing different widgets per tab.

Author: Pierre-Lou Guilloré
License: MIT
"""

from PySide6 import QtWidgets, QtGui, QtCore
from .pl_style_mixin import PlStyleMixin


class PlTabWidget(PlStyleMixin, QtWidgets.QWidget):
    """
    A fully custom-painted tab widget using QPainter and QStackedLayout.

    Signals:
        currentChanged(int): Emitted when the selected tab changes.

    Properties:
        backgroundColor (QColor)
        topColor (QColor)
        textColor (QColor)
        borderColor (QColor)
        hoverColor (QColor)
        radius (int)
    """

    currentChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Style properties
        self._backgroundColor = QtGui.QColor("#1f2227")
        self._selectedColor = QtGui.QColor("#1f2227")
        self._unselectedColor = QtGui.QColor("#26292d")
        self._topColor = QtGui.QColor("#2c2f33")
        self._textColor = QtGui.QColor("#f0f0f0")
        self._borderColor = QtGui.QColor("#44484d")
        self._hoverColor = QtGui.QColor("#4a4e55")
        self._radius = 6

        # Tabs
        self._tab_width = 100
        self._header_height = 28
        self._tabs = []
        self._hover_index = -1
        self._current_index = 0

        # Layout
        self.setMouseTracking(True)
        self._stack = QtWidgets.QStackedLayout()
        self._stack.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, self._header_height + 10, 0, 0)
        layout.addLayout(self._stack)

    def sizeHint(self):
        return QtCore.QSize(self._tab_width * max(1, len(self._tabs)), 150)

    def addTab(self, name="NewTab", widget=None):
        self._tabs.append(name)
        if widget is None:
            widget = QtWidgets.QWidget()
        self._stack.addWidget(widget)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Background
        painter.setBrush(self._backgroundColor)
        painter.drawRoundedRect(self.rect(), self._radius, self._radius)

        # Header path
        r = self._radius
        header_path = QtGui.QPainterPath()
        header_path.moveTo(0, self._header_height)
        header_path.lineTo(0, r)
        header_path.quadTo(0, 0, r, 0)
        header_path.lineTo(self.width() - r, 0)
        header_path.quadTo(self.width(), 0, self.width(), r)
        header_path.lineTo(self.width(), self._header_height)
        header_path.closeSubpath()

        painter.setBrush(self._topColor)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawPath(header_path)

        # Tabs
        for i, title in enumerate(self._tabs):
            tab_rect = QtCore.QRect(i * self._tab_width, 0, self._tab_width, self._header_height + 1)

            if i == self._current_index:
                tab_color = self._selectedColor
            elif i == self._hover_index:
                tab_color = self._hoverColor
            else:
                tab_color = self._unselectedColor

            path = QtGui.QPainterPath()
            path.moveTo(tab_rect.left(), tab_rect.bottom())

            if i == 0:
                path.lineTo(tab_rect.left(), tab_rect.top() + r)
                path.quadTo(tab_rect.left(), tab_rect.top(), tab_rect.left() + r, tab_rect.top())
            else:
                path.lineTo(tab_rect.left(), tab_rect.top())

            if i == len(self._tabs) - 1:
                path.lineTo(tab_rect.right() - r, tab_rect.top())
                path.quadTo(tab_rect.right(), tab_rect.top(), tab_rect.right(), tab_rect.top() + r)
            else:
                path.lineTo(tab_rect.right(), tab_rect.top())

            path.lineTo(tab_rect.right(), tab_rect.bottom())
            path.closeSubpath()

            painter.setBrush(tab_color)
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawPath(path)

            # Text
            painter.setPen(self._textColor)
            font = painter.font()
            font.setBold(i == self._current_index)
            painter.setFont(font)
            painter.drawText(tab_rect, QtCore.Qt.AlignCenter, title)

        # Outer border
        border_rect = self.rect().adjusted(1, 1, -1, -1)
        painter.setPen(QtGui.QPen(self._borderColor))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRoundedRect(border_rect, self._radius, self._radius)

        painter.end()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        index = pos.x() // self._tab_width if pos.y() <= self._header_height else -1
        if index != self._hover_index:
            self._hover_index = index if 0 <= index < len(self._tabs) else -1
            self.update()

    def leaveEvent(self, event):
        self._hover_index = -1
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and event.y() <= self._header_height:
            index = event.x() // self._tab_width
            if 0 <= index < len(self._tabs):
                if self._current_index != index:
                    self._current_index = index
                    self._stack.setCurrentIndex(index)
                    self.currentChanged.emit(index)
                    self.update()

    def currentIndex(self):
        return self._current_index

    def setCurrentIndex(self, index):
        if 0 <= index < len(self._tabs):
            self._current_index = index
            self._stack.setCurrentIndex(index)
            self.update()
            self.currentChanged.emit(index)

    # === Style & Property Interface ===

    @QtCore.Property(QtGui.QColor)
    def backgroundColor(self):
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, color):
        self._backgroundColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def unselectedColor(self):
        return self._unselectedColor

    @unselectedColor.setter
    def unselectedColor(self, color):
        self._unselectedColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def selectedColor(self):
        return self._selectedColor

    @selectedColor.setter
    def selectedColor(self, color):
        self._selectedColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def topColor(self):
        return self._topColor

    @topColor.setter
    def topColor(self, color):
        self._topColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, color):
        self._textColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def borderColor(self):
        return self._borderColor

    @borderColor.setter
    def borderColor(self, color):
        self._borderColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def hoverColor(self):
        return self._hoverColor

    @hoverColor.setter
    def hoverColor(self, color):
        self._hoverColor = color
        self.update()

    @QtCore.Property(int)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self.update()
