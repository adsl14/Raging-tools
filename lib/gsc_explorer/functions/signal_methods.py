from lib.packages import os

from PyQt5.QtGui import QPixmap, QStandardItem

from lib.gsc_explorer.GSCEV import GSCEV


def store_parameters_gsc_explorer(main_window):

    # --------
    # Definitions (GSAC0)
    # --------
    gsac_0 = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[0]
    # Initial gsac event to load
    main_window.initial_gsac_event_value.setValue(int.from_bytes(gsac_0.data.pointers[0].secundary_number_of_pointers.to_bytes(1, 'little') + gsac_0.data.pointers[0].unk0x04, "little"))


    # --------
    # Stage properties (GSAC3)
    # --------
    gsac_3 = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3]
    # Map value
    main_window.map_name_value.setCurrentIndex(gsac_3.data.pointers[0].pointers_data[0].value_GSDT)
    # Music value
    main_window.music_value.setValue(gsac_3.data.pointers[0].pointers_data[1].value_GSDT)

    # Character slot as p1
    main_window.player_character_value.setValue(gsac_3.data.pointers[1].pointers_data[1].value_GSDT)
    # Character slot as cpu
    main_window.cpu_character_value.setValue(gsac_3.data.pointers[1].pointers_data[7].value_GSDT)

    # Character (store in gui, only the first one)
    main_window.char_id_partner_value.setPixmap(QPixmap(os.path.join(GSCEV.path_slot_small_images, "sc_chara_s_" + str(gsac_3.data.pointers[3].pointers_data[0].value_GSDT).zfill(3) + ".png")))
    # Skin (store in gui, only the first one)
    main_window.skin_partner_value.setValue(gsac_3.data.pointers[3].pointers_data[1].value_GSDT)
    # Battle damaged (store in gui, only the first one)
    main_window.damaged_partner_costume.setChecked(gsac_3.data.pointers[3].pointers_data[2].value_GSDT)

    # Character id (select only the first one)
    main_window.character_value.setValue(1)
    # Skin (store in gui, only the first one)
    main_window.skin_value.setValue(gsac_3.data.pointers[5].pointers_data[3].value_GSDT)
    # Battle damaged (store in gui, only the first one)
    main_window.damaged_costume.setChecked(gsac_3.data.pointers[5].pointers_data[4].value_GSDT)
    # Health (store in gui, only the first one)
    main_window.gsc_health_value.setValue(gsac_3.data.pointers[5].pointers_data[8].value_GSDT)
    # Character (store in gui, only the first one)
    main_window.char_id_value.setPixmap(QPixmap(os.path.join(GSCEV.path_slot_small_images, "sc_chara_s_" + str(gsac_3.data.pointers[5].pointers_data[2].value_GSDT).zfill(3) + ".png")))
    # Blast attacks
    value_gsdt = gsac_3.data.pointers[6].pointers_data[1].value_GSDT
    main_window.ico_boost_stick_r_up_value_2.setCurrentIndex(value_gsdt + 1 if value_gsdt != 4294967295 else 0)
    value_gsdt = gsac_3.data.pointers[6].pointers_data[2].value_GSDT
    main_window.ico_boost_stick_r_d_value_2.setCurrentIndex(value_gsdt + 1 if value_gsdt != 4294967295 else 0)
    value_gsdt = gsac_3.data.pointers[6].pointers_data[3].value_GSDT
    main_window.ico_boost_stick_r_l_value_2.setCurrentIndex(value_gsdt + 1 if value_gsdt != 4294967295 else 0)
    value_gsdt = gsac_3.data.pointers[6].pointers_data[4].value_GSDT
    main_window.ico_boost_stick_r_r_value_2.setCurrentIndex(value_gsdt + 1 if value_gsdt != 4294967295 else 0)
    value_gsdt = gsac_3.data.pointers[6].pointers_data[5].value_GSDT
    main_window.ico_boost_stick_r_push_value_2.setCurrentIndex(value_gsdt + 1 if value_gsdt != 4294967295 else 0)

    # --------
    # Subtitle properties (GSAC4)
    # --------
    gsac_4 = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[4]
    # Reset model list view
    main_window.pointer_subtitle_list_view.model().clear()
    # Add each subtitle instruction
    for gsac_4_pointer in gsac_4.data.pointers[1:]:
        item = QStandardItem("Instruction " + str(gsac_4_pointer.pointers_data[0].value_GSDT))
        item.setData(gsac_4_pointer.pointers_data[0])
        item.setEditable(False)
        main_window.pointer_subtitle_list_view.model().appendRow(item)
    # Select the first subtitle instruction
    main_window.pointer_subtitle_list_view.setCurrentIndex(main_window.pointer_subtitle_list_view.model().index(0, 0))

    # --------
    # Events properties (GSAC5 to end)
    # --------
    # Reset gsac, instructions and parameters
    main_window.gsac_events_list.model().clear()
    if main_window.remove_gsac_event_button.isEnabled():
        # Disable the buttons
        main_window.gsac_events_list_up_button.setEnabled(False)
        main_window.gsac_events_list_down_button.setEnabled(False)
        main_window.remove_gsac_event_button.setEnabled(False)

    main_window.events_instructions_list.model().clear()
    # Disable some buttons if there won't be any more instructions
    if main_window.remove_instruction_button.isEnabled():
        # Disable the buttons
        main_window.events_instructions_list_up_button.setEnabled(False)
        main_window.events_instructions_list_down_button.setEnabled(False)
        main_window.remove_instruction_button.setEnabled(False)

    # Disable all the parameters value ui
    for i in range(0, 8):
        if GSCEV.pointers_values_ui[i].isEnabled():
            GSCEV.pointers_values_ui[i].setEnabled(False)

    # Add all gsac events to the list view
    for gsac in GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[5:]:
        item = QStandardItem(str(gsac.id))
        item.setData(gsac)
        item.setEditable(False)
        main_window.gsac_events_list.model().appendRow(item)
    # Select the first gsac entry
    main_window.gsac_events_list.setCurrentIndex(main_window.gsac_events_list.model().index(0, 0))

    # Open the tab (gsc explorer)
    if main_window.tabWidget.currentIndex() != 3:
        main_window.tabWidget.setCurrentIndex(3)
