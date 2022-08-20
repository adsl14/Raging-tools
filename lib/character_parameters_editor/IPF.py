from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.IPV import IPV
from lib.character_parameters_editor.classes.Blast import Blast
from lib.character_parameters_editor.classes.CameraCutscene import CameraCutscene
from lib.character_parameters_editor.classes.Animation import Animation
from lib.character_parameters_editor.functions.IP.action_logic import on_camera_type_key_changed, \
    action_export_camera_button_logic, action_import_camera_button_logic, action_export_all_camera_button_logic, \
    action_import_all_camera_button_logic, on_pivot_value_changed, on_translations_changed, on_rotations_changed, \
    on_speed_camera_changed, on_zoom_start_value_changed, on_zoom_end_value_changed, on_unk13_value_changed, \
    action_export_animation_button_logic, action_import_animation_button_logic, \
    action_export_all_animation_button_logic, action_import_all_animation_button_logic, \
    action_export_blast_button_logic, action_import_blast_button_logic, action_export_all_blast_button_logic, \
    action_import_all_blast_button_logic, on_background_color_trans_change
from lib.character_parameters_editor.functions.IP.auxiliary import read_transformation_effect
from lib.packages import struct, QMessageBox


def initialize_operate_character(main_window):

    # Set the camera cutscene type
    main_window.camera_type_key.currentIndexChanged.connect(lambda: on_camera_type_key_changed(main_window))
    for element in IPV.camera_types_cutscene:
        main_window.camera_type_key.addItem(element)
    # Export camera button
    main_window.exportCameraButton.clicked.connect(lambda: action_export_camera_button_logic(main_window))
    # Import camera button
    main_window.importCameraButton.clicked.connect(lambda: action_import_camera_button_logic(main_window))
    # Export all camera button
    main_window.exportAllCameraButton.clicked.connect(lambda: action_export_all_camera_button_logic(main_window))
    # Import all camera button
    main_window.importAllCameraButton.clicked.connect(lambda: action_import_all_camera_button_logic(main_window))

    # Set the pivots
    main_window.pivot_value.valueChanged.connect(lambda: on_pivot_value_changed(main_window, pivot_index=0))
    main_window.pivot_value_2.valueChanged.connect(lambda: on_pivot_value_changed(main_window, pivot_index=1))
    main_window.pivot_value_3.valueChanged.connect(lambda: on_pivot_value_changed(main_window, pivot_index=2))
    main_window.pivot_value_4.valueChanged.connect(lambda: on_pivot_value_changed(main_window, pivot_index=3))

    # Set the translations
    main_window.translation_y_start_value.valueChanged.connect(lambda: on_translations_changed(main_window, y=0, z=-1))
    main_window.translation_y_end_value.valueChanged.connect(lambda: on_translations_changed(main_window, y=1, z=-1))
    main_window.translation_z_start_value.valueChanged.connect(lambda: on_translations_changed(main_window, y=-1, z=0))
    main_window.translation_z_end_value.valueChanged.connect(lambda: on_translations_changed(main_window, y=-1, z=1))

    # Set the rotations
    main_window.rotation_y_start_value.valueChanged.connect(lambda: on_rotations_changed(main_window, y=0, z=-1))
    main_window.rotation_y_end_value.valueChanged.connect(lambda: on_rotations_changed(main_window, y=1, z=-1))
    main_window.rotation_z_start_value.valueChanged.connect(lambda: on_rotations_changed(main_window, y=-1, z=0))
    main_window.rotation_z_end_value.valueChanged.connect(lambda: on_rotations_changed(main_window, y=-1, z=1))

    # Set the speed
    main_window.speed_camera_value.valueChanged.connect(lambda: on_speed_camera_changed(main_window))

    # Set the zoom
    main_window.zoom_start_value.valueChanged.connect(lambda: on_zoom_start_value_changed(main_window))
    main_window.zoom_end_value.valueChanged.connect(lambda: on_zoom_end_value_changed(main_window))

    # Set unk13
    main_window.unk13_value.valueChanged.connect(lambda: on_unk13_value_changed(main_window))

    # Set the cancel set
    for element in IPV.cancel_set_values:
        main_window.cancel_set_value.addItem(element, IPV.cancel_set_values[element])

    # Set the fighting style
    for element in IPV.type_of_fighting_values:
        main_window.type_fighting_value.addItem(element, IPV.type_of_fighting_values[element])

    # Set the direction last hit combo
    for element in IPV.direction_last_hit_combo_values:
        main_window.direction_last_hit_combo_value.addItem(element, IPV.direction_last_hit_combo_values[element])

    # Set the background color combo
    # Set the transformation background color
    for element in IPV.color_background_values:
        main_window.background_color_combo_value.addItem(element, IPV.color_background_values[element])
        main_window.background_color_trans_value.addItem(element, IPV.color_background_values[element])
    main_window.background_color_trans_value.currentIndexChanged.connect(lambda:
                                                                         on_background_color_trans_change(main_window))

    # Set animations
    for element in IPV.animations_types:
        main_window.animation_type.addItem(element)
    # Export animation button
    main_window.exportAnimationButton.clicked.connect(
        lambda: action_export_animation_button_logic(main_window, main_window.animation_type))
    # Import animation button
    main_window.importAnimationButton.clicked.connect(
        lambda: action_import_animation_button_logic(main_window, main_window.animation_type))
    # Export all animation button
    main_window.exportAllAnimationButton.clicked.connect(
        lambda: action_export_all_animation_button_logic(main_window, main_window.animation_type))
    # Import all animation button
    main_window.importAllAnimationButton.clicked.connect(
        lambda: action_import_all_animation_button_logic(main_window, main_window.animation_type))
    # Set animations properties
    for element in IPV.animations_types:
        main_window.animation_properties.addItem(element)
    # Export animation properties button
    main_window.exportAnimationPropertiesButton.clicked.connect(
        lambda: action_export_animation_button_logic(main_window, main_window.animation_properties))
    # Import animation properties button
    main_window.importAnimationPropertiesButton.clicked.connect(
        lambda: action_import_animation_button_logic(main_window, main_window.animation_properties))
    # Export all animation properties button
    main_window.exportAllAnimationPropertiesButton.clicked.connect(
        lambda: action_export_all_animation_button_logic(main_window, main_window.animation_properties, "_properties"))
    # Import all animation properties button
    main_window.importAllAnimationPropertiesButton.clicked.connect(
        lambda: action_import_all_animation_button_logic(main_window, main_window.animation_properties))

    # Set the blast type
    for i in range(0, 14):
        main_window.blast_key.addItem("Attack " + str(i))
    # Export blast button
    main_window.exportBlastButton.clicked.connect(lambda: action_export_blast_button_logic(main_window))
    # Import blast button
    main_window.importBlastButton.clicked.connect(lambda: action_import_blast_button_logic(main_window))
    # Export all blast button
    main_window.exportAllBlastButton.clicked.connect(lambda: action_export_all_blast_button_logic(main_window))
    # Import all blast button
    main_window.importAllBlastButton.clicked.connect(lambda: action_import_all_blast_button_logic(main_window))


