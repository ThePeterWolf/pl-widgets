#Code Exemple
import sys
from PySide6 import QtWidgets, QtCore
import time

sys.path.append(r"D:\01_PROJECTS\01_PLUI")

from plui import PlWidgets


import sys

app = QtWidgets.QApplication(sys.argv)

# Load stylesheet
try:
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
except FileNotFoundError:
    pass

def increase():
    circle.incrementValue(5)

def print_text():
    check01.setChecked(False)

window = PlWidgets.PlDialog()
window.setTitle("Hunter UI")
layout = QtWidgets.QVBoxLayout()
window.setLayout(layout)

circle = PlWidgets.PlProgressCircle()

check01 = PlWidgets.PlCheckBox()
check02 = PlWidgets.PlCheckBox()

check01.setFixedSize(QtCore.QSize(40, 20))
check02.setFixedSize(QtCore.QSize(40, 20))

combo = PlWidgets.PlComboBox()
combo.addItems(["Option A", "Option B", "Option C"])

flag = PlWidgets.PLFlag()

slider = PlWidgets.PLSlider()
slider.enableStep(10)

player = PlWidgets.PLVideoPlayer()
player.resize(800, 600)
player.show()

lineedit = PlWidgets.PlLineEdit()

search = PlWidgets.PlSearchBar()

load = PlWidgets.PlLoadingIndicator()

style = """
    PlProgressCircle {
        progress-color: #f39c12;
        complete_color: #27ae60;
        background-color: #2f3640;
        text-color: #2c3e50;
        line-width: 14;
        text-visible: false;
        text_size: 14;
    }
"""

circle.setStyleSheet(style)

btn = PlWidgets.PlPushButton("Nice Button")
btn.clicked.connect(print_text)

# layout.addWidget(circle)

layout.addWidget(check01)
layout.addWidget(check02)

layout.addWidget(combo)


layout.addWidget(lineedit)
layout.addWidget(search)

layout.addWidget(btn)

layout.addWidget(flag)

layout.addWidget(slider)

layout.addWidget(load)

# layout.addWidget(player)

# layout.addStretch()
window.show()
sys.exit(app.exec())
