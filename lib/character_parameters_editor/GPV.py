

class GPV:

    # Flag that will tell us if the user has loaded the operate_character_parameters file
    operate_resident_param_file = False
    # path for character info, transformer, skill and game_resident_character_param.da
    resident_character_inf_path = ""
    resident_transformer_i_path = ""
    resident_skill_path = ""
    game_resident_character_param = ""
    # number of bytes between each character
    sizeVisualParameters = 148
    sizeTrans = 33
    sizeCharacterParam = 56
    # Values for the combo box
    trans_effect_values = dict({"Super Saiyan": 0, "Metamoru": 1, "Potara": 2, "Cell": 3, "Super Buu": 4,
                               "Broly": 5, "Freezer": 6, "Super Saiyan 3": 7, "Cooler": 8, "Bojack": 9, "C-13": 10,
                                "Nothing": 11})
    trans_animation_values = dict({"Transform": 0, "Return": 1, "Transform 2": 4, "Absorb": 6, "Special": 12})
    fusion_animation_values = dict({"Metamoru": 0, "Potara": 1})
    color_lightning_values = dict({"Blue": 0, "Cyan": 1, "Rose": 2, "Rose and white": 3})
    glow_lightning_values = dict({"Disabled": 0, "Glow": 1, "Unknown (Androids)": 2, "Lightnings": 4,
                                  "Glow + lightnings": 5})
    aura_type_values = dict({'Plasma Aura ': 0, 'Earth Warriors ': 1, 'Wicked Saiyan': 2, 'Super Saiyan': 3,
                             'Super Saiyan 2': 4, 'Super Saiyan 3': 5, 'Bojack': 6, 'Evil Warrior': 7, 'Dabura': 8,
                             'Gohan': 9, 'Majin Buu ': 10, 'Broly': 11, 'Hatchiyack': 12, 'Android': 13,
                             'Android #13': 14, 'Nappa': 15, 'Jeice': 16, 'Ginyu': 17, 'Zarbon': 18,
                             'Burter': 19, 'Frieza': 20, 'Super Janemba': 21, 'Majin Vegeta': 22, 'Videl': 23,
                             'Red Flame ': 24, 'Blue Flame': 25})

    # panelPortraistlist
    mini_portraits_image = []

    # portraits object for the Select Character window
    previous_chara_selected_character_window = 100
    mini_portraits_image_select_chara_window = []

    # List of character with their data from the file
    character_list = []  # It stores the instances of character with all the info stored within
    chara_selected = 0  # Index of the char selected in the main panel
    trans_slot_panel_selected = 0  # Slot thas is being edited for the transformations
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

    # Outputname for the signature skill
    signature_output_name = "signature"
