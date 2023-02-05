from lib.character_parameters_editor.classes.SignatureKiBlast import SignatureKiBlast


class IPV:

    # Paths
    character_i_path = ""
    camera_i_path = ""
    blast_i_path = ""
    # Warning base message when importing a bone that doesn't exists in memory
    message_bone_import_doesnt_exists = "The following bones are new for the current animation:"
    # Indexes
    signature_folder_index_list_view = None
    # Regex values
    skill_chara_XXX_m_regex = "skill_chara_0[0-9][0-9]_m"
    # Values for the combo box
    type_of_fighting_values = dict({"Type 1": 0, "Type 2": 1, "Type 3": 2, "Type 4": 3, "Type 5": 10, "Type 6": 11,
                                    "Type 7": 12})
    cancel_set_values = dict({"Cancel 1": 0, "Cancel 2": 1, "Cancel 3": 2, "Cancel 4": 3, "Cancel 5": 4,
                              "Cancel 6": 5, "Cancel 7": 6, "Cancel 8": 7, "Cancel 9": 8, "Cancel 10": 9,
                              "Cancel 11": 10, "Cancel 12": 11, "Cancel 13": 13, "Cancel 14": 14})
    direction_last_hit_combo_values = dict({"Forward": 0, "Up": 1, "Down": 2, "Left": 3, "Right": 4})
    color_background_values = dict({"Red": 76, "Pink": 84, "Blue": 88, "Lighter Blue": 86, "Purple": 80,
                                    "Golden": 98, "Yellow": 94, "Darkner Yellow": 74, "Lighter Yellow": 92,
                                    "Lighter Green": 31, "Green": 90, "Black": 78, "Gray": 82, "Unknown": 99,
                                    "Unknown 2": 28})
    # Camera properties
    # Don't change the order, because the file has this order when we read the file
    camera_types_cutscene = ["Entry (1P)", "Entry (2P)", "Entry 2 (1P)", "Entry 2 (2P)", "Entry 3 (1P)",
                             "Entry 3 (2P)", "Victory", "Lose", "Transform in", "Transform result", "Return in",
                             "Return out", "Transform in 2", "Blast Attack 0", "Blast Attack 1", "Blast Attack 2",
                             "Blast Attack 3", "Blast Attack 4", "Blast Attack 5", "Blast Attack 6", "Blast Attack 7",
                             "Blast Attack 8", "Blast Attack 9", "Blast Attack 10", "Blast Attack 11", "Blast Attack 12",
                             "Blast Attack 13", "Unknown"]
    # position where the first camera cutscene starts
    position_camera_cutscene = 208
    size_each_camera_cutscene = 52
    camera_extension = "cam"
    # Animation properties
    # Don't change the order, because the file has this order when we read the file
    animations_types = ["Idle ground", "Idle fly", "Charge", "Charge max", "Idle ground tired", "Idle fly tired",
                        "Dash", "Rush attack ground", "Rush attack ground 2", "Rush attack ground 3",
                        "Rush attack ground 4", "Rush attack ground 5", "Rush attack fly", "Rush attack fly 2",
                        "Rush attack fly 3", "Rush attack fly 4", "Rush attack fly 5", "Smash attack left",
                        "Smash attack right", "Smash attack 2", "Smash attack 3", "Smash attack 4", "Smash attack high",
                        "Smash attack low", "Finish attack teleport", "Charge attack", "Charge attack high",
                        "Charge attack low", "Charge attack left", "Charge attack right", "Dash attack",
                        "Dash charge attack", "Dash charge attack high", "Dash charge attack low",
                        "Dash charge attack left", "Dash charge attack right", "Shot Ki left hand",
                        "Shot Ki right hand", "Charge shot Ki", "Charge shot Ki high", "Charge shot Ki low",
                        "Shot Ki moving forward", "Shot Ki moving left", "Shot Ki moving right", "Shot Ki moving back",
                        "Charged shot Ki moving forward", "Charged shot Ki moving left", "Charged shot Ki moving right",
                        "Charged shot Ki moving back", "Jump attack", "Jump Ki shot left", "Jump Ki shot right",
                        "Jump charged Ki shot", "Throw catch", "Throw", "Throw wall", "Guard", "Transformation in",
                        "Transformation result", "Return in", "Return out", "Fusion in", "Fusion result", "Fusion demo",
                        "Potara in", "Potara result", "Potara demo", "Entry 1", "Entry 2", "Entry 3", "Victory", "Lose",
                        "Signature"]
    animations_extension = "spas"
    animation_extension = "spa"
    animation_bone_extension = "json"
    # Blast properties
    glow_values = dict({"Disabled": 0, "0x01": 1, "0x02": 2, "0x03": 3, "0x04": 4, "0x06": 6, "0x07": 7, "0x08": 8, "0x09": 9, "0x0A": 10, "0x0C": 12,
                        "0x0D": 13, "0x0E": 14, "0x0F": 15, "Enabled": 16})
    stackable_skill = dict({"Infinite": 0, "3 times": 1, "Disabled": 2})
    activation_skill = dict({"Nothing": 0, "0x02": 2, "0x04": 4, "0x05": 5, "0x08": 8, "0x0A": 10, "0x0C": 12, "0x0D": 13, "0x40": 64, "0x48": 72,
                             "0x82": 130, "0x84": 132, "0x85": 133, "0x86": 134, "0x96": 150})
    chargeable_boost = dict({"Nothing": 0, "0x02": 2, "0x08": 8, "0x10": 16, "0x12": 18, "0x14": 20, "0x32": 50, "0x31": 49, "0x35": 53, "0x36": 54,
                             "0x50": 80, "0x71": 113, "0xB0": 176})
    melee_power_up_properties = dict({"Nothing": 0, "Power up": 10, "Power up 2": 15})
    defense_power_up_properties = dict({"Nothing": 0, "0x05": 5})
    super_attack_power_up_properties = dict({"Nothing": 0, "0x1E": 30})
    ki_power_up_properties = dict({"Nothing": 0, "Consumption reduced": 100})
    size_between_blast = 100
    blast_extension = "bla"
    # This var will be used to store the ID of the partner character so we can clean the Window
    old_selected_partner = 0
    # Transformation effect values
    trans_effect_identification_file = b'<#\xd7\n'
    trans_effect_position_byte = 0
    # Signature ki blast var. This will store the parameters of the signature when a Ki blast is triggered
    signature_ki_blast = SignatureKiBlast()
