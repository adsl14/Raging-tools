from PyQt5.QtWidgets import QFileDialog, QMessageBox

from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.classes.Animation import Animation
from lib.character_parameters_editor.classes.CameraCutscene import CameraCutscene
from lib.packages import QLabel, QPixmap, functools, os, struct, natsorted
from lib.design.select_chara import Ui_Dialog


def initialize_cpe(main_window, qt_widgets):

    # --- operate_resident_param ---

    # Load all the mini portraits (main panel)
    CPEV.mini_portraits_image = main_window.mainPanel.findChildren(QLabel)

    for i in range(0, 66):
        index_chara = CPEV.mini_portraits_image[i].objectName().split("_")[1]
        CPEV.mini_portraits_image[i].setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_0" +
                                                                    index_chara + ".bmp")))
        CPEV.mini_portraits_image[i].setStyleSheet("QLabel {border : 3px solid grey;}")
        CPEV.mini_portraits_image[i].mousePressEvent = functools.partial(action_change_character,
                                                                         main_window=main_window,
                                                                         index=int(index_chara),
                                                                         modify_slot_transform=True)

    for i in range(66, len(CPEV.mini_portraits_image)):
        CPEV.mini_portraits_image[i].setStyleSheet("QLabel {border : 3px solid grey;}")

    # Disable all the buttons (operate_resident_param)
    enable_disable_operate_resident_param_frames(main_window, False)

    # Disable all the buttons (operate_character_XXX_m)
    enable_disable_operate_character_xxx_m_frames(main_window, False)

    # Set the health
    main_window.health_value.valueChanged.connect(lambda: on_health_changed(main_window))

    # Set the camera size
    main_window.camera_size_cutscene_value.valueChanged.connect(lambda: on_camera_size_changed(main_window,
                                                                                               camera_index=0))
    main_window.camera_size_idle_value.valueChanged.connect(lambda: on_camera_size_changed(main_window,
                                                                                           camera_index=1))

    # Set the hit box
    main_window.hit_box_value.valueChanged.connect(lambda: on_hit_box_changed(main_window))

    # Set the aura size
    main_window.aura_size_idle_value.valueChanged.connect(lambda: on_aura_size_changed(main_window, aura_index=0))
    main_window.aura_size_dash_value.valueChanged.connect(lambda: on_aura_size_changed(main_window, aura_index=1))
    main_window.aura_size_charge_value.valueChanged.connect(lambda: on_aura_size_changed(main_window, aura_index=2))

    # Set the color lightning
    main_window.color_lightning_value.currentIndexChanged.connect(lambda: on_color_lightning_changed(main_window))
    # Add the values
    for element in CPEV.color_lightning_values:
        main_window.color_lightning_value.addItem(element, CPEV.color_lightning_values[element])

    # Set the glow/lightning
    main_window.glow_lightning_value.currentIndexChanged.connect(lambda: on_glow_lightning_changed(main_window))
    # Add the values
    for element in CPEV.glow_lightning_values:
        main_window.glow_lightning_value.addItem(element, CPEV.glow_lightning_values[element])

    # Set the transform panel
    main_window.transPanel.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_transform.png")))
    main_window.transText.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "tx_transform_US.png")))

    # Set the transformation parameter
    main_window.transEffectValue.currentIndexChanged.connect(lambda: on_transformation_ki_effect_changed(main_window))
    # Add the values
    for element in CPEV.trans_effect_values:
        main_window.transEffectValue.addItem(element, CPEV.trans_effect_values[element])

    # Set the Trasformation partner
    main_window.transPartnerSlot.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_slot.png")))

    # Set the amount ki per transformation
    main_window.amountKi_trans1_value.valueChanged.connect(lambda: on_amount_ki_trans_changed(main_window,
                                                                                              amount_ki_trans_index=0))
    main_window.amountKi_trans2_value.valueChanged.connect(lambda: on_amount_ki_trans_changed(main_window,
                                                                                              amount_ki_trans_index=1))
    main_window.amountKi_trans3_value.valueChanged.connect(lambda: on_amount_ki_trans_changed(main_window,
                                                                                              amount_ki_trans_index=2))
    main_window.amountKi_trans4_value.valueChanged.connect(lambda: on_amount_ki_trans_changed(main_window,
                                                                                              amount_ki_trans_index=3))

    # Set the animation per transformation
    main_window.trans1_animation_value.currentIndexChanged.connect(lambda: on_animation_per_transformation_changed
                                                                   (main_window, animation_per_transformation=0))
    main_window.trans2_animation_value.currentIndexChanged.connect(lambda: on_animation_per_transformation_changed
                                                                   (main_window, animation_per_transformation=1))
    main_window.trans3_animation_value.currentIndexChanged.connect(lambda: on_animation_per_transformation_changed
                                                                   (main_window, animation_per_transformation=2))
    main_window.trans4_animation_value.currentIndexChanged.connect(lambda: on_animation_per_transformation_changed
                                                                   (main_window, animation_per_transformation=3))
    # Add the values
    for element in CPEV.trans_animation_values:
        main_window.trans1_animation_value.addItem(element, CPEV.trans_animation_values[element])
        main_window.trans2_animation_value.addItem(element, CPEV.trans_animation_values[element])
        main_window.trans3_animation_value.addItem(element, CPEV.trans_animation_values[element])
        main_window.trans4_animation_value.addItem(element, CPEV.trans_animation_values[element])

    # Set fusion partner trigger
    main_window.fusionPartnerTrigger_slot.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_slot.png")))

    # Set fusion partner visual
    main_window.fusionPartnerVisual_slot.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_slot.png")))

    # Set the amount ki per fusion
    main_window.amountKi_fusion1_value.valueChanged.connect(lambda:
                                                            on_amount_ki_fusion_changed(main_window,
                                                                                        amount_ki_fusion_index=0))
    main_window.amountKi_fusion2_value.valueChanged.connect(lambda:
                                                            on_amount_ki_fusion_changed(main_window,
                                                                                        amount_ki_fusion_index=1))
    main_window.amountKi_fusion3_value.valueChanged.connect(lambda:
                                                            on_amount_ki_fusion_changed(main_window,
                                                                                        amount_ki_fusion_index=2))
    main_window.amountKi_fusion4_value.valueChanged.connect(lambda:
                                                            on_amount_ki_fusion_changed(main_window,
                                                                                        amount_ki_fusion_index=3))

    # Set the animation per fusion
    main_window.fusion1_animation_value.currentIndexChanged.connect(lambda: on_animation_per_fusion_changed
                                                                    (main_window, animation_per_fusion=0))
    main_window.fusion2_animation_value.currentIndexChanged.connect(lambda: on_animation_per_fusion_changed
                                                                    (main_window, animation_per_fusion=1))
    main_window.fusion3_animation_value.currentIndexChanged.connect(lambda: on_animation_per_fusion_changed
                                                                    (main_window, animation_per_fusion=2))
    main_window.fusion4_animation_value.currentIndexChanged.connect(lambda: on_animation_per_fusion_changed
                                                                    (main_window, animation_per_fusion=3))
    # Add the values
    for element in CPEV.fusion_animation_values:
        main_window.fusion1_animation_value.addItem(element, CPEV.fusion_animation_values[element])
        main_window.fusion2_animation_value.addItem(element, CPEV.fusion_animation_values[element])
        main_window.fusion3_animation_value.addItem(element, CPEV.fusion_animation_values[element])
        main_window.fusion4_animation_value.addItem(element, CPEV.fusion_animation_values[element])

    # Set the fusion panel
    main_window.fusiPanel.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_fusion.png")))
    main_window.fusiPanelText.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "tx_fusion_US.png")))

    # Load the Select Chara window
    main_window.selectCharaWindow = qt_widgets.QMainWindow()
    main_window.selectCharaUI = Ui_Dialog()
    main_window.selectCharaUI.setupUi(main_window.selectCharaWindow)
    CPEV.mini_portraits_image_select_chara_window = main_window.selectCharaUI.frame.findChildren(QLabel)
    for i in range(0, 100):
        CPEV.mini_portraits_image_select_chara_window[i].setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                                        "sc_chara_0" + str(i).zfill(
                                                                                            2) + ".bmp")))
        CPEV.mini_portraits_image_select_chara_window[i].mousePressEvent = functools.partial(
            action_edit_trans_fusion_slot, main_window=main_window, char_selected_new=i)

    # --- operate_character_XXX_m ---

    # Set the camera cutscene type
    main_window.camera_type_key.currentIndexChanged.connect(lambda: on_camera_type_key_changed(main_window))
    for element in CPEV.camera_types_cutscene:
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

    # Set the fighting style
    for element in CPEV.type_of_fighting_values:
        main_window.type_fighting_value.addItem(element, CPEV.type_of_fighting_values[element])

    # Set the direction last hit combo
    for element in CPEV.direction_last_hit_combo_values:
        main_window.direction_last_hit_combo_value.addItem(element, CPEV.direction_last_hit_combo_values[element])

    # Set the background color combo
    for element in CPEV.color_background_combo_values:
        main_window.background_color_combo_value.addItem(element, CPEV.color_background_combo_values[element])

    # Set animations
    for element in CPEV.animations_types:
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
    for element in CPEV.animations_types:
        main_window.animation_properties.addItem(element)
    # Export animation properties button
    main_window.exportAnimationPropertiesButton.clicked.connect(
        lambda: action_export_animation_button_logic(main_window, main_window.animation_properties))
    # Import animation properties button
    main_window.importAnimationPropertiesButton.clicked.connect(
        lambda: action_import_animation_button_logic(main_window, main_window.animation_properties))
    # Export all animation properties button
    main_window.exportAllAnimationPropertiesButton.clicked.connect(
        lambda: action_export_all_animation_button_logic(main_window, main_window.animation_properties, " properties"))
    # Import all animation properties button
    main_window.importAllAnimationPropertiesButton.clicked.connect(
        lambda: action_import_all_animation_button_logic(main_window, main_window.animation_properties))

    # Disable character parameters editor tab
    main_window.character_parameters_editor.setEnabled(False)


