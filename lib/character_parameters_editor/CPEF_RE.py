from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.CPEV_RE import CPEVRE
from lib.character_parameters_editor.classes.Slot import Slot

from lib.design.select_chara_roster import Select_Chara_Roster
from lib.packages import QLabel, QPixmap, functools, os


def initialize_cs_chip(main_window, qt_widgets):
    # Load all the mini portraits (main panel)
    mini_portraits_image_2 = main_window.mainPanel_2.findChildren(QLabel)
    slots_trans_images = mini_portraits_image_2[:CPEVRE.num_slots_transformations]
    slots_characters_images = mini_portraits_image_2[CPEVRE.num_slots_transformations:]

    # Initialize the slots
    # Transformation slots
    for i in range(0, CPEVRE.num_slots_transformations):
        slot = Slot()

        slot.qlabel_object = slots_trans_images[i]
        slot.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                          "chara_chips_101.bmp")))
        slot.qlabel_object.setStyleSheet(CPEV.styleSheetSelectSlotRoster)
        slot.qlabel_object.mousePressEvent = functools.partial(action_change_transformation,
                                                               main_window=main_window,
                                                               index_slot=i)

        # Store te object in the trans array
        CPEVRE.slots_transformations.append(slot)

    # Character slots
    for i in range(0, CPEVRE.num_slots_characters):
        slot = Slot()

        slot.qlabel_object = slots_characters_images[i]
        slot.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                          "chara_chips_101.bmp")))
        slot.qlabel_object.setStyleSheet(CPEV.styleSheetSelectSlotRoster)
        slot.qlabel_object.mousePressEvent = functools.partial(action_change_character,
                                                               main_window=main_window,
                                                               index_slot=i)

        # Store te object in the character array
        CPEVRE.slots_characters.append(slot)

    # Load the Select Chara roster window
    main_window.selectCharaRosterWindow = qt_widgets.QMainWindow()
    main_window.selectCharaRosterUI = Select_Chara_Roster()
    main_window.selectCharaRosterUI.setupUi(main_window.selectCharaRosterWindow)
    mini_portraits_image_select_chara_roster_window = main_window.selectCharaRosterUI.frame.findChildren(QLabel)
    for i in range(0, len(mini_portraits_image_select_chara_roster_window)):
        chara_id = int(mini_portraits_image_select_chara_roster_window[i].objectName().split("_")[-1])
        mini_portraits_image_select_chara_roster_window[i].setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                                          "chara_chips_" +
                                                                                          str(chara_id).zfill(3) +
                                                                                          ".bmp")))
        mini_portraits_image_select_chara_roster_window[i].mousePressEvent = functools.partial(action_modify_character,
                                                               main_window=main_window,
                                                               chara_id=chara_id)
        mini_portraits_image_select_chara_roster_window[i].setStyleSheet(CPEV.styleSheetSlotRosterWindow)


def read_cs_chip_file(main_window):
    # cs_chip
    CPEVRE.cs_chip_path = main_window.listView_2.model().item(0, 0).text()
    # cs_form
    CPEVRE.cs_form_path = main_window.listView_2.model().item(2, 0).text()

    # Read the characters ID for the main panel
    with open(CPEVRE.cs_chip_path, mode="rb") as file_cs_chip:
        with open(CPEVRE.cs_form_path, mode="rb") as file_cs_form:

            # Get what ID of character will be used in the main roster (we start in 5 because from 0 to 4 are the
            # transformation slots)
            for i in range(0, CPEVRE.num_slots_characters):

                slot_character = CPEVRE.slots_characters[i]

                data = file_cs_chip.read(1)
                slot_character.chara_id = int.from_bytes(data, byteorder="big")

                # If the ID is not FF, we will change the image slot
                if slot_character.chara_id != 255:

                    image_name = "chara_chips_" + str(slot_character.chara_id).zfill(3) + ".bmp"

                    # Search the for the slot we're working (i), the ID that is using but in the file cs_form
                    # in order to get the transformations related to that ID
                    search_id(file_cs_form, slot_character)

                # null slots in main roster
                else:
                    # Desactivate the null slot image
                    image_name = ""
                    slot_character.qlabel_object.setStyleSheet("QLabel {}")
                    slot_character.qlabel_object.mousePressEvent = None

                # Change the image slot
                slot_character.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, image_name)))


# Read the file cs_form searching the ID from cs_chip
def search_id(file_cs_form, slot_character):

    data = file_cs_form.read(CPEVRE.size_between_character_cs_form)
    while data:

        # Get the position
        position = file_cs_form.tell() - CPEVRE.size_between_character_cs_form

        # Get the ID of the character for the roster
        chara_id_cs_form = data[15]

        # If are equal, we found the ID from cs_chip in cs_form
        if slot_character.chara_id == chara_id_cs_form:

            # Save the position
            slot_character.position_cs_form = position

            # Get number transformations
            slot_character.num_transformations = data[11]

            # Get the transformations ID
            position = 19
            for i in range(0, 5):
                slot_character.transformations_id[i] = data[position]
                position = position + 4

            # Stop the searching
            break

        # Read the next 36 bytes
        data = file_cs_form.read(CPEVRE.size_between_character_cs_form)

    # Move the pointer of the file to the beginning
    file_cs_form.seek(0)


