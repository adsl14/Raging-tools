from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.GPV import GPV
from lib.character_parameters_editor.functions.GP.action_logic import action_change_character, on_health_changed, \
    on_camera_size_changed, on_hit_box_changed, on_aura_size_changed, on_color_lightning_changed, \
    on_glow_lightning_changed, on_transformation_ki_effect_changed, on_amount_ki_trans_changed, \
    on_animation_per_transformation_changed, on_amount_ki_fusion_changed, on_animation_per_fusion_changed, \
    on_aura_type_changed, action_edit_trans_fusion_slot, on_up_blast_attack_logic, on_p_blast_attack_logic, \
    on_l_blast_attack_logic, on_d_blast_attack_logic, on_r_blast_attack_logic
from lib.design.select_chara import Select_Chara
from lib.packages import QLabel, QPixmap, functools, os, struct


def initialize_operate_resident_param(main_window, qt_widgets):

    # Load all the mini portraits (main panel)
    GPV.mini_portraits_image = main_window.mainPanel.findChildren(QLabel)

    for i in range(0, 66):
        index_chara = GPV.mini_portraits_image[i].objectName().split("_")[1]
        GPV.mini_portraits_image[i].setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_0" +
                                                                   index_chara + ".bmp")))
        GPV.mini_portraits_image[i].setStyleSheet(CPEV.styleSheetSelectSlotRoster)
        GPV.mini_portraits_image[i].mousePressEvent = functools.partial(action_change_character,
                                                                        main_window=main_window,
                                                                        index=int(index_chara),
                                                                        modify_slot_transform=True)

    for i in range(66, len(GPV.mini_portraits_image)):
        GPV.mini_portraits_image[i].setStyleSheet(CPEV.styleSheetSelectSlotRoster)

    # Hide the transformation slots
    main_window.label_trans_0.setVisible(False)
    main_window.label_trans_1.setVisible(False)
    main_window.label_trans_2.setVisible(False)
    main_window.label_trans_3.setVisible(False)

    # Disable all the buttons (operate_resident_param)
    main_window.operate_resident_param_frame.setEnabled(False)

    # Disable all the buttons (operate_character_XXX_m)
    main_window.operate_character_xyz_m_frame.setEnabled(False)

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
    for element in GPV.color_lightning_values:
        main_window.color_lightning_value.addItem(element, GPV.color_lightning_values[element])

    # Set the glow/lightning
    main_window.glow_lightning_value.currentIndexChanged.connect(lambda: on_glow_lightning_changed(main_window))
    # Add the values
    for element in GPV.glow_lightning_values:
        main_window.glow_lightning_value.addItem(element, GPV.glow_lightning_values[element])

    # Set the transform panel
    main_window.transPanel.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_transform.png")))
    main_window.transText.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "tx_transform_US.png")))

    # Set the transformation parameter
    main_window.transEffectValue.currentIndexChanged.connect(lambda: on_transformation_ki_effect_changed(main_window))
    # Add the values
    for element in GPV.trans_effect_values:
        main_window.transEffectValue.addItem(element, GPV.trans_effect_values[element])

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
    for element in GPV.trans_animation_values:
        main_window.trans1_animation_value.addItem(element, GPV.trans_animation_values[element])
        main_window.trans2_animation_value.addItem(element, GPV.trans_animation_values[element])
        main_window.trans3_animation_value.addItem(element, GPV.trans_animation_values[element])
        main_window.trans4_animation_value.addItem(element, GPV.trans_animation_values[element])

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
    for element in GPV.fusion_animation_values:
        main_window.fusion1_animation_value.addItem(element, GPV.fusion_animation_values[element])
        main_window.fusion2_animation_value.addItem(element, GPV.fusion_animation_values[element])
        main_window.fusion3_animation_value.addItem(element, GPV.fusion_animation_values[element])
        main_window.fusion4_animation_value.addItem(element, GPV.fusion_animation_values[element])

    # Set the fusion panel
    main_window.fusiPanel.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_fusion.png")))
    main_window.fusiPanelText.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "tx_fusion_US.png")))

    # Load the Select Chara window
    main_window.selectCharaWindow = qt_widgets.QDialog()
    main_window.selectCharaUI = Select_Chara()
    main_window.selectCharaUI.setupUi(main_window.selectCharaWindow)
    GPV.mini_portraits_image_select_chara_window = main_window.selectCharaUI.frame.findChildren(QLabel)
    for i in range(0, len(GPV.mini_portraits_image_select_chara_window)):
        label_id_image = GPV.mini_portraits_image_select_chara_window[i].objectName().split("_")[-1]
        GPV.mini_portraits_image_select_chara_window[i].setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                                       "chara_chips_" +
                                                                                       label_id_image.zfill(3)
                                                                                       + ".bmp")))
        GPV.mini_portraits_image_select_chara_window[i].setStyleSheet(CPEV.styleSheetSlotRosterWindow)
        GPV.mini_portraits_image_select_chara_window[i].mousePressEvent = functools.partial(
            action_edit_trans_fusion_slot, main_window=main_window, char_selected_new=i)

    # Set the aura type values
    main_window.aura_type_value.currentIndexChanged.connect(lambda: on_aura_type_changed(main_window))
    # Add the values
    for aura_type in GPV.aura_type_values:
        main_window.aura_type_value.addItem(aura_type, GPV.aura_type_values[aura_type])

    # Set the blast attacks
    main_window.ico_boost_stick_r_up_image.setPixmap(QPixmap(os.path.join(CPEV.path_controller_images,
                                                                          "ico_boost_stick_r_up.png")))
    main_window.ico_boost_stick_r_up_value.currentIndexChanged.connect(lambda: on_up_blast_attack_logic(main_window))
    main_window.ico_boost_stick_r_r_image.setPixmap(QPixmap(os.path.join(CPEV.path_controller_images,
                                                                         "ico_boost_stick_r_r.png")))
    main_window.ico_boost_stick_r_r_value.currentIndexChanged.connect(lambda: on_r_blast_attack_logic(main_window))
    main_window.ico_boost_stick_r_d_image.setPixmap(QPixmap(os.path.join(CPEV.path_controller_images,
                                                                         "ico_boost_stick_r_d.png")))
    main_window.ico_boost_stick_r_d_value.currentIndexChanged.connect(lambda: on_d_blast_attack_logic(main_window))
    main_window.ico_boost_stick_r_l_image.setPixmap(QPixmap(os.path.join(CPEV.path_controller_images,
                                                                         "ico_boost_stick_r_l.png")))
    main_window.ico_boost_stick_r_l_value.currentIndexChanged.connect(lambda: on_l_blast_attack_logic(main_window))
    main_window.ico_boost_stick_r_push_image.setPixmap(QPixmap(os.path.join(CPEV.path_controller_images,
                                                                            "ico_boost_stick_r_push_00.png")))
    main_window.ico_boost_stick_r_push_value.currentIndexChanged.connect(lambda: on_p_blast_attack_logic(main_window))