def read_single_character_parameters(main_window):

    # character info
    IPV.character_i_path = main_window.listView_2.model().item(726, 0).text()
    # camera info
    IPV.camera_i_path = main_window.listView_2.model().item(727, 0).text()
    # blast info
    IPV.blast_i_path = main_window.listView_2.model().item(728, 0).text()

    # Read all the animation values
    read_animation_files(main_window, 0, main_window.animation_type)
    main_window.animation_type.setCurrentIndex(0)
    read_animation_files(main_window, IPV.size_between_animation_and_effects, main_window.animation_properties)
    main_window.animation_properties.setCurrentIndex(0)

    # Read character info file
    with open(IPV.character_i_path, mode="rb") as file:

        # Speed of charging
        main_window.speed_of_charging_value.setValue(struct.unpack('>f', file.read(4))[0])
        main_window.speed_of_charging_value_2.setValue(struct.unpack('>f', file.read(4))[0])
        # Ki regeneration rate
        main_window.ki_regeneration_rate_value.setValue(struct.unpack('>f', file.read(4))[0])

        # Ki cost of dash
        file.seek(4, 1)
        main_window.ki_cost_of_dash_value.setValue(struct.unpack('>f', file.read(4))[0])

        # Movement speed normal and sidestep
        file.seek(12, 1)
        main_window.movement_speed_value.setValue(struct.unpack('>f', file.read(4))[0])
        main_window.sidestep_speed_value.setValue(struct.unpack('>f', file.read(4))[0])

        # Movement speed up and down
        file.seek(12, 1)
        main_window.up_speed_value.setValue(struct.unpack('>f', file.read(4))[0])
        main_window.down_speed_value.setValue(struct.unpack('>f', file.read(4))[0])
        main_window.dash_up_speed_value.setValue(struct.unpack('>f', file.read(4))[0])
        main_window.dash_down_speed_value.setValue(struct.unpack('>f', file.read(4))[0])

        # Attack damage
        file.seek(4, 1)
        main_window.attack_value.setValue(int.from_bytes(file.read(2), byteorder='big'))
        # Ki blast damage
        file.seek(4, 1)
        main_window.blast_damage_value.setValue(int.from_bytes(file.read(2), byteorder='big'))

        # Defense/Armor
        file.seek(1, 1)
        main_window.defense_value.setValue(int.from_bytes(file.read(1), byteorder='big'))

        # Number of ki blasts
        file.seek(31, 1)
        main_window.number_ki_blasts_value.setValue(int.from_bytes(file.read(1), byteorder='big'))

        # Cost of ki blast
        file.seek(13, 1)
        main_window.cost_of_blast_value.setValue(int.from_bytes(file.read(1), byteorder='big'))
        # Size of ki blast
        main_window.size_of_blast_value.setValue(struct.unpack('>f', file.read(4))[0])

        # Cancel set and Type fighting
        file.seek(8, 1)
        main_window.cancel_set_value.setCurrentIndex(main_window.cancel_set_value.findData
                                                     (int.from_bytes(file.read(1), "big")))
        main_window.type_fighting_value.setCurrentIndex(main_window.type_fighting_value.findData
                                                        (int.from_bytes(file.read(1), "big")))

        # Direction last hit fast combo
        file.seek(1, 1)
        main_window.direction_last_hit_combo_value.setCurrentIndex(main_window.direction_last_hit_combo_value.findData
                                                                   (int.from_bytes(file.read(1), "big")))

        # Color background fast combo
        file.seek(3, 1)
        main_window.background_color_combo_value.setCurrentIndex(main_window.background_color_combo_value.findData
                                                                 (int.from_bytes(file.read(1), "big")))

    # Read camera info file
    with open(IPV.camera_i_path, mode="rb") as file:

        # Move to position 208 where the first camera cutscene starts
        file.seek(IPV.position_camera_cutscene)

        for i in range(0, len(IPV.camera_types_cutscene)):
            # Create an instance of cameraCutscene
            camera_cutscene = CameraCutscene()

            # Get the pivots
            camera_cutscene.pivots["pivot_1"] = int.from_bytes(file.read(1), byteorder='big')
            camera_cutscene.pivots["pivot_2"] = int.from_bytes(file.read(1), byteorder='big')
            camera_cutscene.pivots["pivot_3"] = int.from_bytes(file.read(1), byteorder='big')
            camera_cutscene.pivots["pivot_4"] = int.from_bytes(file.read(1), byteorder='big')

            # Rotations Z
            camera_cutscene.rotations["Z_start"] = struct.unpack('>f', file.read(4))[0]
            camera_cutscene.rotations["Z_end"] = camera_cutscene.rotations["Z_start"] + \
                struct.unpack('>f', file.read(4))[0]

            # Translations Y
            camera_cutscene.positions["Y_start"] = struct.unpack('>f', file.read(4))[0]
            camera_cutscene.positions["Y_end"] = camera_cutscene.positions["Y_start"] + \
                struct.unpack('>f', file.read(4))[0]

            # Rotations Y
            camera_cutscene.rotations["Y_start"] = struct.unpack('>f', file.read(4))[0]
            camera_cutscene.rotations["Y_end"] = camera_cutscene.rotations["Y_start"] + \
                struct.unpack('>f', file.read(4))[0]

            # Zoom
            camera_cutscene.zooms["Zoom_start"] = struct.unpack('>f', file.read(4))[0]
            camera_cutscene.zooms["Zoom_end"] = camera_cutscene.zooms["Zoom_start"] + \
                struct.unpack('>f', file.read(4))[0]

            # Translations Z
            camera_cutscene.positions["Z_start"] = struct.unpack('>f', file.read(4))[0]
            camera_cutscene.positions["Z_end"] = camera_cutscene.positions["Z_start"] + \
                struct.unpack('>f', file.read(4))[0]

            # Camera speed (float values)
            camera_cutscene.camera_speed = struct.unpack('>f', file.read(4))[0]

            # Unknown value block 13
            camera_cutscene.unknown_block_13 = struct.unpack('>f', file.read(4))[0]

            # Set camera type combo box
            main_window.camera_type_key.setItemData(i, camera_cutscene)

        # Show the first item in the combo box and his values
        main_window.camera_type_key.setCurrentIndex(0)
        change_camera_cutscene_values(main_window, main_window.camera_type_key.itemData(0))

    # Read blast info file
    with open(IPV.blast_i_path, mode="rb") as file:

        for i in range(0, 14):
            # Create an instance of Blast
            blast = Blast()

            # Read data
            blast.data = file.read(IPV.size_between_blast)

            # Set blast combo box
            main_window.blast_key.setItemData(i, blast)

        # Show the first item in the combo box and his values
        main_window.blast_key.setCurrentIndex(0)


