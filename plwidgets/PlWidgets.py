# PlWidgets.py

from .pl_checkbox import PlCheckBox
from .pl_progress_circle import PlProgressCircle
from .pl_dialog import PlDialog
from .pl_title_bar import PlTitleBar
from .pl_line_edit import PlLineEdit
from .pl_search_bar import PlSearchBar
from .pl_push_button import PlPushButton
from .pl_combo_box import PlComboBox
from .pl_flag import PlFlag
from .pl_slider import PLSlider
from .pl_loading_indicator import PlLoadingIndicator
from .pl_form_widget import PlFormWidget
from .pl_check_button_group import PlCheckButtonGroup
from .pl_round_check_button import PlRoundCheckButton
from .pl_overlay_dialog import PlOverlayDialog
from .pl_tab_widget import PlTabWidget
from typing import Type


class PlWidgets:
    """
    Unified access point for all custom widgets in the plui package.
    """

    PlCheckBox: Type[PlCheckBox] = PlCheckBox
    PlProgressCircle: Type[PlProgressCircle] = PlProgressCircle
    PlDialog: Type[PlDialog] = PlDialog
    PlTitleBar: Type[PlTitleBar] = PlTitleBar
    PlLineEdit: Type[PlLineEdit] = PlLineEdit
    PlSearchBar: Type[PlSearchBar] = PlSearchBar
    PlPushButton: Type[PlPushButton] = PlPushButton
    PlComboBox: Type[PlComboBox] = PlComboBox
    PlFlag: Type[PlFlag] = PlFlag
    PLSlider: Type[PLSlider] = PLSlider
    PlLoadingIndicator: Type[PlLoadingIndicator] = PlLoadingIndicator
    PlFormWidget: Type[PlFormWidget] = PlFormWidget
    PlCheckButtonGroup: Type[PlCheckButtonGroup] = PlCheckButtonGroup
    PlRoundCheckButton: Type[PlRoundCheckButton] = PlRoundCheckButton
    PlOverlayDialog: Type[PlOverlayDialog] = PlOverlayDialog
    PlTabWidget: Type[PlTabWidget] = PlTabWidget

