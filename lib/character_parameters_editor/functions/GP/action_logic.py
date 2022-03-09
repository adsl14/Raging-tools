from lib.packages import functools, os, QPixmap
from lib.character_parameters_editor import GPF
from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.GPV import GPV


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
                main_window.transSlotPanel0.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                                main_window=main_window,
                                                                                index=transformations[0],
                                                                                trans_slot_panel_index=0)
                main_window.transSlotPanel0.setVisible(True)
            else:
                main_window.transSlotPanel0.setPixmap(QPixmap())
                main_window.transSlotPanel0.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                                main_window=main_window,
                                                                                index=100, trans_slot_panel_index=0)
            if transformations[1] != 100:
                main_window.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                           "sc_chara_s_" +
                                                                           str(transformations[1]).zfill(3) + ".png")))
                main_window.transSlotPanel1.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                                main_window=main_window,
                                                                                index=transformations[1],
                                                                                trans_slot_panel_index=1)
                main_window.transSlotPanel1.setVisible(True)
            else:
                main_window.transSlotPanel1.setPixmap(QPixmap())
                main_window.transSlotPanel1.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                                main_window=main_window,
                                                                                index=100, trans_slot_panel_index=1)
            if transformations[2] != 100:
                main_window.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                           "sc_chara_s_" +
                                                                           str(transformations[2]).zfill(3) + ".png")))
                main_window.transSlotPanel2.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                                main_window=main_window,
                                                                                index=transformations[2],
                                                                                trans_slot_panel_index=2)
                main_window.transSlotPanel2.setVisible(True)
            else:
                main_window.transSlotPanel2.setPixmap(QPixmap())
                main_window.transSlotPanel2.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                                main_window=main_window,
                                                                                index=100, trans_slot_panel_index=2)
            if transformations[3] != 100:
                main_window.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                           "sc_chara_s_" +
                                                                           str(transformations[3]).zfill(3) + ".png")))
                main_window.transSlotPanel3.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                                main_window=main_window,
                                                                                index=transformations[3],
                                                                                trans_slot_panel_index=3)
                main_window.transSlotPanel3.setVisible(True)
            else:
                main_window.transSlotPanel3.setPixmap(QPixmap())
                main_window.transSlotPanel3.mousePressEvent = functools.partial(GPF.open_select_chara_window,
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
            main_window.transPartnerValue.mousePressEvent = functools.partial(GPF.open_select_chara_window,
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
                main_window.fusiSlotPanel0.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                               main_window=main_window,
                                                                               index=fusions[0],
                                                                               fusion_slot_panel_index=0)
                main_window.fusiSlotPanel0.setVisible(True)
            else:
                main_window.fusiSlotPanel0.setPixmap(QPixmap())
                main_window.fusiSlotPanel0.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                               main_window=main_window,
                                                                               index=100,
                                                                               fusion_slot_panel_index=0)
            if fusions[1] != 100:
                main_window.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                          "sc_chara_s_" +
                                                                          str(fusions[1]).zfill(3) + ".png")))
                main_window.fusiSlotPanel1.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                               main_window=main_window,
                                                                               index=fusions[1],
                                                                               fusion_slot_panel_index=1)
                main_window.fusiSlotPanel1.setVisible(True)
            else:
                main_window.fusiSlotPanel1.setPixmap(QPixmap())
                main_window.fusiSlotPanel1.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                               main_window=main_window,
                                                                               index=100, fusion_slot_panel_index=1)
            if fusions[2] != 100:
                main_window.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                          "sc_chara_s_" +
                                                                          str(fusions[2]).zfill(3) + ".png")))
                main_window.fusiSlotPanel2.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                               main_window=main_window,
                                                                               index=fusions[2],
                                                                               fusion_slot_panel_index=2)
                main_window.fusiSlotPanel2.setVisible(True)
            else:
                main_window.fusiSlotPanel2.setPixmap(QPixmap())
                main_window.fusiSlotPanel2.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                               main_window=main_window,
                                                                               index=100, fusion_slot_panel_index=2)
            if fusions[3] != 100:
                main_window.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                          "sc_chara_s_" +
                                                                          str(fusions[3]).zfill(3) + ".png")))
                main_window.fusiSlotPanel3.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                               main_window=main_window,
                                                                               index=fusions[3],
                                                                               fusion_slot_panel_index=3)
                main_window.fusiSlotPanel3.setVisible(True)
            else:
                main_window.fusiSlotPanel3.setPixmap(QPixmap())
                main_window.fusiSlotPanel3.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                               main_window=main_window,
                                                                               index=100, fusion_slot_panel_index=3)

            # Show the fusion partner trigger
            main_window.fusionPartnerTrigger_value.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                                  "sc_chara_s_" +
                                                                                  str(GPV.character_list[index].
                                                                                      fusion_partner[0]).zfill(3)
                                                                                  + ".png")))
            main_window.fusionPartnerTrigger_value.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                                       main_window=main_window,
                                                                                       index=GPV.character_list[index]
                                                                                       .fusion_partner[0],
                                                                                       fusion_partner_trigger_flag=True)

            # Show the fusion partner visual
            main_window.fusionPartnerVisual_value.setPixmap(
                QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                     str(GPV.character_list[index].fusion_partner[1]).zfill(3)
                                     + ".png")))
            main_window.fusionPartnerVisual_value.mousePressEvent = functools.partial(GPF.open_select_chara_window,
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

            # Blast attacks
            main_window.ico_boost_stick_r_up_value.setCurrentIndex(GPV.character_list[index].blast_attacks["Up"])
            main_window.ico_boost_stick_r_r_value.setCurrentIndex(GPV.character_list[index].blast_attacks["Right"])
            main_window.ico_boost_stick_r_d_value.setCurrentIndex(GPV.character_list[index].blast_attacks["Down"])
            main_window.ico_boost_stick_r_l_value.setCurrentIndex(GPV.character_list[index].blast_attacks["Left"])
            main_window.ico_boost_stick_r_push_value.setCurrentIndex(GPV.character_list[index].blast_attacks["Push"])

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
            main_window.transSlotPanel0.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=0)
        elif GPV.trans_slot_panel_selected == 1:
            main_window.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel1.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=1)
        elif GPV.trans_slot_panel_selected == 2:
            main_window.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel2.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=2)
        elif GPV.trans_slot_panel_selected == 3:
            main_window.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel3.mousePressEvent = functools.partial(GPF.open_select_chara_window,
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
        main_window.transPartnerValue.mousePressEvent = functools.partial(GPF.open_select_chara_window,
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
            main_window.fusiSlotPanel0.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=0)
        elif GPV.fusion_slot_panel_selected == 1:
            main_window.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel1.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=1)
        elif GPV.fusion_slot_panel_selected == 2:
            main_window.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel2.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=2)
        elif GPV.fusion_slot_panel_selected == 3:
            main_window.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel3.mousePressEvent = functools.partial(GPF.open_select_chara_window,
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
        main_window.fusionPartnerTrigger_value.mousePressEvent = functools.partial(GPF.open_select_chara_window,
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
        main_window.fusionPartnerVisual_value.mousePressEvent = functools.partial(GPF.open_select_chara_window,
                                                                                  main_window=main_window,
                                                                                  index=char_selected_new,
                                                                                  fusion_partner_visual_flag=True)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])

    main_window.selectCharaWindow.close()


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