def action_change_character(event, main_window, index_slot=None):

    # Get the chara slot object (old and selected one)
    old_slot_chara = CPEVRE.slots_characters[CPEVRE.slot_chara_selected]
    slot_chara = CPEVRE.slots_characters[index_slot]
    old_trans_selected = old_slot_chara.transformations_id[CPEVRE.slot_trans_selected]

    # Reset the border color in the select chara roster window (chara)
    if CPEVRE.slot_chara_selected != -1 and slot_chara.chara_id != old_slot_chara.chara_id:
        select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                           str(old_slot_chara.
                                                                                               chara_id))
        select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)

    # Reset the border color in the select chara roster window (trans)
    if CPEVRE.slot_trans_selected != -1 and slot_chara.chara_id != old_trans_selected:

        # Change the ID 255 to the noise image ID
        if old_trans_selected == 255:
            old_trans_selected = 101

        select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                           str(old_trans_selected))
        select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)

    # Change color for the selected character in chara roster window
    select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                       str(slot_chara.chara_id))
    select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSelectCharaRosterWindow)

    # The user is changing other slot
    if CPEVRE.slot_chara_selected != index_slot:

        # Load the portrait
        main_window.portrait_2.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_" +
                                                              str(slot_chara.chara_id).zfill(3)
                                                              + ".png")))
        # Load the transformations
        for i in range(0, 5):
            chara_id_trans = slot_chara.transformations_id[i]

            # id is FF, we change it to noise image
            if chara_id_trans == 255:
                chara_id_trans = 101

            slot_transform = CPEVRE.slots_transformations[i]

            # Change the image portrait
            slot_transform.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                        "chara_chips_" +
                                                                        str(chara_id_trans).zfill(3)
                                                                        + ".bmp")))
        # Reset the background color for the transformation
        if CPEVRE.slot_trans_selected != 0:
            CPEVRE.slots_transformations[CPEVRE.slot_trans_selected].qlabel_object.setStyleSheet\
                (CPEV.styleSheetSelectSlotRoster)

            # Change background color for the first transformation slot
            CPEVRE.slots_transformations[0].qlabel_object.setStyleSheet(CPEV.styleSheetSelectTransRoster)
            CPEVRE.slot_trans_selected = 0

        # Mark the selected character in the character roster window
        # Reset the border color
        if CPEVRE.slot_chara_selected != -1:
            # Main roster
            old_slot_chara.qlabel_object.setStyleSheet(CPEV.styleSheetSelectSlotRoster)

        # Main roster
        slot_chara.qlabel_object.setStyleSheet(CPEV.styleSheetSelectCharaRoster)

        # Change the old selected slot to the new one
        CPEVRE.slot_chara_selected = index_slot

    else:

        # Show the select chara roster window
        main_window.selectCharaRosterWindow.show()


def action_change_transformation(event, main_window, index_slot=None):

    # Do nothing if the user doesn't select any character at the start of the tool
    if CPEVRE.slot_chara_selected != -1:

        # Get the chara slot object and the ID of the transformation that the user has selected in main roster
        slot_chara = CPEVRE.slots_characters[CPEVRE.slot_chara_selected]
        old_id_selected_trans = slot_chara.transformations_id[CPEVRE.slot_trans_selected]
        id_selected_trans = slot_chara.transformations_id[index_slot]

        # Reset the border color (between transformation and another transformation)
        if id_selected_trans != old_id_selected_trans:

            # Change the ID 255 to the noise image ID
            if old_id_selected_trans == 255:
                old_id_selected_trans = 101

            # Select chara roster window
            select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                               str(old_id_selected_trans))
            select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)

        # Reset the border color (between chara and transformation)
        if slot_chara.chara_id != id_selected_trans:
            # Select chara roster window
            select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                               str(slot_chara.
                                                                                                   chara_id))
            select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)

        # Change the ID 255 to the noise image ID
        if id_selected_trans == 255:
            id_selected_trans = 101

        # Select chara roster window
        select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                           str(id_selected_trans))
        select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSelectTransRosterWindow)

        # The user is changing other slot
        if CPEVRE.slot_trans_selected != index_slot:

            # Get the trans slot qlabel objects
            old_slot_trans = CPEVRE.slots_transformations[CPEVRE.slot_trans_selected]
            slot_trans = CPEVRE.slots_transformations[index_slot]

            # Load the portrait
            main_window.portrait_2.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_" +
                                                                  str(id_selected_trans).zfill(3)
                                                                  + ".png")))
            # Reset the background color for the transformation
            old_slot_trans.qlabel_object.setStyleSheet(CPEV.styleSheetSelectSlotRoster)

            # Change background color for the new transformation slot
            slot_trans.qlabel_object.setStyleSheet(CPEV.styleSheetSelectTransRoster)

            # Change the old selected trans slot to the new one
            CPEVRE.slot_trans_selected = index_slot

        else:

            # Show the select chara roster window
            main_window.selectCharaRosterWindow.show()


def action_modify_character(event, main_window, chara_id):

    # Get the actual slot
    slot_chara = CPEVRE.slots_characters[CPEVRE.slot_chara_selected]

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
        if slot_chara not in CPEVRE.slots_edited:
            CPEVRE.slots_edited.append(slot_chara)

    # Close the Window
    main_window.selectCharaRosterWindow.close()
