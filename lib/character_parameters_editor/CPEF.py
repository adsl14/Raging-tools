from lib.character_parameters_editor.CPEV import CPEV
from lib.packages import QLabel, QPixmap, functools, os, struct
from lib.design.select_chara import Ui_Dialog


def initialize_cpe(main_window, qt_widgets):
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
        CPEV.mini_portraits_image[i].setDisabled(True)

    for i in range(66, len(CPEV.mini_portraits_image)):
        CPEV.mini_portraits_image[i].setStyleSheet("QLabel {border : 3px solid grey;}")
        CPEV.mini_portraits_image[i].setVisible(False)

    # Set the the big portrait image
    main_window.portrait.setVisible(False)

    # Set the health
    main_window.health_text.setDisabled(True)
    main_window.health_value.setDisabled(True)
    main_window.health_value.valueChanged.connect(lambda: on_health_changed(main_window))

    # Set the camera size
    main_window.camera_size_text.setDisabled(True)
    main_window.camera_size_cutscene_text.setDisabled(True)
    main_window.camera_size_cutscene_value.setDisabled(True)
    main_window.camera_size_idle_text.setDisabled(True)
    main_window.camera_size_idle_value.setDisabled(True)
    main_window.camera_size_cutscene_value.valueChanged.connect(lambda: on_camera_size_changed(main_window,
                                                                                               camera_index=0))
    main_window.camera_size_idle_value.valueChanged.connect(lambda: on_camera_size_changed(main_window,
                                                                                           camera_index=1))

    # Set the hit box
    main_window.hit_box_text.setDisabled(True)
    main_window.hit_box_value.setDisabled(True)
    main_window.hit_box_value.valueChanged.connect(lambda: on_hit_box_changed(main_window))

    # Set the aura size
    main_window.aura_size_text.setDisabled(True)
    main_window.aura_size_idle_text.setDisabled(True)
    main_window.aura_size_idle_value.setDisabled(True)
    main_window.aura_size_dash_text.setDisabled(True)
    main_window.aura_size_dash_value.setDisabled(True)
    main_window.aura_size_charge_text.setDisabled(True)
    main_window.aura_size_charge_value.setDisabled(True)
    main_window.aura_size_idle_value.valueChanged.connect(lambda: on_aura_size_changed(main_window, aura_index=0))
    main_window.aura_size_dash_value.valueChanged.connect(lambda: on_aura_size_changed(main_window, aura_index=1))
    main_window.aura_size_charge_value.valueChanged.connect(lambda: on_aura_size_changed(main_window, aura_index=2))

    # Set the color lightning
    main_window.color_lightning_text.setDisabled(True)
    main_window.color_lightning_value.setDisabled(True)
    main_window.color_lightning_value.currentIndexChanged.connect(lambda: on_color_lightning_changed(main_window))

    # Set the glow/lightning
    main_window.glow_lightning_text.setDisabled(True)
    main_window.glow_lightning_value.setDisabled(True)
    main_window.glow_lightning_value.currentIndexChanged.connect(lambda: on_glow_lightning_changed(main_window))
    main_window.glow_lightning_value.view().setRowHidden(3, True)  # Hide item with ID 3

    # Set the transform panel
    main_window.transPanel.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_transform.png")))
    main_window.transText.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "tx_transform_US.png")))
    main_window.transPanel.setDisabled(True)
    main_window.transText.setDisabled(True)

    # Set the transformation parameter
    main_window.transEffectText.setDisabled(True)
    main_window.transEffectValue.setDisabled(True)
    main_window.transEffectValue.currentIndexChanged.connect(lambda: on_transformation_ki_effect_changed(main_window))

    # Set the Trasformation partner
    main_window.transPartnerSlot.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_slot.png")))
    main_window.transPartnerSlot.setDisabled(True)
    main_window.transPartnerText.setDisabled(True)
    main_window.transPartnerValue.setDisabled(True)

    # Set the amount ki per transformation
    main_window.amount_ki_per_transformation_text.setDisabled(True)
    main_window.amountKi_trans1_text.setDisabled(True)
    main_window.amountKi_trans2_text.setDisabled(True)
    main_window.amountKi_trans3_text.setDisabled(True)
    main_window.amountKi_trans4_text.setDisabled(True)
    main_window.amountKi_trans1_value.setDisabled(True)
    main_window.amountKi_trans2_value.setDisabled(True)
    main_window.amountKi_trans3_value.setDisabled(True)
    main_window.amountKi_trans4_value.setDisabled(True)
    main_window.amountKi_trans1_value.valueChanged.connect(lambda: on_amount_ki_trans_changed(main_window,
                                                                                              amount_ki_trans_index=0))
    main_window.amountKi_trans2_value.valueChanged.connect(lambda: on_amount_ki_trans_changed(main_window,
                                                                                              amount_ki_trans_index=1))
    main_window.amountKi_trans3_value.valueChanged.connect(lambda: on_amount_ki_trans_changed(main_window,
                                                                                              amount_ki_trans_index=2))
    main_window.amountKi_trans4_value.valueChanged.connect(lambda: on_amount_ki_trans_changed(main_window,
                                                                                              amount_ki_trans_index=3))

    # Set the animation per transformation
    main_window.animation_per_transformation_text.setDisabled(True)
    main_window.animation_trans1_text.setDisabled(True)
    main_window.trans1_animation_value.setDisabled(True)
    main_window.animation_trans2_text.setDisabled(True)
    main_window.trans2_animation_value.setDisabled(True)
    main_window.animation_trans3_text.setDisabled(True)
    main_window.trans3_animation_value.setDisabled(True)
    main_window.animation_trans4_text.setDisabled(True)
    main_window.trans4_animation_value.setDisabled(True)
    main_window.trans1_animation_value.currentIndexChanged.connect(lambda: on_animation_per_transformation_changed
                                                                   (main_window, animation_per_transformation=0))
    main_window.trans2_animation_value.currentIndexChanged.connect(lambda: on_animation_per_transformation_changed
                                                                   (main_window, animation_per_transformation=1))
    main_window.trans3_animation_value.currentIndexChanged.connect(lambda: on_animation_per_transformation_changed
                                                                   (main_window, animation_per_transformation=2))
    main_window.trans4_animation_value.currentIndexChanged.connect(lambda: on_animation_per_transformation_changed
                                                                   (main_window, animation_per_transformation=3))
    # Hide items
    for i in [2, 3, 5, 7, 8, 9, 10, 11]:
        main_window.trans1_animation_value.view().setRowHidden(i, True)
        main_window.trans2_animation_value.view().setRowHidden(i, True)
        main_window.trans3_animation_value.view().setRowHidden(i, True)
        main_window.trans4_animation_value.view().setRowHidden(i, True)

    # Set fusion partner trigger
    main_window.fusionPartnerTrigger_slot.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_slot.png")))
    main_window.fusionPartnerTrigger_slot.setDisabled(True)
    main_window.fusionPartnerTrigger_value.setDisabled(True)
    main_window.fusionPartnerTrigger_text.setDisabled(True)

    # Set fusion partner visual
    main_window.fusionPartnerVisual_slot.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_slot.png")))
    main_window.fusionPartnerVisual_slot.setDisabled(True)
    main_window.fusionPartnerVisual_value.setDisabled(True)
    main_window.fusionPartnerVisual_text.setDisabled(True)

    # Set the amount ki per fusion
    main_window.amount_ki_per_fusion_text.setDisabled(True)
    main_window.amountKi_fusion1_text.setDisabled(True)
    main_window.amountKi_fusion2_text.setDisabled(True)
    main_window.amountKi_fusion3_text.setDisabled(True)
    main_window.amountKi_fusion4_text.setDisabled(True)
    main_window.amountKi_fusion1_value.setDisabled(True)
    main_window.amountKi_fusion2_value.setDisabled(True)
    main_window.amountKi_fusion3_value.setDisabled(True)
    main_window.amountKi_fusion4_value.setDisabled(True)
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
    main_window.animation_per_fusion_text.setDisabled(True)
    main_window.animation_fusion1_text.setDisabled(True)
    main_window.fusion1_animation_value.setDisabled(True)
    main_window.animation_fusion2_text.setDisabled(True)
    main_window.fusion2_animation_value.setDisabled(True)
    main_window.animation_fusion3_text.setDisabled(True)
    main_window.fusion3_animation_value.setDisabled(True)
    main_window.animation_fusion4_text.setDisabled(True)
    main_window.fusion4_animation_value.setDisabled(True)
    main_window.fusion1_animation_value.currentIndexChanged.connect(lambda: on_animation_per_fusion_changed
                                                                    (main_window, animation_per_fusion=0))
    main_window.fusion2_animation_value.currentIndexChanged.connect(lambda: on_animation_per_fusion_changed
                                                                    (main_window, animation_per_fusion=1))
    main_window.fusion3_animation_value.currentIndexChanged.connect(lambda: on_animation_per_fusion_changed
                                                                    (main_window, animation_per_fusion=2))
    main_window.fusion4_animation_value.currentIndexChanged.connect(lambda: on_animation_per_fusion_changed
                                                                    (main_window, animation_per_fusion=3))

    # Set the fusion panel
    main_window.fusiPanel.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_fusion.png")))
    main_window.fusiPanelText.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "tx_fusion_US.png")))
    main_window.fusiPanel.setDisabled(True)
    main_window.fusiPanelText.setDisabled(True)

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


