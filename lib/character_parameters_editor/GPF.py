from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.GPV import GPV
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
    main_window.selectCharaWindow = qt_widgets.QMainWindow()
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

    subpak_file_resident_character_param.seek(52, os.SEEK_CUR)


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


def action_change_character(event, main_window, index=None, modify_slot_transform=False):
    # Change only if the char selected is other
    if GPV.chara_selected != index:

        # We're changing the character in the main panel (avoid combo box code)
        CPEV.change_character = True

        # The user has opened the file operate_character_parameters
        if GPV.operate_resident_param_file:

            # Health
            main_window.health_value.setValue(GPV.character_list[index].health)

            # Camera size
            main_window.camera_size_cutscene_value.setValue(GPV.character_list[index].camera_size[0])
            main_window.camera_size_idle_value.setValue(GPV.character_list[index].camera_size[1])

            # hit box
            main_window.hit_box_value.setValue(GPV.character_list[index].hit_box)

            # Aura size
            main_window.aura_size_idle_value.setValue(GPV.character_list[index].aura_size[0])
            main_window.aura_size_dash_value.setValue(GPV.character_list[index].aura_size[1])
            main_window.aura_size_charge_value.setValue(GPV.character_list[index].aura_size[2])

            # Color lightning
            main_window.color_lightning_value.setCurrentIndex(main_window.color_lightning_value.findData
                                                              (GPV.character_list[index].color_lightning))

            # Glow/lightning effect
            main_window.glow_lightning_value.setCurrentIndex(main_window.glow_lightning_value.findData
                                                             (GPV.character_list[index].glow_lightning))

            # Load the transformations for the panel transformations
            transformations = GPV.character_list[index].transformations
            # Change panel transformations and their interactions
            if transformations[0] != 100:
                main_window.transSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                           "sc_chara_s_" +
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
                main_window.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                           "sc_chara_s_" +
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
                main_window.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                           "sc_chara_s_" +
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
                main_window.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                           "sc_chara_s_" +
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
                                                         (GPV.character_list[index].transformation_effect))

            # Trans partner value
            main_window.transPartnerValue.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                         "sc_chara_s_" +
                                                                         str(GPV.character_list[
                                                                                 index].transformation_partner).zfill(3)
                                                                         + ".png")))
            main_window.transPartnerValue.mousePressEvent = functools.partial(open_select_chara_window,
                                                                              main_window=main_window,
                                                                              index=GPV.character_list[
                                                                                  index].transformation_partner,
                                                                              transformation_partner_flag=True)

            # amount ki per transformation
            main_window.amountKi_trans1_value.setValue(GPV.character_list[index].amount_ki_transformations[0])
            main_window.amountKi_trans2_value.setValue(GPV.character_list[index].amount_ki_transformations[1])
            main_window.amountKi_trans3_value.setValue(GPV.character_list[index].amount_ki_transformations[2])
            main_window.amountKi_trans4_value.setValue(GPV.character_list[index].amount_ki_transformations[3])

            # Animation per transformation
            main_window.trans1_animation_value.setCurrentIndex(main_window.trans1_animation_value.findData
                                                               (GPV.character_list[index].transformations_animation[0]))
            main_window.trans2_animation_value.setCurrentIndex(main_window.trans2_animation_value.findData
                                                               (GPV.character_list[index].transformations_animation[1]))
            main_window.trans3_animation_value.setCurrentIndex(main_window.trans3_animation_value.findData
                                                               (GPV.character_list[index].transformations_animation[2]))
            main_window.trans4_animation_value.setCurrentIndex(main_window.trans4_animation_value.findData
                                                               (GPV.character_list[index].transformations_animation[3]))

            # Load the fusions for the panel of fusions
            fusions = GPV.character_list[index].fusions
            # Change panel fusions and their interactions
            if fusions[0] != 100:
                main_window.fusiSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                          "sc_chara_s_" +
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
                main_window.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                          "sc_chara_s_" +
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
                main_window.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                          "sc_chara_s_" +
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
                main_window.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                          "sc_chara_s_" +
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
                                                                                  str(GPV.character_list[index].
                                                                                      fusion_partner[0]).zfill(3)
                                                                                  + ".png")))
            main_window.fusionPartnerTrigger_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                       main_window=main_window,
                                                                                       index=GPV.character_list[index]
                                                                                       .fusion_partner[0],
                                                                                       fusion_partner_trigger_flag=True)

            # Show the fusion partner visual
            main_window.fusionPartnerVisual_value.setPixmap(
                QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                     str(GPV.character_list[index].fusion_partner[1]).zfill(3)
                                     + ".png")))
            main_window.fusionPartnerVisual_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                      main_window=main_window,
                                                                                      index=GPV.character_list[index].
                                                                                      fusion_partner[1],
                                                                                      fusion_partner_visual_flag=True)

            # Show amount ki per fusion
            main_window.amountKi_fusion1_value.setValue(GPV.character_list[index].amount_ki_fusions[0])
            main_window.amountKi_fusion2_value.setValue(GPV.character_list[index].amount_ki_fusions[1])
            main_window.amountKi_fusion3_value.setValue(GPV.character_list[index].amount_ki_fusions[2])
            main_window.amountKi_fusion4_value.setValue(GPV.character_list[index].amount_ki_fusions[3])

            # Show Animation per Fusion
            main_window.fusion1_animation_value.setCurrentIndex(main_window.fusion1_animation_value.findData
                                                                (GPV.character_list[index].fusions_animation[0]))
            main_window.fusion2_animation_value.setCurrentIndex(main_window.fusion2_animation_value.findData
                                                                (GPV.character_list[index].fusions_animation[1]))
            main_window.fusion3_animation_value.setCurrentIndex(main_window.fusion3_animation_value.findData
                                                                (GPV.character_list[index].fusions_animation[2]))
            main_window.fusion4_animation_value.setCurrentIndex(main_window.fusion4_animation_value.findData
                                                                (GPV.character_list[index].fusions_animation[3]))
        else:

            # Aura type
            main_window.aura_type_value.setCurrentIndex(main_window.aura_type_value.findData
                                                        (GPV.character_list[index].aura_type))

        # Load the portrait
        main_window.portrait.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_" +
                                                            str(index).zfill(3) + ".png")))

        # Modify the slots of the transformations in the main panel
        if modify_slot_transform:

            # Disable all the transformations of the slots if it has been activated in the main panel
            if main_window.label_trans_0.isVisible():
                main_window.label_trans_0.setVisible(False)
                main_window.label_trans_1.setVisible(False)
                main_window.label_trans_2.setVisible(False)
                main_window.label_trans_3.setVisible(False)

            # Get the original transformations for the character
            if index in GPV.characters_with_trans:
                transformations = GPV.characters_with_trans_index[GPV.characters_with_trans.index(index)]
                num_transformations = len(transformations)
                if num_transformations > 0:
                    main_window.label_trans_0.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_" +
                                                                             str(transformations[0]).zfill(
                                                                                 3) + ".bmp")))
                    main_window.label_trans_0.mousePressEvent = functools.partial(action_change_character,
                                                                                  main_window=main_window,
                                                                                  index=transformations[0],
                                                                                  modify_slot_transform=False)
                    main_window.label_trans_0.setVisible(True)
                    if num_transformations > 1:
                        main_window.label_trans_1.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                                 "chara_chips_" +
                                                                                 str(transformations[1]).zfill(3) +
                                                                                 ".bmp")))
                        main_window.label_trans_1.mousePressEvent = functools.partial(action_change_character,
                                                                                      main_window=main_window,
                                                                                      index=transformations[1],
                                                                                      modify_slot_transform=False)
                        main_window.label_trans_1.setVisible(True)
                        if num_transformations > 2:
                            main_window.label_trans_2.setPixmap(
                                QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_" +
                                                     str(transformations[2]).zfill(3) +
                                                     ".bmp")))
                            main_window.label_trans_2.mousePressEvent = functools.partial(action_change_character,
                                                                                          main_window=main_window,
                                                                                          index=transformations[2],
                                                                                          modify_slot_transform=False)
                            main_window.label_trans_2.setVisible(True)
                            if num_transformations > 3:
                                main_window.label_trans_3.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                                         "chara_chips_" +
                                                                                         str(transformations[3]).zfill(
                                                                                             3) +
                                                                                         ".bmp")))
                                main_window.label_trans_3.mousePressEvent = functools.partial(action_change_character,
                                                                                              main_window=main_window,
                                                                                              index=transformations[3],
                                                                                              modify_slot_transform=False)
                                main_window.label_trans_3.setVisible(True)

                                # Store the actual index selected of the char
        GPV.chara_selected = index

        # We're not changing the character in the main panel (play combo box code)
        CPEV.change_character = False


