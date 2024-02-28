from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QListView, QComboBox, QMainWindow, QWidget

from lib.character_parameters_editor.IPV import IPV
from lib.character_parameters_editor.REF import read_cs_chip_file, write_cs_chip_file
from lib.character_parameters_editor.IPF import read_single_character_parameters, write_single_character_parameters
from lib.character_parameters_editor.GPF import read_operate_resident_param, read_db_font_pad_ps3, write_db_font_pad_ps3, write_operate_resident_param, read_cs_main, write_cs_main
from lib.character_parameters_editor.GPV import GPV
from lib.character_parameters_editor.REV import REV
from lib.character_parameters_editor.classes.Animation import Animation
from lib.character_parameters_editor.classes.Blast import Blast
from lib.character_parameters_editor.classes.CameraCutscene import CameraCutscene
from lib.character_parameters_editor.classes.CharacterInfo import CharacterInfo
from lib.character_parameters_editor.classes.Slot import Slot
from lib.functions import show_progress_value, del_rw, create_stpk_properties
from lib.packages import rmtree, re, natsorted, os, stat, QLabel, QStandardItemModel
from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.classes.Character import Character
from lib.pak_explorer.PEV import PEV
from lib.pak_explorer.functions.action_logic import action_open_temp_folder_button_logic, action_export_all_2_logic, action_export_2_logic, action_import_2_logic