def store_character_parameters(character, pak_file):
    # Move to the visual parameters position
    pak_file.seek(character.position_visual_parameters)

    # Health
    character.health = int.from_bytes(pak_file.read(4), byteorder='big')

    # Camera size '>f' big endian
    character.camera_size.append(struct.unpack('>f', pak_file.read(4))[0])
    character.camera_size.append(struct.unpack('>f', pak_file.read(4))[0])

    # hit box '>f' big endian
    character.hit_box = struct.unpack('>f', pak_file.read(4))[0]

    # UNK data for now
    pak_file.seek(12, 1)

    # Aura size '>f' big endian
    character.aura_size.append(struct.unpack('>f', pak_file.read(4))[0])
    character.aura_size.append(struct.unpack('>f', pak_file.read(4))[0])
    character.aura_size.append(struct.unpack('>f', pak_file.read(4))[0])

    # UNK data for now
    pak_file.seek(5, 1)

    # Color lightnings
    character.color_lightning = int.from_bytes(pak_file.read(1), byteorder='big')

    # UNK data for now
    pak_file.seek(69, 1)

    # Glow/Lightnings
    character.glow_lightning = int.from_bytes(pak_file.read(1), byteorder='big')

    # Move to the transformations parameters position
    pak_file.seek(character.position_trans)

    # Character ID
    character.character_id = int.from_bytes(pak_file.read(1), byteorder='big')
    # destransformation effect
    character.transformation_effect = int.from_bytes(pak_file.read(1), byteorder='big')
    # transformation_partner
    character.transformation_partner = int.from_bytes(pak_file.read(1), byteorder='big')

    # Transformation 1
    character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # Transformation 2
    character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # Transformation 3
    character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # Transformation 4
    character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='big'))

    # amount_ki_transformations 1
    character.amount_ki_transformations.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # amount_ki_transformations 2
    character.amount_ki_transformations.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # amount_ki_transformations 3
    character.amount_ki_transformations.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # amount_ki_transformations 4
    character.amount_ki_transformations.append(int.from_bytes(pak_file.read(1), byteorder='big'))

    # transformations_animation 1
    character.transformations_animation.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # transformations_animation 2
    character.transformations_animation.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # transformations_animation 3
    character.transformations_animation.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # transformations_animation 4
    character.transformations_animation.append(int.from_bytes(pak_file.read(1), byteorder='big'))

    # Move four positions because is unk data
    pak_file.seek(4, 1)

    # fusion partner (trigger and visual)
    character.fusion_partner.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    character.fusion_partner.append(int.from_bytes(pak_file.read(1), byteorder='big'))

    # fusions 1
    character.fusions.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # fusions 2
    character.fusions.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # fusions 3
    character.fusions.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # fusions 4
    character.fusions.append(int.from_bytes(pak_file.read(1), byteorder='big'))

    # amount_ki_fusions 1
    character.amount_ki_fusions.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # amount_ki_fusions 2
    character.amount_ki_fusions.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # amount_ki_fusions 3
    character.amount_ki_fusions.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # amount_ki_fusions 4
    character.amount_ki_fusions.append(int.from_bytes(pak_file.read(1), byteorder='big'))

    # fusions_animation 1
    character.fusions_animation.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # fusions_animation 2
    character.fusions_animation.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # fusions_animation 3
    character.fusions_animation.append(int.from_bytes(pak_file.read(1), byteorder='big'))
    # fusions_animation 4
    character.fusions_animation.append(int.from_bytes(pak_file.read(1), byteorder='big'))


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
        main_window.color_lightning_value.setCurrentIndex(CPEV.character_list[index].color_lightning)

        # Glow/lightning effect
        main_window.glow_lightning_value.setCurrentIndex(CPEV.character_list[index].glow_lightning)

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
        main_window.transEffectValue.setCurrentIndex(CPEV.character_list[index].transformation_effect)

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
        main_window.trans1_animation_value.setCurrentIndex(CPEV.character_list[index].transformations_animation[0])
        main_window.trans2_animation_value.setCurrentIndex(CPEV.character_list[index].transformations_animation[1])
        main_window.trans3_animation_value.setCurrentIndex(CPEV.character_list[index].transformations_animation[2])
        main_window.trans4_animation_value.setCurrentIndex(CPEV.character_list[index].transformations_animation[3])

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

        # Show Animation per transformation
        main_window.fusion1_animation_value.setCurrentIndex(CPEV.character_list[index].fusions_animation[0])
        main_window.fusion2_animation_value.setCurrentIndex(CPEV.character_list[index].fusions_animation[1])
        main_window.fusion3_animation_value.setCurrentIndex(CPEV.character_list[index].fusions_animation[2])
        main_window.fusion4_animation_value.setCurrentIndex(CPEV.character_list[index].fusions_animation[3])

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
                                                                             str(char_selected_new).zfill(3) + ".png")))
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


