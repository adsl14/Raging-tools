import functools
import os

from PyQt5.QtGui import QPixmap

from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.GPF import open_select_chara_trans_fusion_window, enable_disable_operate_resident_param_values, enable_disable_db_font_pad_ps3_values, \
    enable_disable_cs_main_values
from lib.character_parameters_editor.GPV import GPV


def initialize_buttons_events_operate_GP(main_window, character_zero):

    # Show the health
    main_window.health_value.setValue(character_zero.health)

    # Show the camera size
    main_window.camera_size_cutscene_value.setValue(character_zero.camera_size[0])
    main_window.camera_size_idle_value.setValue(character_zero.camera_size[1])

    # Show the hit box
    main_window.hit_box_value.setValue(character_zero.hit_box)

    # Show the aura size
    main_window.aura_size_idle_value.setValue(character_zero.aura_size[0])
    main_window.aura_size_dash_value.setValue(character_zero.aura_size[1])
    main_window.aura_size_charge_value.setValue(character_zero.aura_size[2])

    # Show the color lightnings parameter
    main_window.color_lightning_value.setCurrentIndex(main_window.color_lightning_value.findData
                                                      (character_zero.color_lightning))

    # Show the glow/lightnings parameter
    main_window.glow_lightning_value.setCurrentIndex(main_window.glow_lightning_value.findData
                                                     (character_zero.glow_lightning))

    # Show the transform panel
    main_window.transSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                               str(character_zero.transformations[0]).zfill(
                                                                   3) + ".png")))
    main_window.transSlotPanel0.mousePressEvent = functools.partial(open_select_chara_trans_fusion_window,
                                                                    main_window=main_window,
                                                                    index=character_zero.transformations[0],
                                                                    trans_slot_panel_index=0)
    main_window.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                               str(character_zero.transformations[1]).zfill(
                                                                   3) + ".png")))
    main_window.transSlotPanel1.mousePressEvent = functools.partial(open_select_chara_trans_fusion_window,
                                                                    main_window=main_window,
                                                                    index=character_zero.transformations[1],
                                                                    trans_slot_panel_index=1)
    main_window.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                               str(character_zero.transformations[2]).zfill(
                                                                   3) + ".png")))
    main_window.transSlotPanel2.mousePressEvent = functools.partial(open_select_chara_trans_fusion_window,
                                                                    main_window=main_window,
                                                                    index=character_zero.transformations[2],
                                                                    trans_slot_panel_index=2)
    main_window.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                               str(character_zero.transformations[3]).zfill(
                                                                   3) + ".png")))
    main_window.transSlotPanel3.mousePressEvent = functools.partial(open_select_chara_trans_fusion_window,
                                                                    main_window=main_window,
                                                                    index=character_zero.transformations[3],
                                                                    trans_slot_panel_index=3)

    # Show the transformation parameter
    main_window.transEffectValue.setCurrentIndex(main_window.transEffectValue.findData
                                                 (character_zero.transformation_effect))

    # Show the transformation partner
    main_window.transPartnerValue.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                 str(character_zero.transformation_partner).zfill(3)
                                                                 + ".png")))
    main_window.transPartnerValue.mousePressEvent = functools.partial(open_select_chara_trans_fusion_window,
                                                                      main_window=main_window,
                                                                      index=character_zero.transformation_partner,
                                                                      transformation_partner_flag=True)

    # Show amount ki per transformation
    main_window.amountKi_trans1_value.setValue(character_zero.amount_ki_transformations[0])
    main_window.amountKi_trans2_value.setValue(character_zero.amount_ki_transformations[1])
    main_window.amountKi_trans3_value.setValue(character_zero.amount_ki_transformations[2])
    main_window.amountKi_trans4_value.setValue(character_zero.amount_ki_transformations[3])

    # Show Animation per transformation
    main_window.trans1_animation_value.setCurrentIndex(main_window.trans1_animation_value.findData
                                                       (character_zero.transformations_animation[0]))
    main_window.trans2_animation_value.setCurrentIndex(main_window.trans2_animation_value.findData
                                                       (character_zero.transformations_animation[1]))
    main_window.trans3_animation_value.setCurrentIndex(main_window.trans3_animation_value.findData
                                                       (character_zero.transformations_animation[2]))
    main_window.trans4_animation_value.setCurrentIndex(main_window.trans4_animation_value.findData
                                                       (character_zero.transformations_animation[3]))

    # Show the fusion panel
    main_window.fusiSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                              str(character_zero.fusions[0]).zfill(3) + ".png")))
    main_window.fusiSlotPanel0.mousePressEvent = functools.partial(open_select_chara_trans_fusion_window,
                                                                   main_window=main_window,
                                                                   index=character_zero.fusions[0],
                                                                   fusion_slot_panel_index=0)
    main_window.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                              str(character_zero.fusions[1]).zfill(3) + ".png")))
    main_window.fusiSlotPanel1.mousePressEvent = functools.partial(open_select_chara_trans_fusion_window,
                                                                   main_window=main_window,
                                                                   index=character_zero.fusions[1],
                                                                   fusion_slot_panel_index=1)
    main_window.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                              str(character_zero.fusions[2]).zfill(3) + ".png")))
    main_window.fusiSlotPanel2.mousePressEvent = functools.partial(open_select_chara_trans_fusion_window,
                                                                   main_window=main_window,
                                                                   index=character_zero.fusions[2],
                                                                   fusion_slot_panel_index=2)
    main_window.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                              str(character_zero.fusions[3]).zfill(3) + ".png")))
    main_window.fusiSlotPanel3.mousePressEvent = functools.partial(open_select_chara_trans_fusion_window,
                                                                   main_window=main_window,
                                                                   index=character_zero.fusions[3],
                                                                   fusion_slot_panel_index=3)

    # Show the fusion partner (trigger)
    main_window.fusionPartnerTrigger_value.setPixmap(
        QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                             str(character_zero.fusion_partner[0]).zfill(3)
                             + ".png")))
    main_window.fusionPartnerTrigger_value.mousePressEvent = functools.partial(open_select_chara_trans_fusion_window,
                                                                               main_window=main_window,
                                                                               index=character_zero.fusion_partner
                                                                               [0],
                                                                               fusion_partner_trigger_flag=True)

    # Show fusion partner visual
    main_window.fusionPartnerVisual_value.setPixmap(
        QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                             str(character_zero.fusion_partner[1]).zfill(3)
                             + ".png")))
    main_window.fusionPartnerVisual_value.mousePressEvent = functools.partial(open_select_chara_trans_fusion_window,
                                                                              main_window=main_window,
                                                                              index=character_zero.
                                                                              fusion_partner[1],
                                                                              fusion_partner_visual_flag=True)

    # Show amount ki per fusion
    main_window.amountKi_fusion1_value.setValue(character_zero.amount_ki_fusions[0])
    main_window.amountKi_fusion2_value.setValue(character_zero.amount_ki_fusions[1])
    main_window.amountKi_fusion3_value.setValue(character_zero.amount_ki_fusions[2])
    main_window.amountKi_fusion4_value.setValue(character_zero.amount_ki_fusions[3])

    # Show Animation per transformation
    main_window.fusion1_animation_value.setCurrentIndex(main_window.fusion1_animation_value.findData
                                                        (character_zero.fusions_animation[0]))
    main_window.fusion2_animation_value.setCurrentIndex(main_window.fusion2_animation_value.findData
                                                        (character_zero.fusions_animation[1]))
    main_window.fusion3_animation_value.setCurrentIndex(main_window.fusion3_animation_value.findData
                                                        (character_zero.fusions_animation[2]))
    main_window.fusion4_animation_value.setCurrentIndex(main_window.fusion4_animation_value.findData
                                                        (character_zero.fusions_animation[3]))
    
    