def write_single_character_parameters(main_window):

    # Save all animation info (replace first the entire files)
    for i in range(0, len(IPV.animations_types)):
        animation_files = main_window.animation_type.itemData(i)
        animation_properties_files = main_window.animation_properties.itemData(i)

        for j in range(0, len(animation_files)):
            if animation_files[j].modified:
                with open(animation_files[j].path, mode="wb") as file:
                    file.write(animation_files[j].data)

            if animation_properties_files[j].modified:
                with open(animation_properties_files[j].path, mode="wb") as file:
                    file.write(animation_properties_files[j].data)

    # Save all character info
    with open(IPV.character_i_path, mode="rb+") as file:
        # Speed of charging
        file.write(struct.pack('>f', main_window.speed_of_charging_value.value()))
        file.write(struct.pack('>f', main_window.speed_of_charging_value_2.value()))
        # Ki regeneration rate
        file.write(struct.pack('>f', main_window.ki_regeneration_rate_value.value()))

        # Ki cost of dash
        file.seek(4, 1)
        file.write(struct.pack('>f', main_window.ki_cost_of_dash_value.value()))

        # Movement speed normal and sidestep
        file.seek(12, 1)
        file.write(struct.pack('>f', main_window.movement_speed_value.value()))
        file.write(struct.pack('>f', main_window.sidestep_speed_value.value()))

        # Movement speed up and down
        file.seek(12, 1)
        file.write(struct.pack('>f', main_window.up_speed_value.value()))
        file.write(struct.pack('>f', main_window.down_speed_value.value()))
        file.write(struct.pack('>f', main_window.dash_up_speed_value.value()))
        file.write(struct.pack('>f', main_window.dash_down_speed_value.value()))

        # Attack damage
        file.seek(4, 1)
        file.write(main_window.attack_value.value().to_bytes(2, byteorder="big"))
        # Ki blast damage
        file.seek(4, 1)
        file.write(main_window.blast_damage_value.value().to_bytes(2, byteorder="big"))

        # Defense/Armor
        file.seek(1, 1)
        file.write(main_window.defense_value.value().to_bytes(1, byteorder="big"))

        # Number of ki blasts
        file.seek(31, 1)
        file.write(main_window.number_ki_blasts_value.value().to_bytes(1, byteorder="big"))

        # Cost of ki blast
        file.seek(13, 1)
        file.write(main_window.cost_of_blast_value.value().to_bytes(1, byteorder="big"))
        # Size of ki blast
        file.write(struct.pack('>f', main_window.size_of_blast_value.value()))

        # Cancel set and Type fighting
        file.seek(8, 1)
        file.write(main_window.cancel_set_value.currentData().to_bytes(1, byteorder="big"))
        file.write(main_window.type_fighting_value.currentData().to_bytes(1, byteorder="big"))

        # Direction last hit fast combo
        file.seek(1, 1)
        file.write(main_window.direction_last_hit_combo_value.currentData().to_bytes(1, byteorder="big"))

        # Color background fast combo
        file.seek(3, 1)
        file.write(main_window.background_color_combo_value.currentData().to_bytes(1, byteorder="big"))

    # Save all camera info
    with open(IPV.camera_i_path, mode="rb+") as file:

        # Move to position 208 where the first camera cutscene starts
        file.seek(IPV.position_camera_cutscene)

        for i in range(0, len(IPV.camera_types_cutscene)):

            camera_cutscene = main_window.camera_type_key.itemData(i)

            # Camera has been modified
            if camera_cutscene.modified:
                # Write the pivots
                file.write(camera_cutscene.pivots["pivot_1"].to_bytes(1, byteorder="big"))
                file.write(camera_cutscene.pivots["pivot_2"].to_bytes(1, byteorder="big"))
                file.write(camera_cutscene.pivots["pivot_3"].to_bytes(1, byteorder="big"))
                file.write(camera_cutscene.pivots["pivot_4"].to_bytes(1, byteorder="big"))

                # Rotations Z
                file.write(struct.pack('>f', camera_cutscene.rotations["Z_start"]))
                file.write(struct.pack('>f', camera_cutscene.rotations["Z_end"] - camera_cutscene.rotations["Z_start"]))

                # Translations Y
                file.write(struct.pack('>f', camera_cutscene.positions["Y_start"]))
                file.write(struct.pack('>f', camera_cutscene.positions["Y_end"] - camera_cutscene.positions["Y_start"]))

                # Rotations Y
                file.write(struct.pack('>f', camera_cutscene.rotations["Y_start"]))
                file.write(struct.pack('>f', camera_cutscene.rotations["Y_end"] - camera_cutscene.rotations["Y_start"]))

                # Zoom
                file.write(struct.pack('>f', camera_cutscene.zooms["Zoom_start"]))
                file.write(struct.pack('>f', camera_cutscene.zooms["Zoom_end"] - camera_cutscene.zooms["Zoom_start"]))

                # Translations Z
                file.write(struct.pack('>f', camera_cutscene.positions["Z_start"]))
                file.write(struct.pack('>f', camera_cutscene.positions["Z_end"] - camera_cutscene.positions["Z_start"]))

                # Camera speed (float values)
                file.write(struct.pack('>f', camera_cutscene.camera_speed))

                # Unknown value block 13
                file.write(struct.pack('>f', camera_cutscene.unknown_block_13))

            # Ignore this camera
            else:
                file.seek(IPV.size_each_camera_cutscene, 1)

    # Save all blast info
    with open(IPV.blast_i_path, mode="rb+") as file:

        for i in range(0, 14):

            blast = main_window.blast_key.itemData(i)

            # Blast has been modified
            if blast.modified:
                # Write all the data
                file.write(blast.data)

            # Ignore this blast
            else:
                file.seek(IPV.size_between_blast, 1)


