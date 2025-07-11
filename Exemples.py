import sys
from PySide6 import QtWidgets, QtCore, QtGui
from plwidgets import PlWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)

    # === Button callbacks ===
    def increase_progress():
        progress.incrementValue(5)

    def reset_progress():
        progress.setValue(0)

    def show_overlay():
        overlay.show()

    # === Main Window ===
    window = PlWidgets.PlDialog()
    window.setTitle("Hunter UI")
    layout = QtWidgets.QVBoxLayout()
    window.setLayout(layout)

    # === Check Button Group ===
    button_group = PlWidgets.PlCheckButtonGroup()
    button_group.addButton("Tutu", "tutu")
    button_group.addButton("Toto", "toto")
    button_group.addButton("Tata", "tata")
    button_group.setChecked("tutu", True)
    button_group.setSelectionMode(PlWidgets.PlCheckButtonGroup.selectionModeSingleForce)

    # === Round Check Button ===
    round_chk = PlWidgets.PlRoundCheckButton("Check")
    round_chk.setFixedSize(100, 40)  

    # === Flag with form content ===
    flag = PlWidgets.PlFlag("Flag Name")
    flag.setLabelAlignment(QtCore.Qt.AlignLeft)
    flag_content_layout = QtWidgets.QVBoxLayout()

    check01 = PlWidgets.PlCheckBox()
    check01.setFixedSize(40, 20)
    form01 = PlWidgets.PlFormWidget("Checkbox title", widget=check01, squash=True)
    form01.setLabelColor(QtGui.QColor("#7a7a7a"))

    check02 = PlWidgets.PlCheckBox()
    check02.setFixedSize(40, 20)
    form02 = PlWidgets.PlFormWidget("Checkbox title", widget=check02, squash=True)
    form02.setLabelColor(QtGui.QColor("#7a7a7a"))

    flag_content_layout.addWidget(form01)
    flag_content_layout.addWidget(form02)
    flag.setLayout(flag_content_layout)

    # === Empty Flag Example ===
    flag1 = PlWidgets.PlFlag("Flag Name")

    # === Tab Widget with content ===
    tab_widget = QtWidgets.QWidget()
    tab_layout = QtWidgets.QVBoxLayout(tab_widget)

    combo = PlWidgets.PlComboBox()
    combo.addItems(["Option A", "Option B", "Option C"])

    tab_layout.addWidget(combo)
    tab_layout.addWidget(PlWidgets.PlCheckBox())
    tab_layout.addWidget(PlWidgets.PlLineEdit())

    tabs = PlWidgets.PlTabWidget()
    tabs.addTab("Tab 01", tab_widget)
    tabs.addTab("Tab 02")
    tabs.addTab("Tab 03")

    # === Circular Progress ===
    progress = PlWidgets.PlProgressCircle()
    progress.setFixedSize(50, 50)
    progress.setStyleSheet("""
        PlProgressCircle {
            progress-color: #f39c12;
            complete_color: #27ae60;
            background-color: #2f3640;
            text-color: #44484d;
            line-width: 8;
            text-visible: true;
            text_size: 8;
        }
    """)

    progress_btn = PlWidgets.PlPushButton("Increase")
    progress_btn.clicked.connect(increase_progress)

    progress_reset_btn = PlWidgets.PlPushButton("Reset")
    progress_reset_btn.clicked.connect(reset_progress)

    # === Slider ===
    slider = PlWidgets.PLSlider()
    slider.enableStep(10)

    # === Search Bar ===
    search = PlWidgets.PlSearchBar()

    # === Overlay Button ===
    btn_overlay = PlWidgets.PlPushButton("Overlay Popup")
    btn_overlay.clicked.connect(show_overlay)

    # === Overlay Dialog ===
    overlay = PlWidgets.PlOverlayDialog(window)

    # === Loading Indicator ===
    load = PlWidgets.PlLoadingIndicator()

    # === Assemble main layout ===
    layout.addWidget(search)
    layout.addWidget(btn_overlay)
    layout.addWidget(button_group)
    layout.addWidget(round_chk)
    layout.addWidget(flag1)
    layout.addWidget(flag)
    layout.addWidget(tabs)
    layout.addWidget(slider)
    layout.addWidget(progress)
    layout.addWidget(progress_btn)
    layout.addWidget(progress_reset_btn)
    layout.addWidget(load)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
