# pl_combo_box.py

"""
PlComboBox - A custom styled combo box widget for PySide6.

This widget is a modern and minimal dropdown list with custom appearance,
animated arrow, and customizable color properties.

Author: Pierre-Lou Guilloré
License: MIT
"""

from PySide6 import QtWidgets, QtCore, QtGui
from .pl_style_mixin import PlStyleMixin
from .resource_utils import resourceLoader


class PlComboBox(QtWidgets.QComboBox):
    """
    A custom combo box with a flat modern style and customizable colors.

    Signals:
        currentIndexChanged(int): Emitted when the selected index changes.

    Properties:
        backgroundColor (QColor): Background color of the combo box.
        textColor (QColor): Text color.
        borderColor (QColor): Border color.
        arrowColor (QColor): Dropdown arrow color.
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setView(QtWidgets.QListView())  # for more control

        self.setEditable(False)
        self.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.setMinimumHeight(30)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(24)

        self._backgroundColor = QtGui.QColor("#2c2f33")
        self._textColor = QtGui.QColor("#f0f0f0")
        self._borderColor = QtGui.QColor("#44484d")
        self._arrow_image = resourceLoader.getIconPath("thin_arrow_down_64x64.png")
        self._arrowColor = QtGui.QColor("#44484d")
        # self._arrowColor = QtGui.QColor("#5683d1")

        font = QtGui.QFont("Segoe UI", 10)
        self.setFont(font)

        self.setStyleSheet(self._generate_style())

    def _generate_style(self) -> str:
        return f"""
        QComboBox {{
            background-color: {self._backgroundColor.name()};
            color: {self._textColor.name()};
            border: 2px solid {self._borderColor.name()};
            border-radius: 6px;
            padding: 1px 30px 2px 4px;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 24px;
            border-left: 1px solid {self._borderColor.name()};
        }}
        QComboBox::down-arrow {{
            image: url("{self._arrow_image}");
        }}
        QComboBox QAbstractItemView {{
            background-color: {self._backgroundColor.name()};
            border: 1px solid {self._borderColor.name()};
            selection-color: white;
            color: {self._textColor.name()};
        }}
        """

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        super().paintEvent(event)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        arrow_width = 10
        arrow_height = 6
        margin = 28

        center_x = self.width() - margin/2
        center_y = self.height()/2

        # Triangle pointant vers le bas
        points = [
            QtCore.QPointF(center_x - arrow_width / 2, center_y - arrow_height / 3),
            QtCore.QPointF(center_x + arrow_width / 2, center_y - arrow_height / 3),
            QtCore.QPointF(center_x, center_y + arrow_height/2),
        ]

        pen = QtGui.QPen(self._arrowColor)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(points[2], points[0])
        painter.drawLine(points[1], points[2])

    # Dynamic styling
    def _refreshStyle(self) -> None:
        self.setStyleSheet(self._generate_style())

    @QtCore.Property(QtGui.QColor)
    def backgroundColor(self) -> QtGui.QColor:
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, color: QtGui.QColor) -> None:
        self._backgroundColor = color
        self._refreshStyle()

    @QtCore.Property(QtGui.QColor)
    def textColor(self) -> QtGui.QColor:
        return self._textColor

    @textColor.setter
    def textColor(self, color: QtGui.QColor) -> None:
        self._textColor = color
        self._refreshStyle()

    @QtCore.Property(QtGui.QColor)
    def borderColor(self) -> QtGui.QColor:
        return self._borderColor

    @borderColor.setter
    def borderColor(self, color: QtGui.QColor) -> None:
        self._borderColor = color
        self._refreshStyle()

    @QtCore.Property(QtGui.QColor)
    def arrowColor(self) -> QtGui.QColor:
        return self._arrowColor

    @arrowColor.setter
    def arrowColor(self, color: QtGui.QColor) -> None:
        self._arrowColor = color
        self._refreshStyle()
