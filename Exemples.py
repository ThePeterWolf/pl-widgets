#Code Exemple
import sys
from PySide6 import QtWidgets, QtCore
from plwidgets import PlWidgets


window = PlWidgets.PlDialog()
window.setTitle("Exemple UI")
layout = QtWidgets.QVBoxLayout()
window.setLayout(layout)

check = PlWidgets.PlCheckBox()
check.setFixedSize(QtCore.QSize(40, 20))

combo = PlWidgets.PlComboBox()
combo.addItems(["Option A", "Option B", "Option C"])

flag = PlWidgets.PLFlag()

slider = PlWidgets.PLSlider()

lineedit = PlWidgets.PlLineEdit()

search = PlWidgets.PlSearchBar()

load = PlWidgets.PlLoadingIndicator()

btn = PlWidgets.PlPushButton("Nice Button")

layout.addWidget(check)
layout.addWidget(combo)
layout.addWidget(lineedit)
layout.addWidget(search)
layout.addWidget(btn)
layout.addWidget(flag)
layout.addWidget(slider)
layout.addWidget(load)


app = QtWidgets.QApplication(sys.argv)
window.show()
sys.exit(app.exec())