def enable_disable_operate_resident_param_values(main_window, flag):

    # --- Transform info values ---
    # Transform section
    main_window.transformPanel.setEnabled(flag)
    main_window.transEffect.setEnabled(flag)
    main_window.transPartner.setEnabled(flag)
    main_window.amount_ki_per_transformation.setEnabled(flag)
    main_window.animation_per_transformation.setEnabled(flag)

    # Fusion section
    main_window.fusionPanel.setEnabled(flag)
    main_window.fusionPartnerTrigger.setEnabled(flag)
    main_window.fusionPartnerVisual.setEnabled(flag)
    main_window.amount_ki_per_fusion.setEnabled(flag)
    main_window.animation_per_fusion.setEnabled(flag)

    # --- Character info values ---
    main_window.health.setEnabled(flag)
    main_window.camera_size.setEnabled(flag)
    main_window.hit_box.setEnabled(flag)
    main_window.aura_size.setEnabled(flag)
    main_window.color_lightning.setEnabled(flag)
    main_window.glow_lightning.setEnabled(flag)


def initialize_roster(main_window):

    # Load the large portrait
    main_window.portrait.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_000.png")))

    # Show the transformations in the main panel
    main_window.label_trans_0.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_001.bmp")))
    main_window.label_trans_0.mousePressEvent = functools.partial(action_change_character, main_window=main_window,
                                                                  index=1, modify_slot_transform=False)
    main_window.label_trans_1.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_002.bmp")))
    main_window.label_trans_1.mousePressEvent = functools.partial(action_change_character, main_window=main_window,
                                                                  index=2, modify_slot_transform=False)
    main_window.label_trans_2.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_003.bmp")))
    main_window.label_trans_2.mousePressEvent = functools.partial(action_change_character, main_window=main_window,
                                                                  index=3, modify_slot_transform=False)
    main_window.label_trans_0.setVisible(True)
    main_window.label_trans_1.setVisible(True)
    main_window.label_trans_2.setVisible(True)
    main_window.label_trans_3.setVisible(False)


def enable_disable_db_font_pad_ps3_values(main_window, flag):

    # Aura section
    main_window.aura_type.setEnabled(flag)

    # Blast attacks
    main_window.ico_boost_stick_r.setEnabled(flag)


def read_operate_resident_param(character, subpak_file_character_inf, subpak_file_transformer_i):
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


