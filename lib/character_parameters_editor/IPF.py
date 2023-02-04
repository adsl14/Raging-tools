import functools
import os
import json

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.IPV import IPV
from lib.character_parameters_editor.classes.BONE.BoneEntry import BoneEntry
from lib.character_parameters_editor.classes.Blast import Blast
from lib.character_parameters_editor.classes.CameraCutscene import CameraCutscene
from lib.character_parameters_editor.classes.Animation import Animation
from lib.character_parameters_editor.classes.SPA.SPAFile import SPAFile
from lib.character_parameters_editor.functions.IP.action_logic import on_camera_type_key_changed, \
    action_export_camera_button_logic, action_import_camera_button_logic, action_export_all_camera_button_logic, \
    action_import_all_camera_button_logic, on_pivot_value_changed, on_translations_changed, on_rotations_changed, \
    on_speed_camera_changed, on_zoom_start_value_changed, on_zoom_end_value_changed, \
    action_export_animation_button_logic, action_import_animation_button_logic, \
    action_export_all_animation_button_logic, action_import_all_animation_button_logic, \
    action_export_blast_button_logic, action_import_blast_button_logic, action_export_all_blast_button_logic, \
    action_import_all_blast_button_logic, on_background_color_trans_change, \
    action_export_signature_ki_blast_button_logic, action_import_signature_ki_blast_button_logic, on_blast_attack_changed, \
    on_glow_activation_changed, on_stackable_skill_changed, on_power_up_changed, on_effect_attack_changed, on_chargeable_changed, \
    on_size_attack_value_changed, on_number_of_hits_value_changed, on_cost_blast_attack_value_changed, on_blast_attack_damage_value_changed, \
    on_speed_attack_value_changed, on_reach_attack_value_changed, on_camera_blast_value_changed, action_change_character, action_modify_character, on_animation_type_changed, \
    on_animation_layer_spas_changed, on_animation_bone_changed, on_animation_bone_translation_block_changed, on_animation_bone_rotations_block_changed, on_animation_bone_unknown_block_changed, \
    action_export_animation_bone_button_logic, action_export_all_animation_bone_button_logic, action_import_animation_bone_button_logic, action_import_all_animation_bone_button_logic, \
    action_remove_animation_bone
from lib.character_parameters_editor.functions.IP.auxiliary import read_transformation_effect, store_blast_values_from_file, \
    write_blast_values_to_file, change_blast_values, change_camera_cutscene_values, write_camera_cutscene_to_file, store_camera_cutscene_from_file, change_animation_bones_section, get_rotation
from lib.functions import check_entry_module, get_name_from_file
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

    # Set the signature ki blast
    main_window.signature_ki_blast_export.clicked.connect(lambda:
                                                          action_export_signature_ki_blast_button_logic(main_window))
    main_window.signature_ki_blast_import.clicked.connect(lambda:
                                                          action_import_signature_ki_blast_button_logic(main_window))

    # Set animations
    for element in IPV.animations_types:
        main_window.animation_type_value.addItem(element)
    main_window.animation_type_value.currentIndexChanged.connect(lambda: on_animation_type_changed(main_window))
    # Export animation button
    main_window.exportAnimationButton.clicked.connect(
        lambda: action_export_animation_button_logic(main_window, 0))
    # Import animation button
    main_window.importAnimationButton.clicked.connect(
        lambda: action_import_animation_button_logic(main_window, 0))
    # Export all animation button
    main_window.exportAllAnimationButton.clicked.connect(
        lambda: action_export_all_animation_button_logic(main_window, 0))
    # Import all animation button
    main_window.importAllAnimationButton.clicked.connect(
        lambda: action_import_all_animation_button_logic(main_window, 0))
    # Export animation properties button
    main_window.exportAnimationEffectsButton.clicked.connect(
        lambda: action_export_animation_button_logic(main_window, 1, "_effects"))
    # Import animation properties button
    main_window.importAnimationEffectsButton.clicked.connect(
        lambda: action_import_animation_button_logic(main_window, 1))
    # Export all animation properties button
    main_window.exportAllAnimationEffectsButton.clicked.connect(
        lambda: action_export_all_animation_button_logic(main_window, 1, "_effects"))
    # Import all animation properties button
    main_window.importAllAnimationEffectsButton.clicked.connect(
        lambda: action_import_all_animation_button_logic(main_window, 1))
    # Bones section
    main_window.animation_spas_layer_value.currentIndexChanged.connect(lambda: on_animation_layer_spas_changed(main_window))
    main_window.animation_bone_value.currentIndexChanged.connect(lambda: on_animation_bone_changed(main_window))
    main_window.animation_bone_translation_block_value.currentIndexChanged.connect(lambda: on_animation_bone_translation_block_changed(main_window))
    main_window.animation_bone_rotation_block_value.currentIndexChanged.connect(lambda: on_animation_bone_rotations_block_changed(main_window))
    main_window.animation_bone_unknown_block_value.currentIndexChanged.connect(lambda: on_animation_bone_unknown_block_changed(main_window))
    # Export bone
    main_window.animation_export_bone.clicked.connect(lambda: action_export_animation_bone_button_logic(main_window))
    main_window.animation_export_all_bone.clicked.connect(lambda: action_export_all_animation_bone_button_logic(main_window))
    # Import bone
    main_window.animation_import_bone.clicked.connect(lambda: action_import_animation_bone_button_logic(main_window))
    main_window.animation_import_all_bone.clicked.connect(lambda: action_import_all_animation_bone_button_logic(main_window))
    # Remove bone
    main_window.animation_remove_bone.clicked.connect(lambda: action_remove_animation_bone(main_window))

    # Set the blast type
    main_window.blast_key.currentIndexChanged.connect(lambda: on_blast_attack_changed(main_window))
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

    # Set the glow values
    main_window.glow_activation_value.currentIndexChanged.connect(lambda: on_glow_activation_changed(main_window))
    for element in IPV.glow_values:
        main_window.glow_activation_value.addItem(element, IPV.glow_values[element])

    # Set the stackable skill values
    main_window.stackable_skill_value.currentIndexChanged.connect(lambda: on_stackable_skill_changed(main_window))
    for element in IPV.stackable_skill:
        main_window.stackable_skill_value.addItem(element, IPV.stackable_skill[element])

    # Set the melee values
    main_window.melee_power_up_value.currentIndexChanged.connect(lambda: on_power_up_changed(main_window, main_window.melee_power_up_value, "Melee"))
    for element in IPV.melee_power_up_properties:
        main_window.melee_power_up_value.addItem(element, IPV.melee_power_up_properties[element])

    # Set the defense values
    main_window.defense_power_up_value.currentIndexChanged.connect(lambda: on_power_up_changed(main_window, main_window.defense_power_up_value,
                                                                                               "Defense"))
    for element in IPV.defense_power_up_properties:
        main_window.defense_power_up_value.addItem(element, IPV.defense_power_up_properties[element])

    # Set the super attack values
    main_window.super_attack_power_up_value.currentIndexChanged.connect(lambda: on_power_up_changed(main_window,
                                                                                                    main_window.super_attack_power_up_value,
                                                                                                    "Super Attack"))
    for element in IPV.super_attack_power_up_properties:
        main_window.super_attack_power_up_value.addItem(element, IPV.super_attack_power_up_properties[element])

    # Set the Ki values
    main_window.ki_power_up_value.currentIndexChanged.connect(lambda: on_power_up_changed(main_window, main_window.ki_power_up_value, "Ki"))
    for element in IPV.ki_power_up_properties:
        main_window.ki_power_up_value.addItem(element, IPV.ki_power_up_properties[element])

    # Set the activation skill values
    main_window.effect_attack_value.currentIndexChanged.connect(lambda: on_effect_attack_changed(main_window))
    for element in IPV.activation_skill:
        main_window.effect_attack_value.addItem(element, IPV.activation_skill[element])

    # Set the chargeable/boost skill values
    main_window.chargeable_value.currentIndexChanged.connect(lambda: on_chargeable_changed(main_window))
    for element in IPV.chargeable_boost:
        main_window.chargeable_value.addItem(element, IPV.chargeable_boost[element])

    # Set reach attack
    main_window.reach_attack_value.valueChanged.connect(lambda: on_reach_attack_value_changed(main_window))

    # Set speed_attack_value
    main_window.speed_attack_value.valueChanged.connect(lambda: on_speed_attack_value_changed(main_window))

    # Set blast_attack_damage_value
    main_window.blast_attack_damage_value.valueChanged.connect(lambda: on_blast_attack_damage_value_changed(main_window))

    # Set cost_blast_attack_value
    main_window.cost_blast_attack_value.valueChanged.connect(lambda: on_cost_blast_attack_value_changed(main_window))

    # Set number_of_hits_value
    main_window.number_of_hits_value.valueChanged.connect(lambda: on_number_of_hits_value_changed(main_window))

    # Set size_attack_value
    main_window.size_attack_value.valueChanged.connect(lambda: on_size_attack_value_changed(main_window))

    # Set camera_blast_value
    main_window.camera_blast_value_0.valueChanged.connect(lambda: on_camera_blast_value_changed(main_window, 0, main_window.camera_blast_value_0))
    main_window.camera_blast_value_1.valueChanged.connect(lambda: on_camera_blast_value_changed(main_window, 1, main_window.camera_blast_value_1))
    main_window.camera_blast_value_2.valueChanged.connect(lambda: on_camera_blast_value_changed(main_window, 2, main_window.camera_blast_value_2))
    main_window.camera_blast_value_3.valueChanged.connect(lambda: on_camera_blast_value_changed(main_window, 3, main_window.camera_blast_value_3))

    # Partner
    # Load the Select Chara partner window
    mini_portraits_image_select_chara_roster_window = main_window.selectCharaPartnerUI.frame.findChildren(QLabel)
    # Prepare each slot in the window
    for i in range(0, len(mini_portraits_image_select_chara_roster_window)):
        chara_id = int(mini_portraits_image_select_chara_roster_window[i].objectName().split("_")[-1])
        mini_portraits_image_select_chara_roster_window[i].setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_" +
                                                                                          str(chara_id).zfill(3) + ".bmp")))
        mini_portraits_image_select_chara_roster_window[i].mousePressEvent = functools.partial(action_modify_character, main_window=main_window,
                                                                                               chara_id=chara_id)
        mini_portraits_image_select_chara_roster_window[i].setStyleSheet(CPEV.styleSheetSlotRosterWindow)

    # Prepare the partner slot
    main_window.partner_character_slot.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_slot.png")))
    main_window.partner_character_value.mousePressEvent = functools.partial(action_change_character, main_window=main_window)


