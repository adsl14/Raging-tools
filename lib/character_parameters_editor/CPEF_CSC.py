from lib.character_parameters_editor.CPEV import CPEV

from lib.design.select_chara_roster import Select_Chara_Roster
from lib.packages import QLabel, QPixmap, functools, os


def initialize_cs_chip(main_window, qt_widgets):

    # Load all the mini portraits (main panel)
    mini_portraits_image_2 = main_window.mainPanel_2.findChildren(QLabel)
    CPEV.mini_portraits_image_trans = mini_portraits_image_2[:5]
    CPEV.mini_portraits_image_chars = mini_portraits_image_2[5:]

    # Initialize the slots
    # Transformation slots
    for i in range(0, len(CPEV.mini_portraits_image_trans)):
        CPEV.mini_portraits_image_trans[i].setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                          "chara_chips_101.bmp")))
        CPEV.mini_portraits_image_trans[i].setStyleSheet(CPEV.styleSheetMainPanelChara)

    # Character slots
    for i in range(0, len(CPEV.mini_portraits_image_chars)):
        CPEV.mini_portraits_image_chars[i].setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                          "chara_chips_101.bmp")))
        CPEV.mini_portraits_image_chars[i].setStyleSheet(CPEV.styleSheetMainPanelChara)
        CPEV.mini_portraits_image_chars[i].mousePressEvent = functools.partial(action_change_character_cs_chip,
                                                                               main_window=main_window,
                                                                               index_slot=i)

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
    CPEV.cs_chip_path = main_window.listView_2.model().item(0, 0).text()
    # cs_form
    CPEV.cs_form_path = main_window.listView_2.model().item(2, 0).text()

    # Read the characters ID for the main panel
    with open(CPEV.cs_chip_path, mode="rb") as file_cs_chip:
        with open(CPEV.cs_form_path, mode="rb") as file_cs_form:

            # Get what ID of character will be used in the main roster (we start in 5 because from 0 to 4 are the
            # transformation slots)
            for i in range(0, len(CPEV.select_chara_main_roster)):
                data = file_cs_chip.read(1)
                CPEV.select_chara_main_roster[i, 2] = int.from_bytes(data, byteorder="big")

                # If the ID is not FF, we will change the image slot
                if CPEV.select_chara_main_roster[i, 2] != 255:

                    image_name = "chara_chips_" + str(CPEV.select_chara_main_roster[i, 2]).zfill(3) + ".bmp"

                    # Search the for the slot we're working (i), the ID that is using but in the file cs_form
                    # in order to get the transformations related to that ID
                    search_id_cs_form(file_cs_form, i)

                # null slots in main roster
                else:
                    # Desactivate the null slots
                    image_name = ""
                    CPEV.mini_portraits_image_chars[i].setStyleSheet("QLabel {}")
                    CPEV.mini_portraits_image_chars[i].mousePressEvent = None

                # Change the image slot
                CPEV.mini_portraits_image_chars[i].setPixmap(QPixmap(os.path.join(CPEV.path_small_images, image_name)))


def search_id_cs_form(file_cs_form, i):

    # Read the file cs_form searching the ID from cs_chip
    data = file_cs_form.read(CPEV.size_between_character_cs_form)
    while data:

        # Get the position
        position = file_cs_form.tell() - CPEV.size_between_character_cs_form

        # Get the ID of the character for the roster
        chara_id_cs_form = data[15]

        # If are equal, we found the ID from cs_chip in cs_form
        if CPEV.select_chara_main_roster[i, 2] == chara_id_cs_form:

            # Save the position
            CPEV.select_chara_main_roster[i, 0] = position

            # Get number transformations
            CPEV.select_chara_main_roster[i, 1] = data[11]

            # Get the transformations ID
            position = 19
            for j in range(3, 8):
                CPEV.select_chara_main_roster[i, j] = data[position]
                position = position + 4

            # Stop the searching
            break

        # Read the next 36 bytes
        data = file_cs_form.read(CPEV.size_between_character_cs_form)

    # Move the pointer of the file to the beginning
    file_cs_form.seek(0)


def action_change_character_cs_chip(event, main_window, index_slot=None):

    # The user is changing other slot
    if CPEV.slot_selected != index_slot:

        chara_id_old = CPEV.select_chara_main_roster[CPEV.slot_selected, 2]
        chara_id = CPEV.select_chara_main_roster[index_slot, 2]

        # Load the portrait
        main_window.portrait_2.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_" +
                                                              str(chara_id).zfill(3)
                                                              + ".png")))
        # Load the transformations
        for i in range(0, 5):
            chara_id_trans = CPEV.select_chara_main_roster[index_slot, i + 3]

            # id is FF, we change it to noise image
            if chara_id_trans == 255:
                chara_id_trans = 101

            # Change the image portrait
            CPEV.mini_portraits_image_trans[i].setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                              "chara_chips_" +
                                                                              str(chara_id_trans).zfill(3)
                                                                              + ".bmp")))

        # Mark the selected character
        # Reset the border color
        if CPEV.slot_selected != -1:
            # Main roster
            CPEV.mini_portraits_image_chars[CPEV.slot_selected].setStyleSheet(CPEV.styleSheetMainPanelChara)
            # Select chara roster window
            select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                               str(chara_id_old))
            select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSelectChara)

        # Main roster
        CPEV.mini_portraits_image_chars[index_slot].setStyleSheet(CPEV.styleSheetSelectCharaRoster)
        # Select chara roster window
        select_chara_roster_window_label = main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                           str(chara_id))
        select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSelectCharaRosterWindow)

        # Change the old selected slot to the new one
        CPEV.slot_selected = index_slot

    else:

        # Show the select chara roster window
        main_window.selectCharaRosterWindow.show()