def read_animation_file(main_window, index_list_view, combo_box_label, number_files_to_load, animation_combo_box):

    item_data_animation = []
    for i in range(0, number_files_to_load):

        # Animation instance
        animation = Animation()
        animation.path = main_window.listView_2.model().item(index_list_view + i, 0).text()
        with open(animation.path, mode="rb") as file:
            animation.data = file.read()
        animation.size = len(animation.data)

        # Check if the file is 'Transformation in' from properties in order to read the background color
        if index_list_view == 671 and animation_combo_box.objectName() == "animation_properties" and i == 0:
            read_transformation_effect(main_window, animation)

        # Add all the instances to an array
        item_data_animation.append(animation)
    # Add the array of Animation instances to the combo box
    animation_combo_box.setItemData(animation_combo_box.findText(combo_box_label), item_data_animation)


# Read all the animation files
def read_animation_files(main_window, offset_index, animation_combo_box):

    # Idle ground
    read_animation_file(main_window, offset_index, "Idle ground", 1, animation_combo_box)
    # Idle fly
    read_animation_file(main_window, 1+offset_index, "Idle fly", 1, animation_combo_box)
    # Charge (in, loop)
    read_animation_file(main_window, 2+offset_index, "Charge", 2, animation_combo_box)
    # Charge max
    read_animation_file(main_window, 4+offset_index, "Charge max", 1, animation_combo_box)
    # Idle ground tired
    read_animation_file(main_window, 5+offset_index, "Idle ground tired", 1, animation_combo_box)
    # Idle fly tired
    read_animation_file(main_window, 6+offset_index, "Idle fly tired", 1, animation_combo_box)
    # Dash
    read_animation_file(main_window, 52+offset_index, "Dash", 1, animation_combo_box)
    # Rush attack ground
    read_animation_file(main_window, 66+offset_index, "Rush attack ground", 1, animation_combo_box)
    read_animation_file(main_window, 67+offset_index, "Rush attack ground 2", 1, animation_combo_box)
    read_animation_file(main_window, 68+offset_index, "Rush attack ground 3", 1, animation_combo_box)
    read_animation_file(main_window, 69+offset_index, "Rush attack ground 4", 1, animation_combo_box)
    read_animation_file(main_window, 70+offset_index, "Rush attack ground 5", 1, animation_combo_box)
    # Rush attack fly
    read_animation_file(main_window, 71+offset_index, "Rush attack fly", 1, animation_combo_box)
    read_animation_file(main_window, 72+offset_index, "Rush attack fly 2", 1, animation_combo_box)
    read_animation_file(main_window, 73+offset_index, "Rush attack fly 3", 1, animation_combo_box)
    read_animation_file(main_window, 74+offset_index, "Rush attack fly 4", 1, animation_combo_box)
    read_animation_file(main_window, 75+offset_index, "Rush attack fly 5", 1, animation_combo_box)
    # Smash attack
    read_animation_file(main_window, 76+offset_index, "Smash attack left", 3, animation_combo_box)
    read_animation_file(main_window, 79+offset_index, "Smash attack right", 3, animation_combo_box)
    read_animation_file(main_window, 82+offset_index, "Smash attack 2", 3, animation_combo_box)
    read_animation_file(main_window, 85+offset_index, "Smash attack 3", 1, animation_combo_box)
    read_animation_file(main_window, 86+offset_index, "Smash attack 4", 3, animation_combo_box)
    read_animation_file(main_window, 89+offset_index, "Smash attack high", 3, animation_combo_box)
    read_animation_file(main_window, 92+offset_index, "Smash attack low", 3, animation_combo_box)
    read_animation_file(main_window, 95+offset_index, "Finish attack teleport", 2, animation_combo_box)
    # Charge attack
    read_animation_file(main_window, 97+offset_index,  "Charge attack", 3, animation_combo_box)
    read_animation_file(main_window, 100+offset_index, "Charge attack high", 3, animation_combo_box)
    read_animation_file(main_window, 103+offset_index, "Charge attack low", 3, animation_combo_box)
    read_animation_file(main_window, 106+offset_index, "Charge attack left", 3, animation_combo_box)
    read_animation_file(main_window, 109+offset_index, "Charge attack right", 3, animation_combo_box)
    # Dash attack
    read_animation_file(main_window, 112+offset_index, "Dash attack", 3, animation_combo_box)
    # Dash charge attack
    read_animation_file(main_window, 115+offset_index, "Dash charge attack", 3, animation_combo_box)
    read_animation_file(main_window, 118+offset_index, "Dash charge attack high", 3, animation_combo_box)
    read_animation_file(main_window, 121+offset_index, "Dash charge attack low", 3, animation_combo_box)
    read_animation_file(main_window, 124+offset_index, "Dash charge attack left", 3, animation_combo_box)
    read_animation_file(main_window, 127+offset_index, "Dash charge attack right", 3, animation_combo_box)
    # Shot ki
    read_animation_file(main_window, 130+offset_index, "Shot Ki left hand", 3, animation_combo_box)
    read_animation_file(main_window, 133+offset_index, "Shot Ki right hand", 3, animation_combo_box)
    # Charge Shot ki
    read_animation_file(main_window, 136+offset_index, "Charge shot Ki", 3, animation_combo_box)
    read_animation_file(main_window, 139+offset_index, "Charge shot Ki high", 3, animation_combo_box)
    read_animation_file(main_window, 142+offset_index, "Charge shot Ki low", 3, animation_combo_box)
    # Shot ki while moving
    read_animation_file(main_window, 145+offset_index, "Shot Ki moving forward", 1, animation_combo_box)
    read_animation_file(main_window, 146+offset_index, "Shot Ki moving left", 1, animation_combo_box)
    read_animation_file(main_window, 147+offset_index, "Shot Ki moving right", 1, animation_combo_box)
    read_animation_file(main_window, 148+offset_index, "Shot Ki moving back", 1, animation_combo_box)
    # Charged shot ki while moving
    read_animation_file(main_window, 149+offset_index, "Charged shot Ki moving forward", 3, animation_combo_box)
    read_animation_file(main_window, 152+offset_index, "Charged shot Ki moving left", 3, animation_combo_box)
    read_animation_file(main_window, 155+offset_index, "Charged shot Ki moving right", 3, animation_combo_box)
    read_animation_file(main_window, 158+offset_index, "Charged shot Ki moving back", 3, animation_combo_box)
    # Jump attack
    read_animation_file(main_window, 161+offset_index, "Jump attack", 3, animation_combo_box)
    read_animation_file(main_window, 164+offset_index, "Jump Ki shot left", 1, animation_combo_box)
    read_animation_file(main_window, 165+offset_index, "Jump Ki shot right", 1, animation_combo_box)
    read_animation_file(main_window, 166+offset_index, "Jump charged Ki shot", 3, animation_combo_box)
    # Throw
    read_animation_file(main_window, 169+offset_index, "Throw catch", 1, animation_combo_box)
    read_animation_file(main_window, 170+offset_index, "Throw", 8, animation_combo_box)
    read_animation_file(main_window, 178+offset_index, "Throw wall", 5, animation_combo_box)
    # Guard
    read_animation_file(main_window, 267 + offset_index, "Guard", 1, animation_combo_box)
    # Transformation
    read_animation_file(main_window, 308+offset_index, "Transformation in", 2, animation_combo_box)
    read_animation_file(main_window, 310+offset_index, "Transformation result", 1, animation_combo_box)
    # Return
    read_animation_file(main_window, 311+offset_index, "Return in", 2, animation_combo_box)
    read_animation_file(main_window, 313+offset_index, "Return out", 1, animation_combo_box)
    # Fusion
    read_animation_file(main_window, 316+offset_index, "Fusion in", 2, animation_combo_box)
    read_animation_file(main_window, 318+offset_index, "Fusion result", 1, animation_combo_box)
    # Potala
    read_animation_file(main_window, 321+offset_index, "Potara in", 2, animation_combo_box)
    read_animation_file(main_window, 323+offset_index, "Potara result", 1, animation_combo_box)
    # Cutscenes
    read_animation_file(main_window, 336+offset_index, "Entry 1", 2, animation_combo_box)
    read_animation_file(main_window, 338+offset_index, "Entry 2", 2, animation_combo_box)
    read_animation_file(main_window, 340+offset_index, "Entry 3", 2, animation_combo_box)
    read_animation_file(main_window, 342+offset_index, "Victory", 2, animation_combo_box)
    read_animation_file(main_window, 344+offset_index, "Lose", 2, animation_combo_box)