def action_edit_trans_fusion_slot(event, main_window, char_selected_new):
    # Check if the user wants to edit the transformation slot
    if GPV.trans_slot_panel_selected is not None:

        # Change the transformation in our array of characters
        GPV.character_list[GPV.chara_selected].transformations[
            GPV.trans_slot_panel_selected] = char_selected_new

        # Change the visual transformation
        if GPV.trans_slot_panel_selected == 0:
            main_window.transSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=0)
        elif GPV.trans_slot_panel_selected == 1:
            main_window.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=1)
        elif GPV.trans_slot_panel_selected == 2:
            main_window.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=2)
        elif GPV.trans_slot_panel_selected == 3:
            main_window.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=3)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])

    # transformation partner slot
    elif GPV.transformation_partner_flag:

        # Change the fusion in our array of characters
        GPV.character_list[GPV.chara_selected].transformation_partner = char_selected_new

        main_window.transPartnerValue.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                     str(char_selected_new).zfill(3) + ".png")))
        main_window.transPartnerValue.mousePressEvent = functools.partial(open_select_chara_window,
                                                                          main_window=main_window,
                                                                          index=char_selected_new,
                                                                          transformation_partner_flag=True)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])

    # fusion slot
    elif GPV.fusion_slot_panel_selected is not None:

        # Change the fusion in our array of characters
        GPV.character_list[GPV.chara_selected].fusions[GPV.fusion_slot_panel_selected] = char_selected_new

        # Change the visual fusion
        if GPV.fusion_slot_panel_selected == 0:
            main_window.fusiSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=0)
        elif GPV.fusion_slot_panel_selected == 1:
            main_window.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=1)
        elif GPV.fusion_slot_panel_selected == 2:
            main_window.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=2)
        elif GPV.fusion_slot_panel_selected == 3:
            main_window.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=3)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])

    # fusion partner trigger slot
    elif GPV.fusion_partner_flag[0]:

        # Change the fusion in our array of characters
        GPV.character_list[GPV.chara_selected].fusion_partner[0] = char_selected_new

        main_window.fusionPartnerTrigger_value.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                              "sc_chara_s_" +
                                                                              str(char_selected_new).zfill(3) +
                                                                              ".png")))
        main_window.fusionPartnerTrigger_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                   main_window=main_window,
                                                                                   index=char_selected_new,
                                                                                   fusion_partner_trigger_flag=True)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])

    # fusion partner visual slot
    elif GPV.fusion_partner_flag[1]:

        # Change the fusion in our array of characters
        GPV.character_list[GPV.chara_selected].fusion_partner[1] = char_selected_new

        main_window.fusionPartnerVisual_value.setPixmap(
            QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                 str(char_selected_new).zfill(3) + ".png")))
        main_window.fusionPartnerVisual_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                  main_window=main_window,
                                                                                  index=char_selected_new,
                                                                                  fusion_partner_visual_flag=True)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])

    main_window.selectCharaWindow.close()


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