# Step 1: Create a worker class
class WorkerPef(QObject):

    # Pak explorer signals
    assign_first_entry_file_signal = pyqtSignal(QListView)
    enable_pack_explorer_assign_title_signal = pyqtSignal(QWidget, QLabel)
    enable_pak_explorer_tab_signal = pyqtSignal(QMainWindow)

    # General parameters signals
    initialize_character_slot_changer_signal = pyqtSignal(QMainWindow)
    initialize_buttons_events_operate_GP_signal = pyqtSignal(QMainWindow, Character)
    enable_tabs_operate_GP_signal = pyqtSignal(QMainWindow)
    initialize_buttons_events_db_font_GP_signal = pyqtSignal(QMainWindow)
    enable_tabs_db_font_GP_signal = pyqtSignal(QMainWindow)
    initialize_buttons_events_cs_main_GP_signal = pyqtSignal(QMainWindow)
    enable_tabs_cs_main_GP_signal = pyqtSignal(QMainWindow)

    # Individual parameters signals
    add_array_of_animation_signal = pyqtSignal(QComboBox, str, list)
    set_first_index_animation_type_value_signal = pyqtSignal(QComboBox)
    read_transformation_effect_signal = pyqtSignal(QComboBox, Animation)
    change_animation_bones_signal = pyqtSignal(QMainWindow, list)
    set_character_info_signal = pyqtSignal(QMainWindow, CharacterInfo)
    set_camera_type_signal = pyqtSignal(QComboBox, int, CameraCutscene)
    show_first_item_camera_signal = pyqtSignal(QMainWindow)
    set_blast_combo_box_signal = pyqtSignal(QComboBox, int, Blast)
    show_first_item_blast_signal = pyqtSignal(QMainWindow)
    enable_individual_parameters_tab_signal = pyqtSignal(QMainWindow)

    # Roster editor signals
    initialize_current_character_image_RE_signal = pyqtSignal(QMainWindow)
    delete_image_slot_RE_signal = pyqtSignal(Slot)
    change_image_slot_RE_signal = pyqtSignal(Slot, str)
    enable_tabs_RE_signal = pyqtSignal(QMainWindow)

    finished = pyqtSignal()
    progressValue = pyqtSignal(float)
    progressText = pyqtSignal(str)

    main_window = None
    path_output_file = ""
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
        unpack(PEV.pak_file_path, os.path.basename(PEV.pak_file_path).split(".")[-1], PEV.temp_folder, self.main_window.listView_2, self)
        show_progress_value(self, step_progress)

        # Assign the first entry to the list view
        self.assign_first_entry_file_signal.emit(self.main_window.listView_2)

        # Enable the pak explorer and add the title
        self.enable_pack_explorer_assign_title_signal.emit(self.main_window.pak_explorer, self.main_window.fileNameText_2)

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
            GPV.db_font_pad_XYZ_s_d = False

            # Read all the data from the files'
            # character_info, transformer_i and skill.dat
            GPV.resident_character_inf_path = self.main_window.listView_2.model().item(3, 0).text()
            GPV.resident_transformer_i_path = self.main_window.listView_2.model().item(11, 0).text()
            GPV.resident_skill_path = self.main_window.listView_2.model().item(16, 0).text()
            GPV.move_list_blast_exp_table_path = self.main_window.listView_2.model().item(367, 0).text()
            subpak_file_character_inf = open(GPV.resident_character_inf_path, mode="rb")
            subpak_file_transformer_i = open(GPV.resident_transformer_i_path, mode="rb")
            subpak_file_skill = open(GPV.resident_skill_path, mode="rb")
            subpak_file_move_list_blast_table = open(GPV.move_list_blast_exp_table_path, mode="rb")
            # Moves to the position 4 in the skill file since there starts the information for the first character
            subpak_file_skill.seek(4)
            # Moves to the position 16 in the blast attack pause menu file since there starts the information for the first character
            subpak_file_move_list_blast_table.seek(16)

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
                read_operate_resident_param(character, subpak_file_character_inf, subpak_file_transformer_i, subpak_file_skill, subpak_file_move_list_blast_table)
                GPV.character_list.append(character)

            # Close the files
            subpak_file_character_inf.close()
            subpak_file_transformer_i.close()
            subpak_file_skill.close()
            subpak_file_move_list_blast_table.close()

            # Initialize main roster
            self.initialize_character_slot_changer_signal.emit(self.main_window)

            # Get the values for the fist character of the list
            character_zero = GPV.character_list[0]

            # Prepare all the buttons, values, events
            self.initialize_buttons_events_operate_GP_signal.emit(self.main_window, character_zero)

            # Enable the tab
            self.enable_tabs_operate_GP_signal.emit(self.main_window)

        # Check if the file is the db_font_pad_PS3_s.zpak or db_font_pad_X360_s.zpak
        elif data == CPEV.db_font_pad_PS3_s_d or data == CPEV.db_font_pad_X360_s_d:

            # reset the values
            GPV.character_list_edited.clear()
            GPV.character_list.clear()
            GPV.chara_selected = 0  # Index of the char selected in the program
            GPV.operate_resident_param_file = False
            GPV.db_font_pad_XYZ_s_d = True

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
            self.initialize_character_slot_changer_signal.emit(self.main_window)

            # Initialize buttons
            self.initialize_buttons_events_db_font_GP_signal.emit(self.main_window)

            # Enable/Disable tabs
            self.enable_tabs_db_font_GP_signal.emit(self.main_window)

        # Check if the file is the cs_main.zpak
        elif data == CPEV.cs_main:
            # reset the values
            GPV.character_list_edited.clear()
            GPV.character_list.clear()
            GPV.chara_selected = 0  # Index of the char selected in the program
            GPV.operate_resident_param_file = False
            GPV.db_font_pad_XYZ_s_d = False

            # Read all the data from the files
            GPV.cs_main_dat = self.main_window.listView_2.model().item(0, 0).text()
            subpak_file_cs_main_dat = open(GPV.cs_main_dat, mode="rb")

            # Read the data from the files and store the parameters
            sub_step_progress = step_progress / 100.0
            for i in range(0, 100):
                # Report progress
                self.progressText.emit("Reading character " + str(i))
                show_progress_value(self, sub_step_progress)

                # Create a Character object
                character = Character()

                # Store the positions where the information is located
                character.position_cs_main = i * GPV.sizeCharacterCsMainDat

                # Store the information in the object and append to a list
                read_cs_main(character, subpak_file_cs_main_dat)
                GPV.character_list.append(character)

            # Close the files
            subpak_file_cs_main_dat.close()

            # Initialize main roster
            self.initialize_character_slot_changer_signal.emit(self.main_window)

            # Initialize buttons
            self.initialize_buttons_events_cs_main_GP_signal.emit(self.main_window)

            # Enable/Disable tabs
            self.enable_tabs_cs_main_GP_signal.emit(self.main_window)

        # Check if the file is an operate_character_xyz_m type
        elif re.search(CPEV.operate_character_xyz_m_regex, data):

            # Save the id of the character to the character parameters editor tab
            CPEV.file_character_id = data.decode('utf-8').split("_")[2]

            # Read all the data from the files and store it in the global_character from IPV.
            read_single_character_parameters(self, step_progress, self.main_window)

            # Check how we enable the tab
            self.enable_individual_parameters_tab_signal.emit(self.main_window)

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
                REV.slots_edited.clear()
                self.initialize_current_character_image_RE_signal.emit(self.main_window)

                REV.slot_chara_selected = -1
                REV.slot_trans_selected = -1
                REV.selecting_character = True
            else:
                REV.roster_editor_first_activation = False

            # Read all the data from the files and store it in the global vars from REV.
            read_cs_chip_file(self, step_progress, self.main_window)

            # Enable/Disable tabs
            self.enable_tabs_RE_signal.emit(self.main_window)

        # Generic pak file
        else:

            # Open the tab (pak explorer)
            self.enable_pak_explorer_tab_signal.emit(self.main_window)

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

    def save_general_parameters_and_pack(self):

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
            subpak_file_move_list_blast_table = open(GPV.move_list_blast_exp_table_path, mode="rb+")

            print("Writing values in the file...")
            # Change the transformations in the file
            for character in GPV.character_list_edited:
                # Report progress
                show_progress_value(self, sub_step_progress)

                # Save all the info for each character
                write_operate_resident_param(character, subpak_file_character_inf, subpak_file_transformer_i, subpak_file_skill, subpak_file_move_list_blast_table)

            # Close the files
            subpak_file_character_inf.close()
            subpak_file_transformer_i.close()
            subpak_file_skill.close()
            subpak_file_move_list_blast_table.close()

        # --- db_font_pad_ps3 ---
        elif GPV.db_font_pad_XYZ_s_d:

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

        # --- cs_main ---
        else:
            # Open the files
            subpak_file_cs_main = open(GPV.cs_main_dat, mode="rb+")
            print("Writing values in the file...")
            # Change the values in the file
            for character in GPV.character_list_edited:
                # Report progress
                show_progress_value(self, sub_step_progress)

                # Save all the info for each character
                write_cs_main(character, subpak_file_cs_main)

            # Close the files
            subpak_file_cs_main.close()

        # Pack the files
        self.step_progress_pack = step_progress
        self.pack_and_save_file()

        # Finish the thread
        self.finished.emit()

    def pack_and_save_file(self):

        # 2 is because the number of tasks (pack and compressing)
        sub_step_progress = self.step_progress_pack / 2

        # Path where the folder with files are located
        folder_input = os.path.join(PEV.temp_folder, os.path.basename(PEV.pak_file_path).split(".")[0])

        # Get the list of files inside the folder unpacked in order to pak the folder
        filenames = natsorted(os.listdir(folder_input), key=lambda y: y.lower())
        num_filenames = len(filenames)
        num_pak_files = int(filenames[-1].split(";")[0]) + 1
        path_output_file = folder_input + ".pak"
        self.progressText.emit("Packing file...")
        pack(self.main_window, folder_input, path_output_file, filenames, num_filenames, num_pak_files)
        show_progress_value(self, sub_step_progress)

        # Generate the final file for the game
        # Check endianess
        compressing_endian_format = ""
        if PEV.endianess_structure_result[0] == PEV.endianess_structure[1]:
            compressing_endian_format = "-ut"
        self.progressText.emit("Compressing file...")
        args = os.path.join(PEV.dbrb_compressor_path) + " \"" + path_output_file + "\" \"" + self.path_output_file + "\" \"" + compressing_endian_format + "\""
        os.system('cmd /c ' + args)
        show_progress_value(self, sub_step_progress)
        # Disable read only
        os.chmod(self.path_output_file, stat.S_IWRITE)

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


