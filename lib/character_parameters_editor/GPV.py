

class GPV:

    # path for character info and transformer
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

    # panelPortraistlist
    mini_portraits_image = []

    # portraits object for the Select Character window
    previous_chara_selected_character_window = 100
    mini_portraits_image_select_chara_window = []

    # List of character with their data from the file
    character_list = []
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