def read_single_character_parameters(worker_pef, start_progress, step_report, main_window):

    # character info
    IPV.character_i_path = main_window.listView_2.model().item(726, 0).text()
    # camera info
    IPV.camera_i_path = main_window.listView_2.model().item(727, 0).text()
    # blast info
    IPV.blast_i_path = main_window.listView_2.model().item(728, 0).text()
    # signature ki blast
    IPV.signature_ki_blast.path = main_window.listView_2.model().item(745, 0).text()

    # Read all the animation values
    worker_pef.progressText.emit("Loading animations")
    # 5 tasks
    sub_step_report = step_report / 5
    start_progress = read_animation_files(worker_pef, start_progress, sub_step_report, main_window, 0)
    change_animation_bones_section(main_window, main_window.animation_type_value.itemData(0))
    main_window.animation_type_value.setCurrentIndex(0)

    # Read character info file
    with open(IPV.character_i_path, mode="rb") as file:

        # Report progress
        worker_pef.progressText.emit("Reading character info")
        start_progress += sub_step_report
        worker_pef.progressValue.emit(start_progress)

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

        # Get number of cameras
        num_cameras = len(IPV.camera_types_cutscene)

        sub_sub_step_report = sub_step_report / num_cameras
        for i in range(0, num_cameras):

            # Report progress
            worker_pef.progressText.emit("Reading camera info " + str(i + 1))
            start_progress += sub_sub_step_report
            worker_pef.progressValue.emit(start_progress)

            # Create an instance of cameraCutscene
            camera_cutscene = CameraCutscene()

            # Store all the data
            store_camera_cutscene_from_file(camera_cutscene, file)

            # Set camera type combo box
            main_window.camera_type_key.setItemData(i, camera_cutscene)

        # Show the first item in the combo box and his values
        main_window.camera_type_key.setCurrentIndex(0)
        change_camera_cutscene_values(main_window, main_window.camera_type_key.itemData(0))

    # Read blast info file
    with open(IPV.blast_i_path, mode="rb") as file:

        sub_sub_step_report = sub_step_report / 14
        for i in range(0, 14):

            # Report progress
            worker_pef.progressText.emit("Reading blast info " + str(i + 1))
            start_progress += sub_sub_step_report
            worker_pef.progressValue.emit(start_progress)

            # Create an instance of Blast
            blast = Blast()

            # Store all the blast values in memory
            store_blast_values_from_file(blast, file)

            # Set blast combo box
            main_window.blast_key.setItemData(i, blast)

        # Show the first item in the combo box and his values
        change_blast_values(main_window, main_window.blast_key.itemData(0))
        main_window.blast_key.setCurrentIndex(0)

    # Read signature info file
    # Report progress
    worker_pef.progressText.emit("Reading signature info")
    start_progress += sub_step_report
    worker_pef.progressValue.emit(start_progress)
    with open(IPV.signature_ki_blast.path, mode="rb") as file:
        IPV.signature_ki_blast.data = file.read()
    IPV.signature_ki_blast.modified = False


