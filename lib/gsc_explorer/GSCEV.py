from lib.packages import os

from lib.gsc_explorer.classes.GSCF.GSCFFile import GscfFile


class GSCEV:

    # number of bytes that usually reads the program
    bytes2Read = 4

    # Paths
    path_slot_image = os.path.join("lib", "character_parameters_editor", "images", "fourSlot")
    path_slot_small_images = os.path.join(path_slot_image, "small")
    path_small_images = os.path.join("lib", "character_parameters_editor", "images", "small")
    path_controller_images = os.path.join("lib", "character_parameters_editor", "images", "controller")

    # This var will be used to store the ID of the character, so we can clean the Character Select Window
    old_chara = 0
    # This var will be used to detect from what option we're opening the Character Select Window
    char_id_option_selected = 0

    # portraits object for the Select Character window
    mini_portraits_image_select_chara_window = []
    # QSpinBox object for instruction values ui
    pointer_values_ui = []

    # Color for the borders
    styleSheetSelectCharaGscBlackWindow = "QLabel {border : 3px solid black;}"
    styleSheetSelectCharaGscCyanWindow = "QLabel {border : 5px solid cyan;}"

    # *** vars that need to be reseted when loading a new gsc file ***
    # GSC file class
    gsc_file = GscfFile()