def on_up_blast_attack_logic(main_window):

    # Avoid trigger the combo box at starting
    if not CPEV.change_character:
        GPV.character_list[GPV.chara_selected].blast_attacks["Up"] = main_window.\
            ico_boost_stick_r_up_value.currentIndex()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_r_blast_attack_logic(main_window):

    # Avoid trigger the combo box at starting
    if not CPEV.change_character:
        GPV.character_list[GPV.chara_selected].blast_attacks["Right"] = main_window.\
            ico_boost_stick_r_r_value.currentIndex()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_d_blast_attack_logic(main_window):

    # Avoid trigger the combo box at starting
    if not CPEV.change_character:
        GPV.character_list[GPV.chara_selected].blast_attacks["Down"] = main_window.\
            ico_boost_stick_r_d_value.currentIndex()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_l_blast_attack_logic(main_window):

    # Avoid trigger the combo box at starting
    if not CPEV.change_character:
        GPV.character_list[GPV.chara_selected].blast_attacks["Left"] = main_window.\
            ico_boost_stick_r_l_value.currentIndex()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_p_blast_attack_logic(main_window):

    # Avoid trigger the combo box at starting
    if not CPEV.change_character:
        GPV.character_list[GPV.chara_selected].blast_attacks["Push"] = main_window.\
            ico_boost_stick_r_push_value.currentIndex()

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])