def write_single_character_parameters(worker_pef, main_window, start_progress, step_progress):

    # 5 is because the number of task in this function
    sub_step_progress = step_progress / 5

    # Save all animation info (replace first the entire files)
    num_animation_types = len(IPV.animations_types)
    sub_sub_step_progress = sub_step_progress / num_animation_types
    for i in range(0, num_animation_types):
        animation_files = main_window.animation_type_value.itemData(i)

        num_animation_files = len(animation_files)
        sub_sub_sub_step_progress = sub_sub_step_progress / num_animation_files
        for j in range(0, num_animation_files):

            # Report progress
            worker_pef.progressText.emit("Writting animation type " + str(i + 1) + " (" + str(j + 1) + "/" + str(num_animation_files) + ")")
            start_progress += sub_sub_sub_step_progress
            worker_pef.progressValue.emit(start_progress)

            # Animation file
            if animation_files[j][0].modified:
                with open(animation_files[j][0].path, mode="wb") as file:
                    data, size = write_spa_file(animation_files[j][0])
                    file.write(data)

            # Animation effects file
            if animation_files[j][1].modified:
                with open(animation_files[j][1].path, mode="wb") as file:
                    file.write(animation_files[j][1].data)

    # Save all character info
    with open(IPV.character_i_path, mode="rb+") as file:

        # Report progress
        worker_pef.progressText.emit("Writting character info")
        start_progress += sub_step_progress
        worker_pef.progressValue.emit(start_progress)

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

        num_cameras = len(IPV.camera_types_cutscene)
        sub_sub_step_progress = sub_step_progress / num_cameras
        for i in range(0, num_cameras):

            # Report progress
            worker_pef.progressText.emit("Writting camera " + str(i + 1))
            start_progress += sub_sub_step_progress
            worker_pef.progressValue.emit(start_progress)

            camera_cutscene = main_window.camera_type_key.itemData(i)

            # Camera has been modified
            if camera_cutscene.modified:
                write_camera_cutscene_to_file(camera_cutscene, file)

            # Ignore this camera
            else:
                file.seek(IPV.size_each_camera_cutscene, 1)

    # Save all blast info
    with open(IPV.blast_i_path, mode="rb+") as file:

        sub_sub_step_progress = sub_step_progress / 14
        for i in range(0, 14):

            # Report progress
            worker_pef.progressText.emit("Writting blast " + str(i + 1))
            start_progress += sub_sub_step_progress
            worker_pef.progressValue.emit(start_progress)

            blast = main_window.blast_key.itemData(i)

            # Blast has been modified
            if blast.modified:
                # Write all the data
                write_blast_values_to_file(blast, file)

            # Ignore this blast
            else:
                file.seek(IPV.size_between_blast, 1)

    # Save all signature ki blast info
    # Report progress
    worker_pef.progressText.emit("Writting signature")
    start_progress += sub_step_progress
    worker_pef.progressValue.emit(start_progress)
    if IPV.signature_ki_blast.modified:
        with open(IPV.signature_ki_blast.path, mode="wb") as file:
            file.write(IPV.signature_ki_blast.data)


def read_spa_file(spa_path):

    # Create the instance for the spa
    spa_file = SPAFile()

    # Store the path
    spa_file.path = spa_path

    # Read the data of the spa
    with open(spa_path, mode="rb") as file:
        spa_file.spa_header.unk0x00 = file.read(4)

        # If there is data in the first 4 bytes, we continue reading
        if spa_file.spa_header.unk0x00 != b'':

            # Read the name and restore the pointer to continue reading the following bytes
            aux_pointer = file.tell()
            spa_file.spa_header.name, spa_file.spa_header.extension = get_name_from_file(file, int.from_bytes(file.read(4), "big"))
            file.seek(aux_pointer + 4)

            # Read header
            spa_file.spa_header.unk0x08 = file.read(4)
            spa_file.spa_header.frame_count = struct.unpack('>f', file.read(4))[0]
            spa_file.spa_header.bone_count = int.from_bytes(file.read(4), "big")
            spa_file.spa_header.maybe_start_offset = int.from_bytes(file.read(4), "big")
            spa_file.spa_header.scene_nodes_count = int.from_bytes(file.read(4), "big")
            spa_file.spa_header.scene_nodes_offset = int.from_bytes(file.read(4), "big")
            spa_file.spa_header.camera_count = int.from_bytes(file.read(4), "big")
            spa_file.spa_header.camera_offset = int.from_bytes(file.read(4), "big")
            spa_file.spa_header.unk0x28 = file.read(4)
            spa_file.spa_header.unk0x2c = file.read(4)

            # Read bones
            for _ in range(0, spa_file.spa_header.bone_count):
                # Create bone instance
                bone_entry = BoneEntry()

                # Read the name and restore the pointer to continue reading the following bytes
                aux_pointer = file.tell()
                bone_entry.name, _ = get_name_from_file(file, int.from_bytes(file.read(4), "big"))
                file.seek(aux_pointer + 4)

                # Meta data
                bone_entry.unk0x04 = file.read(4)
                bone_entry.translation_block_count = int.from_bytes(file.read(4), "big")
                bone_entry.rotation_block_count = int.from_bytes(file.read(4), "big")
                bone_entry.unknown_block_count = int.from_bytes(file.read(4), "big")
                bone_entry.translation_frame_offset = int.from_bytes(file.read(4), "big")
                bone_entry.rotation_frame_offset = int.from_bytes(file.read(4), "big")
                bone_entry.unknown_frame_offset = int.from_bytes(file.read(4), "big")
                bone_entry.translation_float_offset = int.from_bytes(file.read(4), "big")
                bone_entry.rotation_float_offset = int.from_bytes(file.read(4), "big")
                bone_entry.unknown_float_offset = int.from_bytes(file.read(4), "big")
                bone_entry.unk0x2c = file.read(4)

                # Data
                aux_pointer = file.tell()
                # Read translations
                file.seek(bone_entry.translation_frame_offset)
                for i in range(0, bone_entry.translation_block_count):
                    # Read frame
                    bone_entry.translation_frame_data.append(struct.unpack('>f', file.read(4))[0])

                    # Read float (x, y, z, w)
                    aux_translation_pointer = file.tell()
                    file.seek(bone_entry.translation_float_offset + (i * 16))
                    bone_entry.translation_float_data.append(dict({"x": struct.unpack('>f', file.read(4))[0], "y": struct.unpack('>f', file.read(4))[0], "z": struct.unpack('>f', file.read(4))[0],
                                                                   "w": struct.unpack('>f', file.read(4))[0]}))
                    # Return to the next frame translation
                    file.seek(aux_translation_pointer)

                # Read rotations
                file.seek(bone_entry.rotation_frame_offset)
                for i in range(0, bone_entry.rotation_block_count):
                    # Read frame
                    bone_entry.rot_frame_data.append(struct.unpack('>f', file.read(4))[0])

                    # Read float (the calculation of x, y and z, needs more research. When we create the rot value from x, y and z, we don't get the same result as the input)
                    aux_rotation_pointer = file.tell()
                    file.seek(bone_entry.rotation_float_offset + (i * 8))
                    rot = int.from_bytes(file.read(8), "big")
                    ''''x = ((((rot & 0x0fffffffffffffff) >> 40) / 0x7ffff) * 90) - 90
                    y = ((((rot & 0x000000ffffffffff) >> 20) / 0x7ffff) * 90) - 90
                    z = (((rot & 0x00000000000fffff) / 0x7ffff) * 90) - 90'''
                    bone_entry.rot_float_data.append(dict({"rot": rot, "x": 0, "y": 0, "z": 0}))
                    # Return to the next frame rotation
                    file.seek(aux_rotation_pointer)

                # Read unknown
                file.seek(bone_entry.unknown_frame_offset)
                for i in range(0, bone_entry.unknown_block_count):
                    # Read frame
                    bone_entry.unknown_frame_data.append(struct.unpack('>f', file.read(4))[0])

                    # Read float (x, y, z, w)
                    aux_unknown_pointer = file.tell()
                    file.seek(bone_entry.unknown_float_offset + (i * 16))
                    bone_entry.unknown_float_data.append(dict({"x": struct.unpack('>f', file.read(4))[0], "y": struct.unpack('>f', file.read(4))[0], "z": struct.unpack('>f', file.read(4))[0],
                                                                   "w": struct.unpack('>f', file.read(4))[0]}))
                    # Return to the next frame translation
                    file.seek(aux_unknown_pointer)

                # Restore pointer
                file.seek(aux_pointer)

                # Store everything in the dict
                spa_file.bone_entries[bone_entry.name] = bone_entry

        # Store the size of the file
        spa_file.size = file.tell()

    return spa_file