def enable_disable_operate_resident_param_frames(main_window, flag):

    main_window.transEffect.setVisible(flag)
    main_window.transPartner.setVisible(flag)
    main_window.amount_ki_per_transformation.setVisible(flag)
    main_window.animation_per_transformation.setVisible(flag)
    main_window.transformPanel.setVisible(flag)
    main_window.fusionPartnerTrigger.setVisible(flag)
    main_window.fusionPartnerVisual.setVisible(flag)
    main_window.amount_ki_per_fusion.setVisible(flag)
    main_window.animation_per_fusion.setVisible(flag)
    main_window.fusionPanel.setVisible(flag)
    main_window.health.setVisible(flag)
    main_window.camera_size.setVisible(flag)
    main_window.hit_box.setVisible(flag)
    main_window.aura_size.setVisible(flag)
    main_window.color_lightning.setVisible(flag)
    main_window.glow_lightning.setVisible(flag)
    main_window.portrait.setVisible(flag)
    main_window.mainPanel.setVisible(flag)


def enable_disable_operate_character_xxx_m_frames(main_window, flag):

    main_window.ki_values.setVisible(flag)
    main_window.melee_values.setVisible(flag)
    main_window.movement_speed.setVisible(flag)
    main_window.camera_values.setVisible(flag)
    main_window.animation_values.setVisible(flag)


# operate_resident_param
def read_character_parameters(character, subpak_file_character_inf, subpak_file_transformer_i):

    # --- character_inf ---
    # Health
    character.health = int.from_bytes(subpak_file_character_inf.read(4), byteorder='big')

    # Camera size '>f' big endian
    character.camera_size.append(struct.unpack('>f', subpak_file_character_inf.read(4))[0])
    character.camera_size.append(struct.unpack('>f', subpak_file_character_inf.read(4))[0])

    # hit box '>f' big endian
    character.hit_box = struct.unpack('>f', subpak_file_character_inf.read(4))[0]

    # UNK data for now
    subpak_file_character_inf.seek(12, 1)

    # Aura size '>f' big endian
    character.aura_size.append(struct.unpack('>f', subpak_file_character_inf.read(4))[0])
    character.aura_size.append(struct.unpack('>f', subpak_file_character_inf.read(4))[0])
    character.aura_size.append(struct.unpack('>f', subpak_file_character_inf.read(4))[0])

    # UNK data for now
    subpak_file_character_inf.seek(5, 1)

    # Color lightnings
    character.color_lightning = int.from_bytes(subpak_file_character_inf.read(1), byteorder='big')

    # UNK data for now
    subpak_file_character_inf.seek(69, 1)

    # Glow/Lightnings
    character.glow_lightning = int.from_bytes(subpak_file_character_inf.read(1), byteorder='big')

    # UNK data for now
    subpak_file_character_inf.seek(32, 1)

    # --- transformer_i ---

    # Character ID
    character.character_id = int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big')
    # destransformation effect
    character.transformation_effect = int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big')
    # transformation_partner
    character.transformation_partner = int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big')

    # Transformation 1
    character.transformations.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # Transformation 2
    character.transformations.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # Transformation 3
    character.transformations.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # Transformation 4
    character.transformations.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))

    # amount_ki_transformations 1
    character.amount_ki_transformations.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # amount_ki_transformations 2
    character.amount_ki_transformations.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # amount_ki_transformations 3
    character.amount_ki_transformations.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # amount_ki_transformations 4
    character.amount_ki_transformations.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))

    # transformations_animation 1
    character.transformations_animation.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # transformations_animation 2
    character.transformations_animation.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # transformations_animation 3
    character.transformations_animation.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # transformations_animation 4
    character.transformations_animation.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))

    # Move four positions because is unk data
    subpak_file_transformer_i.seek(4, 1)

    # fusion partner (trigger and visual)
    character.fusion_partner.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    character.fusion_partner.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))

    # fusions 1
    character.fusions.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # fusions 2
    character.fusions.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # fusions 3
    character.fusions.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # fusions 4
    character.fusions.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))

    # amount_ki_fusions 1
    character.amount_ki_fusions.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # amount_ki_fusions 2
    character.amount_ki_fusions.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # amount_ki_fusions 3
    character.amount_ki_fusions.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # amount_ki_fusions 4
    character.amount_ki_fusions.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))

    # fusions_animation 1
    character.fusions_animation.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # fusions_animation 2
    character.fusions_animation.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # fusions_animation 3
    character.fusions_animation.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))
    # fusions_animation 4
    character.fusions_animation.append(int.from_bytes(subpak_file_transformer_i.read(1), byteorder='big'))


