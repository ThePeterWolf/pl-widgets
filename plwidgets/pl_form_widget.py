"""
PlFormWidget - A labeled horizontal layout container for PySide6.

Provides a horizontal layout with a customizable label and optional stretch,
designed to pair well with custom input widgets like PlCheckBox.

Author: Pierre-Lou Guilloré
License: MIT
"""

from PySide6 import QtWidgets, QtCore, QtGui
from .pl_style_mixin import PlStyleMixin


class PlFormWidget(PlStyleMixin, QtWidgets.QWidget):
    """
    A reusable form field widget with a label and content widget.

    Properties:
        title (str): The label text.
        squash (bool): Whether to add stretch after the widget.
        labelColor (QColor): The color of the label text.
    """

    def __init__(self, label: str = "Title", widget: QtWidgets.QWidget=None, squash=True, parent: QtWidgets.QWidget = None) -> None:
        """
        Initialize the PlFormWidget.

        Args:
            label (str): The text to display as label.
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self._title = label
        self._squash = squash
        self._widget = None
        self._stretch_item = None

        self._init_ui()

        if widget is not None:
            self.setWidget(widget)

    def _init_ui(self) -> None:
        self.setContentsMargins(0, 0, 0, 0)
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(10)

        self._label_widget = QtWidgets.QLabel(self._title)
        self._label_widget.setFont(QtGui.QFont("Segoe UI", 10))
        self._label_widget.setStyleSheet("color: #fefefe;")
        self._layout.addWidget(self._label_widget)

    def _apply_widget(self) -> None:
        if self._widget:
            self._layout.addWidget(self._widget)
        if self._squash:
            self._add_stretch()

    def _remove_widget(self) -> None:
        if self._widget:
            self._layout.removeWidget(self._widget)
            self._widget.setParent(None)
            self._widget = None
        self._remove_stretch()

    def _add_stretch(self) -> None:
        if not self._stretch_item:
            self._stretch_item = QtWidgets.QSpacerItem(
                0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
            )
            self._layout.addItem(self._stretch_item)

    def _remove_stretch(self) -> None:
        if self._stretch_item:
            self._layout.removeItem(self._stretch_item)
            self._stretch_item = None

    def setWidget(self, widget: QtWidgets.QWidget) -> None:
        """
        Sets the content widget. Replaces the existing one if needed.

        Args:
            widget (QWidget): The widget to embed.
        """
        if not isinstance(widget, QtWidgets.QWidget):
            raise TypeError("setWidget expects a QWidget.")
        self._remove_widget()
        self._widget = widget
        self._apply_widget()

    def setSquash(self, squash: bool) -> None:
        """
        Enables or disables the layout squash (stretch after widget).

        Args:
            squash (bool): Whether to squash. Default is False.
        """
        if self._squash != squash:
            self._squash = squash
            self._remove_stretch()
            if self._widget and self._squash:
                self._add_stretch()

    def setTitle(self, title: str = "Title") -> None:
        """
        Sets the label title.

        Args:
            title (str): The label text.
        """
        self._title = title
        self._label_widget.setText(title)

    def setLabelColor(self, color: QtGui.QColor) -> None:
        """
        Sets the label text color.

        Args:
            color (QColor): The text color.
        """
        self._label_widget.setStyleSheet(f"color: {color.name()};")

    @QtCore.Property(str)
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self.setTitle(value)

    @QtCore.Property(bool)
    def squash(self) -> bool:
        return self._squash

    @squash.setter
    def squash(self, value: bool) -> None:
        self.setSquash(value)

    @QtCore.Property(QtGui.QColor)
    def labelColor(self) -> QtGui.QColor:
        return self._label_widget.palette().color(QtGui.QPalette.WindowText)

    @labelColor.setter
    def labelColor(self, color: QtGui.QColor) -> None:
        self.setLabelColor(color)
