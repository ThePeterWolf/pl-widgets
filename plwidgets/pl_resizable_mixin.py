from PySide6 import QtCore, QtGui


class PlResizableMixin:
    _resize_margin = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._resizing = False
        self._resize_direction = None
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._resize_direction = self._get_resize_edge(event.pos())
            if self._resize_direction:
                self._resizing = True
                self._mouse_start_pos = event.globalPosition().toPoint()
                self._start_geometry = self.geometry()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._resizing and self._resize_direction:
            diff = event.globalPosition().toPoint() - self._mouse_start_pos
            rect = QtCore.QRect(self._start_geometry)

            if "left" in self._resize_direction:
                rect.setLeft(rect.left() + diff.x())
            if "right" in self._resize_direction:
                rect.setRight(rect.right() + diff.x())
            if "top" in self._resize_direction:
                rect.setTop(rect.top() + diff.y())
            if "bottom" in self._resize_direction:
                rect.setBottom(rect.bottom() + diff.y())

            self.setGeometry(rect)
        else:
            
            edge = self._get_resize_edge(event.pos())
            cursor_map = {
                "left": QtCore.Qt.SizeHorCursor,
                "right": QtCore.Qt.SizeHorCursor,
                "top": QtCore.Qt.SizeVerCursor,
                "bottom": QtCore.Qt.SizeVerCursor,
                "top-left": QtCore.Qt.SizeFDiagCursor,
                "top-right": QtCore.Qt.SizeBDiagCursor,
                "bottom-left": QtCore.Qt.SizeBDiagCursor,
                "bottom-right": QtCore.Qt.SizeFDiagCursor,
            }
            self.setCursor(cursor_map.get(edge, QtCore.Qt.ArrowCursor))

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._resize_direction = None
        super().mouseReleaseEvent(event)

    def _get_resize_edge(self, pos):
        rect = self.rect()
        margin = self._resize_margin
        left = pos.x() <= margin
        right = pos.x() >= rect.width() - margin
        top = pos.y() <= margin
        bottom = pos.y() >= rect.height() - margin

        if top and left:
            return "top-left"
        if top and right:
            return "top-right"
        if bottom and left:
            return "bottom-left"
        if bottom and right:
            return "bottom-right"
        if left:
            return "left"
        if right:
            return "right"
        if top:
            return "top"
        if bottom:
            return "bottom"
        return None
