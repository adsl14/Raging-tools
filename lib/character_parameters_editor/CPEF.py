from lib.character_parameters_editor.CPEV import CPEV
from lib.packages import QLabel, QPixmap, functools, os
from lib.design.select_chara import Ui_Dialog


def initialize_cpe(main_window, QtWidgets):
    # Load all the mini portraits (main panel)
    CPEV.mini_portraits_image = main_window.mainPanel.findChildren(QLabel)

    for i in range(0, 66):
        index_chara = CPEV.mini_portraits_image[i].objectName().split("_")[1]
        CPEV.mini_portraits_image[i].setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_0" +
                                                                    index_chara + ".bmp")))
        CPEV.mini_portraits_image[i].setStyleSheet("QLabel {border : 3px solid grey;}")
        CPEV.mini_portraits_image[i].mousePressEvent = functools.partial(main_window.action_change_character,
                                                                         index=int(index_chara),
                                                                         modify_slot_transform=True)
        CPEV.mini_portraits_image[i].setDisabled(True)

    for i in range(66, len(CPEV.mini_portraits_image)):
        CPEV.mini_portraits_image[i].setStyleSheet("QLabel {border : 3px solid grey;}")
        CPEV.mini_portraits_image[i].setVisible(False)

    # Set the the big portrait image
    main_window.portrait.setVisible(False)

    # Set the aura size
    main_window.aura_size_text.setDisabled(True)
    main_window.aura_size_text.setDisabled(True)
    main_window.aura_size_value.setDisabled(True)
    main_window.aura_size_value.valueChanged.connect(main_window.on_aura_size_changed)

    # Set the color lightning
    main_window.color_lightning_text.setDisabled(True)
    main_window.color_lightning_value.setDisabled(True)
    main_window.color_lightning_value.currentIndexChanged.connect(main_window.on_color_lightning_changed)

    # Set the glow/lightning
    main_window.glow_lightning_text.setDisabled(True)
    main_window.glow_lightning_value.setDisabled(True)
    main_window.glow_lightning_value.currentIndexChanged.connect(main_window.on_glow_lightning_changed)
    main_window.glow_lightning_value.view().setRowHidden(3, True)  # Hide item with ID 3

    # Set the transform panel
    main_window.transPanel.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_transform.png")))
    main_window.transText.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "tx_transform_US.png")))
    main_window.transPanel.setDisabled(True)
    main_window.transText.setDisabled(True)

    # Set the transformation parameter
    main_window.transEffectText.setDisabled(True)
    main_window.transEffectValue.setDisabled(True)
    main_window.transEffectValue.currentIndexChanged.connect(main_window.on_transformation_ki_effect_changed)

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
    main_window.amountKi_trans1_value.valueChanged.connect(lambda: main_window.
                                                           on_amount_ki_trans_changed(amount_ki_trans_index=0))
    main_window.amountKi_trans2_value.valueChanged.connect(lambda: main_window.
                                                           on_amount_ki_trans_changed(amount_ki_trans_index=1))
    main_window.amountKi_trans3_value.valueChanged.connect(lambda: main_window.
                                                           on_amount_ki_trans_changed(amount_ki_trans_index=2))
    main_window.amountKi_trans4_value.valueChanged.connect(lambda: main_window.
                                                           on_amount_ki_trans_changed(amount_ki_trans_index=3))

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
    main_window.trans1_animation_value.currentIndexChanged.connect(lambda: main_window.
                                                                   on_animation_per_transformation_changed
                                                                   (animation_per_transformation=0))
    main_window.trans2_animation_value.currentIndexChanged.connect(lambda: main_window.
                                                                   on_animation_per_transformation_changed
                                                                   (animation_per_transformation=1))
    main_window.trans3_animation_value.currentIndexChanged.connect(lambda: main_window.
                                                                   on_animation_per_transformation_changed
                                                                   (animation_per_transformation=2))
    main_window.trans4_animation_value.currentIndexChanged.connect(lambda: main_window.
                                                                   on_animation_per_transformation_changed
                                                                   (animation_per_transformation=3))
    # Hide items
    for i in [2, 3, 5, 7, 8, 9, 10, 11]:
        main_window.trans1_animation_value.view().setRowHidden(i, True)
        main_window.trans2_animation_value.view().setRowHidden(i, True)
        main_window.trans3_animation_value.view().setRowHidden(i, True)
        main_window.trans4_animation_value.view().setRowHidden(i, True)

    # Set partner potara
    main_window.partnerPotara_slot.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_slot.png")))
    main_window.partnerPotara_slot.setDisabled(True)
    main_window.partnerPotara_value.setDisabled(True)
    main_window.partnerPotara_text.setDisabled(True)

    # Set partner metamoran
    main_window.partnerMetamoran_slot.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_slot.png")))
    main_window.partnerMetamoran_slot.setDisabled(True)
    main_window.partnerMetamoran_value.setDisabled(True)
    main_window.partnerMetamoran_text.setDisabled(True)

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
    main_window.amountKi_fusion1_value.valueChanged.connect(lambda: main_window.
                                                            on_amount_ki_fusion_changed(amount_ki_fusion_index=0))
    main_window.amountKi_fusion2_value.valueChanged.connect(lambda: main_window.
                                                            on_amount_ki_fusion_changed(amount_ki_fusion_index=1))
    main_window.amountKi_fusion3_value.valueChanged.connect(lambda: main_window.
                                                            on_amount_ki_fusion_changed(amount_ki_fusion_index=2))
    main_window.amountKi_fusion4_value.valueChanged.connect(lambda: main_window.
                                                            on_amount_ki_fusion_changed(amount_ki_fusion_index=3))

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
    main_window.fusion1_animation_value.currentIndexChanged.connect(lambda: main_window.
                                                                    on_animation_per_fusion_changed
                                                                    (animation_per_fusion=0))
    main_window.fusion2_animation_value.currentIndexChanged.connect(lambda: main_window.
                                                                    on_animation_per_fusion_changed
                                                                    (animation_per_fusion=1))
    main_window.fusion3_animation_value.currentIndexChanged.connect(lambda: main_window.
                                                                    on_animation_per_fusion_changed
                                                                    (animation_per_fusion=2))
    main_window.fusion4_animation_value.currentIndexChanged.connect(lambda: main_window.
                                                                    on_animation_per_fusion_changed
                                                                    (animation_per_fusion=3))

    # Set the fusion panel
    main_window.fusiPanel.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "pl_fusion.png")))
    main_window.fusiPanelText.setPixmap(QPixmap(os.path.join(CPEV.path_fourSlot_images, "tx_fusion_US.png")))
    main_window.fusiPanel.setDisabled(True)
    main_window.fusiPanelText.setDisabled(True)

    # Load the Select Chara window
    main_window.selectCharaWindow = QtWidgets.QMainWindow()
    main_window.selectCharaUI = Ui_Dialog()
    main_window.selectCharaUI.setupUi(main_window.selectCharaWindow)
    CPEV.mini_portraits_image_select_chara_window = main_window.selectCharaUI.frame.findChildren(QLabel)
    for i in range(0, 100):
        CPEV.mini_portraits_image_select_chara_window[i].setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                                        "sc_chara_0" + str(i).zfill(
                                                                                            2) + ".bmp")))
        CPEV.mini_portraits_image_select_chara_window[i].mousePressEvent = functools.partial(
            main_window.action_edit_trans_fusion_slot, char_selected_new=i)


