

class IPV:

    character_i_path = ""
    camera_i_path = ""
    blast_i_path = ""
    # Values for the combo box
    type_of_fighting_values = dict({"Type 1": 0, "Type 2": 1, "Type 3": 2, "Type 4": 3, "Type 5": 10, "Type 6": 11,
                                    "Type 7": 12})
    cancel_set_values = dict({"Cancel 1": 0, "Cancel 2": 1, "Cancel 3": 2, "Cancel 4": 3, "Cancel 5": 4,
                              "Cancel 6": 5, "Cancel 7": 6, "Cancel 8": 7, "Cancel 9": 8, "Cancel 10": 9,
                              "Cancel 11": 10, "Cancel 12": 11, "Cancel 13": 13, "Cancel 14": 14})
    direction_last_hit_combo_values = dict({"Forward": 0, "Up": 1, "Down": 2, "Left": 3, "Right": 4})
    color_background_values = dict({"Red": 76, "Pink": 84, "Blue": 88, "Lighter Blue": 86, "Purple": 80,
                                    "Golden": 98, "Yellow": 94, "Darkner Yellow": 74, "Lighter Yellow": 92,
                                    "Black": 78,  "Gray": 82})
    # Camera properties
    # Don't change the order, because the file has this order when we read the file
    camera_types_cutscene = ["Entry (1P)", "Entry (2P)", "Entry 2 (1P)", "Entry 2 (2P)", "Entry 3 (1P)",
                             "Entry 3 (2P)", "Victory", "Lose", "Transform in", "Transform result", "Return in",
                             "Return out", "Transform in 2"]
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
                        "Transformation result", "Return in", "Return out", "Fusion in", "Fusion result", "Potara in",
                        "Potara result", "Entry 1", "Entry 2", "Entry 3", "Victory", "Lose"]
    animations_extension = "spas"
    # Distance between the 'buffer' folders
    size_between_animation_and_effects = 363
    # Blast properties
    size_between_blast = 100
    blast_extension = "bla"
    # Transformation effect values
    trans_effect_identification_file = b'<#\xd7\n'
    trans_effect_position_byte = 0
