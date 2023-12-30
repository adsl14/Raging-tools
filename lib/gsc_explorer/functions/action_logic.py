from lib.packages import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from lib.gsc_explorer.GSCEV import GSCEV


def on_map_changed(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[0].pointers_data[0].value_GSDT = main_window.map_name_value.currentIndex()


def on_music_changed(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[0].pointers_data[1].value_GSDT = main_window.music_value.value()


def on_num_characters_changed(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[1].pointers_data[7].value_GSDT = main_window.num_characters_value.value()


def on_character_id_changed(main_window):

    # Get gsac_3
    gsac_3 = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3]

    # Skin
    main_window.skin_value.setValue(gsac_3.data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[3].value_GSDT)
    # Battle damaged
    main_window.damaged_costume.setChecked(gsac_3.data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[4].value_GSDT)
    # Health
    main_window.gsc_health_value.setValue(gsac_3.data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[7].value_GSDT)
    # Character
    main_window.char_id_value.setPixmap(QPixmap(os.path.join(GSCEV.path_slot_small_images, "sc_chara_s_" + str(gsac_3.data.pointers[3 + (2 * main_window.character_value.value())]
                                                                                                               .pointers_data[2].value_GSDT).zfill(3) + ".png")))
    # Blast attacks
    value_gsdt = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[4 + (2 * main_window.character_value.value())].pointers_data[1].value_GSDT
    main_window.ico_boost_stick_r_up_value_2.setCurrentIndex(value_gsdt + 1 if value_gsdt != 4294967295 else 0)
    value_gsdt = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[4 + (2 * main_window.character_value.value())].pointers_data[2].value_GSDT
    main_window.ico_boost_stick_r_d_value_2.setCurrentIndex(value_gsdt + 1 if value_gsdt != 4294967295 else 0)
    value_gsdt = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[4 + (2 * main_window.character_value.value())].pointers_data[3].value_GSDT
    main_window.ico_boost_stick_r_l_value_2.setCurrentIndex(value_gsdt + 1 if value_gsdt != 4294967295 else 0)
    value_gsdt = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[4 + (2 * main_window.character_value.value())].pointers_data[4].value_GSDT
    main_window.ico_boost_stick_r_r_value_2.setCurrentIndex(value_gsdt + 1 if value_gsdt != 4294967295 else 0)
    value_gsdt = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[4 + (2 * main_window.character_value.value())].pointers_data[5].value_GSDT
    main_window.ico_boost_stick_r_push_value_2.setCurrentIndex(value_gsdt + 1 if value_gsdt != 4294967295 else 0)


def on_skin_changed(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[3].value_GSDT = main_window.skin_value.value()


def on_damaged_costume(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[4].value_GSDT = int(main_window.damaged_costume.isChecked()
                                                                                                                                                        is True)


def on_gsc_health_value_changed(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[7].value_GSDT = main_window.gsc_health_value.value()


def on_ico_boost_stick_value_changed(main_window, stick_number):

    # Check the stick number the user has selected
    # Up
    if stick_number == 1:
        combobox_index = main_window.ico_boost_stick_r_up_value_2.currentIndex()
    # Down
    elif stick_number == 2:
        combobox_index = main_window.ico_boost_stick_r_d_value_2.currentIndex()
    # Left
    elif stick_number == 3:
        combobox_index = main_window.ico_boost_stick_r_l_value_2.currentIndex()
    # Right
    elif stick_number == 4:
        combobox_index = main_window.ico_boost_stick_r_r_value_2.currentIndex()
    else:
        combobox_index = main_window.ico_boost_stick_r_push_value_2.currentIndex()

    # If there is no blast attack selected, we assign -1 to the edited pointer
    if combobox_index == 0:
        value = 4294967295
    # If there is a blast attack selected, we convert the index from combobox, to the value for gsdt
    else:
        value = combobox_index - 1

    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[4 + (2 * main_window.character_value.value())].pointers_data[stick_number].value_GSDT = value


def on_text_id_changed(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[4].data.pointers[1 + main_window.pointer_subtitle_list_view.currentIndex().row()].pointers_data[2].value_GSDT = main_window.text_id_value.value()


def on_cutscene_changed(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[4].data.pointers[1 + main_window.pointer_subtitle_list_view.currentIndex().row()].pointers_data[1].value_GSDT = int(main_window.
                                                                                                                                                                          subtitle_in_cutscene.
                                                                                                                                                                          isChecked() is False)


def on_pointer_subtitle_list_view_changed(main_window):

    # Get the current subtitle instruction
    index = main_window.pointer_subtitle_list_view.currentIndex().row()

    # Disconnect signals
    try:
        main_window.text_id_value.valueChanged.disconnect()
        main_window.subtitle_in_cutscene.toggled.disconnect()
    except TypeError:
        pass

    # Set text id value
    main_window.text_id_value.setValue(GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[4].data.pointers[1 + index].pointers_data[2].value_GSDT)
    # Subtitle in cutscene
    main_window.subtitle_in_cutscene.setChecked(not GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[4].data.pointers[1 + index].pointers_data[1].value_GSDT)
    # Char name text
    main_window.char_id_subtitle_value.setPixmap(QPixmap(os.path.join(GSCEV.path_slot_small_images, "sc_chara_s_" + str(GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[4].
                                                                                                                        data.pointers[1 + index].pointers_data[3].value_GSDT).zfill(3) + ".png")))

    # Connect signals
    main_window.text_id_value.valueChanged.connect(lambda: on_text_id_changed(main_window))
    main_window.subtitle_in_cutscene.toggled.connect(lambda: on_cutscene_changed(main_window))


def action_change_character(event, main_window, option):

    # Get the current character
    # Chara ID for stage properties
    if option == 0:
        char_id = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[2].value_GSDT
    # Chara ID for subtitle properties
    else:
        char_id = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[4].data.pointers[1 + main_window.pointer_subtitle_list_view.currentIndex().row()].pointers_data[3].value_GSDT

    # Check if the current character is the same as the selected in the window, so we can clean the window
    if GSCEV.old_chara != char_id:

        # Restore the color of the old selected character
        select_chara_roster_window_label = main_window.selectCharaGscUI.frame.findChild(QLabel, "label_" + str(GSCEV.old_chara))
        select_chara_roster_window_label.setStyleSheet(GSCEV.styleSheetSelectCharaGscBlackWindow)

        # Store the current character
        GSCEV.old_chara = char_id

    # Change color for the selected character in chara roster window
    select_chara_roster_window_label = main_window.selectCharaGscUI.frame.findChild(QLabel, "label_" + str(char_id))
    select_chara_roster_window_label.setStyleSheet(GSCEV.styleSheetSelectCharaGscCyanWindow)

    # Set the option selected
    GSCEV.char_id_option_selected = option

    # Show the select chara roster window
    main_window.selectCharaGscWindow.show()


def action_modify_character(event, main_window, chara_id):

    # Check the option selected
    if GSCEV.char_id_option_selected == 0:
        # Change character id
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[2].value_GSDT = chara_id

        # Change character image
        main_window.char_id_value.setPixmap(QPixmap(os.path.join(GSCEV.path_slot_small_images, "sc_chara_s_" + str(chara_id).zfill(3) + ".png")))

    else:
        # Change character id
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[4].data.pointers[1 + main_window.pointer_subtitle_list_view.currentIndex().row()].pointers_data[3].value_GSDT = chara_id

        # Change character image
        main_window.char_id_subtitle_value.setPixmap(QPixmap(os.path.join(GSCEV.path_slot_small_images, "sc_chara_s_" + str(chara_id).zfill(3) + ".png")))

    # Close Window
    main_window.selectCharaGscWindow.close()
