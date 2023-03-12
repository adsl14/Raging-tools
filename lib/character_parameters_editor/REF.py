from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.REV import REV
from lib.character_parameters_editor.classes.Slot import Slot
from lib.character_parameters_editor.functions.RE.action_logic import action_change_transformation, \
    action_change_character, action_modify_character
from lib.character_parameters_editor.functions.RE.auxiliary import search_id
from lib.functions import show_progress_value
from lib.packages import QLabel, QPixmap, functools, os


def initialize_cs_chip(main_window):

    # Load all the mini portraits (main panel)
    mini_portraits_image_2 = main_window.mainPanel_2.findChildren(QLabel)
    slots_trans_images = mini_portraits_image_2[:REV.num_slots_transformations]
    slots_characters_images = mini_portraits_image_2[REV.num_slots_transformations:]

    # Initialize the slots
    # Transformation slots
    for i in range(0, REV.num_slots_transformations):
        slot = Slot()

        slot.qlabel_object = slots_trans_images[i]
        slot.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                          "chara_chips_101.bmp")))
        slot.qlabel_object.setStyleSheet(CPEV.styleSheetSelectSlotRoster)
        slot.qlabel_object.mousePressEvent = functools.partial(action_change_transformation,
                                                               main_window=main_window,
                                                               index_slot=i)

        # Store te object in the trans array
        REV.slots_transformations.append(slot)

    # Character slots
    for i in range(0, REV.num_slots_characters):
        slot = Slot()

        slot.qlabel_object = slots_characters_images[i]
        slot.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                          "chara_chips_101.bmp")))
        slot.qlabel_object.setStyleSheet(CPEV.styleSheetSelectSlotRoster)
        slot.qlabel_object.mousePressEvent = functools.partial(action_change_character,
                                                               main_window=main_window,
                                                               index_slot=i)

        # Store te object in the character array
        REV.slots_characters.append(slot)

    # Load the Select Chara roster window
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


def read_cs_chip_file(worker_pef, step_progress, main_window):

    # cs_chip
    REV.cs_chip_path = main_window.listView_2.model().item(0, 0).text()
    # cs_form
    REV.cs_form_path = main_window.listView_2.model().item(2, 0).text()

    # Read the characters ID for the main panel
    with open(REV.cs_chip_path, mode="rb") as file_cs_chip:
        with open(REV.cs_form_path, mode="rb") as file_cs_form:

            # Get what ID of character will be used in the main roster
            sub_step_progress = step_progress / REV.num_slots_characters
            for i in range(0, REV.num_slots_characters):

                # Report progress
                worker_pef.progressText.emit("Reading character ID: " + str(i))
                show_progress_value(worker_pef, sub_step_progress)

                # get a slot object
                slot_character = REV.slots_characters[i]

                # Read the byte and store the values
                data = file_cs_chip.read(1)
                slot_character.chara_id = int.from_bytes(data, byteorder="big")
                slot_character.position_cs_chip = i

                # If the ID is not FF, we will change the image slot
                if slot_character.chara_id != 255:

                    image_name = "chara_chips_" + str(slot_character.chara_id).zfill(3) + ".bmp"

                    # Search the for the slot we're working (i), the ID that is using but in the file cs_form
                    # in order to get the transformations related to that ID
                    search_id(file_cs_form, slot_character)

                # null slots in main roster
                else:
                    # Deactivate the null slot image
                    image_name = ""
                    worker_pef.delete_image_slot_RE_signal.emit(slot_character)

                    # Change to 101 so the ID is the same as noise image
                    slot_character.chara_id = 101

                # Change the image slot
                worker_pef.change_image_slot_RE_signal.emit(slot_character, image_name)


def write_cs_chip_file(worker_pef, step_progress):

    # Write the slots that were edited
    with open(REV.cs_chip_path, mode="rb+") as file_cs_chip:
        with open(REV.cs_form_path, mode="rb+") as file_cs_form:

            # Get all the slots that were edited
            sub_step_progress = step_progress / len(REV.slots_edited)
            worker_pef.progressText.emit("Writing edited characters")
            for slot in REV.slots_edited:

                # Report progress
                show_progress_value(worker_pef, sub_step_progress)

                # Write in cs_chip
                file_cs_chip.seek(slot.position_cs_chip)
                file_cs_chip.write(slot.chara_id.to_bytes(1, byteorder="big"))

                # Write in cs_form
                file_cs_form.seek(slot.position_cs_form + 11)
                file_cs_form.write(slot.num_transformations.to_bytes(1, byteorder="big"))
                file_cs_form.write(b'\x00\x00\x00' + slot.chara_id.to_bytes(1, byteorder="big"))

                for transformation in slot.transformations_id:
                    if transformation != 101:
                        file_cs_form.write(b'\x00\x00\x00' + transformation.to_bytes(1, byteorder="big"))
                    else:
                        file_cs_form.write(b'\xFF\xFF\xFF\xFF')
