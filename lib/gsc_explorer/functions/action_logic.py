from lib.gsc_explorer.functions.auxiliary import assign_pointer_to_ui, get_pointer_data_info_name
from lib.packages import os

from PyQt5.QtGui import QPixmap, QStandardItem
from PyQt5.QtWidgets import QLabel, QMessageBox

from lib.gsc_explorer.GSCEV import GSCEV


def action_change_character(event, main_window, option):

    # Get the current character
    # Chara ID for stage properties
    if option == 0:
        char_id = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[2].value_GSDT
    # Chara ID for subtitle properties
    elif option == 1:
        char_id = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[4].data.pointers[1 + main_window.pointer_subtitle_list_view.currentIndex().row()].pointers_data[3].value_GSDT
    # Chara ID for partner
    else:
        char_id = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[2 + main_window.character_partner_value.value()].pointers_data[0].value_GSDT

    # Check if the chara_id is 4294967295 (empty value), so we convert the value to the proper format for ui
    char_id = char_id if char_id != 4294967295 else 101

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

    # Check if the chara_id is 101 (empty value), so we convert the value to the proper format in memory
    chara_id_value = chara_id if chara_id < 100 else 4294967295

    # Check the option selected
    if GSCEV.char_id_option_selected == 0:
        # Change character id
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[2].value_GSDT = chara_id_value

        # Change character image
        main_window.char_id_value.setPixmap(QPixmap(os.path.join(GSCEV.path_slot_small_images, "sc_chara_s_" + str(chara_id).zfill(3) + ".png")))

    elif GSCEV.char_id_option_selected == 1:
        # Change character id
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[4].data.pointers[1 + main_window.pointer_subtitle_list_view.currentIndex().row()].pointers_data[3].value_GSDT = chara_id_value

        # Change character image
        main_window.char_id_subtitle_value.setPixmap(QPixmap(os.path.join(GSCEV.path_slot_small_images, "sc_chara_s_" + str(chara_id).zfill(3) + ".png")))
    else:
        # Change character id
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[2 + main_window.character_partner_value.value()].pointers_data[0].value_GSDT = chara_id_value

        # Change character image
        main_window.char_id_partner_value.setPixmap(QPixmap(os.path.join(GSCEV.path_slot_small_images, "sc_chara_s_" + str(chara_id).zfill(3) + ".png")))

    # Close Window
    main_window.selectCharaGscWindow.close()


def action_gsac_events_list_up_button_logic(main_window):

    # Get the current pointer instruction
    index_gsac = main_window.gsac_events_list.currentIndex().row()

    # Check if is the last instrunction entry
    if index_gsac > 0:

        # Get current gsac name and data
        current_instruction_name = main_window.gsac_events_list.model().item(index_gsac).text()
        current_instruction_data = main_window.gsac_events_list.model().item(index_gsac).data()

        # Get next gsac name and data
        before_instruction_name = main_window.gsac_events_list.model().item(index_gsac - 1).text()
        before_instruction_data = main_window.gsac_events_list.model().item(index_gsac - 1).data()

        # Make the swap
        main_window.gsac_events_list.model().item(index_gsac).setText(before_instruction_name)
        main_window.gsac_events_list.model().item(index_gsac).setData(before_instruction_data)
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[5 + index_gsac] = before_instruction_data

        main_window.gsac_events_list.model().item(index_gsac - 1).setText(current_instruction_name)
        main_window.gsac_events_list.model().item(index_gsac - 1).setData(current_instruction_data)
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[5 + index_gsac - 1] = current_instruction_data

        # Select the next gsac entry
        main_window.gsac_events_list.setCurrentIndex(main_window.gsac_events_list.model().index(index_gsac - 1, 0))


def action_gsac_events_list_down_button_logic(main_window):

    # Get the current pointer instruction
    index_gsac = main_window.gsac_events_list.currentIndex().row()

    # Check if is the last instrunction entry
    if index_gsac < main_window.gsac_events_list.model().rowCount() - 1:

        # Get current instruction name and data
        current_instruction_name = main_window.gsac_events_list.model().item(index_gsac).text()
        current_instruction_data = main_window.gsac_events_list.model().item(index_gsac).data()

        # Get next instruction name and data
        next_instruction_name = main_window.gsac_events_list.model().item(index_gsac + 1).text()
        next_instruction_data = main_window.gsac_events_list.model().item(index_gsac + 1).data()

        # Make the swap
        main_window.gsac_events_list.model().item(index_gsac).setText(next_instruction_name)
        main_window.gsac_events_list.model().item(index_gsac).setData(next_instruction_data)
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[5 + index_gsac] = next_instruction_data

        main_window.gsac_events_list.model().item(index_gsac + 1).setText(current_instruction_name)
        main_window.gsac_events_list.model().item(index_gsac + 1).setData(current_instruction_data)
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[5 + index_gsac] = current_instruction_data

        # Select the next instruction
        main_window.gsac_events_list.setCurrentIndex(main_window.gsac_events_list.model().index(index_gsac + 1, 0))