def write_character_parameters(character, subpak_file_character_inf, subpak_file_transformer_i):

    # Move to the visual parameters character
    subpak_file_character_inf.seek(character.position_visual_parameters)

    # Health
    subpak_file_character_inf.write(character.health.to_bytes(4, byteorder="big"))

    # Camera size (cutscene)
    subpak_file_character_inf.write(struct.pack('>f', character.camera_size[0]))
    # Camera size (idle)
    subpak_file_character_inf.write(struct.pack('>f', character.camera_size[1]))

    # hit box
    subpak_file_character_inf.write(struct.pack('>f', character.hit_box))

    # UNK data for now
    subpak_file_character_inf.seek(12, 1)

    # Aura size (idle)
    subpak_file_character_inf.write(struct.pack('>f', character.aura_size[0]))
    # Aura size (dash)
    subpak_file_character_inf.write(struct.pack('>f', character.aura_size[1]))
    # Aura size (charge)
    subpak_file_character_inf.write(struct.pack('>f', character.aura_size[2]))

    # UNK data for now
    subpak_file_character_inf.seek(5, 1)
    # Color lightnining
    subpak_file_character_inf.write(character.color_lightning.to_bytes(1, byteorder="big"))

    # UNK data for now
    subpak_file_character_inf.seek(69, 1)
    # Glow/Lightning
    subpak_file_character_inf.write(character.glow_lightning.to_bytes(1, byteorder="big"))

    # Move to the transformation parameters
    subpak_file_transformer_i.seek(character.position_trans)

    subpak_file_transformer_i.write(character.character_id.to_bytes(1, byteorder="big"))

    subpak_file_transformer_i.write(character.transformation_effect.to_bytes(1, byteorder="big"))
    subpak_file_transformer_i.write(character.transformation_partner.to_bytes(1, byteorder="big"))
    for transformation in character.transformations:
        subpak_file_transformer_i.write(transformation.to_bytes(1, byteorder="big"))
    for trans_ki_ammount in character.amount_ki_transformations:
        subpak_file_transformer_i.write(trans_ki_ammount.to_bytes(1, byteorder="big"))
    for trans_animation in character.transformations_animation:
        subpak_file_transformer_i.write(trans_animation.to_bytes(1, byteorder="big"))

    # Move four positions because is unk data
    subpak_file_transformer_i.seek(4, 1)

    subpak_file_transformer_i.write(character.fusion_partner[0].to_bytes(1, byteorder="big"))
    subpak_file_transformer_i.write(character.fusion_partner[1].to_bytes(1, byteorder="big"))
    for fusion in character.fusions:
        subpak_file_transformer_i.write(fusion.to_bytes(1, byteorder="big"))
    for fusion_ki_ammount in character.amount_ki_fusions:
        subpak_file_transformer_i.write(fusion_ki_ammount.to_bytes(1, byteorder="big"))
    for fusion_animation in character.fusions_animation:
        subpak_file_transformer_i.write(fusion_animation.to_bytes(1, byteorder="big"))


# operate_character_XXX functions (single_character_parameters)
def read_single_character_parameters(main_window):

    # Read all the animation values
    read_animation_files(main_window, 0, main_window.animation_type)
    main_window.animation_type.setCurrentIndex(0)
    read_animation_files(main_window, CPEV.size_between_animation_and_effects, main_window.animation_properties)
    main_window.animation_properties.setCurrentIndex(0)

    # character info
    CPEV.character_i_path = main_window.listView_2.model().item(726, 0).text()
    # camera info
    CPEV.camera_i_path = main_window.listView_2.model().item(727, 0).text()

    # Read character info file
    with open(CPEV.character_i_path, mode="rb") as file:

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

        # Type fighting
        file.seek(9, 1)
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
    with open(CPEV.camera_i_path, mode="rb") as file:

        # Move to position 208 where the first camera cutscene starts
        file.seek(CPEV.position_camera_cutscene)

        for i in range(0, len(CPEV.camera_types_cutscene)):
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


def write_single_character_parameters(main_window):

    # Save all animation info (replace first the entire files)
    for i in range(0, len(CPEV.animations_types)):
        animation_files = main_window.animation_type.itemData(i)
        animation_properties_files = main_window.animation_properties.itemData(i)

        for j in range(0, len(animation_files)):
            if animation_files[j].modified:
                with open(animation_files[j].path, mode="wb") as file:
                    file.write(animation_files[j].data)

            if animation_properties_files[j].modified:
                with open(animation_properties_files[j].path, mode="wb") as file:
                    file.write(animation_properties_files[j].data)

    # Save all camera info
    with open(CPEV.camera_i_path, mode="rb+") as file:

        # Move to position 208 where the first camera cutscene starts
        file.seek(CPEV.position_camera_cutscene)

        for i in range(0, len(CPEV.camera_types_cutscene)):

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
                file.seek(CPEV.size_each_camera_cutscene, 1)

    # Save all the info
    with open(CPEV.character_i_path, mode="rb+") as file:
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

        # Type fighting
        file.seek(9, 1)
        file.write(main_window.type_fighting_value.currentData().to_bytes(1, byteorder="big"))

        # Direction last hit fast combo
        file.seek(1, 1)
        file.write(main_window.direction_last_hit_combo_value.currentData().to_bytes(1, byteorder="big"))

        # Color background fast combo
        file.seek(3, 1)
        file.write(main_window.background_color_combo_value.currentData().to_bytes(1, byteorder="big"))


# Load the necesary animation files.
# index_list_view (index file in the list view from pack explorer)
# combo_box_label (label from combo box in design)
# number_files_to_load (number of files that is necessary to load in order to save the animation.
# animation_combo_box (combo box with all the data for each label)
# It doesn't count the effects)
def read_animation_file(main_window, index_list_view, combo_box_label, number_files_to_load, animation_combo_box):

    item_data_animation = []
    for i in range(0, number_files_to_load):

        # Animation instance
        animation = Animation()
        animation.path = main_window.listView_2.model().item(index_list_view + i, 0).text()
        with open(animation.path, mode="rb") as file:
            animation.data = file.read()
        animation.size = len(animation.data)

        # Add all the instances to an array
        item_data_animation.append(animation)
    # Add the array of Animation instances to the combo box
    animation_combo_box.setItemData(animation_combo_box.findText(combo_box_label), item_data_animation)


# Read all the animation files
def read_animation_files(main_window, offset_index, animation_combo_box):

    # Idle ground
    read_animation_file(main_window, 0+offset_index, "Idle ground", 1, animation_combo_box)
    # Idle fly
    read_animation_file(main_window, 1+offset_index, "Idle fly", 1, animation_combo_box)
    # Charge (in, loop)
    read_animation_file(main_window, 2+offset_index, "Charge", 2, animation_combo_box)
    # Charge max
    read_animation_file(main_window, 3+offset_index, "Charge max", 1, animation_combo_box)
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


