from PySide6 import QtWidgets, QtCore, QtGui
from .resource_utils import resourceLoader


class CenterWidget(QtWidgets.QWidget):

    closed = QtCore.Signal()

    def __init__(self, title="NewDialog", parent=None):
        super().__init__(parent)

        self._title = title
        self._cross_hover = False
        self._topColor = QtGui.QColor("#2c2f33")
        self._bottomColor = QtGui.QColor("#1f2227")
        self._borderColor = QtGui.QColor("#44484d")
        self._radius = 4

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMinimumSize(300, 200)

        # Load the pixmap (replace this path as needed)
        self._cross_pixmap = QtGui.QPixmap(resourceLoader.getIconPath("close_cross_128x128.png"))
        self._cross_size = 12
        self._cross_margin = 8
        self._cross_rect = QtCore.QRect()  # placeholder for interaction

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect()
        width = rect.width()
        height = rect.height()
        radius = self._radius
        header_height = min(24, height)

        # Header arrondi
        top_path = QtGui.QPainterPath()
        top_path.moveTo(0, header_height)
        top_path.lineTo(0, radius)
        top_path.quadTo(0, 0, radius, 0)
        top_path.lineTo(width - radius, 0)
        top_path.quadTo(width, 0, width, radius)
        top_path.lineTo(width, header_height)
        top_path.closeSubpath()

        painter.setBrush(self._topColor)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawPath(top_path)

        # Fond du corps
        body_rect = QtCore.QRect(0, header_height, width, height - header_height)
        painter.setBrush(self._bottomColor)
        painter.drawRect(body_rect)

        # Bordure
        pen = QtGui.QPen(self._borderColor)
        pen.setWidth(1)
        painter.setPen(pen)
        border_rect = rect.adjusted(1, 1, -1, -1)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRoundedRect(border_rect, radius, radius)

        # Titre centré
        painter.setPen(QtGui.QColor("white"))
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)

        text_rect = QtCore.QRectF(0, 0, width, header_height)
        painter.drawText(text_rect, QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter, self._title)

        # --- Icône de fermeture ---
        cross_rect = QtCore.QRect(
            width - self._cross_size - self._cross_margin,
            (header_height - self._cross_size) // 2,
            self._cross_size,
            self._cross_size
        )
        self._cross_rect = cross_rect  # Pour gestion de clic ultérieure

        if not self._cross_pixmap.isNull():
            painter.drawPixmap(
                cross_rect,
                self._cross_pixmap.scaled(
                    self._cross_size,
                    self._cross_size,
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation
                )
            )

    def mouseReleaseEvent(self, event):
        if hasattr(self, "_cross_rect") and self._cross_rect.contains(event.pos()):
            self.closed.emit()


class PlOverlayDialog(QtWidgets.QWidget):
    def __init__(self, parent, title="NewDialog"):
        super().__init__(parent)
        self._parent = parent

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._parent.installEventFilter(self)

        self.setGeometry(self._parent.contentGeometry())

        # Layout principal de l'overlay
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # Widget central
        self.center_widget = CenterWidget(title=title, parent=self)
        self.center_widget.closed.connect(self._on_center_widget_closed)
        layout.addWidget(self.center_widget)
    
    def _on_center_widget_closed(self):
        self.close()

    def eventFilter(self, obj, event):
        if obj == self._parent and event.type() in [QtCore.QEvent.Resize, QtCore.QEvent.Move]:
            self.setGeometry(self._parent.contentGeometry())
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 160))

    def setLayout(self, layout):
        return self.center_widget.setLayout(layout)

    def layout(self):
        return self.center_widget.layout()

    def addWidget(self, widget):
        lay = self.center_widget.layout()
        if lay is not None:
            lay.addWidget(widget)
        else:
            raise RuntimeError("Le center_widget n'a pas de layout défini.")

    def setFixedSize(self, w, h=None):
        if h is None:
            return self.center_widget.setFixedSize(w)
        return self.center_widget.setFixedSize(w, h)

    def setStyleSheet(self, style):
        return self.center_widget.setStyleSheet(style)