def change_camera_cutscene_values(main_window, camera_cutscene):
    # Pivots
    main_window.pivot_value.setValue(camera_cutscene.pivots["pivot_1"])
    main_window.pivot_value_2.setValue(camera_cutscene.pivots["pivot_2"])
    main_window.pivot_value_3.setValue(camera_cutscene.pivots["pivot_3"])
    main_window.pivot_value_4.setValue(camera_cutscene.pivots["pivot_4"])

    # Translations
    main_window.translation_y_start_value.setValue(camera_cutscene.positions["Y_start"])
    main_window.translation_y_end_value.setValue(camera_cutscene.positions["Y_end"])
    main_window.translation_z_start_value.setValue(camera_cutscene.positions["Z_start"])
    main_window.translation_z_end_value.setValue(camera_cutscene.positions["Z_end"])

    # Rotations
    main_window.rotation_y_start_value.setValue(camera_cutscene.rotations["Y_start"])
    main_window.rotation_y_end_value.setValue(camera_cutscene.rotations["Y_end"])
    main_window.rotation_z_start_value.setValue(camera_cutscene.rotations["Z_start"])
    main_window.rotation_z_end_value.setValue(camera_cutscene.rotations["Z_end"])

    # Zoom
    main_window.zoom_start_value.setValue(camera_cutscene.zooms["Zoom_start"])
    main_window.zoom_end_value.setValue(camera_cutscene.zooms["Zoom_end"])

    # Speed
    main_window.speed_camera_value.setValue(camera_cutscene.camera_speed)

    # Block 13
    main_window.unk13_value.setValue(camera_cutscene.unknown_block_13)