def write_spa_file(spa_file):

    header_data = b''
    header_size = 0
    bone_entry = b''
    bone_entry_size = 48 * spa_file.spa_header.bone_count
    bone_data = b''
    bone_data_start_offset = spa_file.spa_header.maybe_start_offset + bone_entry_size
    bone_data_size = 0
    string_table = b''
    string_table_size = 0

    # If there is data within in the spa_file instance, we create the output
    if spa_file.size > 0:
        # Write first all the data
        for bone_entry_name in spa_file.bone_entries:
            # Get the bone data
            bone_entry_data = spa_file.bone_entries[bone_entry_name]

            # Write frames
            # Translation
            # Update offset (only if there is data)
            if bone_entry_data.translation_block_count > 0:

                # Check if the data, the module of 16 is 0 before writting
                bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

                bone_entry_data.translation_frame_offset = bone_data_start_offset + bone_data_size
                for translation_frame in bone_entry_data.translation_frame_data:
                    bone_data = bone_data + struct.pack('>f', translation_frame)
                    bone_data_size += 4
            else:
                bone_entry_data.translation_frame_offset = 0

            # Rotations
            # Update offset (only if there is data)
            if bone_entry_data.rotation_block_count > 0:

                # Check if the data, the module of 16 is 0 before writting
                bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

                bone_entry_data.rotation_frame_offset = bone_data_start_offset + bone_data_size
                for rotarion_frame in bone_entry_data.rot_frame_data:
                    bone_data = bone_data + struct.pack('>f', rotarion_frame)
                    bone_data_size += 4
            else:
                bone_entry_data.rotation_frame_offset = 0

            # Unknown
            # Update offset (only if there is data)
            if bone_entry_data.unknown_block_count > 0:

                # Check if the data, the module of 16 is 0 before writting
                bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

                bone_entry_data.unknown_frame_offset = bone_data_start_offset + bone_data_size
                for unknown_frame in bone_entry_data.unknown_frame_data:
                    bone_data = bone_data + struct.pack('>f', unknown_frame)
                    bone_data_size += 4
            else:
                bone_entry_data.unknown_frame_offset = 0

            # Write floats
            # Translation
            # Update offset (only if there is data)
            if bone_entry_data.translation_block_count > 0:

                # Check if the data, the module of 16 is 0 before writting
                bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

                bone_entry_data.translation_float_offset = bone_data_start_offset + bone_data_size
                for translation_float in bone_entry_data.translation_float_data:
                    bone_data = bone_data + struct.pack('>f', translation_float['x'])
                    bone_data = bone_data + struct.pack('>f', translation_float['y'])
                    bone_data = bone_data + struct.pack('>f', translation_float['z'])
                    bone_data = bone_data + struct.pack('>f', translation_float['w'])
                    bone_data_size += 16

            else:
                bone_entry_data.translation_float_offset = 0

            # Rotation
            # Update offset (only if there is data)
            if bone_entry_data.rotation_block_count > 0:

                # Check if the data, the module of 16 is 0 before writting
                bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

                bone_entry_data.rotation_float_offset = bone_data_start_offset + bone_data_size
                for rotation_float in bone_entry_data.rot_float_data:
                    # Convert each axis rotation in order to write the 'rot' value propertly. It needs more research since the rot calculated is not the same from the original
                    '''rot_x = get_rotation(rotation_float['x']) << 40
                    rot_y = get_rotation(rotation_float['y']) << 20
                    rot_z = get_rotation(rotation_float['z'])
                    rot = 0x3000000000000000 | rot_x | rot_y | rot_z
                    bone_data = bone_data + rot.to_bytes(8, 'big')'''
                    bone_data = bone_data + rotation_float['rot'].to_bytes(8, 'big')
                    bone_data_size += 8
            else:
                bone_entry_data.rotation_float_offset = 0

            # Unknown
            # Update offset (only if there is data)
            if bone_entry_data.unknown_block_count > 0:

                # Check if the data, the module of 16 is 0 before writting
                bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

                bone_entry_data.unknown_float_offset = bone_data_start_offset + bone_data_size
                for unknown_float in bone_entry_data.unknown_float_data:
                    bone_data = bone_data + struct.pack('>f', unknown_float['x'])
                    bone_data = bone_data + struct.pack('>f', unknown_float['y'])
                    bone_data = bone_data + struct.pack('>f', unknown_float['z'])
                    bone_data = bone_data + struct.pack('>f', unknown_float['w'])
                    bone_data_size += 16

            else:
                bone_entry_data.unknown_float_offset = 0

        # Write the name of the spa
        string_table_start_offset = bone_data_start_offset + bone_data_size
        name = spa_file.spa_header.name + "." + spa_file.spa_header.extension
        string_table += name.encode('utf-8') + b'\x00'
        string_table_size += 1 + len(name)

        # Once the data is written and we know the size, we can create the spa entirely, We have to, again, loop all the bones
        for bone_entry_name in spa_file.bone_entries:
            # Get the bone data
            bone_entry_data = spa_file.bone_entries[bone_entry_name]

            # Write each bone entry
            bone_entry += (string_table_start_offset + string_table_size).to_bytes(4, 'big')
            bone_entry += bone_entry_data.unk0x04
            bone_entry += bone_entry_data.translation_block_count.to_bytes(4, 'big')
            bone_entry += bone_entry_data.rotation_block_count.to_bytes(4, 'big')
            bone_entry += bone_entry_data.unknown_block_count.to_bytes(4, 'big')
            bone_entry += bone_entry_data.translation_frame_offset.to_bytes(4, 'big')
            bone_entry += bone_entry_data.rotation_frame_offset.to_bytes(4, 'big')
            bone_entry += bone_entry_data.unknown_frame_offset.to_bytes(4, 'big')
            bone_entry += bone_entry_data.translation_float_offset.to_bytes(4, 'big')
            bone_entry += bone_entry_data.rotation_float_offset.to_bytes(4, 'big')
            bone_entry += bone_entry_data.unknown_float_offset.to_bytes(4, 'big')
            bone_entry += bone_entry_data.unk0x2c

            # Write the name in the string table
            string_table += bone_entry_name.encode('utf-8') + b'\x00'
            string_table_size += len(bone_entry_name) + 1

        # Write finally the header
        header_data += spa_file.spa_header.unk0x00
        header_data += string_table_start_offset.to_bytes(4, 'big')
        header_data += spa_file.spa_header.unk0x08
        header_data += struct.pack('>f', spa_file.spa_header.frame_count)
        header_data += spa_file.spa_header.bone_count.to_bytes(4, 'big')
        header_data += spa_file.spa_header.maybe_start_offset.to_bytes(4, 'big')
        header_data += spa_file.spa_header.scene_nodes_count.to_bytes(4, 'big')
        header_data += spa_file.spa_header.scene_nodes_offset.to_bytes(4, 'big')
        header_data += spa_file.spa_header.camera_count.to_bytes(4, 'big')
        header_data += spa_file.spa_header.camera_offset.to_bytes(4, 'big')
        header_data += spa_file.spa_header.unk0x28
        header_data += spa_file.spa_header.unk0x2c
        header_size = 48

    return (header_data + bone_entry + bone_data + string_table), (header_size + bone_entry_size + bone_data_size + string_table_size)


