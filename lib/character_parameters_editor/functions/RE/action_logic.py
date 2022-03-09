from lib.packages import QLabel, QPixmap, os
from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.REV import REV
from lib.character_parameters_editor.functions.RE.auxiliary import get_num_transformations


def action_change_character(event, main_window, index_slot=None):

    # Get the chara slot object (old and selected one)
    old_slot_chara = REV.slots_characters[REV.slot_chara_selected]
    slot_chara = REV.slots_characters[index_slot]
    old_trans_selected = old_slot_chara.transformations_id[REV.slot_trans_selected]

    # Reset the border color in the select chara roster window (chara)

    # The selection before was a character
    if REV.selecting_character:

        if REV.slot_chara_selected != -1 and slot_chara.chara_id != old_slot_chara.chara_id:
            select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                               str(old_slot_chara.
                                                                                                   chara_id))
            select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)

    # The selection before was a transformation
    else:

        # Reset the border color in the select chara roster window (trans)
        if REV.slot_trans_selected != -1 and slot_chara.chara_id != old_trans_selected:

            select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                               str(old_trans_selected))
            select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)

    # Change color for the selected character in chara roster window
    select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                       str(slot_chara.chara_id))
    select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSelectCharaRosterWindow)

    # The user is changing other slot
    if REV.slot_chara_selected != index_slot:

        # Load the portrait
        main_window.portrait_2.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_" +
                                                              str(slot_chara.chara_id).zfill(3)
                                                              + ".png")))
        # Load the transformations
        for i in range(0, REV.num_slots_transformations):
            chara_id_trans = slot_chara.transformations_id[i]

            # Get the slot of the selected transformation
            slot_transform = REV.slots_transformations[i]

            # Change in memory the transformations
            slot_transform.chara_id = chara_id_trans

            # Change the image portrait
            slot_transform.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                        "chara_chips_" +
                                                                        str(chara_id_trans).zfill(3)
                                                                        + ".bmp")))

        # Reset the background color for the transformation
        if REV.slot_trans_selected != 0:
            REV.slots_transformations[REV.slot_trans_selected].qlabel_object\
                .setStyleSheet(CPEV.styleSheetSelectSlotRoster)

            # Change background color for the first transformation slot
            REV.slots_transformations[0].qlabel_object.setStyleSheet(CPEV.styleSheetSelectTransRoster)
            REV.slot_trans_selected = 0

        # Mark the selected character in the character roster window
        # Reset the border color
        if REV.slot_chara_selected != -1:
            # Main roster
            old_slot_chara.qlabel_object.setStyleSheet(CPEV.styleSheetSelectSlotRoster)

        # Main roster
        slot_chara.qlabel_object.setStyleSheet(CPEV.styleSheetSelectCharaRoster)

        # Change the old selected slot to the new one
        REV.slot_chara_selected = index_slot

    else:

        # Show the select chara roster window
        main_window.selectCharaRosterWindow.show()

    # The user is selecting a character
    if not REV.selecting_character:
        REV.selecting_character = True


def action_change_transformation(event, main_window, index_slot=None):

    # Do nothing if the user doesn't select any character at the start of the tool
    if REV.slot_chara_selected != -1:

        # Get the chara slot object and the ID of the transformation that the user has selected in main roster
        slot_chara = REV.slots_characters[REV.slot_chara_selected]
        old_id_selected_trans = slot_chara.transformations_id[REV.slot_trans_selected]
        id_selected_trans = slot_chara.transformations_id[index_slot]

        # The selection before was a character
        if REV.selecting_character:

            # Reset the border color (between chara and transformation)
            if slot_chara.chara_id != id_selected_trans:
                # Select chara roster window
                select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                                   str(slot_chara.
                                                                                                       chara_id))
                select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)

        # The selection before was a transformation
        else:
            # Reset the border color (between transformation and another transformation)
            if id_selected_trans != old_id_selected_trans:

                # Select chara roster window
                select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.\
                    findChild(QLabel, "label_" + str(old_id_selected_trans))
                select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)

        # Select chara roster window
        select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                           str(id_selected_trans))
        select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSelectTransRosterWindow)

        # The user is changing other slot
        if REV.slot_trans_selected != index_slot:

            # Get the trans slot qlabel objects
            old_slot_trans = REV.slots_transformations[REV.slot_trans_selected]
            slot_trans = REV.slots_transformations[index_slot]

            # Load the portrait
            main_window.portrait_2.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_" +
                                                                  str(id_selected_trans).zfill(3)
                                                                  + ".png")))
            # Reset the background color for the transformation
            old_slot_trans.qlabel_object.setStyleSheet(CPEV.styleSheetSelectSlotRoster)

            # Change background color for the new transformation slot
            slot_trans.qlabel_object.setStyleSheet(CPEV.styleSheetSelectTransRoster)

            # Change the old selected trans slot to the new one
            REV.slot_trans_selected = index_slot

        else:
            # Show the select chara roster window
            main_window.selectCharaRosterWindow.show()

        # The user is selecting a transformation
        if REV.selecting_character:
            REV.selecting_character = False


def action_modify_character(event, main_window, chara_id):

    # Get the actual slot
    slot_chara = REV.slots_characters[REV.slot_chara_selected]

    # The user is selecting a character
    if REV.selecting_character:

        # If the actual ID is not equal to the selected one in the roster window, we don't modify anything
        if slot_chara.chara_id != chara_id:

            # Reset chara portrait backtround color in roster window
            select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                               str(slot_chara.chara_id))
            select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)

            # Change the chara ID for the selected slot
            slot_chara.chara_id = chara_id

            # Change chara roster background color in roster window
            select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                               str(slot_chara.chara_id))
            select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSelectCharaRosterWindow)

            # Change large portrait
            main_window.portrait_2.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_" +
                                                                  str(slot_chara.chara_id).zfill(3)
                                                                  + ".png")))
            # Change portrait in select chara matrix
            slot_chara.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                    "chara_chips_" + str(slot_chara.chara_id).zfill(3)
                                                                    + ".bmp")))

            # If the character was edited before, we won't append the reference of the slot
            if slot_chara not in REV.slots_edited:
                REV.slots_edited.append(slot_chara)

    # The user is selecting a transformation
    elif slot_chara.transformations_id[REV.slot_trans_selected] != chara_id:

        # Get the qlabel of the transformation slot
        trans_slot = REV.slots_transformations[REV.slot_trans_selected]

        # Change large portrait
        main_window.portrait_2.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_" +
                                                              str(chara_id).zfill(3)
                                                              + ".png")))

        # Change portrait in select chara matrix
        trans_slot.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                "chara_chips_" + str(chara_id).zfill(3)
                                                                + ".bmp")))

        # Reset chara portrait backtground color in roster window
        select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                           str(trans_slot.chara_id))
        select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)

        # Change the chara ID for the selected slot
        slot_chara.transformations_id[REV.slot_trans_selected] = chara_id
        trans_slot.chara_id = chara_id

        # Change the number of transformations for the character slot
        slot_chara.num_transformations = get_num_transformations(slot_chara)

        # Change chara roster background color in roster window
        select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                           str(trans_slot.chara_id))
        select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSelectCharaRosterWindow)

        # If the character was edited before, we won't append the reference of the slot
        if slot_chara not in REV.slots_edited:
            REV.slots_edited.append(slot_chara)

    # Close the Window
    main_window.selectCharaRosterWindow.close()