def enable_tabs_operate_GP(main_window):
    
    # Open the tab (character parameters editor)
    if main_window.tabWidget.currentIndex() != 2:
        main_window.tabWidget.setCurrentIndex(2)

    # Open the tab operate_resident_param
    if main_window.tabWidget_2.currentIndex() != 0:
        main_window.tabWidget_2.setCurrentIndex(0)

    # Enable completely the tab character parameters editor
    if not main_window.character_parameters_editor.isEnabled():
        main_window.character_parameters_editor.setEnabled(True)

    # Enable all the buttons (character parameters editor -> operate_resident_param)
    if not main_window.operate_parameters_frame.isEnabled():
        enable_disable_operate_resident_param_values(main_window, True)
        enable_disable_db_font_pad_ps3_values(main_window, False)
        enable_disable_cs_main_values(main_window, False)
    if not main_window.general_parameters_frame.isEnabled():
        main_window.general_parameters_frame.setEnabled(True)

    # Disable all the buttons (character parameters editor -> operate_character_XXX_m)
    if main_window.operate_character_xyz_m_frame.isEnabled():
        main_window.operate_character_xyz_m_frame.setEnabled(False)
    # Disable all the buttons (character parameters editor -> cs_chip)
    if main_window.cs_chip.isEnabled():
        main_window.cs_chip.setEnabled(False)


