# pl_check_button_group.py

"""
PlCheckButtonGroup - A checkable button group widget for PySide6.

This widget allows grouping of checkable push buttons with selectable styles
and multiple selection modes, including single selection and enforced selection.

Author: Pierre-Lou Guilloré
License: MIT
"""

from PySide6 import QtWidgets, QtCore, QtGui
from .pl_style_mixin import PlStyleMixin


class PlCheckButtonGroup(QtWidgets.QWidget, PlStyleMixin):
    """
    A stylable group of checkable buttons supporting multiple selection modes.

    Parameters
    ----------
    parent : QWidget, optional
        Parent widget (default is None).

    Signals
    -------
    checked(str)
        Emitted when a button becomes checked.

    Properties
    ----------
    backgroundColor : QColor
        The default background color of buttons.
    textColor : QColor
        The color of the button text.
    borderColor : QColor
        The border color for buttons.
    checkedColor : QColor
        The background color when a button is checked.
    hoverColor : QColor
        The background color on mouse hover.
    hoverCheckedColor : QColor
        The hover color for a checked button.
    pressedColor : QColor
        The background color when the button is pressed.
    radius : int
        The corner radius in pixels.
    """

    selectionModeMultiple = 0
    selectionModeSingle = 1
    selectionModeSingleForce = 2

    checked = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setSpacing(1)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._buttons: list[QtWidgets.QPushButton] = []
        self._selection_mode = self.selectionModeMultiple

        # Style properties
        self._backgroundColor = QtGui.QColor("#3b3f45")
        self._textColor = QtGui.QColor("#f0f0f0")
        self._borderColor = QtGui.QColor("#44484d")
        self._checkedColor = QtGui.QColor("#5683d1")
        self._hoverCheckedColor = QtGui.QColor("#749fe8")
        self._hoverColor = QtGui.QColor("#4a4e55")
        self._pressedColor = QtGui.QColor("#2e3237")
        self._radius = 4

    def addButton(self, label: str, name: str):
        button = QtWidgets.QPushButton(label)
        button.setObjectName(name)
        button.setCheckable(True)
        button.setCursor(QtCore.Qt.PointingHandCursor)
        button.setMinimumHeight(28)
        button.setFont(QtGui.QFont("Segoe UI", 10))
        button.setFlat(True)
        button.toggled.connect(self._onButtonToggled)
        self._buttons.append(button)
        self._layout.addWidget(button)
        self._updateStyles()

    def setSelectionMode(self, mode: int):
        if mode not in (
            self.selectionModeMultiple,
            self.selectionModeSingle,
            self.selectionModeSingleForce,
        ):
            raise ValueError("Invalid selection mode.")
        self._selection_mode = mode

    def setChecked(self, name: str, checked: bool = True):
        for btn in self._buttons:
            if btn.objectName() == name:
                if self._selection_mode in (
                    self.selectionModeSingle,
                    self.selectionModeSingleForce,
                ):
                    for b in self._buttons:
                        b.setChecked(b == btn if checked else False)
                else:
                    btn.setChecked(checked)
                return

    def _onButtonToggled(self, checked: bool):
        sender = self.sender()

        if checked:
            if self._selection_mode in (
                self.selectionModeSingle,
                self.selectionModeSingleForce,
            ):
                for btn in self._buttons:
                    if btn != sender:
                        btn.setChecked(False)
            self.checked.emit(sender.objectName())
        else:
            if self._selection_mode == self.selectionModeSingleForce:
                still_checked = any(
                    btn.isChecked() for btn in self._buttons if btn != sender
                )
                if not still_checked:
                    sender.setChecked(True)

    def _updateStyles(self):
        self._resolveStyleProperties()

        for i, btn in enumerate(self._buttons):
            radius_left = f"{self._radius}px" if i == 0 else "0"
            radius_right = f"{self._radius}px" if i == len(self._buttons) - 1 else "0"

            btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._backgroundColor.name()};
                color: {self._textColor.name()};
                border: 1px solid {self._borderColor.name()};
                padding: 4px 12px;
                font-family: 'Segoe UI';
                font-size: 10pt;
                border-left: none;
                border-top-left-radius: {radius_left};
                border-bottom-left-radius: {radius_left};
                border-top-right-radius: {radius_right};
                border-bottom-right-radius: {radius_right};
            }}
            QPushButton:first-child {{
                border-left: 1px solid {self._borderColor.name()};
            }}
            QPushButton:checked {{
                background-color: {self._checkedColor.name()};
            }}
            QPushButton:hover {{
                background-color: {self._hoverColor.name()};
            }}
            QPushButton:checked:hover {{
                background-color: {self._hoverCheckedColor.name()};
            }}
            QPushButton:pressed {{
                background-color: {self._pressedColor.name()};
            }}
            QPushButton:disabled {{
                background-color: #2a2d31;
                color: #888888;
            }}
            """)

    def _resolveStyleProperties(self):
        self._backgroundColor = self.getColor("background-color", self._backgroundColor)
        self._textColor = self.getColor("text-color", self._textColor)
        self._borderColor = self.getColor("border-color", self._borderColor)
        self._checkedColor = self.getColor("checked-color", self._checkedColor)
        self._hoverColor = self.getColor("hover-color", self._hoverColor)
        self._hoverCheckedColor = self.getColor("hover-checked-color", self._hoverCheckedColor)
        self._pressedColor = self.getColor("pressed-color", self._pressedColor)
        self._radius = self.getInt("radius", self._radius)

    # === Style & Property Interface ===

    @QtCore.Property(QtGui.QColor)
    def backgroundColor(self): return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, color): self._backgroundColor = color; self._updateStyles()

    @QtCore.Property(QtGui.QColor)
    def checkedColor(self): return self._checkedColor

    @checkedColor.setter
    def checkedColor(self, color): self._checkedColor = color; self._updateStyles()

    @QtCore.Property(QtGui.QColor)
    def borderColor(self): return self._borderColor

    @borderColor.setter
    def borderColor(self, color): self._borderColor = color; self._updateStyles()

    @QtCore.Property(QtGui.QColor)
    def textColor(self): return self._textColor

    @textColor.setter
    def textColor(self, color): self._textColor = color; self._updateStyles()

    @QtCore.Property(QtGui.QColor)
    def hoverColor(self): return self._hoverColor

    @hoverColor.setter
    def hoverColor(self, color): self._hoverColor = color; self._updateStyles()

    @QtCore.Property(QtGui.QColor)
    def hoverCheckedColor(self): return self._hoverCheckedColor

    @hoverCheckedColor.setter
    def hoverCheckedColor(self, color): self._hoverCheckedColor = color; self._updateStyles()

    @QtCore.Property(QtGui.QColor)
    def pressedColor(self): return self._pressedColor

    @pressedColor.setter
    def pressedColor(self, color): self._pressedColor = color; self._updateStyles()

    @QtCore.Property(int)
    def radius(self): return self._radius

    @radius.setter
    def radius(self, value): self._radius = value; self._updateStyles()
