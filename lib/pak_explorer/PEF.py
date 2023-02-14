from PyQt5.QtCore import QObject, pyqtSignal

from lib.character_parameters_editor.IPV import IPV
from lib.character_parameters_editor.REF import read_cs_chip_file, write_cs_chip_file
from lib.character_parameters_editor.IPF import read_single_character_parameters, write_single_character_parameters
from lib.character_parameters_editor.GPF import read_operate_resident_param, \
    open_select_chara_window, read_db_font_pad_ps3, enable_disable_operate_resident_param_values, \
    enable_disable_db_font_pad_ps3_values, initialize_roster, write_db_font_pad_ps3, write_operate_resident_param
from lib.character_parameters_editor.GPV import GPV
from lib.character_parameters_editor.REV import REV
from lib.functions import show_progress_value
from lib.packages import rmtree, re, natsorted, move
from lib import functions
from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.classes.Character import Character
from lib.packages import os, functools, stat, QPixmap, QLabel, QStandardItem, QStandardItemModel
from lib.pak_explorer.PEV import PEV
from lib.pak_explorer.functions.action_logic import action_open_temp_folder_button_logic, action_export_all_2_logic, action_export_2_logic, action_import_2_logic


# Step 1: Create a worker class
class WorkerPef(QObject):
    finished = pyqtSignal()
    progressValue = pyqtSignal(float)
    progressText = pyqtSignal(str)

    main_window = None
    path_output_file = ""
    separator = b''
    separator_size = 0
    start_progress = 0.0
    step_progress_pack = 0.0
    end_progress = 100.0

    def load_data_to_pe_cpe(self):

        # 2 main tasks
        step_progress = self.end_progress / 2

        # Reset model list view
        self.main_window.listView_2.model().clear()

        # Unpack pak file (pak explorer)
        IPV.signature_folder_index_list_view = None
        PEV.number_files = 0

        # Report progress
        self.progressText.emit("Unpacking file...")
        unpack(PEV.pak_file_path, os.path.basename(PEV.pak_file_path).split(".")[-1], PEV.temp_folder,
               self.main_window.listView_2)
        show_progress_value(self, step_progress)

        # Assign the first entry to the list view
        self.main_window.listView_2.setCurrentIndex(self.main_window.listView_2.model().index(0, 0))

        # Enable the pak explorer
        self.main_window.pak_explorer.setEnabled(True)
        # Add the title
        self.main_window.fileNameText_2.setText(os.path.basename(PEV.pak_file_path_original))

        # Read the pak file (character parameters editor)
        pak_file = open(PEV.pak_file_path, mode="rb")

        # Read the header (STPK)
        pak_file.seek(32)
        data = pak_file.read(32).replace(b'\x00', b'')
        pak_file.seek(176)
        data_2 = pak_file.read(32).replace(b'\x00', b'')
        pak_file.close()

        # Check if the file is the operate_resident_param.pak and is from RB2 (effect_resident_m)
        if data == CPEV.operate_resident_param and data_2 == CPEV.effect_resident_m:

            # reset the values
            GPV.character_list_edited.clear()
            GPV.character_list.clear()
            GPV.chara_selected = 0  # Index of the char selected in the program
            GPV.operate_resident_param_file = True

            # Read all the data from the files
            # character_info, transformer_i and skill.dat
            GPV.resident_character_inf_path = self.main_window.listView_2.model().item(3, 0).text()
            GPV.resident_transformer_i_path = self.main_window.listView_2.model().item(11, 0).text()
            GPV.resident_skill_path = self.main_window.listView_2.model().item(16, 0).text()
            subpak_file_character_inf = open(GPV.resident_character_inf_path, mode="rb")
            subpak_file_transformer_i = open(GPV.resident_transformer_i_path, mode="rb")
            subpak_file_skill = open(GPV.resident_skill_path, mode="rb")
            # Moves to the position 4 in the skill file since there starts the information for the first character
            subpak_file_skill.seek(4)

            # Read the data from the files and store the parameters
            sub_step_progress = step_progress / 100
            for i in range(0, 100):
                # Report progress
                self.progressText.emit("Reading character " + str(i))
                show_progress_value(self, sub_step_progress)

                # Create a Character object
                character = Character()

                # Store the positions where the information is located
                character.position_visual_parameters = i * GPV.sizeVisualParameters
                character.position_trans = i * GPV.sizeTrans

                # Store the information in the object and append to a list
                read_operate_resident_param(character, subpak_file_character_inf, subpak_file_transformer_i,
                                            subpak_file_skill)
                GPV.character_list.append(character)

            # Close the files
            subpak_file_character_inf.close()
            subpak_file_transformer_i.close()
            subpak_file_skill.close()

            # Initialize main roster
            initialize_roster(self.main_window)

            # Get the values for the fist character of the list
            character_zero = GPV.character_list[0]

            # Show the health
            self.main_window.health_value.setValue(character_zero.health)

            # Show the camera size
            self.main_window.camera_size_cutscene_value.setValue(character_zero.camera_size[0])
            self.main_window.camera_size_idle_value.setValue(character_zero.camera_size[1])

            # Show the hit box
            self.main_window.hit_box_value.setValue(character_zero.hit_box)

            # Show the aura size
            self.main_window.aura_size_idle_value.setValue(character_zero.aura_size[0])
            self.main_window.aura_size_dash_value.setValue(character_zero.aura_size[1])
            self.main_window.aura_size_charge_value.setValue(character_zero.aura_size[2])

            # Show the color lightnings parameter
            self.main_window.color_lightning_value.setCurrentIndex(self.main_window.color_lightning_value.findData
                                                                   (character_zero.color_lightning))

            # Show the glow/lightnings parameter
            self.main_window.glow_lightning_value.setCurrentIndex(self.main_window.glow_lightning_value.findData
                                                                  (character_zero.glow_lightning))

            # Show the transform panel
            self.main_window.transSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                            str(character_zero.transformations[0]).zfill(
                                                                                3) + ".png")))
            self.main_window.transSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                 main_window=self.main_window,
                                                                                 index=character_zero.transformations[0],
                                                                                 trans_slot_panel_index=0)
            self.main_window.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                            str(character_zero.transformations[1]).zfill(
                                                                                3) + ".png")))
            self.main_window.transSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                 main_window=self.main_window,
                                                                                 index=character_zero.transformations[1],
                                                                                 trans_slot_panel_index=1)
            self.main_window.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                            str(character_zero.transformations[2]).zfill(
                                                                                3) + ".png")))
            self.main_window.transSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                 main_window=self.main_window,
                                                                                 index=character_zero.transformations[2],
                                                                                 trans_slot_panel_index=2)
            self.main_window.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                            str(character_zero.transformations[3]).zfill(
                                                                                3) + ".png")))
            self.main_window.transSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                 main_window=self.main_window,
                                                                                 index=character_zero.transformations[3],
                                                                                 trans_slot_panel_index=3)

            # Show the transformation parameter
            self.main_window.transEffectValue.setCurrentIndex(self.main_window.transEffectValue.findData
                                                              (character_zero.transformation_effect))

            # Show the transformation partner
            self.main_window.transPartnerValue.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                              str(character_zero.transformation_partner).zfill(3)
                                                                              + ".png")))
            self.main_window.transPartnerValue.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                   main_window=self.main_window,
                                                                                   index=character_zero.transformation_partner,
                                                                                   transformation_partner_flag=True)

            # Show amount ki per transformation
            self.main_window.amountKi_trans1_value.setValue(character_zero.amount_ki_transformations[0])
            self.main_window.amountKi_trans2_value.setValue(character_zero.amount_ki_transformations[1])
            self.main_window.amountKi_trans3_value.setValue(character_zero.amount_ki_transformations[2])
            self.main_window.amountKi_trans4_value.setValue(character_zero.amount_ki_transformations[3])

            # Show Animation per transformation
            self.main_window.trans1_animation_value.setCurrentIndex(self.main_window.trans1_animation_value.findData
                                                                    (character_zero.transformations_animation[0]))
            self.main_window.trans2_animation_value.setCurrentIndex(self.main_window.trans2_animation_value.findData
                                                                    (character_zero.transformations_animation[1]))
            self.main_window.trans3_animation_value.setCurrentIndex(self.main_window.trans3_animation_value.findData
                                                                    (character_zero.transformations_animation[2]))
            self.main_window.trans4_animation_value.setCurrentIndex(self.main_window.trans4_animation_value.findData
                                                                    (character_zero.transformations_animation[3]))

            # Show the fusion panel
            self.main_window.fusiSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                           str(character_zero.fusions[0]).zfill(3) + ".png")))
            self.main_window.fusiSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                main_window=self.main_window,
                                                                                index=character_zero.fusions[0],
                                                                                fusion_slot_panel_index=0)
            self.main_window.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                           str(character_zero.fusions[1]).zfill(3) + ".png")))
            self.main_window.fusiSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                main_window=self.main_window,
                                                                                index=character_zero.fusions[1],
                                                                                fusion_slot_panel_index=1)
            self.main_window.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                           str(character_zero.fusions[2]).zfill(3) + ".png")))
            self.main_window.fusiSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                main_window=self.main_window,
                                                                                index=character_zero.fusions[2],
                                                                                fusion_slot_panel_index=2)
            self.main_window.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                           str(character_zero.fusions[3]).zfill(3) + ".png")))
            self.main_window.fusiSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                main_window=self.main_window,
                                                                                index=character_zero.fusions[3],
                                                                                fusion_slot_panel_index=3)

            # Show the fusion partner (trigger)
            self.main_window.fusionPartnerTrigger_value.setPixmap(
                QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                     str(character_zero.fusion_partner[0]).zfill(3)
                                     + ".png")))
            self.main_window.fusionPartnerTrigger_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                            main_window=self.main_window,
                                                                                            index=character_zero.fusion_partner
                                                                                            [0],
                                                                                            fusion_partner_trigger_flag=True)

            # Show fusion partner visual
            self.main_window.fusionPartnerVisual_value.setPixmap(
                QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                     str(character_zero.fusion_partner[1]).zfill(3)
                                     + ".png")))
            self.main_window.fusionPartnerVisual_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                           main_window=self.main_window,
                                                                                           index=character_zero.
                                                                                           fusion_partner[1],
                                                                                           fusion_partner_visual_flag=True)

            # Show amount ki per fusion
            self.main_window.amountKi_fusion1_value.setValue(character_zero.amount_ki_fusions[0])
            self.main_window.amountKi_fusion2_value.setValue(character_zero.amount_ki_fusions[1])
            self.main_window.amountKi_fusion3_value.setValue(character_zero.amount_ki_fusions[2])
            self.main_window.amountKi_fusion4_value.setValue(character_zero.amount_ki_fusions[3])

            # Show Animation per transformation
            self.main_window.fusion1_animation_value.setCurrentIndex(self.main_window.fusion1_animation_value.findData
                                                                     (character_zero.fusions_animation[0]))
            self.main_window.fusion2_animation_value.setCurrentIndex(self.main_window.fusion2_animation_value.findData
                                                                     (character_zero.fusions_animation[1]))
            self.main_window.fusion3_animation_value.setCurrentIndex(self.main_window.fusion3_animation_value.findData
                                                                     (character_zero.fusions_animation[2]))
            self.main_window.fusion4_animation_value.setCurrentIndex(self.main_window.fusion4_animation_value.findData
                                                                     (character_zero.fusions_animation[3]))

            # Open the tab (character parameters editor)
            if self.main_window.tabWidget.currentIndex() != 2:
                self.main_window.tabWidget.setCurrentIndex(2)

            # Open the tab operate_resident_param
            if self.main_window.tabWidget_2.currentIndex() != 0:
                self.main_window.tabWidget_2.setCurrentIndex(0)

            # Enable completely the tab character parameters editor
            if not self.main_window.character_parameters_editor.isEnabled():
                self.main_window.character_parameters_editor.setEnabled(True)

            # Enable all the buttons (character parameters editor -> operate_resident_param)
            if not self.main_window.health.isEnabled():
                enable_disable_operate_resident_param_values(self.main_window, True)
                enable_disable_db_font_pad_ps3_values(self.main_window, False)
            if not self.main_window.operate_resident_param_frame.isEnabled():
                self.main_window.operate_resident_param_frame.setEnabled(True)

            # Disable all the buttons (character parameters editor -> operate_character_XXX_m)
            if self.main_window.operate_character_xyz_m_frame.isEnabled():
                self.main_window.operate_character_xyz_m_frame.setEnabled(False)
            # Disable all the buttons (character parameters editor -> cs_chip)
            if self.main_window.cs_chip.isEnabled():
                self.main_window.cs_chip.setEnabled(False)

        # Check if the file is the db_font_pad_PS3_s.zpak or db_font_pad_X360_s.zpak
        elif data == CPEV.db_font_pad_PS3_s_d or data == CPEV.db_font_pad_X360_s_d:

            # reset the values
            GPV.character_list_edited.clear()
            GPV.character_list.clear()
            GPV.chara_selected = 0  # Index of the char selected in the program
            GPV.operate_resident_param_file = False

            # Read all the data from the files
            GPV.game_resident_character_param = self.main_window.listView_2.model().item(2, 0).text()
            subpak_file_resident_character_param = open(GPV.game_resident_character_param, mode="rb")

            # Read the data from the files and store the parameters
            sub_step_progress = step_progress / 100.0
            for i in range(0, 100):
                # Report progress
                self.progressText.emit("Reading character " + str(i))
                show_progress_value(self, sub_step_progress)

                # Create a Character object
                character = Character()

                # Store the positions where the information is located
                character.position_resident_character_param = i * GPV.sizeCharacterParam

                # Store the information in the object and append to a list
                read_db_font_pad_ps3(character, subpak_file_resident_character_param)
                GPV.character_list.append(character)

            # Close the files
            subpak_file_resident_character_param.close()

            # Initialize main roster
            initialize_roster(self.main_window)

            # Show the aura_type parameter
            self.main_window.aura_type_value.setCurrentIndex(self.main_window.aura_type_value.findData(
                GPV.character_list[0].aura_type))

            # Show the blast attacks
            self.main_window.ico_boost_stick_r_up_value.setCurrentIndex(GPV.character_list[0].blast_attacks["Up"])
            self.main_window.ico_boost_stick_r_r_value.setCurrentIndex(GPV.character_list[0].blast_attacks["Right"])
            self.main_window.ico_boost_stick_r_d_value.setCurrentIndex(GPV.character_list[0].blast_attacks["Down"])
            self.main_window.ico_boost_stick_r_l_value.setCurrentIndex(GPV.character_list[0].blast_attacks["Left"])
            self.main_window.ico_boost_stick_r_push_value.setCurrentIndex(GPV.character_list[0].blast_attacks["Push"])

            # Open the tab (character parameters editor)
            if self.main_window.tabWidget.currentIndex() != 2:
                self.main_window.tabWidget.setCurrentIndex(2)

            # Open the tab operate_resident_param
            if self.main_window.tabWidget_2.currentIndex() != 0:
                self.main_window.tabWidget_2.setCurrentIndex(0)

            # Enable completely the tab character parameters editor
            if not self.main_window.character_parameters_editor.isEnabled():
                self.main_window.character_parameters_editor.setEnabled(True)

            # Enable all the buttons (db_font_pad_PS3_s -> game_resident_param)
            if not self.main_window.aura_type.isEnabled():
                enable_disable_operate_resident_param_values(self.main_window, False)
                enable_disable_db_font_pad_ps3_values(self.main_window, True)
            if not self.main_window.operate_resident_param_frame.isEnabled():
                self.main_window.operate_resident_param_frame.setEnabled(True)

            # Disable all the buttons (character parameters editor -> operate_character_XXX_m)
            if self.main_window.operate_character_xyz_m_frame.isEnabled():
                self.main_window.operate_character_xyz_m_frame.setEnabled(False)
            # Disable all the buttons (character parameters editor -> cs_chip)
            if self.main_window.cs_chip.isEnabled():
                self.main_window.cs_chip.setEnabled(False)

        # Check if the file is an operate_character_xyz_m type
        elif re.search(CPEV.operate_character_xyz_m_regex, data):

            # Save the id of the character to the character parameters editor tab
            CPEV.file_character_id = data.decode('utf-8').split("_")[2]

            # Read all the data from the files and store it in the global_character from IPV.
            read_single_character_parameters(self, step_progress, self.main_window)

            # Open the tab (character parameters editor)
            if self.main_window.tabWidget.currentIndex() != 2:
                self.main_window.tabWidget.setCurrentIndex(2)

            # Open the tab operate_character_XXX_m
            if self.main_window.tabWidget_2.currentIndex() != 1:
                self.main_window.tabWidget_2.setCurrentIndex(1)

            # Enable completely the tab character parameters editor
            if not self.main_window.character_parameters_editor.isEnabled():
                self.main_window.character_parameters_editor.setEnabled(True)

            # Disable all the buttons (character parameters editor -> operate_resident_param)
            if self.main_window.operate_resident_param_frame.isEnabled():
                self.main_window.operate_resident_param_frame.setEnabled(False)
            # Enable all the buttons (character parameters editor -> operate_character_XXX_m)
            if not self.main_window.operate_character_xyz_m_frame.isEnabled():
                self.main_window.operate_character_xyz_m_frame.setEnabled(True)
            # Disable all the buttons (character parameters editor -> cs_chip)
            if self.main_window.cs_chip.isEnabled():
                self.main_window.cs_chip.setEnabled(False)

        # Check if the file is cs_chip
        elif data == CPEV.cs_chip:

            # reset the values only if we activate again the roster editor tab
            if not REV.roster_editor_first_activation:

                # Get the slot of the selected character and the slot of the selected transformation
                slot_chara = REV.slots_characters[REV.slot_chara_selected]
                slot_chara.qlabel_object.setStyleSheet(CPEV.styleSheetSelectSlotRoster)
                slot_trans = REV.slots_transformations[REV.slot_trans_selected]
                slot_trans.qlabel_object.setStyleSheet(CPEV.styleSheetSelectSlotRoster)

                # Reset only the background color for the slot that was selected before (selecting character in cyan, or
                # selecting transformation in red)
                if REV.selecting_character:
                    # Reset slot in roster window
                    select_chara_roster_window_label = self.main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                                            str(slot_chara.
                                                                                                                chara_id))
                    select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)
                else:

                    select_chara_roster_window_label = self.main_window.selectCharaRosterUI.frame.findChild(QLabel, "label_" +
                                                                                                            str(slot_trans.
                                                                                                                chara_id))
                    select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)

                # Reset the rest of the vars
                self.main_window.portrait_2.setPixmap(QPixmap(""))
                REV.slots_edited.clear()
                for i in range(0, REV.num_slots_characters):
                    slot = REV.slots_characters[i]
                    slot.reset()
                for i in range(0, REV.num_slots_transformations):
                    slot = REV.slots_transformations[i]
                    slot.reset()
                    slot.qlabel_object.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_101.bmp")))

                REV.slot_chara_selected = -1
                REV.slot_trans_selected = -1
                REV.selecting_character = True
            else:
                REV.roster_editor_first_activation = False

            # Read all the data from the files and store it in the global vars from REV.
            read_cs_chip_file(self, step_progress, self.main_window)

            # Open the tab (character parameters editor)
            if self.main_window.tabWidget.currentIndex() != 2:
                self.main_window.tabWidget.setCurrentIndex(2)

            # Open the tab operate_character_XXX_m
            if self.main_window.tabWidget_2.currentIndex() != 2:
                self.main_window.tabWidget_2.setCurrentIndex(2)

            # Enable completely the tab character parameters editor
            if not self.main_window.character_parameters_editor.isEnabled():
                self.main_window.character_parameters_editor.setEnabled(True)

            # Disable all the buttons (character parameters editor -> operate_resident_param)
            if self.main_window.operate_resident_param_frame.isEnabled():
                self.main_window.operate_resident_param_frame.setEnabled(False)
            # Disable all the buttons (character parameters editor -> operate_character_XXX_m)
            if self.main_window.operate_character_xyz_m_frame.isEnabled():
                self.main_window.operate_character_xyz_m_frame.setEnabled(False)
            # Disable all the buttons (character parameters editor -> cs_chip)
            if not self.main_window.cs_chip.isEnabled():
                self.main_window.cs_chip.setEnabled(True)

        # Generic pak file
        else:

            # Open the tab (pak explorer)
            if self.main_window.tabWidget.currentIndex() != 1:
                self.main_window.tabWidget.setCurrentIndex(1)

            # Disable completely the tab character parameters editor
            if self.main_window.character_parameters_editor.isEnabled():
                self.main_window.character_parameters_editor.setEnabled(False)

            self.progressText.emit("Unpacked")
            show_progress_value(self, step_progress)

        # Finish the thread
        self.finished.emit()

    def save_operate_character_and_pack(self):

        # 2 main tasks
        step_progress = self.end_progress / 2

        # Save all the info
        print("Writing values in the file...")
        write_single_character_parameters(self, self.main_window, step_progress)

        # Pack the files
        self.step_progress_pack = step_progress
        self.pack_and_save_file()

        # Finish the thread
        self.finished.emit()

    def save_cs_chip_and_pack(self):

        # 2 main tasks
        step_progress = self.end_progress / 2

        # Save all the info
        print("Writing values in the file...")
        write_cs_chip_file(self, step_progress)

        # Pack the files
        self.step_progress_pack = step_progress
        self.pack_and_save_file()

        # Finish the thread
        self.finished.emit()

    def save_operate_resident_param_db_font_pad_ps3_and_pack(self):

        # Values for the progress bar
        # 2 main tasks
        step_progress = self.end_progress / 2
        sub_step_progress = step_progress / len(GPV.character_list_edited)
        self.progressText.emit("Writting character...")

        # --- operate_resident_param ---
        if GPV.operate_resident_param_file:
            # Open the files
            subpak_file_character_inf = open(GPV.resident_character_inf_path, mode="rb+")
            subpak_file_transformer_i = open(GPV.resident_transformer_i_path, mode="rb+")
            subpak_file_skill = open(GPV.resident_skill_path, mode="rb+")
            subpak_file_skill.seek(4)

            print("Writing values in the file...")
            # Change the transformations in the file
            for character in GPV.character_list_edited:
                # Report progress
                show_progress_value(self, sub_step_progress)

                # Save all the info for each character
                write_operate_resident_param(character, subpak_file_character_inf,
                                             subpak_file_transformer_i, subpak_file_skill)

            # Close the files
            subpak_file_character_inf.close()
            subpak_file_transformer_i.close()
            subpak_file_skill.close()

        # --- db_font_pad_ps3 ---
        else:

            # Open the files
            subpak_file_resident_character_param = open(GPV.game_resident_character_param,
                                                        mode="rb+")
            print("Writing values in the file...")
            # Change the values in the file
            for character in GPV.character_list_edited:
                # Report progress
                show_progress_value(self, sub_step_progress)

                # Save all the info for each character
                write_db_font_pad_ps3(character, subpak_file_resident_character_param)

            # Close the files
            subpak_file_resident_character_param.close()

        # Pack the files
        self.step_progress_pack = step_progress
        self.pack_and_save_file()

        # Finish the thread
        self.finished.emit()

    def pack_and_save_file(self):

        # 2 is because the number of tasks (pack and compressing)
        sub_step_progress = self.step_progress_pack / 2

        # Due to we have issues with the permissions in the SPTK file from  drb_compressor, we move the pak file
        # to the folder 'old_pak', so we can create a new packed file
        old_pak_folder = ""
        if PEV.stpz_file:
            old_pak_folder = os.path.join(PEV.temp_folder, "old_pak")
            if not os.path.exists(old_pak_folder):
                os.mkdir(old_pak_folder)
            move(PEV.pak_file_path, os.path.join(old_pak_folder, os.path.basename(PEV.pak_file_path)))

        # Path where the folder with files are located
        folder_input = os.path.join(PEV.temp_folder, os.path.basename(PEV.pak_file_path).split(".")[0])

        # Get the list of files inside the folder unpacked in order to pak the folder
        filenames = natsorted(os.listdir(folder_input), key=lambda y: y.lower())
        num_filenames = len(filenames)
        num_pak_files = int(filenames[-1].split(";")[0]) + 1
        path_output_file = folder_input + ".pak"
        self.progressText.emit("Packing file...")
        pack(folder_input, path_output_file, filenames, num_filenames, num_pak_files, self.separator_size, self.separator)
        show_progress_value(self, sub_step_progress)

        # Generate the final file for the game
        self.progressText.emit("Compressing file...")
        args = os.path.join(PEV.dbrb_compressor_path) + " \"" + path_output_file + "\" \"" + self.path_output_file + "\""
        os.system('cmd /c ' + args)
        show_progress_value(self, sub_step_progress)
        # Disable read only
        os.chmod(self.path_output_file, stat.S_IWRITE)

        # Remove the 'old_pak' folder
        if PEV.stpz_file:
            rmtree(old_pak_folder, onerror=functions.del_rw)

        # Finish the thread
        self.finished.emit()


