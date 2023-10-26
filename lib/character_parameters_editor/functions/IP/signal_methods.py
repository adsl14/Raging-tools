from lib.character_parameters_editor.functions.IP.auxiliary import change_camera_cutscene_values, change_blast_values


def add_array_of_animation(animation_type_value_combo_box, combo_box_label, item_data_animation):
    animation_type_value_combo_box.setItemData(animation_type_value_combo_box.findText(combo_box_label), item_data_animation)


def set_first_index_animation_type_value(animation_type_value):
    animation_type_value.setCurrentIndex(0)


def set_character_info(main_window, character_info):

    # Speed of charging
    main_window.speed_of_charging_value.setValue(character_info.speed_of_charging_value)
    main_window.speed_of_charging_value_2.setValue(character_info.speed_of_charging_value_2)
    # Ki regeneration rate
    main_window.ki_regeneration_rate_value.setValue(character_info.ki_regeneration_rate_value)

    # Ki cost of dash
    main_window.ki_cost_of_dash_value.setValue(character_info.ki_cost_of_dash_value)

    # Movement speed normal and sidestep
    main_window.movement_speed_value.setValue(character_info.movement_speed_value)
    main_window.sidestep_speed_value.setValue(character_info.sidestep_speed_value)

    # Movement speed up and down
    main_window.up_speed_value.setValue(character_info.up_speed_value)
    main_window.down_speed_value.setValue(character_info.down_speed_value)
    main_window.dash_up_speed_value.setValue(character_info.dash_up_speed_value)
    main_window.dash_down_speed_value.setValue(character_info.dash_down_speed_value)

    # Attack damage
    main_window.attack_value.setValue(character_info.attack_value)
    # Ki blast damage
    main_window.blast_damage_value.setValue(character_info.blast_damage_value)

    # Defense/Armor
    main_window.defense_value.setValue(character_info.defense_value)

    # Number of ki blasts
    main_window.number_ki_blasts_value.setValue(character_info.number_ki_blasts_value)

    # Cost of ki blast
    main_window.cost_of_blast_value.setValue(character_info.cost_of_blast_value)
    # Size of ki blast
    main_window.size_of_blast_value.setValue(character_info.size_of_blast_value)

    # Cancel set and Type fighting
    main_window.cancel_set_value.setCurrentIndex(main_window.cancel_set_value.findData(character_info.cancel_set_value))
    main_window.type_fighting_value.setCurrentIndex(main_window.type_fighting_value.findData(character_info.type_fighting_value))

    # Direction last hit fast combo
    main_window.direction_last_hit_combo_value.setCurrentIndex(main_window.direction_last_hit_combo_value.findData(character_info.direction_last_hit_combo_value))

    # Color background fast combo
    main_window.background_color_combo_value.setCurrentIndex(main_window.background_color_combo_value.findData(character_info.background_color_combo_value))


def set_camera_type(camera_type_key_combo_box, i, camera_cutscene):
    camera_type_key_combo_box.setItemData(i, camera_cutscene)


def show_first_item_camera(main_window):
    main_window.camera_type_key.setCurrentIndex(0)
    change_camera_cutscene_values(main_window, main_window.camera_type_key.itemData(0))


def set_blast_combo_box(blast_key_combo_box, i, blast):
    blast_key_combo_box.setItemData(i, blast)


def show_first_item_blast(main_window):
    main_window.blast_key.setCurrentIndex(0)
    change_blast_values(main_window, main_window.blast_key.itemData(0))


def enable_individual_parameters_tab(main_window):

    # Open the tab (character parameters editor)
    if main_window.tabWidget.currentIndex() != 2:
        main_window.tabWidget.setCurrentIndex(2)

    # Open the tab operate_character_XXX_m
    if main_window.tabWidget_2.currentIndex() != 1:
        main_window.tabWidget_2.setCurrentIndex(1)

    # Enable completely the tab character parameters editor
    if not main_window.character_parameters_editor.isEnabled():
        main_window.character_parameters_editor.setEnabled(True)

    # Disable all the buttons (character parameters editor -> operate_resident_param)
    if main_window.general_parameters_frame.isEnabled():
        main_window.general_parameters_frame.setEnabled(False)
    # Enable all the buttons (character parameters editor -> operate_character_XXX_m)
    if not main_window.operate_character_xyz_m_frame.isEnabled():
        main_window.operate_character_xyz_m_frame.setEnabled(True)
    # Disable all the buttons (character parameters editor -> cs_chip)
    if main_window.cs_chip.isEnabled():
        main_window.cs_chip.setEnabled(False)