def on_color_lightning_changed(main_window):
    # Avoid change the values when the program is changing the character from the main panel
    if not CPEV.change_character:
        CPEV.character_list[CPEV.chara_selected].color_lightning = main_window.color_lightning_value.currentIndex()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_glow_lightning_changed(main_window):
    # Avoid change the values when the program is changing the character from the main panel
    if not CPEV.change_character:
        CPEV.character_list[CPEV.chara_selected].glow_lightning = main_window.glow_lightning_value.currentIndex()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_transformation_ki_effect_changed(main_window):
    # Avoid change the values when the program is changing the character from the main panel
    if not CPEV.change_character:
        CPEV.character_list[CPEV.chara_selected].transformation_effect = main_window.transEffectValue.currentIndex()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_amount_ki_trans_changed(main_window, amount_ki_trans_index):
    # Avoid change the values when the program is changing the character from the main panel
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
    # Avoid change the values when the program is changing the character from the main panel
    if not CPEV.change_character:
        if animation_per_transformation == 0:
            CPEV.character_list[CPEV.chara_selected].transformations_animation[animation_per_transformation] = \
                main_window.trans1_animation_value.currentIndex()
        elif animation_per_transformation == 1:
            CPEV.character_list[CPEV.chara_selected].transformations_animation[animation_per_transformation] = \
                main_window.trans2_animation_value.currentIndex()
        elif animation_per_transformation == 2:
            CPEV.character_list[CPEV.chara_selected].transformations_animation[animation_per_transformation] = \
                main_window.trans3_animation_value.currentIndex()
        elif animation_per_transformation == 3:
            CPEV.character_list[CPEV.chara_selected].transformations_animation[animation_per_transformation] = \
                main_window.trans4_animation_value.currentIndex()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_amount_ki_fusion_changed(main_window, amount_ki_fusion_index):
    # Avoid change the values when the program is changing the character from the main panel
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
    # Avoid change the values when the program is changing the character from the main panel
    if not CPEV.change_character:
        if animation_per_fusion == 0:
            CPEV.character_list[CPEV.chara_selected].fusions_animation[animation_per_fusion] = \
                main_window.fusion1_animation_value.currentIndex()
        elif animation_per_fusion == 1:
            CPEV.character_list[CPEV.chara_selected].fusions_animation[animation_per_fusion] = \
                main_window.fusion2_animation_value.currentIndex()
        elif animation_per_fusion == 2:
            CPEV.character_list[CPEV.chara_selected].fusions_animation[animation_per_fusion] = \
                main_window.fusion3_animation_value.currentIndex()
        elif animation_per_fusion == 3:
            CPEV.character_list[CPEV.chara_selected].fusions_animation[animation_per_fusion] = \
                main_window.fusion4_animation_value.currentIndex()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_aura_size_changed(main_window, aura_index):
    # Avoid change the values when the program is changing the character from the main panel
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
    # Avoid change the values when the program is changing the character from the main panel
    if not CPEV.change_character:

        # Change the slot of health
        CPEV.character_list[CPEV.chara_selected].health = main_window.health_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


def on_camera_size_changed(main_window, camera_index):
    # Avoid change the values when the program is changing the character from the main panel
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
    # Avoid change the values when the program is changing the character from the main panel
    if not CPEV.change_character:

        # Change the slot of health
        CPEV.character_list[CPEV.chara_selected].hit_box = main_window.hit_box_value.value()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
            CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])