def read_json_bone_file(file_import_path):

    spa_file = SPAFile()
    # Open the json file
    with open(file_import_path, mode='r') as input_file:

        # Check if is a valid json file
        try:
            # return a json object
            data = json.load(input_file)

            # Read header
            spa_file.spa_header.unk0x00 = data['unk0x00'].to_bytes(4, 'big')
            spa_file.spa_header.name = data['name']
            spa_file.spa_header.unk0x08 = data['unk0x08'].to_bytes(4, 'big')
            spa_file.spa_header.frame_count = data['frame_count']
            spa_file.spa_header.scene_nodes_count = data['scene_nodes_count']
            spa_file.spa_header.camera_count = data['camera_count']
            spa_file.spa_header.unk0x28 = data['unk0x28'].to_bytes(4, 'big')
            spa_file.spa_header.unk0x28 = data['unk0x28'].to_bytes(4, 'big')
            spa_file.spa_header.unk0x2c = data['unk0x2c'].to_bytes(4, 'big')

            # Read each bone from json
            for bone_entry_json in data['bones']:

                # Count the number of bones in json file
                spa_file.spa_header.bone_count += 1

                # Create bone instance
                bone_entry = BoneEntry()

                bone_entry.name = bone_entry_json['name']

                # Meta data
                bone_entry.unk0x04 = bone_entry_json['unk0x04'].to_bytes(4, 'big')
                bone_entry.translation_block_count = bone_entry_json['translation_block_count']
                bone_entry.rotation_block_count = bone_entry_json['rotation_block_count']
                bone_entry.unknown_block_count = bone_entry_json['unknown_block_count']
                bone_entry.unk0x2c = bone_entry_json['unk0x2c'].to_bytes(4, 'big')

                # Data
                # Read translations
                for i in range(0, bone_entry.translation_block_count):
                    # Read frame
                    bone_entry.translation_frame_data.append(bone_entry_json['translation_frame_data'][i])

                    # Read float (x, y, z, w)
                    bone_entry.translation_float_data.append(bone_entry_json['translation_float_data'][i])

                # Read rotations
                for i in range(0, bone_entry.rotation_block_count):
                    # Read frame
                    bone_entry.rot_frame_data.append(bone_entry_json['rot_frame_data'][i])

                    # Read float
                    bone_entry.rot_float_data.append(bone_entry_json['rot_float_data'][i])

                # Read unknown
                for i in range(0, bone_entry.unknown_block_count):
                    # Read frame
                    bone_entry.unknown_frame_data.append(bone_entry_json['unknown_frame_data'][i])

                    # Read float (x, y, z, w)
                    bone_entry.unknown_float_data.append(bone_entry_json['unknown_float_data'][i])

                # Store everything in the dict
                spa_file.bone_entries[bone_entry.name] = bone_entry
        except BaseException:
            print("ERROR -> Wrong json file.")

        return spa_file


