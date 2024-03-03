from PyQt5.QtWidgets import QFileDialog, QMessageBox

from lib.packages import functools, os, QPixmap
from lib.character_parameters_editor import GPF
from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.GPV import GPV


def action_change_character(event, main_window, index=None):

    # Change only if the char selected is other
    if GPV.chara_selected != index:

        # We're changing the character (avoid combo box code)
        GPF.listen_events_logic(main_window, False)

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
                main_window.transSlotPanel0.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                                main_window=main_window,
                                                                                index=transformations[0],
                                                                                trans_slot_panel_index=0)
                main_window.transSlotPanel0.setVisible(True)
            else:
                main_window.transSlotPanel0.setPixmap(QPixmap())
                main_window.transSlotPanel0.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                                main_window=main_window,
                                                                                index=100, trans_slot_panel_index=0)
            if transformations[1] != 100:
                main_window.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                           "sc_chara_s_" +
                                                                           str(transformations[1]).zfill(3) + ".png")))
                main_window.transSlotPanel1.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                                main_window=main_window,
                                                                                index=transformations[1],
                                                                                trans_slot_panel_index=1)
                main_window.transSlotPanel1.setVisible(True)
            else:
                main_window.transSlotPanel1.setPixmap(QPixmap())
                main_window.transSlotPanel1.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                                main_window=main_window,
                                                                                index=100, trans_slot_panel_index=1)
            if transformations[2] != 100:
                main_window.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                           "sc_chara_s_" +
                                                                           str(transformations[2]).zfill(3) + ".png")))
                main_window.transSlotPanel2.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                                main_window=main_window,
                                                                                index=transformations[2],
                                                                                trans_slot_panel_index=2)
                main_window.transSlotPanel2.setVisible(True)
            else:
                main_window.transSlotPanel2.setPixmap(QPixmap())
                main_window.transSlotPanel2.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                                main_window=main_window,
                                                                                index=100, trans_slot_panel_index=2)
            if transformations[3] != 100:
                main_window.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                           "sc_chara_s_" +
                                                                           str(transformations[3]).zfill(3) + ".png")))
                main_window.transSlotPanel3.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                                main_window=main_window,
                                                                                index=transformations[3],
                                                                                trans_slot_panel_index=3)
                main_window.transSlotPanel3.setVisible(True)
            else:
                main_window.transSlotPanel3.setPixmap(QPixmap())
                main_window.transSlotPanel3.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
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
            main_window.transPartnerValue.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
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
                main_window.fusiSlotPanel0.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                               main_window=main_window,
                                                                               index=fusions[0],
                                                                               fusion_slot_panel_index=0)
                main_window.fusiSlotPanel0.setVisible(True)
            else:
                main_window.fusiSlotPanel0.setPixmap(QPixmap())
                main_window.fusiSlotPanel0.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                               main_window=main_window,
                                                                               index=100,
                                                                               fusion_slot_panel_index=0)
            if fusions[1] != 100:
                main_window.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                          "sc_chara_s_" +
                                                                          str(fusions[1]).zfill(3) + ".png")))
                main_window.fusiSlotPanel1.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                               main_window=main_window,
                                                                               index=fusions[1],
                                                                               fusion_slot_panel_index=1)
                main_window.fusiSlotPanel1.setVisible(True)
            else:
                main_window.fusiSlotPanel1.setPixmap(QPixmap())
                main_window.fusiSlotPanel1.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                               main_window=main_window,
                                                                               index=100, fusion_slot_panel_index=1)
            if fusions[2] != 100:
                main_window.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                          "sc_chara_s_" +
                                                                          str(fusions[2]).zfill(3) + ".png")))
                main_window.fusiSlotPanel2.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                               main_window=main_window,
                                                                               index=fusions[2],
                                                                               fusion_slot_panel_index=2)
                main_window.fusiSlotPanel2.setVisible(True)
            else:
                main_window.fusiSlotPanel2.setPixmap(QPixmap())
                main_window.fusiSlotPanel2.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                               main_window=main_window,
                                                                               index=100, fusion_slot_panel_index=2)
            if fusions[3] != 100:
                main_window.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                          "sc_chara_s_" +
                                                                          str(fusions[3]).zfill(3) + ".png")))
                main_window.fusiSlotPanel3.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                               main_window=main_window,
                                                                               index=fusions[3],
                                                                               fusion_slot_panel_index=3)
                main_window.fusiSlotPanel3.setVisible(True)
            else:
                main_window.fusiSlotPanel3.setPixmap(QPixmap())
                main_window.fusiSlotPanel3.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                               main_window=main_window,
                                                                               index=100, fusion_slot_panel_index=3)

            # Show the fusion partner trigger
            main_window.fusionPartnerTrigger_value.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images,
                                                                                  "sc_chara_s_" +
                                                                                  str(GPV.character_list[index].
                                                                                      fusion_partner[0]).zfill(3)
                                                                                  + ".png")))
            main_window.fusionPartnerTrigger_value.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                                       main_window=main_window,
                                                                                       index=GPV.character_list[index]
                                                                                       .fusion_partner[0],
                                                                                       fusion_partner_trigger_flag=True)

            # Show the fusion partner visual
            main_window.fusionPartnerVisual_value.setPixmap(
                QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                     str(GPV.character_list[index].fusion_partner[1]).zfill(3)
                                     + ".png")))
            main_window.fusionPartnerVisual_value.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
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

            # Show blast attack pause menu
            main_window.blast_attack_id_value.setCurrentIndex(0)
            main_window.blast_attack_name_id_value.setValue(GPV.character_list[index].blast_attacks_pause_menu_text[0][0])
            main_window.blast_attack_description_id_value.setValue(GPV.character_list[index].blast_attacks_pause_menu_text[0][1])

            # Show blast attack in game
            main_window.blast_attack_id_ingame_value.setCurrentIndex(0)
            main_window.blast_attack_name_id_ingame_value.setValue(GPV.character_list[index].blast_attacks_id_text_in_game[0])

        # The user has opened the file db_fond_pad
        elif GPV.db_font_pad_XYZ_s_d:

            # Aura type
            main_window.aura_type_value.setCurrentIndex(main_window.aura_type_value.findData
                                                        (GPV.character_list[index].aura_type))

            # Blast attacks
            main_window.ico_boost_stick_r_up_value.setCurrentIndex(GPV.character_list[index].blast_attacks["Up"])
            main_window.ico_boost_stick_r_r_value.setCurrentIndex(GPV.character_list[index].blast_attacks["Right"])
            main_window.ico_boost_stick_r_d_value.setCurrentIndex(GPV.character_list[index].blast_attacks["Down"])
            main_window.ico_boost_stick_r_l_value.setCurrentIndex(GPV.character_list[index].blast_attacks["Left"])
            main_window.ico_boost_stick_r_push_value.setCurrentIndex(GPV.character_list[index].blast_attacks["Push"])

        # The user has opened the file cs_main
        else:

            # Name id parameter
            # Check if there is a character that doesn't have any name written. We have to adjust the value to the tool if that's the case
            if GPV.character_list[index].character_name_text_id == 4294967295:
                value = -1
            else:
                value = GPV.character_list[index].character_name_text_id
            main_window.name_value.setValue(value)

            # Sub-name id parameter
            # Check if there is a character that doesn't have any name written. We have to adjust the value to the tool if that's the case
            if GPV.character_list[index].character_sub_name_text_id == 4294967295:
                value = -1
            else:
                value = GPV.character_list[index].character_sub_name_text_id
            main_window.sub_name_value.setValue(value)

        # Reset border color in the select chara window
        GPV.mini_portraits_image_select_chara[GPV.chara_selected].setStyleSheet(CPEV.styleSheetSlotRosterWindow)

        # Change character image
        main_window.general_parameter_character_slot.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_" + str(index).zfill(3) + ".bmp")))

        # Update the current selected chara
        GPV.chara_selected = index

        # Close the window
        main_window.selectGeneralCharaRosterWindow.close()

        # We're not changing the character in the main panel (play combo box code)
        GPF.listen_events_logic(main_window, True)


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
            main_window.transSlotPanel0.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=0)
        elif GPV.trans_slot_panel_selected == 1:
            main_window.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel1.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=1)
        elif GPV.trans_slot_panel_selected == 2:
            main_window.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel2.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                            main_window=main_window,
                                                                            index=char_selected_new,
                                                                            trans_slot_panel_index=2)
        elif GPV.trans_slot_panel_selected == 3:
            main_window.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(char_selected_new).zfill(3) + ".png")))
            main_window.transSlotPanel3.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
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
        main_window.transPartnerValue.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
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
            main_window.fusiSlotPanel0.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=0)
        elif GPV.fusion_slot_panel_selected == 1:
            main_window.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel1.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=1)
        elif GPV.fusion_slot_panel_selected == 2:
            main_window.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel2.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                           main_window=main_window,
                                                                           index=char_selected_new,
                                                                           fusion_slot_panel_index=2)
        elif GPV.fusion_slot_panel_selected == 3:
            main_window.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(char_selected_new).zfill(3) + ".png")))
            main_window.fusiSlotPanel3.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
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
        main_window.fusionPartnerTrigger_value.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
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
        main_window.fusionPartnerVisual_value.mousePressEvent = functools.partial(GPF.open_select_chara_trans_fusion_window,
                                                                                  main_window=main_window,
                                                                                  index=char_selected_new,
                                                                                  fusion_partner_visual_flag=True)

        # If the character was edited before, we won't append the index to our array of characters edited once
        if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
            GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])

    main_window.selectCharaTransFusionWindow.close()