def action_change_character(event, main_window, index=None, modify_slot_transform=False):
    # Change only if the char selected is other
    if CPEV.chara_selected != index:

        # We're changing the character in the main panel (avoid combo box code)
        CPEV.change_character = True

        # Load the portrait
        main_window.portrait.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_" +
                                                            str(index).zfill(3) + ".png")))

        # Health
        main_window.health_value.setValue(CPEV.character_list[index].health)

        # Camera size
        main_window.camera_size_cutscene_value.setValue(CPEV.character_list[index].camera_size[0])
        main_window.camera_size_idle_value.setValue(CPEV.character_list[index].camera_size[1])

        # hit box
        main_window.hit_box_value.setValue(CPEV.character_list[index].hit_box)

        # Aura size
        main_window.aura_size_idle_value.setValue(CPEV.character_list[index].aura_size[0])
        main_window.aura_size_dash_value.setValue(CPEV.character_list[index].aura_size[1])
        main_window.aura_size_charge_value.setValue(CPEV.character_list[index].aura_size[2])

        # Color lightning
        main_window.color_lightning_value.setCurrentIndex(main_window.color_lightning_value.findData
                                                          (CPEV.character_list[index].color_lightning))

        # Glow/lightning effect
        main_window.glow_lightning_value.setCurrentIndex(main_window.glow_lightning_value.findData
                                                         (CPEV.character_list[index].glow_lightning))

        # Load the transformations for the panel transformations
        transformations = CPEV.character_list[index].transformations
        # Change panel transformations and their interactions
        if transformations[0] != 100:
            main_window.transSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(transformations[0]).zfill(3) + ".png")))
            main_window.transSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=transformations[0],
                                                                            trans_slot_panel_index=0)
            main_window.transSlotPanel0.setVisible(True)
        else:
            main_window.transSlotPanel0.setPixmap(QPixmap())
            main_window.transSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=100, trans_slot_panel_index=0)
        if transformations[1] != 100:
            main_window.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(transformations[1]).zfill(3) + ".png")))
            main_window.transSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=transformations[1],
                                                                            trans_slot_panel_index=1)
            main_window.transSlotPanel1.setVisible(True)
        else:
            main_window.transSlotPanel1.setPixmap(QPixmap())
            main_window.transSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=100, trans_slot_panel_index=1)
        if transformations[2] != 100:
            main_window.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(transformations[2]).zfill(3) + ".png")))
            main_window.transSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=transformations[2],
                                                                            trans_slot_panel_index=2)
            main_window.transSlotPanel2.setVisible(True)
        else:
            main_window.transSlotPanel2.setPixmap(QPixmap())
            main_window.transSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=100, trans_slot_panel_index=2)
        if transformations[3] != 100:
            main_window.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(transformations[3]).zfill(3) + ".png")))
            main_window.transSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=transformations[3],
                                                                            trans_slot_panel_index=3)
            main_window.transSlotPanel3.setVisible(True)
        else:
            main_window.transSlotPanel3.setPixmap(QPixmap())
            main_window.transSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=100, trans_slot_panel_index=3)

        # Transformation effect
        main_window.transEffectValue.setCurrentIndex(main_window.transEffectValue.findData
                                                     (CPEV.character_list[index].transformation_effect))

        # Trans partner value
        main_window.transPartnerValue.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                     str(CPEV.character_list[
                                                                             index].transformation_partner).zfill(3)
                                                                     + ".png")))
        main_window.transPartnerValue.mousePressEvent = functools.partial(open_select_chara_window,
                                                                          main_window=main_window,
                                                                          index=CPEV.character_list[
                                                                              index].transformation_partner,
                                                                          transformation_partner_flag=True)

        # amount ki per transformation
        main_window.amountKi_trans1_value.setValue(CPEV.character_list[index].amount_ki_transformations[0])
        main_window.amountKi_trans2_value.setValue(CPEV.character_list[index].amount_ki_transformations[1])
        main_window.amountKi_trans3_value.setValue(CPEV.character_list[index].amount_ki_transformations[2])
        main_window.amountKi_trans4_value.setValue(CPEV.character_list[index].amount_ki_transformations[3])

        # Animation per transformation
        main_window.trans1_animation_value.setCurrentIndex(main_window.trans1_animation_value.findData
                                                           (CPEV.character_list[index].transformations_animation[0]))
        main_window.trans2_animation_value.setCurrentIndex(main_window.trans2_animation_value.findData
                                                           (CPEV.character_list[index].transformations_animation[1]))
        main_window.trans3_animation_value.setCurrentIndex(main_window.trans3_animation_value.findData
                                                           (CPEV.character_list[index].transformations_animation[2]))
        main_window.trans4_animation_value.setCurrentIndex(main_window.trans4_animation_value.findData
                                                           (CPEV.character_list[index].transformations_animation[3]))

        # Load the fusions for the panel of fusions
        fusions = CPEV.character_list[index].fusions
        # Change panel fusions and their interactions
        if fusions[0] != 100:
            main_window.fusiSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(fusions[0]).zfill(3) + ".png")))
            main_window.fusiSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=fusions[0],
                                                                           fusion_slot_panel_index=0)
            main_window.fusiSlotPanel0.setVisible(True)
        else:
            main_window.fusiSlotPanel0.setPixmap(QPixmap())
            main_window.fusiSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=100,
                                                                           fusion_slot_panel_index=0)
        if fusions[1] != 100:
            main_window.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(fusions[1]).zfill(3) + ".png")))
            main_window.fusiSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=fusions[1],
                                                                           fusion_slot_panel_index=1)
            main_window.fusiSlotPanel1.setVisible(True)
        else:
            main_window.fusiSlotPanel1.setPixmap(QPixmap())
            main_window.fusiSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=100, fusion_slot_panel_index=1)
        if fusions[2] != 100:
            main_window.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(fusions[2]).zfill(3) + ".png")))
            main_window.fusiSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=fusions[2],
                                                                           fusion_slot_panel_index=2)
            main_window.fusiSlotPanel2.setVisible(True)
        else:
            main_window.fusiSlotPanel2.setPixmap(QPixmap())
            main_window.fusiSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=100, fusion_slot_panel_index=2)
        if fusions[3] != 100:
            main_window.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(fusions[3]).zfill(3) + ".png")))
            main_window.fusiSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=fusions[3],
                                                                           fusion_slot_panel_index=3)
            main_window.fusiSlotPanel3.setVisible(True)
        else:
            main_window.fusiSlotPanel3.setPixmap(QPixmap())
            main_window.fusiSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=100, fusion_slot_panel_index=3)

        # Show the fusion partner trigger
        main_window.fusionPartnerTrigger_value.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                              "sc_chara_s_" +
                                                                              str(CPEV.character_list[
                                                                               index].fusion_partner[0]).zfill(3)
                                                                              + ".png")))
        main_window.fusionPartnerTrigger_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                   main_window=main_window,
                                                                                   index=CPEV.character_list[index]
                                                                                   .fusion_partner[0],
                                                                                   fusion_partner_trigger_flag=True)

        # Show the fusion partner visual
        main_window.fusionPartnerVisual_value.setPixmap(
            QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                 str(CPEV.character_list[index].fusion_partner[1]).zfill(3)
                                 + ".png")))
        main_window.fusionPartnerVisual_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                  main_window=main_window,
                                                                                  index=CPEV.character_list[index].
                                                                                  fusion_partner[1],
                                                                                  fusion_partner_visual_flag=True)

        # Show amount ki per fusion
        main_window.amountKi_fusion1_value.setValue(CPEV.character_list[index].amount_ki_fusions[0])
        main_window.amountKi_fusion2_value.setValue(CPEV.character_list[index].amount_ki_fusions[1])
        main_window.amountKi_fusion3_value.setValue(CPEV.character_list[index].amount_ki_fusions[2])
        main_window.amountKi_fusion4_value.setValue(CPEV.character_list[index].amount_ki_fusions[3])

        # Show Animation per Fusion
        main_window.fusion1_animation_value.setCurrentIndex(main_window.fusion1_animation_value.findData
                                                            (CPEV.character_list[index].fusions_animation[0]))
        main_window.fusion2_animation_value.setCurrentIndex(main_window.fusion2_animation_value.findData
                                                            (CPEV.character_list[index].fusions_animation[1]))
        main_window.fusion3_animation_value.setCurrentIndex(main_window.fusion3_animation_value.findData
                                                            (CPEV.character_list[index].fusions_animation[2]))
        main_window.fusion4_animation_value.setCurrentIndex(main_window.fusion4_animation_value.findData
                                                            (CPEV.character_list[index].fusions_animation[3]))

        # Modify the slots of the transformations in the main panel
        if modify_slot_transform:

            # Disable all the transformations of the slots if it has been activated in the main panel
            if main_window.label_trans_0.isVisible():
                main_window.label_trans_0.setVisible(False)
                main_window.label_trans_1.setVisible(False)
                main_window.label_trans_2.setVisible(False)
                main_window.label_trans_3.setVisible(False)

            # Get the original transformations for the character
            if index in CPEV.characters_with_trans:
                transformations = CPEV.characters_with_trans_index[CPEV.characters_with_trans.index(index)]
                num_transformations = len(transformations)
                if num_transformations > 0:
                    main_window.label_trans_0.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_" +
                                                                             str(transformations[0]).zfill(
                                                                                 3) + ".bmp")))
                    main_window.label_trans_0.mousePressEvent = functools.partial(action_change_character,
                                                                                  main_window=main_window,
                                                                                  index=transformations[0],
                                                                                  modify_slot_transform=False)
                    main_window.label_trans_0.setVisible(True)
                    if num_transformations > 1:
                        main_window.label_trans_1.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_" +
                                                                                 str(transformations[1]).zfill(3) +
                                                                                 ".bmp")))
                        main_window.label_trans_1.mousePressEvent = functools.partial(action_change_character,
                                                                                      main_window=main_window,
                                                                                      index=transformations[1],
                                                                                      modify_slot_transform=False)
                        main_window.label_trans_1.setVisible(True)
                        if num_transformations > 2:
                            main_window.label_trans_2.setPixmap(
                                QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_" +
                                                     str(transformations[2]).zfill(3) +
                                                     ".bmp")))
                            main_window.label_trans_2.mousePressEvent = functools.partial(action_change_character,
                                                                                          main_window=main_window,
                                                                                          index=transformations[2],
                                                                                          modify_slot_transform=False)
                            main_window.label_trans_2.setVisible(True)
                            if num_transformations > 3:
                                main_window.label_trans_3.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                                         "sc_chara_" +
                                                                                         str(transformations[3]).zfill(
                                                                                             3) +
                                                                                         ".bmp")))
                                main_window.label_trans_3.mousePressEvent = functools.partial(action_change_character,
                                                                                              main_window=main_window,
                                                                                              index=transformations[3],
                                                                                              modify_slot_transform=False)
                                main_window.label_trans_3.setVisible(True)

                                # Store the actual index selected of the char
        CPEV.chara_selected = index

        # We're not changing the character in the main panel (play combo box code)
        CPEV.change_character = False