def initialize_pe(main_window):

    # Prepare the list view 2 in order to add the names
    model = QStandardItemModel()
    main_window.listView_2.setModel(model)

    # Open temp folder button
    main_window.openTempFolderButton.clicked.connect(action_open_temp_folder_button_logic)

    # Export all button
    main_window.exportAllButton_2.clicked.connect(lambda: action_export_all_2_logic(main_window))

    # Export button
    main_window.exportButton_2.clicked.connect(lambda: action_export_2_logic(main_window))

    # Import button
    main_window.importButton_2.clicked.connect(lambda: action_import_2_logic(main_window))

    # Disable pak explorer tab
    main_window.pak_explorer.setEnabled(False)


def unpack(path_file, extension, main_temp_folder, list_view_2):
    # Open the file
    with open(path_file, mode="rb") as file:

        # Read the first four bytes
        data = file.read(4)

        # If data is STPK, means is a pak file that has inside multiple paks files
        if data == b'STPK':

            # Create a folder with the name of the file that is already opened (main pak)
            # If is the main pak of all paks, it will create the folder in the temp folder
            if not main_temp_folder:
                path_file_without_basename = os.path.dirname(path_file)
            else:
                path_file_without_basename = main_temp_folder
            folder_name = os.path.basename(path_file).split(".")[0]
            folder_path = os.path.join(path_file_without_basename, folder_name)
            if os.path.exists(folder_path):
                rmtree(folder_path, onerror=functions.del_rw)
            os.mkdir(folder_path)

            # Get the number of subpak files that has the main pak file
            file.seek(4, 1)
            num_files = int.from_bytes(file.read(4), byteorder="big")
            file.seek(4, 1)

            # Write each subpak file
            for i in range(0, num_files):

                # Get the properties of the subpak file thas is inside the main pak file
                offset = int.from_bytes(file.read(4), byteorder="big")
                size = int.from_bytes(file.read(4), byteorder="big")
                file.seek(8, 1)
                name = file.read(32).decode("utf-8").replace("\00", "")
                name_splitted = name.split(".")
                name = name_splitted[0] + ".pak"
                new_file_path = os.path.join(folder_path, str(i) + ";" + name)
                # There are some files that doesn't have extension, so we add an empty value
                if len(name_splitted) == 1:
                    name_splitted.append("")

                # Store the offset from the main pak file
                offset_aux = file.tell()

                # Write the subpak file
                file.seek(offset)
                data = file.read(size)
                with open(new_file_path, mode="wb") as output_file:
                    output_file.write(data)

                # Prepare the pointer of the main pak file for the next subpak file
                file.seek(offset_aux)

                # Call the function again
                unpack(new_file_path, name_splitted[1], "", list_view_2)

        # means the pak file doesn't have subpak.
        else:

            # Change the extension to his original one
            file.close()
            dir_name = os.path.dirname(path_file)
            base_name = os.path.basename(path_file)
            new_file_path = os.path.join(dir_name, base_name.split(".")[0] + "." + extension)
            os.rename(path_file, new_file_path)

            # Add to the listView_2, each time. If is None, we won't add anything. We just only unpack the packed file
            if list_view_2 is not None:
                item = QStandardItem(new_file_path)
                item.setData(os.path.basename(new_file_path).split(";")[1])
                item.setEditable(False)
                list_view_2.model().appendRow(item)

            # Check if we find a folder that is the signature one in order to store the index of the listView
            dir_name_splited = dir_name.split(";")
            if IPV.signature_folder_index_list_view is None and len(dir_name_splited) > 1 and \
                    re.search(IPV.skill_chara_XXX_m_regex, dir_name_splited[1]):
                IPV.signature_folder_index_list_view = PEV.number_files

            # Increment the number of total files inside the pak file
            PEV.number_files += 1


