from PySide6 import QtWidgets, QtCore, QtGui
from .pl_style_mixin import PlStyleMixin


class PlLineEdit(PlStyleMixin, QtWidgets.QWidget):
    """
    A custom QLineEdit with dark theme and subtle rounded border.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Style properties

        self._backgroundColor = QtGui.QColor("#2c2f33")
        self._borderColor = QtGui.QColor("#44484d")
        self._textColor = QtGui.QColor("#f0f0f0")
        self._radius = 4
        self._focusBorderColor = QtGui.QColor("#5683d1")

        self.setFixedHeight(24)

        self._line_edit = QtWidgets.QLineEdit()
        self._line_edit.setStyleSheet("background: transparent; border: none; color: white;")
        self._line_edit.setFont(QtGui.QFont("Segoe UI", 10))
        self._line_edit.setAttribute(QtCore.Qt.WA_Hover)
        self._line_edit.installEventFilter(self)

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.addWidget(self._line_edit)
        self._layout.setContentsMargins(4, 2, 4, 2)
        self.setLayout(self._layout)

        self._hover = False
        self._hasFocus = False


    def __getattr__(self, name):
        """
        Delegate attribute access to the internal QLineEdit if not found on self.
        """
        return getattr(self._line_edit, name)

    def eventFilter(self, watched, event):
        if watched == self._line_edit:
            if event.type() == QtCore.QEvent.FocusIn:
                self._hasFocus = True
                self.update()
            elif event.type() == QtCore.QEvent.FocusOut:
                self._hasFocus = False
                self.update()
        return super().eventFilter(watched, event)

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._line_edit.setFocus()
        super().mousePressEvent(event)

    def focusInEvent(self, event):
        self._hasFocus = True
        self.update()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self._hasFocus = False
        self.update()
        super().focusOutEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)

        # Background
        painter.setBrush(self._backgroundColor)
        painter.setPen(QtGui.QPen(self._focusBorderColor if self._hasFocus else self._borderColor, 1.5))
        painter.drawRoundedRect(rect, self._radius, self._radius)

        # Call base to draw text
        super().paintEvent(event)

    # === Style & Property Interface ===
    
    @QtCore.Property(QtGui.QColor)
    def backgroundColor(self):
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, color: QtGui.QColor):
        self._backgroundColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def borderColor(self):
        return self._borderColor

    @borderColor.setter
    def borderColor(self, color: QtGui.QColor):
        self._borderColor = color
        self.update()

    @QtCore.Property(QtGui.QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, color: QtGui.QColor):
        self.setStyleSheet(f"color: {color.name()}; background: transparent; border: none;")
        self._textColor = color
        self.update()
