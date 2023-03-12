import os

from PyQt5.QtGui import QPixmap

from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.REV import REV


def initialize_current_character_image_RE(main_window):

    main_window.portrait_2.setPixmap(QPixmap(""))
    for i in range(0, REV.num_slots_characters):
        slot = REV.slots_characters[i]
        slot.reset()
    for i in range(0, REV.num_slots_transformations):
        slot = REV.slots_transformations[i]
        slot.reset()
        slot.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_101.bmp")))


def delete_image_slot_RE(slot_character):
    slot_character.qlabel_object.setStyleSheet("QLabel {}")
    slot_character.qlabel_object.mousePressEvent = None


def change_image_slot_RE(slot_character, image_name):
    slot_character.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, image_name)))


def enable_tabs_RE(main_window):

    # Open the tab (character parameters editor)
    if main_window.tabWidget.currentIndex() != 2:
        main_window.tabWidget.setCurrentIndex(2)

    # Open the tab operate_character_XXX_m
    if main_window.tabWidget_2.currentIndex() != 2:
        main_window.tabWidget_2.setCurrentIndex(2)

    # Enable completely the tab character parameters editor
    if not main_window.character_parameters_editor.isEnabled():
        main_window.character_parameters_editor.setEnabled(True)

    # Disable all the buttons (character parameters editor -> operate_resident_param)
    if main_window.operate_resident_param_frame.isEnabled():
        main_window.operate_resident_param_frame.setEnabled(False)
    # Disable all the buttons (character parameters editor -> operate_character_XXX_m)
    if main_window.operate_character_xyz_m_frame.isEnabled():
        main_window.operate_character_xyz_m_frame.setEnabled(False)
    # Disable all the buttons (character parameters editor -> cs_chip)
    if not main_window.cs_chip.isEnabled():
        main_window.cs_chip.setEnabled(True)
