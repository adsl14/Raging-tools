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
    pointers_values_ui = []

    # Dictionary of values for each instruction [Functions (0x01), Properties (0x08)]. The key in the dictionary is in decimal
    instructions_names = [dict({1: "Initialize cutscene", 2: "End of event", 27: "Pause until next iteration", 30: "Apply sound effect", 32: "Dialogue (cutscene)",
                                35: "Character position (cutscene)", 36: "Move character", 38: "Character position (gameplay)", 39: "Character animation", 40: "Character face", 44: "Move eyes",
                                49: "Activate aura", 52: "Camera (start)", 53: "Camera (end)", 56: "Fade out", 57: "Fade in", 61: "Apply Visual filter", 64: "Apply visual speed effect",
                                67: "Apply black effect", 76: "Cutscene mode"}),
                          dict({97: "Trigger GSAC event", 112: "Next audio to reproduce", 118: "Dialogue (gameplay)", 116: "Cutscene mode"})]

    # Color for the borders
    styleSheetSelectCharaGscBlackWindow = "QLabel {border : 3px solid black;}"
    styleSheetSelectCharaGscCyanWindow = "QLabel {border : 5px solid cyan;}"

    # *** vars that need to be reseted when loading a new gsc file ***
    # GSC file class
    gsc_file = GscfFile()