def on_color_lightning_changed(main_window):
    # Avoid trigger the combo box at starting
    if not CPEV.change_character:
        GPV.character_list[GPV.chara_selected].color_lightning = main_window.color_lightning_value.currentData()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_glow_lightning_changed(main_window):
    # Avoid trigger the combo box at starting
    if not CPEV.change_character:
        GPV.character_list[GPV.chara_selected].glow_lightning = main_window.glow_lightning_value.currentData()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_transformation_ki_effect_changed(main_window):
    # Avoid trigger the combo box at starting
    if not CPEV.change_character:
        GPV.character_list[
            GPV.chara_selected].transformation_effect = main_window.transEffectValue.currentData()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_amount_ki_trans_changed(main_window, amount_ki_trans_index):
    # Avoid trigger the combo box at starting
    if not CPEV.change_character:

        # Change the slot of amount ki
        if amount_ki_trans_index == 0:
            GPV.character_list[GPV.chara_selected].amount_ki_transformations[amount_ki_trans_index] = \
                main_window.amountKi_trans1_value.value()
        elif amount_ki_trans_index == 1:
            GPV.character_list[GPV.chara_selected].amount_ki_transformations[amount_ki_trans_index] = \
                main_window.amountKi_trans2_value.value()
        elif amount_ki_trans_index == 2:
            GPV.character_list[GPV.chara_selected].amount_ki_transformations[amount_ki_trans_index] = \
                main_window.amountKi_trans3_value.value()
        elif amount_ki_trans_index == 3:
            GPV.character_list[GPV.chara_selected].amount_ki_transformations[amount_ki_trans_index] = \
                main_window.amountKi_trans4_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_animation_per_transformation_changed(main_window, animation_per_transformation):
    # Avoid trigger the combo box at starting
    if not CPEV.change_character:
        if animation_per_transformation == 0:
            GPV.character_list[GPV.chara_selected].transformations_animation[animation_per_transformation] = \
                main_window.trans1_animation_value.currentData()
        elif animation_per_transformation == 1:
            GPV.character_list[GPV.chara_selected].transformations_animation[animation_per_transformation] = \
                main_window.trans2_animation_value.currentData()
        elif animation_per_transformation == 2:
            GPV.character_list[GPV.chara_selected].transformations_animation[animation_per_transformation] = \
                main_window.trans3_animation_value.currentData()
        elif animation_per_transformation == 3:
            GPV.character_list[GPV.chara_selected].transformations_animation[animation_per_transformation] = \
                main_window.trans4_animation_value.currentData()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_amount_ki_fusion_changed(main_window, amount_ki_fusion_index):
    # Avoid trigger the combo box at starting
    if not CPEV.change_character:

        # Change the slot of amount ki
        if amount_ki_fusion_index == 0:
            GPV.character_list[GPV.chara_selected].amount_ki_fusions[amount_ki_fusion_index] = \
                main_window.amountKi_fusion1_value.value()
        elif amount_ki_fusion_index == 1:
            GPV.character_list[GPV.chara_selected].amount_ki_fusions[amount_ki_fusion_index] = \
                main_window.amountKi_fusion2_value.value()
        elif amount_ki_fusion_index == 2:
            GPV.character_list[GPV.chara_selected].amount_ki_fusions[amount_ki_fusion_index] = \
                main_window.amountKi_fusion3_value.value()
        elif amount_ki_fusion_index == 3:
            GPV.character_list[GPV.chara_selected].amount_ki_fusions[amount_ki_fusion_index] = \
                main_window.amountKi_fusion4_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_animation_per_fusion_changed(main_window, animation_per_fusion):
    # Avoid trigger the combo box at starting
    if not CPEV.change_character:
        if animation_per_fusion == 0:
            GPV.character_list[GPV.chara_selected].fusions_animation[animation_per_fusion] = \
                main_window.fusion1_animation_value.currentData()
        elif animation_per_fusion == 1:
            GPV.character_list[GPV.chara_selected].fusions_animation[animation_per_fusion] = \
                main_window.fusion2_animation_value.currentData()
        elif animation_per_fusion == 2:
            GPV.character_list[GPV.chara_selected].fusions_animation[animation_per_fusion] = \
                main_window.fusion3_animation_value.currentData()
        elif animation_per_fusion == 3:
            GPV.character_list[GPV.chara_selected].fusions_animation[animation_per_fusion] = \
                main_window.fusion4_animation_value.currentData()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_aura_size_changed(main_window, aura_index):
    # Avoid trigger the combo box at starting
    if not CPEV.change_character:

        if aura_index == 0:
            # Change the slot of aura idle size
            GPV.character_list[GPV.chara_selected].aura_size[0] = main_window.aura_size_idle_value.value()
        elif aura_index == 1:
            # Change the slot of aura dash size
            GPV.character_list[GPV.chara_selected].aura_size[1] = main_window.aura_size_dash_value.value()
        else:
            # Change the slot of aura dash size
            GPV.character_list[GPV.chara_selected].aura_size[2] = main_window.aura_size_charge_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_health_changed(main_window):
    # Avoid trigger the combo box at starting
    if not CPEV.change_character:

        # Change the slot of health
        GPV.character_list[GPV.chara_selected].health = int(main_window.health_value.value())

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_camera_size_changed(main_window, camera_index):
    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:

        if camera_index == 0:
            # Change the slot of camera cutscene size
            GPV.character_list[GPV.chara_selected].camera_size[
                0] = main_window.camera_size_cutscene_value.value()
        else:
            # Change the slot of camera idle size
            GPV.character_list[GPV.chara_selected].camera_size[1] = main_window.camera_size_idle_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_hit_box_changed(main_window):
    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:

        # Change the slot of health
        GPV.character_list[GPV.chara_selected].hit_box = main_window.hit_box_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_aura_type_changed(main_window):

    # Avoid trigger the combo box at starting
    if not CPEV.change_character:
        GPV.character_list[GPV.chara_selected].aura_type = main_window.aura_type_value.currentData()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])
