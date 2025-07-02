# plwidgets

**plwidgets** is a custom widget library built on top of PySide6, offering modern UI components like sliders, toggles, progress indicators, and more — designed to give your PyQt/PySide apps a polished look.

---

## 📦 Installation

```bash
pip install plwidgets
```

> Note: You must have `PySide6` installed. If not:

```bash
pip install PySide6
```

---

## 🧩 Available Widgets

| Widget Name         | Description                                 |
|---------------------|---------------------------------------------|
| `PLSlider`          | Custom slider with circular thumb and step support |
| `PlCheckBox`        | Animated toggle switch (on/off)             |
| `PlLoadingIndicator`| Spinning loader to indicate async tasks     |
| `PlVideoPlayer`     | (WIP) Widget to play video files            |
| `PlProgressCircle`  | Circular progress bar                       |
| `PlPushButton`      | Styled button                               |
| `PlComboBox`        | Dropdown with custom style                  |
| `PlLineEdit`        | Custom input field                          |
| `PlSearchBar`       | Input field with search icon                |

---

## 🧪 Quick Example

```python
from PySide6 import QtWidgets
from plwidgets import PLSlider, PlCheckBox

app = QtWidgets.QApplication([])

window = QtWidgets.QWidget()
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
    handleColor: #ffffff;
    backgroundColor: #888888;
}
```

---

## 🚀 Publishing

To release to PyPI:

```bash
python -m build
python -m twine upload dist/*
```

Or push a Git tag like `v0.1.0` to trigger GitHub Actions if configured.

---

## 📄 License

MIT License © Pierre-Lou Guilloré