def action_export_signature_button_logic(main_window):

    # Ask the user the file output
    name_file = str(GPV.chara_selected).zfill(3) + "_" + GPV.signature_output_name
    file_export_path = QFileDialog.getSaveFileName(main_window, "Export signature parameters",
                                                   os.path.join(main_window.old_path_file, name_file), "")[0]

    # The user has selected an output
    if file_export_path:

        # Get the current character
        character = GPV.character_list[GPV.chara_selected]

        # Export the signature
        with open(file_export_path, mode="wb") as output:
            output.write(character.signature_values)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setWindowIcon(main_window.ico_image)
        message = "The signature file was exported in: <b>" + file_export_path \
                  + "</b><br><br> Do you wish to open the path?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + os.path.dirname(file_export_path).replace("/", "\\"))


def action_import_signature_button_logic(main_window):

    # Ask the user from what file wants to open the signature
    file_import_path = QFileDialog.getOpenFileName(main_window, "Import signature parameters",
                                                   main_window.old_path_file, "")[0]

    if os.path.exists(file_import_path):

        with open(file_import_path, mode="rb") as input_file:
            signature_input_data = input_file.read()

        # If the length of the imported signature is not 88, we won't import it
        if len(signature_input_data) != 88:
            # Wrong signature file
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setWindowIcon(main_window.ico_image)
            msg.setText("Invalid signature file.")
            msg.exec()
        else:
            character = GPV.character_list[GPV.chara_selected]
            character.signature_values = signature_input_data

            # Append the character class to the list of characters edited, but only once
            if character not in GPV.character_list_edited:
                GPV.character_list_edited.append(character)

            # signature imported
            msg = QMessageBox()
            msg.setWindowTitle("Message")
            msg.setWindowIcon(main_window.ico_image)
            msg.setText("The signature file was imported suscessfully.")
            msg.exec()

        # Change old path
        main_window.old_path_file = file_import_path