def action_remove_gsac_logic(main_window):

    # Ask the user if is sure to remove the texture
    msg = QMessageBox()
    msg.setWindowTitle("Message")
    msg.setWindowIcon(main_window.ico_image)
    message = "The gsac entry will be removed. Are you sure to continue?"
    answer = msg.question(main_window, '', message, msg.Yes | msg.No | msg.Cancel)

    # Check if the user has selected something
    if answer:

        # The user wants to remove the selected texture
        if answer == msg.Yes:

            # Get the current gsac entry
            index_gsac = main_window.gsac_events_list.currentIndex().row()

            # Get the gsac entries
            gsac_entries = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[5:]

            # Remove the instruction in memory, creating a new array
            new_gsac_entries = []
            for i in range(0, index_gsac):
                new_gsac_entries.append(gsac_entries[i])
            for i in range(index_gsac + 1, len(gsac_entries)):
                new_gsac_entries.append(gsac_entries[i])
            GSCEV.gsc_file.gscf_header.gscd_header.gsac_array = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[:5] + new_gsac_entries

            # Remove from the array of instructions in the list
            main_window.gsac_events_list.model().removeRow(index_gsac)


def action_events_instructions_list_up_button_logic(main_window):

    # Get the current pointer instruction
    index_intruction = main_window.events_instructions_list.currentIndex().row()

    # Check if is the last instrunction entry
    if index_intruction > 0:

        # Get the current gsac entry
        index_gsac = main_window.gsac_events_list.currentIndex().row()

        # Get current instruction name and data
        current_instruction_name = main_window.events_instructions_list.model().item(index_intruction).text()
        current_instruction_data = main_window.events_instructions_list.model().item(index_intruction).data()

        # Get next instruction name and data
        before_instruction_name = main_window.events_instructions_list.model().item(index_intruction - 1).text()
        before_instruction_data = main_window.events_instructions_list.model().item(index_intruction - 1).data()

        # Make the swap
        main_window.events_instructions_list.model().item(index_intruction).setText(before_instruction_name)
        main_window.events_instructions_list.model().item(index_intruction).setData(before_instruction_data)
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[5 + index_gsac].data.pointers[index_intruction] = before_instruction_data

        main_window.events_instructions_list.model().item(index_intruction - 1).setText(current_instruction_name)
        main_window.events_instructions_list.model().item(index_intruction - 1).setData(current_instruction_data)
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[5 + index_gsac].data.pointers[index_intruction - 1] = current_instruction_data

        # Select the next instruction
        main_window.events_instructions_list.setCurrentIndex(main_window.events_instructions_list.model().index(index_intruction - 1, 0))


def action_events_instructions_list_down_button_logic(main_window):

    # Get the current pointer instruction
    index_intruction = main_window.events_instructions_list.currentIndex().row()

    # Check if is the last instrunction entry
    if index_intruction < main_window.events_instructions_list.model().rowCount() - 1:

        # Get the current gsac entry
        index_gsac = main_window.gsac_events_list.currentIndex().row()

        # Get current instruction name and data
        current_instruction_name = main_window.events_instructions_list.model().item(index_intruction).text()
        current_instruction_data = main_window.events_instructions_list.model().item(index_intruction).data()

        # Get next instruction name and data
        next_instruction_name = main_window.events_instructions_list.model().item(index_intruction + 1).text()
        next_instruction_data = main_window.events_instructions_list.model().item(index_intruction + 1).data()

        # Make the swap
        main_window.events_instructions_list.model().item(index_intruction).setText(next_instruction_name)
        main_window.events_instructions_list.model().item(index_intruction).setData(next_instruction_data)
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[5 + index_gsac].data.pointers[index_intruction] = next_instruction_data

        main_window.events_instructions_list.model().item(index_intruction + 1).setText(current_instruction_name)
        main_window.events_instructions_list.model().item(index_intruction + 1).setData(current_instruction_data)
        GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[5 + index_gsac].data.pointers[index_intruction + 1] = current_instruction_data

        # Select the next instruction
        main_window.events_instructions_list.setCurrentIndex(main_window.events_instructions_list.model().index(index_intruction + 1, 0))