def write_json_bone_file(file_export_path, spa_header, bone_entries):

    header_text = ""
    bone_text = ""
    with open(file_export_path, mode='w') as output_file:

        # Header (before bone count)
        header_text += "\t\"unk0x00\": " + str(int.from_bytes(spa_header.unk0x00, "big")) + ",\n"
        header_text += "\t\"name\": \"" + spa_header.name + "\",\n"
        header_text += "\t\"unk0x08\": " + str(int.from_bytes(spa_header.unk0x08, "big")) + ",\n"
        header_text += "\t\"frame_count\": " + str(spa_header.frame_count) + ",\n"

        # Bones
        bone_text += "\t\"bones\": \n\t\t\t[\n"
        for bone_entry_name in bone_entries:
            bone_entry_data = bone_entries[bone_entry_name]
            bone_text += "\t\t\t\t{"
            bone_text += "\"name\": " + "\"" + bone_entry_data.name + "\", "
            bone_text += "\"unk0x04\": " + str(int.from_bytes(bone_entry_data.unk0x04, "big")) + ", "
            bone_text += "\"translation_block_count\": " + str(bone_entry_data.translation_block_count) + ", "
            bone_text += "\"rotation_block_count\": " + str(bone_entry_data.rotation_block_count) + ", "
            bone_text += "\"unknown_block_count\": " + str(bone_entry_data.unknown_block_count) + ", "
            bone_text += "\"unk0x2c\": " + str(int.from_bytes(bone_entry_data.unk0x2c, "big")) + ",\n"

            bone_text += "\t\t\t\t\t\"translation_frame_data\": ["
            text_write = ""
            for translation_frame in bone_entry_data.translation_frame_data:
                text_write += str(translation_frame) + ", "
            bone_text += text_write[:-2]
            bone_text += "]" + ",\n"

            bone_text += "\t\t\t\t\t\"translation_float_data\": ["
            text_write = ""
            for translation_float in bone_entry_data.translation_float_data:
                text_write += "{\"x\": " + str(translation_float['x']) + ", " + "\"y\": " + str(translation_float['y']) + ", " + "\"z\": " + str(translation_float['z']) + ", " + \
                              "\"w\": " + str(translation_float['w']) + "}" + ", "
            bone_text += text_write[:-2]
            bone_text += "]" + ",\n"

            bone_text += "\t\t\t\t\t\"rot_frame_data\": ["
            text_write = ""
            for rot_frame in bone_entry_data.rot_frame_data:
                text_write += str(rot_frame) + ", "
            bone_text += text_write[:-2]
            bone_text += "]" + ",\n"

            bone_text += "\t\t\t\t\t\"rot_float_data\": ["
            text_write = ""
            for rot_float in bone_entry_data.rot_float_data:
                text_write += "{\"rot\": " + str(rot_float['rot']) + "}" + ", "
            bone_text += text_write[:-2]
            bone_text += "]" + ",\n"

            bone_text += "\t\t\t\t\t\"unknown_frame_data\": ["
            text_write = ""
            for unknown_frame in bone_entry_data.unknown_frame_data:
                text_write += str(unknown_frame) + ", "
            bone_text += text_write[:-2]
            bone_text += "]" + ",\n"

            bone_text += "\t\t\t\t\t\"unknown_float_data\": ["
            text_write = ""
            for unknown_float in bone_entry_data.unknown_float_data:
                text_write += "{\"x\": " + str(unknown_float['x']) + ", " + "\"y\": " + str(unknown_float['y']) + ", " + "\"z\": " + str(unknown_float['z']) + ", " + \
                              "\"w\": " + str(unknown_float['w']) + "}" + ", "
            bone_text += text_write[:-2]
            bone_text += "]"

            bone_text += "\n\t\t\t\t}" + "," + "\n"
        bone_text = bone_text[:-2] + "\n\t\t\t]\n"

        # Rest of header (after bone count)
        header_text += "\t\"scene_nodes_count\": " + str(spa_header.scene_nodes_count) + ",\n"
        header_text += "\t\"camera_count\": " + str(spa_header.camera_count) + ",\n"
        header_text += "\t\"unk0x28\": " + str(int.from_bytes(spa_header.unk0x28, "big")) + ",\n"
        header_text += "\t\"unk0x2c\": " + str(int.from_bytes(spa_header.unk0x2c, "big")) + ",\n"

        # Write json
        output_file.write("{\n")
        output_file.write(header_text)
        output_file.write(bone_text)
        output_file.write("}")


# Read animation spa and spae files at the same time
def read_animation_file(worker_pef, start_progress, step_report, main_window, index_list_view, combo_box_label, number_files_to_load,
                        size_between_animation, size_between_animation_and_effects):

    item_data_animation = []
    sub_step_report = step_report / number_files_to_load
    for i in range(0, number_files_to_load, size_between_animation):

        # Report progress
        worker_pef.progressText.emit("Reading " + combo_box_label)
        start_progress += (sub_step_report * size_between_animation)
        worker_pef.progressValue.emit(start_progress)

        # Animation instance (detailed version)
        spa_file = read_spa_file(main_window.listView_2.model().item(index_list_view + i, 0).text())

        # Animation effect instance
        animation_effect = Animation()
        animation_effect.path = main_window.listView_2.model().item(size_between_animation_and_effects +
                                                                    index_list_view + i, 0).text()
        with open(animation_effect.path, mode="rb") as file:
            animation_effect.data = file.read()
        animation_effect.size = len(animation_effect.data)

        # Check if the file is 'Transformation in' from properties in order to read the background color
        if index_list_view == 308 and i == 0:
            read_transformation_effect(main_window, animation_effect)

        # Add all the instances to an array
        item_data_animation.append([spa_file, animation_effect])

    # Add the array of Animation instances to the combo box
    main_window.animation_type_value.setItemData(main_window.animation_type_value.findText(combo_box_label),
                                                 item_data_animation)

    return start_progress


