from PySide6 import QtWidgets, QtCore, QtGui
from .pl_style_mixin import PlStyleMixin
from .resource_utils import resourceLoader


class PlSearchBar(PlStyleMixin, QtWidgets.QWidget):
    BUTTON_WIDTH = 40
    def __init__(self, parent=None):
        super().__init__(parent)

        # Style properties
        self._bgColor = QtGui.QColor("#2c2f33")
        self._bgColorRight = self._bgColor.darker(115)
        self._borderColor = QtGui.QColor("#44484d")
        self._focusBorderColor = QtGui.QColor("#5683d1")
        self._textColor = QtGui.QColor("#f0f0f0")
        self._radius = 4
        self._hasFocus = False
        self._hover = False

        self.setFixedHeight(24)
        self.setAttribute(QtCore.Qt.WA_Hover)
        
        self._line_edit = QtWidgets.QLineEdit(self)
        self._line_edit.setStyleSheet("background: transparent; border: none; color: white;")
        self._line_edit.setFont(QtGui.QFont("Segoe UI", 10))
        self._line_edit.setAttribute(QtCore.Qt.WA_Hover)
        self._line_edit.installEventFilter(self)

        self._search_btn = QtWidgets.QToolButton(self)
        self._search_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self._search_btn.setIcon(QtGui.QIcon(resourceLoader.getIconPath("magnifying_glass_64x64.png")))
        self._search_btn.setFixedWidth(self.BUTTON_WIDTH)
        self._search_btn.setObjectName("PLSearchGlassButton")
        self._search_btn.setStyleSheet("""
            QToolButton#PLSearchGlassButton {
                background-color: transparent;
                border: none;
                color: white;
                margin-left: 8px;
            }
        """)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(0)
        layout.addWidget(self._line_edit)
        layout.addWidget(self._search_btn)

    def __getattr__(self, name):
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

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)
        radius = self._radius
        btn_width = self._search_btn.width()

        left_rect = QtCore.QRectF(rect.x(), rect.y(), rect.width() - btn_width, rect.height())
        painter.setBrush(self._bgColor)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(left_rect, radius, radius)

        clip_rect = QtCore.QRectF(rect.right() - btn_width, rect.y(), btn_width, rect.height())
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(path)

        painter.setBrush(self._bgColorRight)
        painter.drawRect(clip_rect)

        painter.setClipping(False)

        border_color = self._focusBorderColor if self._hasFocus else self._borderColor
        painter.setPen(QtGui.QPen(border_color, 1.5))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)

    def mousePressEvent(self, event):
        self._line_edit.setFocus()
        super().mousePressEvent(event)

    # === Style & Property Interface ===

    @QtCore.Property(QtGui.QColor)
    def backgroundColor(self):
        return self._bgColor

    @backgroundColor.setter
    def backgroundColor(self, color: QtGui.QColor):
        self._bgColor = color
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
        self._textColor = color
        self._line_edit.setStyleSheet(
            f"background: transparent; border: none; color: {color.name()};"
        )
        self.update()