def unpack(path_file, extension, main_temp_folder, list_view_2, worker_pef):
    # Open the file
    with open(path_file, mode="rb") as file:

        # Read the first four bytes
        data = file.read(4)

        # If data is STPK, means is a pak file that has inside multiple paks files
        if data == PEV.STPK:

            # Create a folder with the name of the file that is already opened (main pak)
            # If is the main pak of all paks, it will create the folder in the temp folder
            if not main_temp_folder:
                path_file_without_basename = os.path.dirname(path_file)
            else:
                path_file_without_basename = main_temp_folder
            folder_name = os.path.basename(path_file).split(".")[0]
            folder_path = os.path.join(path_file_without_basename, folder_name)
            if os.path.exists(folder_path):
                rmtree(folder_path, onerror=del_rw)
            os.mkdir(folder_path)

            # Get the number of subpak files that has the main pak file
            unk0x04 = file.read(4)
            num_files = int.from_bytes(file.read(4), byteorder="big")
            stpk_type = file.read(4)

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

                # --- CREATING DUMMY DATA ----
                if i+1 < num_files:
                    # Get dummy size
                    offset_dummy = file.tell()
                    file.seek(offset_aux)
                    offset = int.from_bytes(file.read(4), byteorder="big")
                    dummy_size = offset - offset_dummy

                    # Check number of bytes in order to complete a 16 bytes line. We're doing this since we don't really need all the dummy bytes in dummy file
                    result = offset_dummy % 16
                    if result != 0:
                        num_bytes_mod_16 = 16 - result
                    else:
                        num_bytes_mod_16 = result
                    dummy_size = dummy_size - num_bytes_mod_16

                    if dummy_size > 0:
                        dummy_file_path = os.path.join(folder_path, str(i) + ";" + name_splitted[0] + PEV.dummy_extension)
                        with open(dummy_file_path, mode="wb") as output_dummy_file:
                            output_dummy_file.write(PEV.DUMMY)
                            for _ in range(0, dummy_size):
                                output_dummy_file.write(b'\x00')

                # Prepare the pointer of the main pak file for the next subpak file
                file.seek(offset_aux)

                # Call the function again
                unpack(new_file_path, name_splitted[1], "", list_view_2, worker_pef)

            # --- CREATING TYPE PAK ----
            path_type_pak_file = os.path.join(path_file_without_basename, folder_name + PEV.type_extension)
            with open(path_type_pak_file, mode='wb') as output_type_pak_file:
                output_type_pak_file.write(PEV.TYPE)
                output_type_pak_file.write(unk0x04)
                output_type_pak_file.write(stpk_type)

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