def export_camera(file_export_path, camera_cutscene):
    with open(file_export_path, mode="wb") as file:
        # Write the pivots
        file.write(camera_cutscene.pivots["pivot_1"].to_bytes(1, byteorder="big"))
        file.write(camera_cutscene.pivots["pivot_2"].to_bytes(1, byteorder="big"))
        file.write(camera_cutscene.pivots["pivot_3"].to_bytes(1, byteorder="big"))
        file.write(camera_cutscene.pivots["pivot_4"].to_bytes(1, byteorder="big"))

        # Rotations Z
        file.write(struct.pack('>f', camera_cutscene.rotations["Z_start"]))
        file.write(struct.pack('>f', camera_cutscene.rotations["Z_end"] - camera_cutscene.rotations["Z_start"]))

        # Translations Y
        file.write(struct.pack('>f', camera_cutscene.positions["Y_start"]))
        file.write(struct.pack('>f', camera_cutscene.positions["Y_end"] - camera_cutscene.positions["Y_start"]))

        # Rotations Y
        file.write(struct.pack('>f', camera_cutscene.rotations["Y_start"]))
        file.write(struct.pack('>f', camera_cutscene.rotations["Y_end"] - camera_cutscene.rotations["Y_start"]))

        # Zoom
        file.write(struct.pack('>f', camera_cutscene.zooms["Zoom_start"]))
        file.write(struct.pack('>f', camera_cutscene.zooms["Zoom_end"] - camera_cutscene.zooms["Zoom_start"]))

        # Translations Z
        file.write(struct.pack('>f', camera_cutscene.positions["Z_start"]))
        file.write(struct.pack('>f', camera_cutscene.positions["Z_end"] - camera_cutscene.positions["Z_start"]))

        # Camera speed (float values)
        file.write(struct.pack('>f', camera_cutscene.camera_speed))

        # Unknown value block 13
        file.write(struct.pack('>f', camera_cutscene.unknown_block_13))


