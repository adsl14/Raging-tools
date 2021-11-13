from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.CPEV_CSC import CPEVCSC
from lib.character_parameters_editor.classes.Slot import Slot

from lib.design.select_chara_roster import Select_Chara_Roster
from lib.packages import QLabel, QPixmap, functools, os


def initialize_cs_chip(main_window, qt_widgets):
    # Load all the mini portraits (main panel)
    mini_portraits_image_2 = main_window.mainPanel_2.findChildren(QLabel)
    slots_trans_images = mini_portraits_image_2[:CPEVCSC.num_slots_transformations]
    slots_characters_images = mini_portraits_image_2[CPEVCSC.num_slots_transformations:]

    # Initialize the slots
    # Transformation slots
    for i in range(0, CPEVCSC.num_slots_transformations):
        slot = Slot()

        slot.qlabel_object = slots_trans_images[i]
        slot.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                          "chara_chips_101.bmp")))
        slot.qlabel_object.setStyleSheet(CPEV.styleSheetMainPanelChara)

        # Store te object in the trans array
        CPEVCSC.slots_transformations.append(slot)

    # Character slots
    for i in range(0, CPEVCSC.num_slots_characters):
        slot = Slot()

        slot.qlabel_object = slots_characters_images[i]
        slot.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                          "chara_chips_101.bmp")))
        slot.qlabel_object.setStyleSheet(CPEV.styleSheetMainPanelChara)
        slot.qlabel_object.mousePressEvent = functools.partial(action_change_character,
                                                               main_window=main_window,
                                                               index_slot=i)

        # Store te object in the character array
        CPEVCSC.slots_characters.append(slot)

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
        mini_portraits_image_select_chara_roster_window[i].setStyleSheet(CPEV.styleSheetSelectChara)


def read_cs_chip_file(main_window):
    # cs_chip
    CPEVCSC.cs_chip_path = main_window.listView_2.model().item(0, 0).text()
    # cs_form
    CPEVCSC.cs_form_path = main_window.listView_2.model().item(2, 0).text()

    # Read the characters ID for the main panel
    with open(CPEVCSC.cs_chip_path, mode="rb") as file_cs_chip:
        with open(CPEVCSC.cs_form_path, mode="rb") as file_cs_form:

            # Get what ID of character will be used in the main roster (we start in 5 because from 0 to 4 are the
            # transformation slots)
            for i in range(0, CPEVCSC.num_slots_characters):

                slot_character = CPEVCSC.slots_characters[i]

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

    data = file_cs_form.read(CPEVCSC.size_between_character_cs_form)
    while data:

        # Get the position
        position = file_cs_form.tell() - CPEVCSC.size_between_character_cs_form

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
        data = file_cs_form.read(CPEVCSC.size_between_character_cs_form)

    # Move the pointer of the file to the beginning
    file_cs_form.seek(0)


def action_change_character(event, main_window, index_slot=None):
    # The user is changing other slot
    if CPEVCSC.slot_selected != index_slot:

        old_slot_chara = CPEVCSC.slots_characters[CPEVCSC.slot_selected]
        slot_chara = CPEVCSC.slots_characters[index_slot]

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

            slot_transform = CPEVCSC.slots_transformations[i]

            # Change the image portrait
            slot_transform.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                        "chara_chips_" +
                                                                        str(chara_id_trans).zfill(3)
                                                                        + ".bmp")))

        # Mark the selected character
        # Reset the border color
        if CPEVCSC.slot_selected != -1:
            # Main roster
            old_slot_chara.qlabel_object.setStyleSheet(CPEV.styleSheetMainPanelChara)
            # Select chara roster window
            select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                               str(old_slot_chara.
                                                                                                   chara_id))
            select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSelectChara)

        # Main roster
        slot_chara.qlabel_object.setStyleSheet(CPEV.styleSheetSelectCharaRoster)
        # Select chara roster window
        select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                           str(slot_chara.chara_id))
        select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSelectCharaRosterWindow)

        # Change the old selected slot to the new one
        CPEVCSC.slot_selected = index_slot

    else:

        # Show the select chara roster window
        main_window.selectCharaRosterWindow.show()
