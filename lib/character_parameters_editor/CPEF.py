from lib.character_parameters_editor.REF import initialize_cs_chip
from lib.character_parameters_editor.IPF import initialize_operate_character
from lib.character_parameters_editor.GPF import initialize_operate_resident_param


def initialize_cpe(main_window, qt_widgets):

    initialize_operate_resident_param(main_window, qt_widgets)

    initialize_operate_character(main_window, qt_widgets)

    initialize_cs_chip(main_window, qt_widgets)

    # Disable character parameters editor tab
    main_window.character_parameters_editor.setEnabled(False)