# Read all the animation files
def read_animation_files(worker_pef, start_progress, step_report, main_window, offset_index):

    sub_step_report = step_report / IPV.animations_types.__len__()

    # Idle ground
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, offset_index, "Idle ground", 1, 1, 363)
    # Idle fly
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 1 + offset_index, "Idle fly", 1, 1, 363)
    # Charge (in, loop)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 2 + offset_index, "Charge", 2, 1, 363)
    # Charge max
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 4 + offset_index, "Charge max", 1, 1, 363)
    # Idle ground tired
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 5 + offset_index, "Idle ground tired", 1, 1, 363)
    # Idle fly tired
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 6 + offset_index, "Idle fly tired", 1, 1, 363)
    # Dash
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 52 + offset_index, "Dash", 1, 1, 363)
    # Rush attack ground
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 66 + offset_index, "Rush attack ground", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 67 + offset_index, "Rush attack ground 2", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 68 + offset_index, "Rush attack ground 3", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 69 + offset_index, "Rush attack ground 4", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 70 + offset_index, "Rush attack ground 5", 1, 1, 363)
    # Rush attack fly
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 71 + offset_index, "Rush attack fly", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 72 + offset_index, "Rush attack fly 2", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 73 + offset_index, "Rush attack fly 3", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 74 + offset_index, "Rush attack fly 4", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 75 + offset_index, "Rush attack fly 5", 1, 1, 363)
    # Smash attack
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 76 + offset_index, "Smash attack left", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 79 + offset_index, "Smash attack right", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 82 + offset_index, "Smash attack 2", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 85 + offset_index, "Smash attack 3", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 86 + offset_index, "Smash attack 4", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 89 + offset_index, "Smash attack high", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 92 + offset_index, "Smash attack low", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 95 + offset_index, "Finish attack teleport", 2, 1, 363)
    # Charge attack
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 97 + offset_index, "Charge attack", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 100 + offset_index, "Charge attack high", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 103 + offset_index, "Charge attack low", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 106 + offset_index, "Charge attack left", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 109 + offset_index, "Charge attack right", 3, 1, 363)
    # Dash attack
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 112 + offset_index, "Dash attack", 3, 1, 363)
    # Dash charge attack
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 115 + offset_index, "Dash charge attack", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 118 + offset_index, "Dash charge attack high", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 121 + offset_index, "Dash charge attack low", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 124 + offset_index, "Dash charge attack left", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 127 + offset_index, "Dash charge attack right", 3, 1, 363)
    # Shot ki
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 130 + offset_index, "Shot Ki left hand", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 133 + offset_index, "Shot Ki right hand", 3, 1, 363)
    # Charge Shot ki
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 136 + offset_index, "Charge shot Ki", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 139 + offset_index, "Charge shot Ki high", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 142 + offset_index, "Charge shot Ki low", 3, 1, 363)
    # Shot ki while moving
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 145 + offset_index, "Shot Ki moving forward", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 146 + offset_index, "Shot Ki moving left", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 147 + offset_index, "Shot Ki moving right", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 148 + offset_index, "Shot Ki moving back", 1, 1, 363)
    # Charged shot ki while moving
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 149 + offset_index, "Charged shot Ki moving forward", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 152 + offset_index, "Charged shot Ki moving left", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 155 + offset_index, "Charged shot Ki moving right", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 158 + offset_index, "Charged shot Ki moving back", 3, 1, 363)
    # Jump attack
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 161 + offset_index, "Jump attack", 3, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 164 + offset_index, "Jump Ki shot left", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 165 + offset_index, "Jump Ki shot right", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 166 + offset_index, "Jump charged Ki shot", 3, 1, 363)
    # Throw
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 169 + offset_index, "Throw catch", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 170 + offset_index, "Throw", 8, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 178 + offset_index, "Throw wall", 5, 1, 363)
    # Guard
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 267 + offset_index, "Guard", 1, 1, 363)
    # Transformation
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 308 + offset_index, "Transformation in", 2, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 310 + offset_index, "Transformation result", 1, 1, 363)
    # Return
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 311 + offset_index, "Return in", 2, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 313 + offset_index, "Return out", 1, 1, 363)
    # Fusion
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 316 + offset_index, "Fusion in", 2, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 318 + offset_index, "Fusion result", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 319 + offset_index, "Fusion demo", 2, 1, 363)
    # Potala
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 321 + offset_index, "Potara in", 2, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 323 + offset_index, "Potara result", 1, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 324 + offset_index, "Potara demo", 2, 1, 363)
    # Cutscenes
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 336 + offset_index, "Entry 1", 2, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 338 + offset_index, "Entry 2", 2, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 340 + offset_index, "Entry 3", 2, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 342 + offset_index, "Victory", 2, 1, 363)
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, 344 + offset_index, "Lose", 2, 1, 363)

    # Signature
    # Get the total number of signature spa and spae files that are inside the folder
    number_spa_signature_files = os.listdir(os.path.dirname(main_window.listView_2.model().
                                                            item(IPV.signature_folder_index_list_view,
                                                                 0).text())).__len__()
    start_progress = read_animation_file(worker_pef, start_progress, sub_step_report, main_window, IPV.signature_folder_index_list_view + offset_index, "Signature",
                                         number_spa_signature_files, 2, 1)

    return start_progress


def export_camera(file_export_path, camera_cutscene):
    with open(file_export_path, mode="wb") as file:
        write_camera_cutscene_to_file(camera_cutscene, file)


def import_camera(camera_cutscene, file):

    # Import camera to memory
    store_camera_cutscene_from_file(camera_cutscene, file)

    # Set camera as modified
    camera_cutscene.modified = True


def export_animation(animation_array, file_export_path, animation_type_index):

    # We will calculate the number of files that will be written. Some are stored in memory but they have 0 data inside
    number_anim_files = 0

    # Prepare all the output
    header_file = b''
    data_file = b''

    # Get the sizes and data from each animation
    for animation_file in animation_array:
        # Since we've readed the spa storing each bone, we have to create the file output from scratch
        if animation_type_index == 0:
            data, size = write_spa_file(animation_file[animation_type_index])
        else:
            data = animation_file[animation_type_index].data
            size = animation_file[animation_type_index].size

        # We add the animation in the file only if there is data. If there is no data, we add only in the header, the total number of animation files and the size (it will be 0)
        header_file = header_file + struct.pack('>I', size)
        if size > 0:
            data_file = data_file + data
        number_anim_files += 1

    # Write the header properties and then the data
    with open(file_export_path, mode="wb") as file:
        # The header will have the 'SPAS', 'number of animation files', and the size of each animation
        file.write(bytes(IPV.animations_extension.upper(), encoding='utf-8') + struct.pack('>I', number_anim_files) + header_file)

        # Write the data
        file.write(data_file)