def open_select_chara_window(event, main_window, index, trans_slot_panel_index=None, fusion_slot_panel_index=None,
                             transformation_partner_flag=False, fusion_partner_trigger_flag=False,
                             fusion_partner_visual_flag=False):
    # Check what selected the user. If the user didn't select the transform panel or transform partner
    # then, the user selected the fusion panel (or potara or metamoran)
    if trans_slot_panel_index is not None or transformation_partner_flag:
        q_label_style = "QLabel {border : 3px solid red;}"
    else:
        q_label_style = "QLabel {border : 3px solid green;}"

    # Store in a global var what slot in the transformation and fusion panel has been selected
    CPEV.trans_slot_panel_selected = trans_slot_panel_index
    CPEV.transformation_partner_flag = transformation_partner_flag
    CPEV.fusion_slot_panel_selected = fusion_slot_panel_index
    CPEV.fusion_partner_flag[0] = fusion_partner_trigger_flag
    CPEV.fusion_partner_flag[1] = fusion_partner_visual_flag

    # The character selected in the slot panel (trans or fusion) is not empty
    if index != 100:

        # The previous chara selected and the new are differents
        if CPEV.previous_chara_selected_character_window != index:

            # Add the color border to the character that has been selected in the trans/fusion slot
            CPEV.mini_portraits_image_select_chara_window[index].setStyleSheet(q_label_style)

            # Reset the previous character select if is not a empty character
            if CPEV.previous_chara_selected_character_window != 100:
                CPEV.mini_portraits_image_select_chara_window[CPEV.previous_chara_selected_character_window] \
                    .setStyleSheet("QLabel {}")

            # Store the actual character selected in the select character window
            CPEV.previous_chara_selected_character_window = index

        # If the color border isn't the same, means the user has selected a different slot (trans or fusion
        # or partners)
        elif CPEV.mini_portraits_image_select_chara_window[index].styleSheet() != q_label_style:

            # Add the color border to the character that has been selected in the trans/fusion slot
            CPEV.mini_portraits_image_select_chara_window[index].setStyleSheet(q_label_style)

            # Store the actual character selected in the select character window
            CPEV.previous_chara_selected_character_window = index

    # If the index is 100 (means there's no character transformation),
    # we will remove the red/green border for the previous character transform panel
    elif CPEV.previous_chara_selected_character_window != index:
        CPEV.mini_portraits_image_select_chara_window[CPEV.previous_chara_selected_character_window] \
            .setStyleSheet("QLabel {}")

        CPEV.previous_chara_selected_character_window = index

    main_window.selectCharaWindow.show()