def pack(main_window, path_folder, path_output_file, filenames, num_filenames, num_pak_files):

    # Create the headers and data vars
    unk0x04, stpk_type, separator_size, separator = create_stpk_properties(num_pak_files, path_folder)
    header_0 = b'STPK' + unk0x04 + num_pak_files.to_bytes(4, 'big') + stpk_type
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
            pack(main_window, sub_folder_path, sub_path_output_file, sub_filenames, num_sub_filenames, num_subpak_files)

        else:
            with open(os.path.join(path_folder, filename), mode="rb") as file_pointer:

                # Check if is a dummy or type file
                data_header = file_pointer.read(4)
                if data_header == PEV.DUMMY or data_header == PEV.TYPE:
                    continue
                file_pointer.seek(0)

                # Get the original data and size
                data_aux = file_pointer.read()
                size_o = file_pointer.tell()

                # Number of bytes in order to complete a 16 bytes line
                result = size_o % 16
                if result != 0:
                    num_bytes_mod_16 = 16 - result
                else:
                    num_bytes_mod_16 = result

                # Add the "00" to the end of data in order to append the full data to the pack file.
                # Also, change the size
                for j in range(0, num_bytes_mod_16):
                    data_aux = data_aux + bytes.fromhex("00")
                size = size_o + num_bytes_mod_16

                # --- READING DUMMY DATA ----
                dummy_path = os.path.join(path_folder, filename.split(".")[0] + PEV.dummy_extension)
                dummy_data = b''
                if os.path.exists(dummy_path):
                    with open(dummy_path, mode='rb') as dummy_input_file:
                        data_header = dummy_input_file.read(4)
                        if data_header == PEV.DUMMY:
                            dummy_data = dummy_input_file.read()
                            dummy_size = dummy_input_file.tell() - 4
                            size = size + dummy_size

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

            header = header + offset.to_bytes(4, "big") + size_o.to_bytes(4, "big") + bytes.fromhex("00 00 00 00 00 00 00 00") + filename
            data = data + data_aux + dummy_data

    # Create the pak file
    pak_file = header_0 + header + separator + pak_file + data

    # Write the new pak file in the folder
    with open(path_output_file, mode="wb") as output_file:
        output_file.write(pak_file)