def import_animation(main_window, file_export_path, animation_array, animation_type_index, animation_combobox_index,
                     name_file=None, animations_files_error=None):

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

                # Read the number of files that are written in the header
                number_anim_files = int.from_bytes(file.read(4), "big")

                # Get the sizes of each file in the header. While reading we will sum all the sizes to check if the sizes in the header are exactly the same as the size of
                # the file data inside
                sizes_number_of_files = []
                total_size_file_in_header = 0

                # Read the size of each animation file
                for _ in range(number_anim_files):
                    size = int.from_bytes(file.read(4), "big")
                    sizes_number_of_files.append(size)
                    total_size_file_in_header += size

                # The rest of data in the file, is the animations (keyframes and effects) info. We will store the actual size of the data in the file and we will compare them
                data = file.read()
                total_size_file_in_data = len(data)

                # Check if the sizes in the header of the file and in the rest of the data, is exactly the same
                if total_size_file_in_header != total_size_file_in_data:
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

                # Get number of animations stored in memory
                number_anim_memory = len(animation_array)

                # If the modified file has a different number of files inside than the original,
                # we refuse the modified file. With the exception that if the animation that we're modifying is the
                # signature (72)
                if number_anim_memory != number_anim_files:
                    # Means it's not the signature animation
                    if animation_combobox_index != 72:
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

                    # We're changing the signature animation. Since in memory could be more or less files compared
                    # with the ones we're importing, we will 'disable' the leftover files
                    else:
                        data_index_start = 0
                        if number_anim_memory > number_anim_files:
                            # Get each animation file
                            for i in range(0, number_anim_files):
                                data_index_end = data_index_start + sizes_number_of_files[i]

                                # Spa file
                                if animation_type_index == 0:
                                    # We create a temp spa file output in order to reuse the method we created so we can make a spa_file instance
                                    with open("temp_spa", mode="wb") as file_temp:
                                        file_temp.write(data[data_index_start:data_index_end])
                                    spa_file = read_spa_file("temp_spa")

                                    # Modify the spa that is stored in the array memory
                                    animation_array[i][animation_type_index].spa_header = spa_file.spa_header
                                    animation_array[i][animation_type_index].bone_entries = spa_file.bone_entries
                                    animation_array[i][animation_type_index].size = spa_file.size
                                    animation_array[i][animation_type_index].modified = True

                                    # We remove the temporal spa
                                    os.remove("temp_spa")

                                # spae file
                                else:
                                    data_index_end = data_index_start + sizes_number_of_files[i]
                                    animation_array[i][animation_type_index].data = data[data_index_start:data_index_end]
                                    animation_array[i][animation_type_index].size = sizes_number_of_files[i]
                                    animation_array[i][animation_type_index].modified = True

                                data_index_start = data_index_end
                            # Reset the rest of the animations
                            for i in range(number_anim_files, number_anim_memory):
                                # Spa file
                                if animation_type_index == 0:
                                    spa_file = SPAFile()
                                    # Modify the spa that is stored in the array memory
                                    animation_array[i][animation_type_index].spa_header = spa_file.spa_header
                                    animation_array[i][animation_type_index].bone_entries = spa_file.bone_entries
                                    animation_array[i][animation_type_index].size = spa_file.size
                                    animation_array[i][animation_type_index].modified = True
                                else:
                                    animation_array[i][animation_type_index].data = b''
                                    animation_array[i][animation_type_index].size = 0
                                    animation_array[i][animation_type_index].modified = True
                        else:
                            # Get each animation file
                            for i in range(0, number_anim_memory):
                                data_index_end = data_index_start + sizes_number_of_files[i]

                                # Spa file
                                if animation_type_index == 0:
                                    # We create a temp spa file output in order to reuse the method we created so we can make a spa_file instance
                                    with open("temp_spa", mode="wb") as file_temp:
                                        file_temp.write(data[data_index_start:data_index_end])
                                    spa_file = read_spa_file("temp_spa")

                                    # Modify the spa that is stored in the array memory
                                    animation_array[i][animation_type_index].spa_header = spa_file.spa_header
                                    animation_array[i][animation_type_index].bone_entries = spa_file.bone_entries
                                    animation_array[i][animation_type_index].size = spa_file.size
                                    animation_array[i][animation_type_index].modified = True

                                    # We remove the temporal spa
                                    os.remove("temp_spa")

                                # spae file
                                else:
                                    data_index_end = data_index_start + sizes_number_of_files[i]
                                    animation_array[i][animation_type_index].data = data[data_index_start:data_index_end]
                                    animation_array[i][animation_type_index].size = sizes_number_of_files[i]
                                    animation_array[i][animation_type_index].modified = True

                                data_index_start = data_index_end

                            # Get a template basename for the brand new files in the signature
                            path_fist_spa_signature = main_window.listView_2.model()\
                                .item(IPV.signature_folder_index_list_view, 0).text()
                            dirname = os.path.dirname(path_fist_spa_signature)
                            basename = os.path.basename(path_fist_spa_signature)
                            template_basename = basename.split(";")[1]
                            template_basename = template_basename.split("TOK")[0]

                            # Append brand new animations slots
                            for i in range(number_anim_memory, number_anim_files):
                                data_index_end = data_index_start + sizes_number_of_files[i]

                                # Create empty instances
                                spa_file = SPAFile()
                                animation_spae = Animation()

                                # Check if we're importing spa animation
                                if animation_type_index == 0:
                                    # We create a temp spa file output in order to reuse the method we created so we can make a spa_file instance
                                    with open("temp_spa", mode="wb") as file_temp:
                                        file_temp.write(data[data_index_start:data_index_end])
                                    spa_file = read_spa_file("temp_spa")

                                    # Modify the spa that will be stored in the array memory
                                    spa_file.modified = True
                                    spa_file.path = os.path.join(dirname, str(i * 2) + ";" + template_basename + "TOK_" + str(i) + ".spa")

                                    # We remove the temporal spa
                                    os.remove("temp_spa")
                                # Check if we're importing spae animation
                                else:
                                    animation_spae.path = os.path.join(dirname, str((i * 2) + 1) + ";" +
                                                                       template_basename + "TOK_" + str(i) + ".spae")
                                    animation_spae.data = data[data_index_start:data_index_end]
                                    animation_spae.size = sizes_number_of_files[i]
                                    animation_spae.modified = True
                                data_index_start = data_index_end

                                animation_array.append([spa_file, animation_spae])
                else:
                    # Get each animation file
                    data_index_start = 0
                    for i in range(0, number_anim_memory):
                        data_index_end = data_index_start + sizes_number_of_files[i]

                        # Spa file
                        if animation_type_index == 0:
                            # We create a temp spa file output in order to reuse the method we created so we can make a spa_file instance
                            with open("temp_spa", mode="wb") as file_temp:
                                file_temp.write(data[data_index_start:data_index_end])
                            spa_file = read_spa_file("temp_spa")

                            # Modify the spa that is stored in the array memory
                            animation_array[i][animation_type_index].spa_header = spa_file.spa_header
                            animation_array[i][animation_type_index].bone_entries = spa_file.bone_entries
                            animation_array[i][animation_type_index].size = spa_file.size
                            animation_array[i][animation_type_index].modified = True

                            # We remove the temporal spa
                            os.remove("temp_spa")

                        # spae file
                        else:
                            data_index_end = data_index_start + sizes_number_of_files[i]
                            animation_array[i][animation_type_index].data = data[data_index_start:data_index_end]
                            animation_array[i][animation_type_index].size = sizes_number_of_files[i]
                            animation_array[i][animation_type_index].modified = True

                        data_index_start = data_index_end


def export_blast(file_export_path, blast):

    with open(file_export_path, mode="wb") as file:
        write_blast_values_to_file(blast, file)


def import_blast(blast, file):

    # Get the data
    store_blast_values_from_file(blast, file)

    # Set blast as modified
    blast.modified = True