def action_edit_trans_fusion_slot(event, main_window, char_selected_new):
    # Check if the user wants to edit the transformation slot
    if CPEV.trans_slot_panel_selected is not None:

        # If the selected character in the window is the same as in the panel transformations,
        # we assume there won't be any transformation in that slot
        # so it will be 100
        if CPEV.character_list[CPEV.chara_selected].transformations[CPEV.trans_slot_panel_selected] == \
           char_selected_new:
            char_selected_new = 100

        # Change the transformation in our array of characters
        CPEV.character_list[CPEV.chara_selected].transformations[CPEV.trans_slot_panel_selected] = char_selected_new

        # Change the visual transformation
        if CPEV.trans_slot_panel_selected == 0:
            main_window.transSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=0)
        elif CPEV.trans_slot_panel_selected == 1:
            main_window.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=1)
        elif CPEV.trans_slot_panel_selected == 2:
            main_window.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=2)
        elif CPEV.trans_slot_panel_selected == 3:
            main_window.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=3)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])

    # transformation partner slot
    elif CPEV.transformation_partner_flag:

        # If the selected character in the window is the same as in the transformation partner slot,
        # we assume there won't be any transformation partner in that slot
        # so it will be 100
        if CPEV.character_list[CPEV.chara_selected].transformation_partner == \
           char_selected_new:
            char_selected_new = 100

        # Change the fusion in our array of characters
        CPEV.character_list[CPEV.chara_selected].transformation_partner = char_selected_new

        main_window.transPartnerValue.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                     str(char_selected_new).zfill(3) + ".png")))
        main_window.transPartnerValue.mousePressEvent = functools.partial(open_select_chara_window,
                                                                          main_window=main_window,
                                                                          index=char_selected_new,
                                                                          transformation_partner_flag=True)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])

    # fusion slot
    elif CPEV.fusion_slot_panel_selected is not None:

        # If the selected character in the window is the same as in the panel fusions,
        # we assume there won't be any fusion in that slot
        # so it will be 100
        if CPEV.character_list[CPEV.chara_selected].fusions[CPEV.fusion_slot_panel_selected] == \
           char_selected_new:
            char_selected_new = 100

        # Change the fusion in our array of characters
        CPEV.character_list[CPEV.chara_selected].fusions[CPEV.fusion_slot_panel_selected] = char_selected_new

        # Change the visual fusion
        if CPEV.fusion_slot_panel_selected == 0:
            main_window.fusiSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=0)
        elif CPEV.fusion_slot_panel_selected == 1:
            main_window.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=1)
        elif CPEV.fusion_slot_panel_selected == 2:
            main_window.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=2)
        elif CPEV.fusion_slot_panel_selected == 3:
            main_window.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=3)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])

    # fusion partner trigger slot
    elif CPEV.fusion_partner_flag[0]:

        # If the selected character in the window is the same as in the potara partner slot,
        # we assume there won't be any potara partner in that slot
        # so it will be 100
        if CPEV.character_list[CPEV.chara_selected].fusion_partner[0] == \
           char_selected_new:
            char_selected_new = 100

        # Change the fusion in our array of characters
        CPEV.character_list[CPEV.chara_selected].fusion_partner[0] = char_selected_new

        main_window.fusionPartnerTrigger_value.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                              "sc_chara_s_" +
                                                                              str(char_selected_new).zfill(3) +
                                                                              ".png")))
        main_window.fusionPartnerTrigger_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                   main_window=main_window,
                                                                                   index=char_selected_new,
                                                                                   fusion_partner_trigger_flag=True)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])

    # fusion partner visual slot
    elif CPEV.fusion_partner_flag[1]:

        # If the selected character in the window is the same as in the metamoran partner slot,
        # we assume there won't be any metamoran partner in that slot
        # so it will be 100
        if CPEV.character_list[CPEV.chara_selected].fusion_partner[1] == \
           char_selected_new:
            char_selected_new = 100

        # Change the fusion in our array of characters
        CPEV.character_list[CPEV.chara_selected].fusion_partner[1] = char_selected_new

        main_window.fusionPartnerVisual_value.setPixmap(
            QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                 str(char_selected_new).zfill(3) + ".png")))
        main_window.fusionPartnerVisual_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                  main_window=main_window,
                                                                                  index=char_selected_new,
                                                                                  fusion_partner_visual_flag=True)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])

    main_window.selectCharaWindow.close()


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


def action_export_camera_button_logic(main_window):

    # Ask to the user the file output
    name_file = CPEV.character_id + "_" + str(main_window.camera_type_key.currentIndex()) + "_" + \
                main_window.camera_type_key.currentText().replace(" ", "_") + "." + CPEV.camera_extension
    file_export_path = QFileDialog.getSaveFileName(main_window, "Export camera", name_file, "")[0]

    if file_export_path:

        camera_cutscene = main_window.camera_type_key.currentData()

        export_camera(file_export_path, camera_cutscene)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        message = "The camera file was exported in: <b>" + file_export_path \
                  + "</b><br><br> Do you wish to open the path?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + os.path.dirname(file_export_path).replace("/", "\\"))


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


def action_import_camera_button_logic(main_window):

    # Ask to the user from what file wants to open the camera files
    file_export_path = QFileDialog.getOpenFileName(main_window, "Import camera", main_window.old_path_file, "")[0]

    if os.path.exists(file_export_path):

        with open(file_export_path, mode="rb") as file:

            size_file = len(file.read())

            # The file of the camera has to be 52 bytes length
            if size_file == CPEV.size_each_camera_cutscene:
                file.seek(0)
            else:
                # Wrong camera file
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Invalid camera file.")
                msg.exec()
                return

            # Get the instance of the combo box
            camera_cutscene = main_window.camera_type_key.currentData()

            # Import camera to memory
            import_camera(camera_cutscene, file)

        # Set camera values to current combo box and show them in the tool
        change_camera_cutscene_values(main_window, camera_cutscene)

        # Change old path
        main_window.old_path_file = file_export_path


def action_export_all_camera_button_logic(main_window):

    # Ask to the user the folder output
    name_folder = CPEV.character_id + "_cameras"
    folder_export_path = QFileDialog.getSaveFileName(main_window, "Export cameras", name_folder, "")[0]

    if folder_export_path:

        # Create the folder
        if not os.path.exists(folder_export_path):
            os.mkdir(folder_export_path)

        # Export all the files to the folder
        for i in range(0, main_window.camera_type_key.count()):
            name_file = CPEV.character_id + "_" + str(i) + "_" + \
                        main_window.camera_type_key.itemText(i).replace(" ", "_") + "." + CPEV.camera_extension
            file_export_path = os.path.join(folder_export_path, name_file)

            camera_cutscene = main_window.camera_type_key.itemData(i)

            export_camera(file_export_path, camera_cutscene)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        message = "The camera files weres exported in: <b>" + folder_export_path \
                  + "</b><br><br> Do you wish to open the path?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + folder_export_path.replace("/", "\\"))


