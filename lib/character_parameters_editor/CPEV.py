from lib.packages import os


class CPEV:

    # Allowed files
    operate_resident_param = 'operate_resident_param.pak'
    operate_character_xyz_m_regex = "operate_character_0[0-9][0-9]_m.pak"
    cs_chip = "cs_chip.dat"
    db_font_pad_PS3_s_d = "db_font_pad_PS3.spr"

    # path images
    path_small_images = os.path.join("lib", "character_parameters_editor", "images", "small")
    path_large_images = os.path.join("lib", "character_parameters_editor", "images", "large")
    path_fourSlot_images = os.path.join("lib", "character_parameters_editor", "images", "fourSlot")
    path_controller_images = os.path.join("lib", "character_parameters_editor", "images", "controller")
    path_small_four_slot_images = os.path.join(path_fourSlot_images, "small")

    # Color for the borders
    styleSheetSelectSlotRoster = "QLabel {border : 3px solid black;}"
    styleSheetSelectTransRoster = "QLabel {border : 3px solid red;}"
    styleSheetSelectCharaRoster = "QLabel {border : 3px solid cyan;}"
    styleSheetSlotRosterWindow = "QLabel {border : 3px solid black;}"
    styleSheetSelectTransRosterWindow = "QLabel {border : 5px solid red;}"
    styleSheetSelectFusionRosterWindow = "QLabel {border : 5px solid  #33ff44;}"
    styleSheetSelectCharaRosterWindow = "QLabel {border : 5px solid cyan;}"

    # ID of the character
    file_character_id = ""

    # Flag that will tell us if the character has been changed in the main panel (avoid combo box)
    change_character = False