def import_camera(camera_cutscene, file):
    # Get the pivots
    camera_cutscene.pivots["pivot_1"] = int.from_bytes(file.read(1), byteorder='big')
    camera_cutscene.pivots["pivot_2"] = int.from_bytes(file.read(1), byteorder='big')
    camera_cutscene.pivots["pivot_3"] = int.from_bytes(file.read(1), byteorder='big')
    camera_cutscene.pivots["pivot_4"] = int.from_bytes(file.read(1), byteorder='big')

    # Rotations Z
    camera_cutscene.rotations["Z_start"] = struct.unpack('>f', file.read(4))[0]
    camera_cutscene.rotations["Z_end"] = camera_cutscene.rotations["Z_start"] + \
        struct.unpack('>f', file.read(4))[0]

    # Translations Y
    camera_cutscene.positions["Y_start"] = struct.unpack('>f', file.read(4))[0]
    camera_cutscene.positions["Y_end"] = camera_cutscene.positions["Y_start"] + \
        struct.unpack('>f', file.read(4))[0]

    # Rotations Y
    camera_cutscene.rotations["Y_start"] = struct.unpack('>f', file.read(4))[0]
    camera_cutscene.rotations["Y_end"] = camera_cutscene.rotations["Y_start"] + \
        struct.unpack('>f', file.read(4))[0]

    # Zoom
    camera_cutscene.zooms["Zoom_start"] = struct.unpack('>f', file.read(4))[0]
    camera_cutscene.zooms["Zoom_end"] = camera_cutscene.zooms["Zoom_start"] + \
        struct.unpack('>f', file.read(4))[0]

    # Translations Z
    camera_cutscene.positions["Z_start"] = struct.unpack('>f', file.read(4))[0]
    camera_cutscene.positions["Z_end"] = camera_cutscene.positions["Z_start"] + \
        struct.unpack('>f', file.read(4))[0]

    # Camera speed (float values)
    camera_cutscene.camera_speed = struct.unpack('>f', file.read(4))[0]

    # Unknown value block 13
    camera_cutscene.unknown_block_13 = struct.unpack('>f', file.read(4))[0]

    # Set camera as modified
    camera_cutscene.modified = True