def action_import_all_camera_button_logic(main_window):

    # Ask to the user from what file wants to open the camera files
    folder_import = QFileDialog.getExistingDirectory(main_window, "Import cameras", "")

    cameras_files_error = []

    if folder_import:

        cameras_files = natsorted(os.listdir(folder_import), key=lambda y: y.lower())
        # Get the filename of each camera
        for i in range(0, len(cameras_files)):

            # Read all the data
            file_export_path = os.path.join(folder_import, cameras_files[i])
            with open(file_export_path, mode="rb") as file:

                size_file = len(file.read())
                file.seek(0)

                # Check if camera has the correct size
                if size_file == CPEV.size_each_camera_cutscene:

                    # Create an instance of cameraCutscene
                    camera_cutscene = main_window.camera_type_key.itemData(i)

                    # Import camera to memory
                    import_camera(camera_cutscene, file)

                    # Change the values in the tool only for the current selected item
                    if main_window.camera_type_key.currentIndex() == i:
                        change_camera_cutscene_values(main_window, camera_cutscene)

                else:
                    cameras_files_error.append(cameras_files[i])
        
        # We show a message with the cameras files that couldn't get imported
        if cameras_files_error:

            message = ""

            for cameras_file_error in cameras_files_error:
                message = message + "<li>" + cameras_file_error + "</li>"
            message = "The following cameras couldn't get imported <ul>" + message + "</ul>"

            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText(message)
            msg.exec()


def action_export_animation_button_logic(main_window, animation_combo_box):
    # Ask to the user the file output
    name_file = CPEV.character_id + "_" + str(animation_combo_box.currentIndex()) + "_" + \
                animation_combo_box.currentText().replace(" ", "_") + "." + CPEV.animations_extension
    file_export_path = QFileDialog.getSaveFileName(main_window, "Export animation", name_file, "")[0]

    # The user has selected an output
    if file_export_path:

        # Get from the combo box, the array of animations ([[keyframes + effect], [keyframes + effects]])
        animation_array = animation_combo_box.currentData()

        export_animation(animation_array, file_export_path)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        message = "The animation file was exported in: <b>" + file_export_path \
                  + "</b><br><br> Do you wish to open the path?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + os.path.dirname(file_export_path).replace("/", "\\"))


def action_export_all_animation_button_logic(main_window, animation_combo_box, properties_text=""):
    # Ask to the user the folder output
    name_folder = CPEV.character_id + "_animations" + ("_" + properties_text if properties_text else "")
    folder_export_path = QFileDialog.getSaveFileName(main_window,
                                                     "Export animations" + properties_text, name_folder, "")[0]

    if folder_export_path:

        # Create the folder
        if not os.path.exists(folder_export_path):
            os.mkdir(folder_export_path)

        # Export all the files to the folder
        for i in range(0, animation_combo_box.count()):
            name_file = CPEV.character_id + "_" + str(i) + "_" + \
                        animation_combo_box.itemText(i).replace(" ", "_") + "." + CPEV.animations_extension
            file_export_path = os.path.join(folder_export_path, name_file)

            animation = animation_combo_box.itemData(i)

            export_animation(animation, file_export_path)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        message = "The animation files weres exported in: <b>" + folder_export_path \
                  + "</b><br><br> Do you wish to open the path?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + folder_export_path.replace("/", "\\"))


def export_animation(animation_array, file_export_path):

    # Get the number of animations files
    number_anim_files = len(animation_array)

    # The header will have the 'SPAS', 'number of animation files', and the size of each
    # of one in the same order
    header_file = bytes(CPEV.animations_extension.upper(), encoding='utf-8')
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


def action_import_animation_button_logic(main_window, animation_combo_box):

    # Ask to the user from what file wants to open the camera files
    file_export_path = QFileDialog.getOpenFileName(main_window, "Import animation", main_window.old_path_file, "")[0]

    if os.path.exists(file_export_path):

        # Import a single animation
        animation_array = animation_combo_box.currentData()
        import_animation(file_export_path, animation_array)

        # Change old path
        main_window.old_path_file = file_export_path


def action_import_all_animation_button_logic(main_window, animation_combo_box):
    # Ask to the user from what file wants to open the camera files
    folder_import = QFileDialog.getExistingDirectory(main_window, "Import animations", "")

    animations_files_error = []

    if folder_import:

        animation_files = natsorted(os.listdir(folder_import), key=lambda y: y.lower())
        # Get the filename of each animation
        for i in range(0, len(animation_files)):

            # Import every single animation
            animation_array = animation_combo_box.itemData(i)
            import_animation(os.path.join(folder_import, animation_files[i]), animation_array,
                             animation_files[i], animations_files_error)

        # We show a message with the animations files that couldn't get imported
        if animations_files_error:

            message = ""

            for animations_file_error in animations_files_error:
                message = message + "<li>" + animations_file_error + "</li>"
            message = "The following animations couldn't get imported <ul>" + message + "</ul>"

            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText(message)
            msg.exec()


def import_animation(file_export_path, animation_array, name_file=None, animations_files_error=None):

    if file_export_path:

        with open(file_export_path, mode="rb") as file:

            header_type = file.read(4)

            # The header needs to have 'SPAS' as a header
            if header_type.decode("utf-8").lower() != CPEV.animations_extension:
                if animations_files_error is not None:
                    animations_files_error.append(name_file)
                    return
                else:
                    # Wrong animation file
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
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
                for i in range(number_anim_files):
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