def pack(path_folder, path_output_file, filenames, num_filenames, num_pak_files, separator_size, separator):
    # Create the headers and data vars
    header_0 = b'STPK' + bytes.fromhex("00 00 00 01") + num_pak_files.to_bytes(4, 'big') + bytes.fromhex("00 00 00 10")
    header = b''
    data = b''

    # Store the sizes
    acumulated_sizes = 0
    size_total_block_header_subpak = num_pak_files * 48
    stpk_header_size = 16

    # Final pak file
    pak_file = b''

    # Store all the data from a folder
    for i in range(0, num_filenames):

        filename = filenames[i]
        sub_folder_path = os.path.join(path_folder, filename)

        # We step in the first folder we find
        if os.path.isdir(sub_folder_path):

            # Get all the files inside the folder, with the number of files
            sub_filenames = natsorted(os.listdir(sub_folder_path), key=lambda y: y.lower())
            num_sub_filenames = len(sub_filenames)
            num_subpak_files = int(sub_filenames[-1].split(";")[0]) + 1
            sub_path_output_file = sub_folder_path + ".pak"

            pack(sub_folder_path, sub_path_output_file, sub_filenames, num_sub_filenames, num_subpak_files, separator_size, separator)

        else:
            with open(os.path.join(path_folder, filename), mode="rb") as file_pointer:

                # Get the original data and size
                data_aux = file_pointer.read()
                size_o = len(data_aux)

                # Number of bytes in order to complete a 16 bytes line
                result = size_o % 16
                if result != 0:
                    num_bytes_mod_16 = 16 - result
                else:
                    num_bytes_mod_16 = result

                # Add the '00' to the end of data in order to append the full data to the pack file.
                # Also, change the size
                for j in range(0, num_bytes_mod_16):
                    data_aux = data_aux + bytes.fromhex("00")
                size = size_o + num_bytes_mod_16

            # Calculate offset fot the subpak (the last var is because of the separator)
            offset = stpk_header_size + size_total_block_header_subpak + acumulated_sizes + separator_size

            # Increase the size for the next offset
            acumulated_sizes = acumulated_sizes + size

            # Number of bytes in order to complete a 32 bytes line for the name
            filename = filename.split(";")[1].encode('utf-8')
            extra_bytes = 32 - len(filename)
            if extra_bytes >= 0:
                for j in range(0, extra_bytes):
                    filename = filename + bytes.fromhex("00")
            else:
                filename = filename[:extra_bytes]

            header = header + offset.to_bytes(4, "big") + size_o.to_bytes(4, "big") + bytes.fromhex(
                "00 00 00 00 00 00 00 00") + filename
            data = data + data_aux

    # Add the last 112 bytes due to is the end of the file (maybe it's not necessary)
    for i in range(0, 112):
        data = data + bytes.fromhex("00")

    # Create the pak file
    pak_file = header_0 + header + separator + pak_file + data

    # Write the new pak file in the folder
    with open(path_output_file, mode="wb") as output_file:
        output_file.write(pak_file)