def on_color_lightning_changed(main_window):

    GPV.character_list[GPV.chara_selected].color_lightning = main_window.color_lightning_value.currentData()

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_glow_lightning_changed(main_window):

    GPV.character_list[GPV.chara_selected].glow_lightning = main_window.glow_lightning_value.currentData()

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_transformation_ki_effect_changed(main_window):

    GPV.character_list[
        GPV.chara_selected].transformation_effect = main_window.transEffectValue.currentData()

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_amount_ki_trans_changed(main_window, amount_ki_trans_index):

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

    # Change the slot of health
    GPV.character_list[GPV.chara_selected].health = int(main_window.health_value.value())

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_camera_size_changed(main_window, camera_index):

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

    # Change the slot of health
    GPV.character_list[GPV.chara_selected].hit_box = main_window.hit_box_value.value()

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_aura_type_changed(main_window):

    GPV.character_list[GPV.chara_selected].aura_type = main_window.aura_type_value.currentData()

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_up_blast_attack_logic(main_window):

    GPV.character_list[GPV.chara_selected].blast_attacks["Up"] = main_window.\
        ico_boost_stick_r_up_value.currentIndex()

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_r_blast_attack_logic(main_window):

    GPV.character_list[GPV.chara_selected].blast_attacks["Right"] = main_window.\
        ico_boost_stick_r_r_value.currentIndex()

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_d_blast_attack_logic(main_window):

    GPV.character_list[GPV.chara_selected].blast_attacks["Down"] = main_window.\
        ico_boost_stick_r_d_value.currentIndex()

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_l_blast_attack_logic(main_window):

    GPV.character_list[GPV.chara_selected].blast_attacks["Left"] = main_window.\
        ico_boost_stick_r_l_value.currentIndex()

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_p_blast_attack_logic(main_window):

    GPV.character_list[GPV.chara_selected].blast_attacks["Push"] = main_window.\
        ico_boost_stick_r_push_value.currentIndex()

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_name_text_changed(main_window):

    # Store the id text name selected by the user. Check if the value in the tool is '-1' so we can store in memory the proper value
    if main_window.name_value.value() == -1:
        value = 4294967295
    else:
        value = main_window.name_value.value()
    GPV.character_list[GPV.chara_selected].character_name_text_id = value

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_sub_name_text_changed(main_window):

    # Store the id text name selected by the user. Check if the value in the tool is '-1' so we can store in memory the proper value
    if main_window.sub_name_value.value() == -1:
        value = 4294967295
    else:
        value = main_window.sub_name_value.value()
    GPV.character_list[GPV.chara_selected].character_sub_name_text_id = value

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_blast_attack_id_pause_menu_changed(main_window):

    # Disable functions
    try:
        main_window.blast_attack_name_id_value.valueChanged.disconnect()
        main_window.blast_attack_description_id_value.valueChanged.disconnect()
    except TypeError:
        pass

    main_window.blast_attack_name_id_value.setValue(GPV.character_list[GPV.chara_selected].blast_attacks_pause_menu_text[main_window.blast_attack_id_value.currentIndex()][0])
    main_window.blast_attack_description_id_value.setValue(GPV.character_list[GPV.chara_selected].blast_attacks_pause_menu_text[main_window.blast_attack_id_value.currentIndex()][1])

    # Enable functions again
    main_window.blast_attack_name_id_value.valueChanged.connect(lambda: on_blast_attack_name_and_description_pause_menu_changed(main_window, 0))
    main_window.blast_attack_description_id_value.valueChanged.connect(lambda: on_blast_attack_name_and_description_pause_menu_changed(main_window, 1))