def read_db_font_pad_ps3(character, subpak_file_resident_character_param):

    # --- resident_character_param ---
    # Aura type
    subpak_file_resident_character_param.seek(3, os.SEEK_CUR)
    character.aura_type = int.from_bytes(subpak_file_resident_character_param.read(1), byteorder='big')

    # Blast attacks
    subpak_file_resident_character_param.seek(3, os.SEEK_CUR)
    character.blast_attacks["Up"] = int.from_bytes(subpak_file_resident_character_param.read(1), byteorder='big')
    subpak_file_resident_character_param.seek(3, os.SEEK_CUR)
    character.blast_attacks["Right"] = int.from_bytes(subpak_file_resident_character_param.read(1), byteorder='big')
    subpak_file_resident_character_param.seek(3, os.SEEK_CUR)
    character.blast_attacks["Down"] = int.from_bytes(subpak_file_resident_character_param.read(1), byteorder='big')
    subpak_file_resident_character_param.seek(3, os.SEEK_CUR)
    character.blast_attacks["Left"] = int.from_bytes(subpak_file_resident_character_param.read(1), byteorder='big')
    subpak_file_resident_character_param.seek(3, os.SEEK_CUR)
    character.blast_attacks["Push"] = int.from_bytes(subpak_file_resident_character_param.read(1), byteorder='big')

    subpak_file_resident_character_param.seek(32, os.SEEK_CUR)


def write_operate_resident_param(character, subpak_file_character_inf, subpak_file_transformer_i):
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


def write_db_font_pad_ps3(character, subpak_file_resident_character_param):

    # Move to the visual parameters character
    subpak_file_resident_character_param.seek(character.position_resident_character_param)

    # Aura type
    subpak_file_resident_character_param.seek(3, os.SEEK_CUR)
    subpak_file_resident_character_param.write(character.aura_type.to_bytes(1, byteorder="big"))

    # Blast attacks
    subpak_file_resident_character_param.seek(3, os.SEEK_CUR)
    subpak_file_resident_character_param.write(character.blast_attacks["Up"].to_bytes(1, byteorder="big"))
    subpak_file_resident_character_param.seek(3, os.SEEK_CUR)
    subpak_file_resident_character_param.write(character.blast_attacks["Right"].to_bytes(1, byteorder="big"))
    subpak_file_resident_character_param.seek(3, os.SEEK_CUR)
    subpak_file_resident_character_param.write(character.blast_attacks["Down"].to_bytes(1, byteorder="big"))
    subpak_file_resident_character_param.seek(3, os.SEEK_CUR)
    subpak_file_resident_character_param.write(character.blast_attacks["Left"].to_bytes(1, byteorder="big"))
    subpak_file_resident_character_param.seek(3, os.SEEK_CUR)
    subpak_file_resident_character_param.write(character.blast_attacks["Push"].to_bytes(1, byteorder="big"))


def open_select_chara_window(event, main_window, index, trans_slot_panel_index=None, fusion_slot_panel_index=None,
                             transformation_partner_flag=False, fusion_partner_trigger_flag=False,
                             fusion_partner_visual_flag=False):
    # Check what selected the user. If the user didn't select the transform panel or transform partner
    # then, the user selected the fusion panel (or potara or metamoran)
    if trans_slot_panel_index is not None or transformation_partner_flag:
        q_label_style = CPEV.styleSheetSelectTransRosterWindow
    else:
        q_label_style = CPEV.styleSheetSelectFusionRosterWindow

    # Store in a global var what slot in the transformation and fusion panel has been selected
    GPV.trans_slot_panel_selected = trans_slot_panel_index
    GPV.transformation_partner_flag = transformation_partner_flag
    GPV.fusion_slot_panel_selected = fusion_slot_panel_index
    GPV.fusion_partner_flag[0] = fusion_partner_trigger_flag
    GPV.fusion_partner_flag[1] = fusion_partner_visual_flag

    # The previous chara selected and the new are differents
    if GPV.previous_chara_selected_character_window != index:

        # Add the color border to the character that has been selected in the trans/fusion slot
        GPV.mini_portraits_image_select_chara_window[index].setStyleSheet(q_label_style)

        # Reset the previous character select
        GPV.mini_portraits_image_select_chara_window[GPV.previous_chara_selected_character_window]\
            .setStyleSheet(CPEV.styleSheetSlotRosterWindow)

        # Store the actual character selected in the select character window
        GPV.previous_chara_selected_character_window = index

    # If the color border isn't the same, means the user has selected a different slot (trans or fusion
    # or partners)
    elif GPV.mini_portraits_image_select_chara_window[index].styleSheet() != q_label_style:

        # Add the color border to the character that has been selected in the trans/fusion slot
        GPV.mini_portraits_image_select_chara_window[index].setStyleSheet(q_label_style)

        # Store the actual character selected in the select character window
        GPV.previous_chara_selected_character_window = index

    main_window.selectCharaWindow.show()