def export_animation(animation_array, file_export_path):
    # Get the number of animations files
    number_anim_files = len(animation_array)

    # The header will have the 'SPAS', 'number of animation files', and the size of each
    # of one in the same order
    header_file = bytes(IPV.animations_extension.upper(), encoding='utf-8')
    header_file = header_file + struct.pack('>I', number_anim_files)
    data_file = b''

    # Get the sizes and data from each animation
    for animation_file in animation_array:
        header_file = header_file + struct.pack('>I', animation_file.size)
        data_file = data_file + animation_file.data

    # Write the header properties and then the data
    with open(file_export_path, mode="wb") as file:
        # Write the header (SPAS, number of animation files, and sizes)
        file.write(header_file)

        # Write the data
        file.write(data_file)


def import_animation(main_window, file_export_path, animation_array, name_file=None, animations_files_error=None):

    if file_export_path:

        with open(file_export_path, mode="rb") as file:

            header_type = file.read(4)

            # The header needs to have 'SPAS' as a header
            if header_type.decode("utf-8").lower() != IPV.animations_extension:
                if animations_files_error is not None:
                    animations_files_error.append(name_file)
                    return
                else:
                    # Wrong animation file
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setWindowIcon(main_window.ico_image)
                    msg.setText("Invalid animation file.")
                    msg.exec()
                    return
            else:

                # Read the number of files
                number_anim_files = int.from_bytes(file.read(4), "big")

                # Get the sizes of each file. While reading we will sum all the sizes to check if the file has
                # the same data size
                sizes_number_of_files = []
                total_size = 0

                # Read the size of each animation file
                for _ in range(number_anim_files):
                    size = int.from_bytes(file.read(4), "big")
                    sizes_number_of_files.append(size)
                    total_size += size

                # The rest of data in the file, is the animations (keyframes and effects) info
                data = file.read()
                total_size_file = len(data)

                # Check if the sizes are the same
                if total_size != total_size_file:
                    if animations_files_error is not None:
                        animations_files_error.append(name_file)
                        return
                    else:
                        # Wrong animation file
                        msg = QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setWindowIcon(main_window.ico_image)
                        msg.setText("Invalid animation file.")
                        msg.exec()
                        return

                # If the modified file has more files inside than the original, we refuse the modified file
                if len(animation_array) != number_anim_files:
                    if animations_files_error is not None:
                        animations_files_error.append(name_file)
                        return
                    else:
                        # Wrong animation file
                        msg = QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setWindowIcon(main_window.ico_image)
                        msg.setText("Incompatible animation file.")
                        msg.exec()
                        return

                data_index_start = 0
                # Get each animation file
                for i in range(0, len(animation_array)):
                    data_index_end = data_index_start + sizes_number_of_files[i]
                    animation_array[i].data = data[data_index_start:data_index_end]
                    animation_array[i].size = sizes_number_of_files[i]
                    animation_array[i].modified = True
                    data_index_start = data_index_end


def export_blast(file_export_path, blast):

    with open(file_export_path, mode="wb") as file:

        # Write all the data
        file.write(blast.data)


def import_blast(blast, file):

    # Get the data
    blast.data = file.read()

    # Set blast as modified
    blast.modified = True
