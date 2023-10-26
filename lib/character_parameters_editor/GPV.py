

class GPV:

    # Flag that will tell us if the user has loaded the operate_character_parameters or, db_font_pad_PS3_s_d and db_font_pad_X360_s_d
    operate_resident_param_file = False
    db_font_pad_XYZ_s_d = False
    # path for character info, transformer, skill and game_resident_character_param.da
    resident_character_inf_path = ""
    resident_transformer_i_path = ""
    resident_skill_path = ""
    game_resident_character_param = ""
    cs_main_dat = ""
    # number of bytes between each character
    sizeVisualParameters = 148
    sizeTrans = 33
    sizeCharacterParam = 56
    sizeCharacterCsMainDat = 80
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

    # select general chara window portraits
    mini_portraits_image_select_chara = []

    # portraits object for the Select Character window
    previous_chara_selected_character_window = 100
    mini_portraits_image_select_chara_trans_fusion_window = []

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

    # Outputname for the signature skill
    signature_output_name = "Signature_parameters"