def on_blast_attack_name_and_description_pause_menu_changed(main_window, description):

    # Check if we're editing the ID text for the description of the blast attack or only the name
    if description:
        value = main_window.blast_attack_description_id_value.value()
    else:
        value = main_window.blast_attack_name_id_value.value()
    GPV.character_list[GPV.chara_selected].blast_attacks_pause_menu_text[main_window.blast_attack_id_value.currentIndex()][description] = value

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])


def on_blast_attack_id_ingame_changed(main_window):

    # Disable functions
    try:
        main_window.blast_attack_name_id_ingame_value.valueChanged.disconnect()
    except TypeError:
        pass

    main_window.blast_attack_name_id_ingame_value.setValue(GPV.character_list[GPV.chara_selected].blast_attacks_id_text_in_game[main_window.blast_attack_id_ingame_value.currentIndex()])

    # Enable functions again
    main_window.blast_attack_name_id_ingame_value.valueChanged.connect(lambda: on_blast_attack_name_ingame_changed(main_window))


def on_blast_attack_name_ingame_changed(main_window):

    GPV.character_list[GPV.chara_selected].blast_attacks_id_text_in_game[main_window.blast_attack_id_ingame_value.currentIndex()] = main_window.blast_attack_name_id_ingame_value.value()

    # If the character was edited before, we won't append the index to our array of characters edited once
    if GPV.character_list[GPV.chara_selected] not in GPV.character_list_edited:
        GPV.character_list_edited.append(GPV.character_list[GPV.chara_selected])
