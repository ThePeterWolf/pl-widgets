# plwidgets

**plwidgets** is a custom widget library built on top of PySide6, offering modern UI components like sliders, toggles, progress indicators, and more — designed to give your PyQt/PySide apps a polished look.

---

## 🖼 UI Preview

![Demo interface](assets/preview.png)

---

## 📦 Installation

This package is not yet available on PyPI.
You can clone this repository and add it to your PYTHONPATH manually.

> Note: You must have `PySide6` installed. If not:

```bash
pip install PySide6
```

---

## 🧩 Available Widgets

| Widget | Description |
|--------|-------------|
| `PlCheckBox` | Custom checkbox with styling. |
| `PlCheckButtonGroup` | Group of toggle buttons (single or multi-select). |
| `PlComboBox` | Styled dropdown selector. |
| `PlDialog` | Base dialog window container. |
| `PlFlag` | Titled content container with a styled header. |
| `PlFormWidget` | Labeled horizontal layout for form elements. |
| `PlLineEdit` | Styled single-line text input. |
| `PlLoadingIndicator` | Animated loading spinner. |
| `PlOverlayDialog` | Modal overlay popup with blur or dimming. |
| `PlProgressCircle` | Circular progress indicator with text. |
| `PlPushButton` | Custom push button with hover and press effects. |
| `PlRoundCheckButton` | Rounded toggle button (styled checkbox). |
| `PlSearchBar` | Input with icon for search actions. |
| `PlSlider` | Custom horizontal slider. |
| `PlTabWidget` | Custom tab navigation with painted tabs. |

---

## 🧪 Quick Example

```python
from PySide6 import QtWidgets
from plwidgets import PLSlider, PlCheckBox, PlDialog

app = QtWidgets.QApplication([])

window = PlDialog()
layout = QtWidgets.QVBoxLayout(window)

slider = PLSlider()
slider.enableStep(10)

toggle = PlCheckBox()
toggle.setChecked(True)

layout.addWidget(slider)
layout.addWidget(toggle)

window.show()
app.exec()
```

---

## 🎨 Styling with QSS

All widgets support custom styles using Qt Style Sheets (QSS):

```css
PLSlider {
    background-color: #cccccc;
    thumb-color: #3498db;
}

PlCheckBox {
    handle-color: #ffffff;
    background-color: #888888;
}
```

---
## 📚 API Reference

See the [docs (WIP!)](./docs/README.md) for detailed information on each widget.

---

## 📄 License

MIT License © Pierre-Lou Guilloré