def on_color_lightning_changed(main_window):
    #  and starting
    if not CPEV.change_character:
        CPEV.character_list[CPEV.chara_selected].color_lightning = main_window.color_lightning_value.currentData()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_glow_lightning_changed(main_window):
    #  and starting
    if not CPEV.change_character:
        CPEV.character_list[CPEV.chara_selected].glow_lightning = main_window.glow_lightning_value.currentData()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_transformation_ki_effect_changed(main_window):
    #  and starting
    if not CPEV.change_character:
        CPEV.character_list[CPEV.chara_selected].transformation_effect = main_window.transEffectValue.currentData()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_amount_ki_trans_changed(main_window, amount_ki_trans_index):
    #  and starting
    if not CPEV.change_character:

        # Change the slot of amount ki
        if amount_ki_trans_index == 0:
            CPEV.character_list[CPEV.chara_selected].amount_ki_transformations[amount_ki_trans_index] = \
                main_window.amountKi_trans1_value.value()
        elif amount_ki_trans_index == 1:
            CPEV.character_list[CPEV.chara_selected].amount_ki_transformations[amount_ki_trans_index] = \
                main_window.amountKi_trans2_value.value()
        elif amount_ki_trans_index == 2:
            CPEV.character_list[CPEV.chara_selected].amount_ki_transformations[amount_ki_trans_index] = \
                main_window.amountKi_trans3_value.value()
        elif amount_ki_trans_index == 3:
            CPEV.character_list[CPEV.chara_selected].amount_ki_transformations[amount_ki_trans_index] = \
                main_window.amountKi_trans4_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_animation_per_transformation_changed(main_window, animation_per_transformation):
    #  and starting
    if not CPEV.change_character:
        if animation_per_transformation == 0:
            CPEV.character_list[CPEV.chara_selected].transformations_animation[animation_per_transformation] = \
                main_window.trans1_animation_value.currentData()
        elif animation_per_transformation == 1:
            CPEV.character_list[CPEV.chara_selected].transformations_animation[animation_per_transformation] = \
                main_window.trans2_animation_value.currentData()
        elif animation_per_transformation == 2:
            CPEV.character_list[CPEV.chara_selected].transformations_animation[animation_per_transformation] = \
                main_window.trans3_animation_value.currentData()
        elif animation_per_transformation == 3:
            CPEV.character_list[CPEV.chara_selected].transformations_animation[animation_per_transformation] = \
                main_window.trans4_animation_value.currentData()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_amount_ki_fusion_changed(main_window, amount_ki_fusion_index):
    #  and starting
    if not CPEV.change_character:

        # Change the slot of amount ki
        if amount_ki_fusion_index == 0:
            CPEV.character_list[CPEV.chara_selected].amount_ki_fusions[amount_ki_fusion_index] = \
                main_window.amountKi_fusion1_value.value()
        elif amount_ki_fusion_index == 1:
            CPEV.character_list[CPEV.chara_selected].amount_ki_fusions[amount_ki_fusion_index] = \
                main_window.amountKi_fusion2_value.value()
        elif amount_ki_fusion_index == 2:
            CPEV.character_list[CPEV.chara_selected].amount_ki_fusions[amount_ki_fusion_index] = \
                main_window.amountKi_fusion3_value.value()
        elif amount_ki_fusion_index == 3:
            CPEV.character_list[CPEV.chara_selected].amount_ki_fusions[amount_ki_fusion_index] = \
                main_window.amountKi_fusion4_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_animation_per_fusion_changed(main_window, animation_per_fusion):
    #  and starting
    if not CPEV.change_character:
        if animation_per_fusion == 0:
            CPEV.character_list[CPEV.chara_selected].fusions_animation[animation_per_fusion] = \
                main_window.fusion1_animation_value.currentData()
        elif animation_per_fusion == 1:
            CPEV.character_list[CPEV.chara_selected].fusions_animation[animation_per_fusion] = \
                main_window.fusion2_animation_value.currentData()
        elif animation_per_fusion == 2:
            CPEV.character_list[CPEV.chara_selected].fusions_animation[animation_per_fusion] = \
                main_window.fusion3_animation_value.currentData()
        elif animation_per_fusion == 3:
            CPEV.character_list[CPEV.chara_selected].fusions_animation[animation_per_fusion] = \
                main_window.fusion4_animation_value.currentData()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_aura_size_changed(main_window, aura_index):
    #  and starting
    if not CPEV.change_character:

        if aura_index == 0:
            # Change the slot of aura idle size
            CPEV.character_list[CPEV.chara_selected].aura_size[0] = main_window.aura_size_idle_value.value()
        elif aura_index == 1:
            # Change the slot of aura dash size
            CPEV.character_list[CPEV.chara_selected].aura_size[1] = main_window.aura_size_dash_value.value()
        else:
            # Change the slot of aura dash size
            CPEV.character_list[CPEV.chara_selected].aura_size[2] = main_window.aura_size_charge_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_health_changed(main_window):
    #  and starting
    if not CPEV.change_character:

        # Change the slot of health
        CPEV.character_list[CPEV.chara_selected].health = main_window.health_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_camera_size_changed(main_window, camera_index):
    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:

        if camera_index == 0:
            # Change the slot of camera cutscene size
            CPEV.character_list[CPEV.chara_selected].camera_size[0] = main_window.camera_size_cutscene_value.value()
        else:
            # Change the slot of camera idle size
            CPEV.character_list[CPEV.chara_selected].camera_size[1] = main_window.camera_size_idle_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_hit_box_changed(main_window):
    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:

        # Change the slot of health
        CPEV.character_list[CPEV.chara_selected].hit_box = main_window.hit_box_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_camera_type_key_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        change_camera_cutscene_values(main_window, main_window.camera_type_key.currentData())


def on_pivot_value_changed(main_window, pivot_index):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        if pivot_index == 0:
            main_window.camera_type_key.currentData().pivots["pivot_1"] = \
                main_window.pivot_value.value()
            main_window.camera_type_key.currentData().modified = True
        elif pivot_index == 1:
            main_window.camera_type_key.currentData().pivots["pivot_2"] = \
                main_window.pivot_value_2.value()
            main_window.camera_type_key.currentData().modified = True
        elif pivot_index == 2:
            main_window.camera_type_key.currentData().pivots["pivot_3"] = \
                main_window.pivot_value_3.value()
            main_window.camera_type_key.currentData().modified = True
        else:
            main_window.camera_type_key.currentData().pivots["pivot_4"] = \
                main_window.pivot_value_4.value()
            main_window.camera_type_key.currentData().modified = True


def on_translations_changed(main_window, y, z):
    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        if y >= 0:
            if y == 0:
                main_window.camera_type_key.currentData().positions["Y_start"] =\
                    main_window.translation_y_start_value.value()
                main_window.camera_type_key.currentData().modified = True
            else:
                main_window.camera_type_key.currentData().positions["Y_end"] = \
                    main_window.translation_y_end_value.value()
                main_window.camera_type_key.currentData().modified = True
        else:
            if z == 0:
                main_window.camera_type_key.currentData().positions["Z_start"] =\
                    main_window.translation_z_start_value.value()
                main_window.camera_type_key.currentData().modified = True
            else:
                main_window.camera_type_key.currentData().positions["Z_end"] = \
                    main_window.translation_z_end_value.value()
                main_window.camera_type_key.currentData().modified = True


def on_rotations_changed(main_window, y, z):
    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        if y >= 0:
            if y == 0:
                main_window.camera_type_key.currentData().rotations["Y_start"] =\
                    main_window.rotation_y_start_value.value()
                main_window.camera_type_key.currentData().modified = True
            else:
                main_window.camera_type_key.currentData().rotations["Y_end"] = \
                    main_window.rotation_y_end_value.value()
                main_window.camera_type_key.currentData().modified = True
        else:
            if z == 0:
                main_window.camera_type_key.currentData().rotations["Z_start"] =\
                    \
                    main_window.rotation_z_start_value.value()
                main_window.camera_type_key.currentData().modified = True
            else:
                main_window.camera_type_key.currentData().rotations["Z_end"] = \
                    main_window.rotation_z_end_value.value()
                main_window.camera_type_key.currentData().modified = True


def on_speed_camera_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        main_window.camera_type_key.currentData().camera_speed = \
            main_window.speed_camera_value.value()
        main_window.camera_type_key.currentData().modified = True


def on_zoom_start_value_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        main_window.camera_type_key.currentData().zooms["Zoom_start"] = \
            main_window.zoom_start_value.value()
        main_window.camera_type_key.currentData().modified = True


def on_zoom_end_value_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        main_window.camera_type_key.currentData().zooms["Zoom_end"] = \
            main_window.zoom_end_value.value()
        main_window.camera_type_key.currentData().modified = True


def on_unk10_value_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        main_window.camera_type_key.currentData().unknowns["unknown_block_10"] = \
            main_window.unk10_value.value()
        main_window.camera_type_key.currentData().modified = True


def on_unk13_value_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        main_window.camera_type_key.currentData().unknowns["unknown_block_13"] = \
            main_window.unk13_value.value()
        main_window.camera_type_key.currentData().modified = True
