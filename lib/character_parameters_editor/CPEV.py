from lib.packages import os


class CPEV:

    # Allowed files
    operate_resident_param = 'operate_resident_param'
    operate_character_XXX_m_regex = "operate_character_0[0-9][0-9]_m"

    # path images
    path_small_images = os.path.join("lib", "character_parameters_editor", "images", "small")
    path_large_images = os.path.join("lib", "character_parameters_editor", "images", "large")
    path_fourSlot_images = os.path.join("lib", "character_parameters_editor", "images", "fourSlot")
    path_small_four_slot_images = os.path.join(path_fourSlot_images, "small")

    # path for character info and transformer (operate_resident_param)
    resident_character_inf_path = ""
    resident_transformer_i_path = ""
    # number of bytes between each character
    sizeVisualParameters = 148
    sizeTrans = 33
    # Values for the combo box
    trans_effect_values = dict({"Super Saiyan": 0, "Metamoru": 1, "Potara": 2, "Cell": 3, "Super Buu": 4,
                               "Broly": 5, "Freezer": 6, "Super Saiyan 3": 7, "Cooler": 8, "Bojack": 9, "C-13": 10,
                                "Nothing": 11})
    trans_animation_values = dict({"Transform": 0, "Return": 1, "Transform 2": 4, "Absorb": 6, "Special": 12})
    fusion_animation_values = dict({"Metamoru": 0, "Potara": 1})
    color_lightning_values = dict({"Blue": 0, "Cyan": 1, "Rose": 2, "Rose and white": 3})
    glow_lightning_values = dict({"Disabled": 0, "Glow": 1, "Unknown (Androids)": 2, "Lightnings": 4,
                                  "Glow + lightnings": 5})

    # operate_character_XXX_m
    # path and positions of files and data
    character_i_path = ""
    camera_i_path = ""
    # Values for the combo box
    type_of_fighting_values = dict({"Type 1": 0, "Type 2": 1, "Type 3": 2, "Type 4": 3, "Type 5": 10, "Type 6": 11,
                                    "Type 7": 12})
    direction_last_hit_combo_values = dict({"Forward": 0, "Up": 1, "Down": 2, "Left": 3, "Right": 4})
    color_background_combo_values = dict({"Blue": 88, "Yellow 1": 94, "Yellow 2": 92, "Gray": 82, "Purple": 80,
                                          "Red": 76, "Black": 78})
    # Don't change the order, because the file has this order when we read the file
    camera_types_cutscene = ["Entry (1P)", "Entry (2P)", "Entry 2 (1P)", "Entry 2 (2P)", "Entry 3 (1P)",
                             "Entry 3 (2P)", "Victory", "Lose", "Transform in", "Transform result", "Return in",
                             "Return out", "Transform in 2"]
    # position where the first camera cutscene starts
    position_camera_cutscene = 208
    size_each_camera_cutscene = 52

    # panelPortraistlist
    mini_portraits_image = []

    # portraits object for the Select Character window
    previous_chara_selected_character_window = 100
    mini_portraits_image_select_chara_window = []

    # List of character with their data from the file
    character_list = []
    chara_selected = 0  # Index of the char selected in the main panel
    change_character = False  # Flag that will tell us if the character has been changed in the main panel
    trans_slot_panel_selected = 0   # Slot thas is being edited for the transformations
    transformation_partner_flag = False  # Flag transformation partner slot to know if the user has selected that
    fusion_slot_panel_selected = 0  # Slot that is being edited for the fusions
    # Flag for fusion partner (trigger 0, visual 1) slot to know if the user has selected that
    fusion_partner_flag = [False, False]
    # Array of the characters that has been edited
    character_list_edited = []

    # Store what character has original transform version
    characters_with_trans = [0, 5, 8, 17, 22, 24, 27, 29, 31, 34, 40, 48, 58, 63, 67, 79, 82, 85, 88]
    # Store what transformations has the character originally
    characters_with_trans_index = [[1, 2, 3], [6, 7], [9, 10], [18, 19, 20], [23], [25, 26], [28], [30], [32, 33],
                                   [35], [41], [49, 50, 51, 52], [59, 60, 61], [64, 65], [68, 69], [80], [83], [86],
                                   [89]]