def store_character_parameters(character, pak_file):
    # Move to the visual parameters position
    pak_file.seek(character.position_visual_parameters)

    # UNK data for now
    pak_file.seek(33, 1)

    # Aura size
    character.aura_size = (int.from_bytes(pak_file.read(1), byteorder='little'))

    # UNK data for now
    pak_file.seek(7, 1)

    # Color lightnings
    character.color_lightning = int.from_bytes(pak_file.read(1), byteorder='little')

    # UNK data for now
    pak_file.seek(69, 1)

    # Glow/Lightnings
    character.glow_lightning = int.from_bytes(pak_file.read(1), byteorder='little')

    # Move to the transformations parameters position
    pak_file.seek(character.position_trans)

    # Character ID
    character.character_id = int.from_bytes(pak_file.read(1), byteorder='little')
    # destransformation effect
    character.transformation_effect = int.from_bytes(pak_file.read(1), byteorder='little')
    # transformation_partner
    character.transformation_partner = int.from_bytes(pak_file.read(1), byteorder='little')

    # Transformation 1
    character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # Transformation 2
    character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # Transformation 3
    character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # Transformation 4
    character.transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))

    # amount_ki_transformations 1
    character.amount_ki_transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # amount_ki_transformations 2
    character.amount_ki_transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # amount_ki_transformations 3
    character.amount_ki_transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # amount_ki_transformations 4
    character.amount_ki_transformations.append(int.from_bytes(pak_file.read(1), byteorder='little'))

    # transformations_animation 1
    character.transformations_animation.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # transformations_animation 2
    character.transformations_animation.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # transformations_animation 3
    character.transformations_animation.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # transformations_animation 4
    character.transformations_animation.append(int.from_bytes(pak_file.read(1), byteorder='little'))

    # Move four positions because is unk data
    pak_file.seek(4, 1)

    # transformation_partner
    character.partner_potara = int.from_bytes(pak_file.read(1), byteorder='little')
    # partner_metamoru
    character.partner_metamoru = int.from_bytes(pak_file.read(1), byteorder='little')

    # fusions 1
    character.fusions.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # fusions 2
    character.fusions.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # fusions 3
    character.fusions.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # fusions 4
    character.fusions.append(int.from_bytes(pak_file.read(1), byteorder='little'))

    # amount_ki_fusions 1
    character.amount_ki_fusions.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # amount_ki_fusions 2
    character.amount_ki_fusions.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # amount_ki_fusions 3
    character.amount_ki_fusions.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # amount_ki_fusions 4
    character.amount_ki_fusions.append(int.from_bytes(pak_file.read(1), byteorder='little'))

    # fusions_animation 1
    character.fusions_animation.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # fusions_animation 2
    character.fusions_animation.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # fusions_animation 3
    character.fusions_animation.append(int.from_bytes(pak_file.read(1), byteorder='little'))
    # fusions_animation 4
    character.fusions_animation.append(int.from_bytes(pak_file.read(1), byteorder='little'))