def initialize_buttons_events_db_font_GP(main_window):
    
    # Show the aura_type parameter
    main_window.aura_type_value.setCurrentIndex(main_window.aura_type_value.findData(
        GPV.character_list[0].aura_type))

    # Show the blast attacks
    main_window.ico_boost_stick_r_up_value.setCurrentIndex(GPV.character_list[0].blast_attacks["Up"])
    main_window.ico_boost_stick_r_r_value.setCurrentIndex(GPV.character_list[0].blast_attacks["Right"])
    main_window.ico_boost_stick_r_d_value.setCurrentIndex(GPV.character_list[0].blast_attacks["Down"])
    main_window.ico_boost_stick_r_l_value.setCurrentIndex(GPV.character_list[0].blast_attacks["Left"])
    main_window.ico_boost_stick_r_push_value.setCurrentIndex(GPV.character_list[0].blast_attacks["Push"])
    
    
def enable_tabs_db_font_GP(main_window):

    # Open the tab (character parameters editor)
    if main_window.tabWidget.currentIndex() != 2:
        main_window.tabWidget.setCurrentIndex(2)

    # Open the tab operate_resident_param
    if main_window.tabWidget_2.currentIndex() != 0:
        main_window.tabWidget_2.setCurrentIndex(0)

    # Enable completely the tab character parameters editor
    if not main_window.character_parameters_editor.isEnabled():
        main_window.character_parameters_editor.setEnabled(True)

    # Enable all the buttons (db_font_pad_PS3_s -> game_resident_param)
    if not main_window.db_font_pad_frame.isEnabled():
        enable_disable_operate_resident_param_values(main_window, False)
        enable_disable_db_font_pad_ps3_values(main_window, True)
        enable_disable_cs_main_values(main_window, False)
    if not main_window.general_parameters_frame.isEnabled():
        main_window.general_parameters_frame.setEnabled(True)

    # Disable all the buttons (character parameters editor -> operate_character_XXX_m)
    if main_window.operate_character_xyz_m_frame.isEnabled():
        main_window.operate_character_xyz_m_frame.setEnabled(False)
    # Disable all the buttons (character parameters editor -> cs_chip)
    if main_window.cs_chip.isEnabled():
        main_window.cs_chip.setEnabled(False)


def initialize_buttons_events_cs_main_GP(main_window):
    # Show the name id parameter
    if GPV.character_list[0].character_name_text_id == 4294967295:
        value = -1
    else:
        value = GPV.character_list[0].character_name_text_id
    main_window.name_value.setValue(value)

    # Show the sub-name id parameter
    if GPV.character_list[0].character_sub_name_text_id == 4294967295:
        value = -1
    else:
        value = GPV.character_list[0].character_sub_name_text_id
    main_window.sub_name_value.setValue(value)


def enable_tabs_cs_main_GP(main_window):

    # Open the tab (character parameters editor)
    if main_window.tabWidget.currentIndex() != 2:
        main_window.tabWidget.setCurrentIndex(2)

    # Open the tab operate_resident_param
    if main_window.tabWidget_2.currentIndex() != 0:
        main_window.tabWidget_2.setCurrentIndex(0)

    # Enable completely the tab character parameters editor
    if not main_window.character_parameters_editor.isEnabled():
        main_window.character_parameters_editor.setEnabled(True)

    # Enable all the buttons (cs_main -> cs_main_dat)
    if not main_window.text_names_chara_frame.isEnabled():
        enable_disable_operate_resident_param_values(main_window, False)
        enable_disable_db_font_pad_ps3_values(main_window, False)
        enable_disable_cs_main_values(main_window, True)
    if not main_window.general_parameters_frame.isEnabled():
        main_window.general_parameters_frame.setEnabled(True)

    # Disable all the buttons (character parameters editor -> operate_character_XXX_m)
    if main_window.operate_character_xyz_m_frame.isEnabled():
        main_window.operate_character_xyz_m_frame.setEnabled(False)
    # Disable all the buttons (character parameters editor -> cs_chip)
    if main_window.cs_chip.isEnabled():
        main_window.cs_chip.setEnabled(False)