def action_remove_instruction_logic(main_window):

    # Ask the user if is sure to remove the texture
    msg = QMessageBox()
    msg.setWindowTitle("Message")
    msg.setWindowIcon(main_window.ico_image)
    message = "The instruction will be removed. Are you sure to continue?"
    answer = msg.question(main_window, '', message, msg.Yes | msg.No | msg.Cancel)

    # Check if the user has selected something
    if answer:

        # The user wants to remove the selected texture
        if answer == msg.Yes:

            # Get the current gsac entry
            index_gsac = main_window.gsac_events_list.currentIndex().row()

            # Get the current pointer instruction
            index_intruction = main_window.events_instructions_list.currentIndex().row()

            # Get the pointers for the specific gasc entry
            pointers = main_window.gsac_events_list.model().item(index_gsac).data().data.pointers

            # Remove the instruction in memory, creating a new array
            new_pointers = []
            for i in range(0, index_intruction):
                new_pointers.append(pointers[i])
            for i in range(index_intruction + 1, len(pointers)):
                new_pointers.append(pointers[i])
            GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[5 + index_gsac].data.pointers = new_pointers

            # Remove from the array of instructions in the list
            main_window.events_instructions_list.model().removeRow(index_intruction)


def on_initial_gsac_event_changed(main_window):

    # Convert the value to hex
    hex_value = '{:08x}'.format(main_window.initial_gsac_event_value.value())
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[0].data.pointers[0].secundary_number_of_pointers = int(hex_value[-2:], 16)
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[0].data.pointers[0].unk0x04 = bytes.fromhex(hex_value[-4:-2])


