from PySide6 import QtWidgets, QtCore, QtGui
from .pl_style_mixin import PlStyleMixin
from .resource_utils import resourceLoader


class PlTitleBar(QtWidgets.QWidget):

    titleBarHeight = 36

    def __init__(self, parent=None):
        super().__init__(parent)
        self._mouse_offset = None
        self._titleBarColor = QtGui.QColor("#24272e")
        self._title = "New Dialog"

        self.setFixedHeight(self.titleBarHeight)
        self.setMinimumWidth(350)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(10, 0, 0, 0)
        self._layout.setSpacing(0)

        # Left area (menu zone)
        self.menuArea = QtWidgets.QHBoxLayout()
        self.menuArea.setSpacing(4)
        self.menuArea.setContentsMargins(0, 0, 0, 0)
        self._layout.addLayout(self.menuArea)

        self._layout.addStretch()

        # Window control buttons
        self.minimizeButton = QtWidgets.QToolButton()
        self.minimizeButton.setIcon(QtGui.QIcon(resourceLoader.getIconPath("reduce_bar_128x128.png")))
        self.maximizeButton = QtWidgets.QToolButton()
        self.maximizeButton.setIcon(QtGui.QIcon(resourceLoader.getIconPath("maximize_128x128.png")))

        [btn.setObjectName("PLtitleBarButton") for btn in [self.minimizeButton, self.maximizeButton]]
        self.closeButton = QtWidgets.QToolButton()
        self.closeButton.setIcon(QtGui.QIcon(resourceLoader.getIconPath("close_cross_128x128.png")))
        self.closeButton.setObjectName("PLtitleBarCloseButton")

        buttonWidth = self.titleBarHeight + self.titleBarHeight/3

        for btn in [self.minimizeButton, self.maximizeButton, self.closeButton]:
            btn.setFixedSize(buttonWidth, self.titleBarHeight)
            btn.setStyleSheet("""
                QToolButton#PLtitleBarButton {
                    color: white;
                    background-color: transparent;
                    border: none;
                }
                QToolButton#PLtitleBarButton:hover {
                    color: white;
                    background-color: rgba(200, 200, 200, 20);
                }
                QToolButton#PLtitleBarCloseButton {
                    color: white;
                    background-color: transparent;
                    border: none;
                }
                QToolButton#PLtitleBarCloseButton:hover {
                    color: white;
                    background-color: rgba(200, 50, 50, 200);
                }
            """)
            self._layout.addWidget(btn)

        self.closeButton.clicked.connect(self.parent().close)
        self.minimizeButton.clicked.connect(self.parent().showMinimized)
        self.maximizeButton.clicked.connect(self._toggle_maximize)

    def _toggle_maximize(self):
        win = self.parent()
        if win.isMaximized():
            win.showNormal()
        else:
            win.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._mouse_offset = event.globalPosition().toPoint() - self.parent().frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._mouse_offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.parent().move(event.globalPosition().toPoint() - self._mouse_offset)

    def mouseReleaseEvent(self, event):
        self._mouse_offset = None

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Draw background
        color = self.property("titleBarColor") or self._titleBarColor
        painter.fillRect(self.rect(), color)

        # Draw centered title
        painter.setPen(QtGui.QColor("white"))
        font = painter.font()
        font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(self.rect(), QtCore.Qt.AlignCenter, self._title)

    @QtCore.Property(QtGui.QColor)
    def titleBarColor(self):
        return self._titleBarColor

    @titleBarColor.setter
    def titleBarColor(self, color: QtGui.QColor):
        self._titleBarColor = color
        self.update()

    @QtCore.Property(str)
    def title(self):
        return self._title

    @title.setter
    def title(self, text: str):
        self._title = text
        self.update()