def on_map_changed(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[0].pointers_data[0].value_GSDT = main_window.map_name_value.currentIndex()


def on_music_changed(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[0].pointers_data[1].value_GSDT = main_window.music_value.value()


def on_player_slot_changed(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[1].pointers_data[1].value_GSDT = main_window.player_character_value.value()


def on_cpu_slot_changed(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[1].pointers_data[7].value_GSDT = main_window.cpu_character_value.value()


def on_partner_character_id_changed(main_window):

    # Get gsac_3
    gsac_3 = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3]

    # Skin
    main_window.skin_partner_value.setValue(gsac_3.data.pointers[2 + main_window.character_partner_value.value()].pointers_data[1].value_GSDT)
    # Battle damaged
    main_window.damaged_partner_costume.setChecked(gsac_3.data.pointers[2 + main_window.character_partner_value.value()].pointers_data[2].value_GSDT)
    # Health
    main_window.gsc_health_value.setValue(gsac_3.data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[8].value_GSDT)
    # Character
    main_window.char_id_partner_value.setPixmap(QPixmap(os.path.join(GSCEV.path_slot_small_images, "sc_chara_s_" + str(gsac_3.data.pointers[2 + main_window.character_partner_value.value()]
                                                                                                                       .pointers_data[0].value_GSDT).zfill(3) + ".png")))


def on_partner_skin_changed(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[2 + main_window.character_partner_value.value()].pointers_data[1].value_GSDT = main_window.skin_partner_value.value()


def on_partner_damaged_costume(main_window):
    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[2 + main_window.character_partner_value.value()].pointers_data[2].value_GSDT = \
        int(main_window.damaged_partner_costume.isChecked() is True)


def on_character_id_changed(main_window):

    # Get gsac_3
    gsac_3 = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3]

    # Skin
    main_window.skin_value.setValue(gsac_3.data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[3].value_GSDT)
    # Battle damaged
    main_window.damaged_costume.setChecked(gsac_3.data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[4].value_GSDT)
    # Health
    main_window.gsc_health_value.setValue(gsac_3.data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[8].value_GSDT)
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
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[3 + (2 * main_window.character_value.value())].pointers_data[8].value_GSDT = int(main_window.gsc_health_value.value())


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


def on_gsac_events_list_changed(main_window):

    # Reset instructions list view
    main_window.events_instructions_list.model().clear()

    # Get the current gsac entry
    index = main_window.gsac_events_list.currentIndex().row()

    # Add each instruction pointer from current gsac. If there is any gsac entry, it will throw 'AttributeError' exception
    try:
        num_instructions = 0
        gsac = main_window.gsac_events_list.model().item(index).data()
        for event_instruction in gsac.data.pointers:
            name = get_pointer_data_info_name(event_instruction)
            item = QStandardItem(name)
            item.setData(event_instruction)
            item.setEditable(False)
            main_window.events_instructions_list.model().appendRow(item)
            num_instructions = num_instructions + 1

        if not main_window.remove_gsac_event_button.isEnabled():
            # Enable the buttons
            main_window.gsac_events_list_up_button.setEnabled(True)
            main_window.gsac_events_list_down_button.setEnabled(True)
            main_window.remove_gsac_event_button.setEnabled(True)

        if num_instructions > 0:
            # Enable the buttons if they're disabled
            if not main_window.remove_instruction_button.isEnabled():
                # Enable the buttons
                main_window.events_instructions_list_up_button.setEnabled(True)
                main_window.events_instructions_list_down_button.setEnabled(True)
                main_window.remove_instruction_button.setEnabled(True)

            # Select the first instruction
            main_window.events_instructions_list.setCurrentIndex(main_window.events_instructions_list.model().index(0, 0))
        else:
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

    except AttributeError:

        if main_window.remove_gsac_event_button.isEnabled():
            # Enable the buttons
            main_window.gsac_events_list_up_button.setEnabled(False)
            main_window.gsac_events_list_down_button.setEnabled(False)
            main_window.remove_gsac_event_button.setEnabled(False)


def on_events_instructions_list_changed(main_window):

    # Get the current pointer instruction
    index_intruction = main_window.events_instructions_list.currentIndex().row()

    try:
        # Get the pointer data info
        pointer_data_info = main_window.events_instructions_list.model().item(index_intruction).data()

        # Get number of pointers (pointers that are not 08 in their first byte, means the number of pointers_data is in the second byte, otherwise the third byte)
        number_of_pointers = pointer_data_info.number_of_pointers if pointer_data_info.type != b'\x08' else pointer_data_info.secundary_number_of_pointers

        # Disconnect the instruction values
        try:
            # GSAC 5 and so on
            main_window.instruction_value_0.valueChanged.disconnect()
            main_window.instruction_value_1.valueChanged.disconnect()
            main_window.instruction_value_2.valueChanged.disconnect()
            main_window.instruction_value_3.valueChanged.disconnect()
            main_window.instruction_value_4.valueChanged.disconnect()
            main_window.instruction_value_5.valueChanged.disconnect()
            main_window.instruction_value_6.valueChanged.disconnect()
            main_window.instruction_value_7.valueChanged.disconnect()
        except TypeError:
            pass

        # Assign each pointer value from the instruction
        assign_pointer_to_ui(GSCEV.pointers_values_ui, pointer_data_info, number_of_pointers)

        # Connect the instruction values
        main_window.instruction_value_0.valueChanged.connect(lambda: on_instruction_value_changed(main_window, 0))
        main_window.instruction_value_1.valueChanged.connect(lambda: on_instruction_value_changed(main_window, 1))
        main_window.instruction_value_2.valueChanged.connect(lambda: on_instruction_value_changed(main_window, 2))
        main_window.instruction_value_3.valueChanged.connect(lambda: on_instruction_value_changed(main_window, 3))
        main_window.instruction_value_4.valueChanged.connect(lambda: on_instruction_value_changed(main_window, 4))
        main_window.instruction_value_5.valueChanged.connect(lambda: on_instruction_value_changed(main_window, 5))
        main_window.instruction_value_6.valueChanged.connect(lambda: on_instruction_value_changed(main_window, 6))
        main_window.instruction_value_7.valueChanged.connect(lambda: on_instruction_value_changed(main_window, 7))

    except AttributeError:

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


def on_instruction_value_changed(main_window, value_index):

    # Get the current gsac entry
    index_gsac = main_window.gsac_events_list.currentIndex().row()

    # Get the current pointer instruction
    index_intruction = main_window.events_instructions_list.currentIndex().row()

    # Get the pointer data info
    pointer_data_info = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[5 + index_gsac].data.pointers[index_intruction]

    # Store the value modified into the pointer in memory. Check if the pointer value is in integer or float, to convert it to the proper format
    pointer_value_ui = GSCEV.pointers_values_ui[value_index].value()
    pointer_data_info.pointers_data[value_index].value_GSDT = int(pointer_value_ui) if pointer_data_info.pointers_data[value_index].type_GSDT == b'\x0A' else pointer_value_ui
