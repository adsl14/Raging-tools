from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QInputDialog

from lib.character_parameters_editor.GPF import initialize_roster
from lib.character_parameters_editor.IPV import IPV
from lib.character_parameters_editor.GPV import GPV
from lib.character_parameters_editor.REV import REV
from lib.character_parameters_editor.functions.GP.signal_methods import initialize_buttons_events_operate_GP, enable_tabs_operate_GP, enable_tabs_db_font_GP, initialize_buttons_events_db_font_GP
from lib.character_parameters_editor.functions.IP.auxiliary import change_animation_bones_section, read_transformation_effect
from lib.character_parameters_editor.functions.IP.signal_methods import add_array_of_animation, show_first_item_camera, set_blast_combo_box, show_first_item_blast, set_camera_type, \
    set_first_index_animation_type_value, set_character_info, enable_individual_parameters_tab
from lib.character_parameters_editor.functions.RE.signal_methods import initialize_current_character_image_RE, delete_image_slot_RE, change_image_slot_RE, enable_tabs_RE
from lib.design.Raging_Tools.Raging_Tools import *
from lib.design.material_children.material_children import Material_Child_Editor
from lib.design.progress_bar.progress_bar import Progress_Bar
from lib.design.select_chara.select_chara import Select_Chara
from lib.design.select_chara.select_chara_roster import Select_Chara_Roster
from lib.packages import os, rmtree, QFileDialog, QMessageBox, stat, shutil, datetime, natsorted
from lib.functions import del_rw, ask_pack_structure, read_spa_file, write_json_bone_file, read_json_bone_file, write_spa_file, show_progress_value
# vram explorer
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer import VEF

# pak explorer
from lib.pak_explorer import PEF
from lib.pak_explorer.PEV import PEV

# character parameters editor
from lib.character_parameters_editor import CPEF, GPF, IPF

from lib.pak_explorer.functions.signal_methods import assign_first_entry_file, enable_pack_explorer_assign_title, enable_pak_explorer_tab
from lib.vram_explorer.functions.signal_methods import prepare_buttons_combobox_vram_explorer


class WorkerMainWindow(QObject):

    finished = pyqtSignal()
    progressValue = pyqtSignal(float)
    progressText = pyqtSignal(str)
    path_file = ""
    path_output_file = ""
    extension_file = ""
    folder_path = ""
    folder_output_path = ""
    separator = b''
    separator_size = 0
    start_progress = 0.0
    end_progress = 0.0

    def convert_SPA_to_JSON(self):

        # 2 main tasks
        step_progress = self.end_progress / 2

        # Show text
        self.progressText.emit("Loading " + os.path.basename(self.path_file))

        # Convert spa and store it to memory
        spa_file = read_spa_file(self.path_file)

        # Show progress
        show_progress_value(self, step_progress)

        # Create the new output
        output_path = os.path.join(os.path.dirname(self.path_output_file), os.path.basename(self.path_file).split(".")[0] + "." + IPV.animation_bone_extension)

        # Show text
        self.progressText.emit("Writing " + os.path.basename(output_path))

        # Write the output
        write_json_bone_file(output_path, spa_file.spa_header, spa_file.bone_entries)

        # Show progress
        show_progress_value(self, step_progress)

        # Finish the thread
        self.finished.emit()

    def convert_JSON_to_SPA(self):

        # 2 main tasks
        step_progress = self.end_progress / 2

        # Show text
        self.progressText.emit("Loading " + os.path.basename(self.path_file))

        # Convert spa and store it to memory
        spa_file = read_json_bone_file(self.path_file)

        # Show progress
        show_progress_value(self, step_progress)

        # Create the new output
        output_path = os.path.join(os.path.dirname(self.path_output_file), os.path.basename(self.path_file).split(".")[0] + "." + IPV.animation_extension)

        # Show text
        self.progressText.emit("Writing " + os.path.basename(output_path))
        # Write the output
        data, _ = write_spa_file(spa_file)
        with open(output_path, mode="wb") as output_file:
            output_file.write(data)

        # Show progress
        show_progress_value(self, step_progress)

        # Finish the thread
        self.finished.emit()

    def convert_multiple_SPA_to_multiple_JSON(self):

        path_files = os.listdir(self.folder_path)
        total_files = len(path_files)
        sub_step_progress = self.end_progress / total_files
        self.end_progress = sub_step_progress
        for i in range(0, total_files):
            self.path_file = os.path.join(self.folder_path, path_files[i])
            self.path_output_file = os.path.join(self.folder_output_path, path_files[i])
            self.convert_SPA_to_JSON()

        self.finished.emit()

    def convert_multiple_JSON_to_multiple_SPA(self):

        path_files = os.listdir(self.folder_path)
        total_files = len(path_files)
        sub_step_progress = self.end_progress / total_files
        self.end_progress = sub_step_progress
        for i in range(0, total_files):
            self.path_file = os.path.join(self.folder_path, path_files[i])
            self.path_output_file = os.path.join(self.folder_output_path, path_files[i])
            self.convert_JSON_to_SPA()

        self.finished.emit()

    def single_unpack_file(self):

        # Only 1 task
        step_progress = self.end_progress

        # Show text
        self.progressText.emit("Unpacking file " + os.path.basename(self.path_file))

        PEF.unpack(self.path_file, "", self.path_output_file, None, None)

        show_progress_value(self, step_progress)

        self.finished.emit()

    def multiple_unpack_file(self):

        path_files = os.listdir(self.folder_path)
        total_files = len(path_files)
        sub_step_progress = self.end_progress / total_files
        self.end_progress = sub_step_progress
        for i in range(0, total_files):
            self.path_file = os.path.join(self.folder_path, path_files[i])
            self.path_output_file = os.path.join(self.folder_output_path, os.path.dirname(path_files[i]))
            self.single_unpack_file()

        self.finished.emit()

    def single_pack_file(self):

        # Only 1 task
        step_progress = self.end_progress

        # Show text
        self.progressText.emit("Packing folder " + os.path.basename(self.path_file))

        # Get the list of files inside the folder unpacked in order to pak the folder
        filenames = natsorted(os.listdir(self.path_file), key=lambda y: y.lower())
        num_filenames = len(filenames)
        num_pak_files = int(filenames[-1].split(";")[0]) + 1
        PEF.pack(self.path_file, self.path_output_file, filenames, num_filenames, num_pak_files, self.separator_size, self.separator)

        show_progress_value(self, step_progress)

        self.finished.emit()

    def multiple_pack_file(self):

        path_files = os.listdir(self.folder_path)
        total_files = len(path_files)
        sub_step_progress = self.end_progress / total_files
        self.end_progress = sub_step_progress
        for i in range(0, total_files):
            self.path_file = os.path.join(self.folder_path, path_files[i])
            self.path_output_file = os.path.join(self.folder_output_path, path_files[i] + ".pak")
            self.single_pack_file()

        self.finished.emit()

    def encrypt_decrypt_file(self):

        # Only 1 task
        step_progress = self.end_progress

        # Show text
        if self.extension_file == "zpak":
            message = "Decrypting"
        elif self.extension_file == "pak":
            message = "Encrypting"
        else:
            message = "Encrypting or Decrypting"
        self.progressText.emit(message + " " + os.path.basename(self.path_file))

        # Execute the script in a command line for the encrypted file
        args = os.path.join(PEV.dbrb_compressor_path) + " \"" + self.path_file + "\" \"" + self.path_output_file + "\""
        os.system('cmd /c ' + args)
        # Disable read only
        try:
            os.chmod(self.path_output_file, stat.S_IWRITE)
        except FileNotFoundError:
            pass

        show_progress_value(self, step_progress)

        self.finished.emit()

    def convert_multiple_encrypted_decrypted_files(self):

        path_files = os.listdir(self.folder_path)
        total_files = len(path_files)
        sub_step_progress = self.end_progress / total_files
        self.end_progress = sub_step_progress
        for i in range(0, total_files):
            self.path_file = os.path.join(self.folder_path, path_files[i])

            basename_splited = path_files[i].split(".")
            extension = ""
            if len(basename_splited) > 1:
                if basename_splited[1] == "zpak":
                    extension = "pak"
                else:
                    extension = "zpak"
                basename = basename_splited[0] + "." + extension
            else:
                basename = path_files[i]
            self.extension_file = extension
            self.path_output_file = os.path.join(self.folder_output_path, basename)

            self.encrypt_decrypt_file()

        self.finished.emit()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    # old path where the user loaded the previous file
    old_path_file = ""
    # QIcon instance
    ico_image = None
    # Extensions
    extension_zpak = "Zpack files (*.zpak)"
    extension_spr_vram = "Spr/Vram files (*._)"

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.thread = None
        self.worker = None
        self.setupUi(self)

        # Icon
        self.ico_image = QtGui.QIcon("lib/design/Raging_Tools/Raging_Tools.ico")

        # File tab
        self.actionOpen.triggered.connect(self.action_open_logic)
        self.actionSave.triggered.connect(self.action_save_logic)
        self.actionClose.triggered.connect(self.close)

        # Utilities tab
        # Converter
        self.actionto_JSON.triggered.connect(self.action_SPA_to_JSON_logic)
        self.actionto_SPA.triggered.connect(self.action_JSON_to_SPA_logic)
        self.actionto_multiple_JSON.triggered.connect(self.action_multiple_SPA_to_multiple_JSON_logic)
        self.actionto_multiple_SPA.triggered.connect(self.action_multiple_JSON_to_multiple_SPA_logic)
        # Packer
        self.actionSingle_pack.triggered.connect(self.action_single_pack_logic)
        self.actionAll_pack.triggered.connect(self.action_multiple_pack_logic)
        self.actionSingle_unpack.triggered.connect(self.action_single_unpack_logic)
        self.actionAll_unpack.triggered.connect(self.action_multiple_unpack_logic)
        # Compressor
        self.actionSingle_encrypt_decrypt.triggered.connect(self.action_single_encrypt_decrypt_logic)
        self.actionAll_encrypt_decrypt.triggered.connect(self.action_multiple_encrypt_decrypt_logic)

        # About tab
        self.actionAuthor.triggered.connect(self.action_author_logic)
        self.actionCredits.triggered.connect(self.action_credits_logic)

        # Generate external windows
        # Select Chara window
        self.selectCharaWindow = QtWidgets.QDialog()
        self.selectCharaUI = Select_Chara()
        self.selectCharaUI.setupUi(self.selectCharaWindow)
        # Select Chara partner window
        self.selectCharaPartnerWindow = QtWidgets.QDialog()
        self.selectCharaPartnerUI = Select_Chara()
        self.selectCharaPartnerUI.setupUi(self.selectCharaPartnerWindow)
        # Select Chara roster window
        self.selectCharaRosterWindow = QtWidgets.QDialog()
        self.selectCharaRosterUI = Select_Chara_Roster()
        self.selectCharaRosterUI.setupUi(self.selectCharaRosterWindow)
        # Material windows
        self.MaterialChildEditorWindow = QtWidgets.QDialog()
        self.MaterialChildEditorUI = Material_Child_Editor()
        self.MaterialChildEditorUI.setupUi(self.MaterialChildEditorWindow)
        # Progress bar
        self.progressBarWindow = QtWidgets.QDialog()
        self.progressBarUI = Progress_Bar()
        self.progressBarUI.setupUi(self.progressBarWindow)

        # --- vram explorer ---
        VEF.initialize_ve(self)

        # --- pak explorer ---
        PEF.initialize_pe(self)

        # --- character parameters editor ---
        CPEF.initialize_cpe(self)

    def report_progress_value(self, n):
        self.progressBarUI.progressBar.setValue(int(n * 100))
        self.progressBarUI.progressBar.setFormat("%.02f %%" % n)

    def report_progress_text(self, t):
        self.progressBarUI.label.setText(t)

    def reset_progress_bar(self):
        self.thread.finished.connect(lambda: self.report_progress_value(0.0))
        self.thread.finished.connect(lambda: self.report_progress_text(""))
        self.thread.finished.connect(lambda: self.progressBarWindow.close())

    def run_load_data_to_ve(self):

        # Create a QThread object
        self.thread = QThread()
        # Create a worker object
        self.worker = VEF.WorkerVef()
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Create vars
        self.worker.start_progress = 0.0
        self.worker.end_progress = 100.0
        self.worker.main_window = self
        # Connect signals and slots
        # Vram explorer
        self.worker.prepare_buttons_combobox_vram_explorer_signal.connect(prepare_buttons_combobox_vram_explorer)

        # Progress bar
        self.worker.progressValue.connect(self.report_progress_value)
        self.worker.progressText.connect(self.report_progress_text)

        # Main method
        self.thread.started.connect(self.worker.load_spr_vram_file)

        # Finish thread
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: VEF.listen_events_logic(self, True))
        self.reset_progress_bar()

        # Starts thread
        VEF.listen_events_logic(self, False)
        self.progressBarWindow.show()
        self.thread.start()

    def run_save_ve_to_data(self, vram_separator, path_output_file):

        # Create a QThread object
        self.thread = QThread()
        # Create a worker object
        self.worker = VEF.WorkerVef()
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Create vars
        self.worker.main_window = self
        self.worker.vram_separator = vram_separator
        self.worker.path_output_file = path_output_file
        self.worker.start_progress = 0.0
        self.worker.end_progress = 100.0
        # Connect signals and slots
        self.worker.progressValue.connect(self.report_progress_value)
        self.worker.progressText.connect(self.report_progress_text)

        self.thread.started.connect(self.worker.save_spr_vram_file)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.reset_progress_bar()

        # Starts thread
        self.progressBarWindow.show()
        self.thread.start()

    def run_load_data_to_pe_cpe(self):

        # Create a QThread object
        self.thread = QThread()
        # Create a worker object
        self.worker = PEF.WorkerPef()
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Create vars
        self.worker.main_window = self
        self.worker.start_progress = 0.0
        self.worker.end_progress = 100.0
        # Connect signals and slots

        # Pak explorer signals
        self.worker.assign_first_entry_file_signal.connect(assign_first_entry_file)
        self.worker.enable_pack_explorer_assign_title_signal.connect(enable_pack_explorer_assign_title)
        self.worker.enable_pak_explorer_tab_signal.connect(enable_pak_explorer_tab)

        # General parameters signals
        self.worker.initialize_roster_signal.connect(initialize_roster)
        self.worker.initialize_buttons_events_operate_GP_signal.connect(initialize_buttons_events_operate_GP)
        self.worker.enable_tabs_operate_GP_signal.connect(enable_tabs_operate_GP)
        self.worker.initialize_buttons_events_db_font_GP_signal.connect(initialize_buttons_events_db_font_GP)
        self.worker.enable_tabs_db_font_GP_signal.connect(enable_tabs_db_font_GP)

        # Individual parameters signals
        self.worker.add_array_of_animation_signal.connect(add_array_of_animation)
        self.worker.read_transformation_effect_signal.connect(read_transformation_effect)
        self.worker.set_first_index_animation_type_value_signal.connect(set_first_index_animation_type_value)
        self.worker.change_animation_bones_signal.connect(change_animation_bones_section)
        self.worker.set_character_info_signal.connect(set_character_info)
        self.worker.set_camera_type_signal.connect(set_camera_type)
        self.worker.show_first_item_camera_signal.connect(show_first_item_camera)
        self.worker.set_blast_combo_box_signal.connect(set_blast_combo_box)
        self.worker.show_first_item_blast_signal.connect(show_first_item_blast)
        self.worker.enable_individual_parameters_tab_signal.connect(enable_individual_parameters_tab)

        # Roster signals
        self.worker.initialize_current_character_image_RE_signal.connect(initialize_current_character_image_RE)
        self.worker.delete_image_slot_RE_signal.connect(delete_image_slot_RE)
        self.worker.change_image_slot_RE_signal.connect(change_image_slot_RE)
        self.worker.enable_tabs_RE_signal.connect(enable_tabs_RE)

        # Progress bar signals
        self.worker.progressValue.connect(self.report_progress_value)
        self.worker.progressText.connect(self.report_progress_text)

        # Main method
        self.thread.started.connect(self.worker.load_data_to_pe_cpe)

        # End signals
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: GPF.listen_events_logic(self, True))
        self.thread.finished.connect(lambda: IPF.listen_events_logic(self, True))
        self.reset_progress_bar()

        # Starts thread
        GPF.listen_events_logic(self, False)
        IPF.listen_events_logic(self, False)
        self.progressBarWindow.show()
        self.thread.start()

    def run_save_operate_character_and_pack(self, path_output_file, separator, separator_size):

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = PEF.WorkerPef()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.worker.main_window = self
        self.worker.path_output_file = path_output_file
        self.worker.separator = separator
        self.worker.separator_size = separator_size
        self.worker.start_progress = 0.0
        self.worker.end_progress = 100.0
        self.thread.started.connect(self.worker.save_operate_character_and_pack)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progressValue.connect(self.report_progress_value)
        self.worker.progressText.connect(self.report_progress_text)
        # Step 6: Start the thread
        self.progressBarWindow.show()
        self.thread.start()

        # Reset progressbar
        self.reset_progress_bar()

    def run_save_cs_chip_and_pack(self, path_output_file, separator, separator_size):

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = PEF.WorkerPef()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.worker.main_window = self
        self.worker.path_output_file = path_output_file
        self.worker.separator = separator
        self.worker.separator_size = separator_size
        self.worker.start_progress = 0.0
        self.worker.end_progress = 100.0
        self.thread.started.connect(self.worker.save_cs_chip_and_pack)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progressValue.connect(self.report_progress_value)
        self.worker.progressText.connect(self.report_progress_text)
        # Step 6: Start the thread
        self.progressBarWindow.show()
        self.thread.start()

        # Reset progressbar
        self.reset_progress_bar()

    def run_save_operate_resident_param_db_font_pad_ps3_and_pack(self, path_output_file, separator, separator_size):

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = PEF.WorkerPef()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.worker.path_output_file = path_output_file
        self.worker.separator = separator
        self.worker.separator_size = separator_size
        self.worker.start_progress = 0.0
        self.worker.end_progress = 100.0
        self.thread.started.connect(self.worker.save_operate_resident_param_db_font_pad_ps3_and_pack)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progressValue.connect(self.report_progress_value)
        self.worker.progressText.connect(self.report_progress_text)
        # Step 6: Start the thread
        self.progressBarWindow.show()
        self.thread.start()

        # Reset progressbar
        self.reset_progress_bar()

    def run_save_pe_to_data(self, path_output_file, separator, separator_size):

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = PEF.WorkerPef()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.worker.path_output_file = path_output_file
        self.worker.separator = separator
        self.worker.separator_size = separator_size
        self.worker.start_progress = 0.0
        self.worker.step_progress_pack = 100.0
        self.thread.started.connect(self.worker.pack_and_save_file)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progressValue.connect(self.report_progress_value)
        self.worker.progressText.connect(self.report_progress_text)
        # Step 6: Start the thread
        self.progressBarWindow.show()
        self.thread.start()

        # Reset progressbar
        self.reset_progress_bar()

    def action_open_logic(self):

        # Open the file
        path_file = QFileDialog.getOpenFileName(self,
                                                "Open file", MainWindow.old_path_file,
                                                "Supported files "
                                                "(*.pak *.zpak *.spr *.vram)"
                                                ";;Packed files "
                                                "(*.pak *.zpak)"
                                                ";;Info files (*.spr)"
                                                ";;Texture files "
                                                "(*.vram)")[0]
        # Check if the user has selected a file
        if os.path.exists(path_file):

            # Save the path_file to our aux var old_path_file
            MainWindow.old_path_file = path_file

            # Get the header of the file
            with open(path_file, mode="rb") as input_file:
                header_type = input_file.read(4)

            # Check what type of file we're loading (STPZ, STPK, SPR, SPRP)
            # compressed pak file
            if header_type == b'STPZ':

                # Create a folder where we store the necessary files (always for pak explorer). If already exists,
                # we remove every file's in it
                if os.path.exists(PEV.temp_folder):
                    rmtree(PEV.temp_folder, onerror=del_rw)
                os.mkdir(PEV.temp_folder)

                # Store the path of the pak file
                PEV.pak_file_path_original = path_file

                basename = os.path.basename(PEV.pak_file_path_original)
                extension = basename.split(".")[-1]

                # Execute the script in a command line for the pak file
                PEV.pak_file_path = os.path.join(os.path.abspath(os.getcwd()), PEV.temp_folder,
                                                 basename.replace("." + extension, "_d.pak"))
                args = os.path.join(PEV.dbrb_compressor_path) + " \"" + PEV.pak_file_path_original + "\" \"" + \
                    PEV.pak_file_path + "\""
                os.system('cmd /c ' + args)
                # Disable read only
                os.chmod(PEV.pak_file_path, stat.S_IWRITE)

                PEV.stpz_file = True
                PEV.stpk_file = False

                # Reset the flag
                PEV.spr_type_pak = True

                # Load all the data from pak file to pak_explorer/character_parameters_editor
                self.run_load_data_to_pe_cpe()

            # uncompressed pak file
            elif header_type == b'STPK':

                # Create a folder where we store the necessary files (always for pak explorer). If already exists,
                # we remove every file's in it
                if os.path.exists(PEV.temp_folder):
                    rmtree(PEV.temp_folder, onerror=del_rw)
                os.mkdir(PEV.temp_folder)

                # Store the paths of the pak file
                PEV.pak_file_path_original = path_file
                PEV.pak_file_path = PEV.pak_file_path_original

                PEV.stpz_file = False
                PEV.stpk_file = True

                # Reset the flag
                PEV.spr_type_pak = True

                # Load all the data from pak file to pak_explorer/character_parameters_editor
                self.run_load_data_to_pe_cpe()

            # spr file
            elif header_type == b'SPRP' or header_type == b'SPR3' or header_type == b'SPR\x00':

                # Open vram file
                path_file_2 = QFileDialog.getOpenFileName(self, "Open file", path_file,
                                                          "Texture files (*.vram)")[0]

                if os.path.exists(path_file_2):
                    # Get the header of the new file
                    with open(path_file_2, mode="rb") as input_file:
                        header_type_2 = input_file.read(4)

                    # Check if the type of file is vram
                    if header_type_2 == b'STPZ' or header_type_2 == b'STPK' or header_type_2 == b'SPRP' \
                            or header_type_2 == b'SPR3' or header_type_2 == b'SPR\x00':
                        # Wrong vram file
                        msg = QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setWindowIcon(self.ico_image)
                        msg.setText("Invalid vram file.")
                        msg.exec()
                        return

                    else:
                        # Store spr and vram paths
                        VEV.spr_file_path = path_file
                        VEV.vram_file_path = path_file_2
                        # Store spr header
                        VEV.header_type_spr_file = header_type
                else:
                    # Wrong vram file
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setWindowIcon(self.ico_image)
                    msg.setText("A vram file is needed.")
                    msg.exec()
                    return

                # Load all the data to the vram_explorer from the spr and vram files
                self.run_load_data_to_ve()

            # vram file
            else:

                # Open spr file
                path_file_2 = QFileDialog.getOpenFileName(self, "Open file", path_file,
                                                          "Info files (*.spr)")[0]

                if os.path.exists(path_file_2):

                    # Get the header of the new file
                    with open(path_file_2, mode="rb") as input_file:
                        header_type_2 = input_file.read(4)

                    # Check if the type of file is vram
                    if header_type_2 != b'SPRP' and header_type_2 != b'SPR3' and \
                            header_type_2 != b'SPR\x00':
                        # Wrong spr file
                        msg = QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setWindowIcon(self.ico_image)
                        msg.setText("Invalid spr file.")
                        msg.exec()
                        return

                    else:
                        # Store spr and vram paths
                        VEV.vram_file_path = path_file
                        VEV.spr_file_path = path_file_2
                        # Store spr header
                        VEV.header_type_spr_file = header_type_2
                else:
                    # Wrong spr file
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setWindowIcon(self.ico_image)
                    msg.setText("A spr file is needed.")
                    msg.exec()
                    return

                # Load all the data to the vram_explorer from the spr and vram files
                self.run_load_data_to_ve()

    def action_save_logic(self):

        # Ask the user where to save the file
        path_output_file = os.path.splitext(MainWindow.old_path_file)[0].split(".")[0]

        # If the current tab that the user is seeing is the vram explorer, when saving the default extension will be
        # the extension for spr/vram
        if self.tabWidget.currentIndex() == 0:
            initial_extension = self.extension_spr_vram
        # The current tab is pak explorer or character parameters editor
        else:
            initial_extension = self.extension_zpak
        path_output_file, extension = QFileDialog.getSaveFileName(self,
                                                                  "Save file", path_output_file,
                                                                  self.extension_zpak + ";;" +
                                                                  self.extension_spr_vram, initial_extension)

        # The user has selected a path
        if path_output_file:

            # Save spr_vram in a folder
            if extension == self.extension_spr_vram:

                if not VEV.sprp_file:
                    msg = QMessageBox()
                    msg.setWindowTitle("Warning")
                    msg.setWindowIcon(self.ico_image)
                    msg.setText("There is no file loaded.")
                    msg.exec()
                else:

                    # Ask the user the format for the vram file (only when is saving a vram and spr for PS3)
                    # If is for Xbox, by default we won't add any vram separator between textures. We're saving
                    # it with Raging Blast compatibility instead
                    if VEV.header_type_spr_file != b'SPR3':
                        vram_format = QInputDialog().getItem(self, "Vram format", VEV.message_vram_format,
                                                             VEV.vram_export_format, editable=False, current=1)
                    else:
                        vram_format = [VEV.vram_export_format[0], True]

                    # The user has selected something
                    if vram_format[1]:
                        vram_separator = True
                        # If the format is the Raging Blast 1, we won't add any separator between textures
                        if vram_format[0] == VEV.vram_export_format[0]:
                            vram_separator = False

                        # Create the folder where we save the modified files
                        if not os.path.exists(path_output_file):
                            os.mkdir(path_output_file)

                        # Save vram and spr file
                        self.run_save_ve_to_data(vram_separator, path_output_file)

            # Save pak file
            else:

                # Check if character parameters editor is enabled in order to save the parameters from that tab
                if self.character_parameters_editor.isEnabled():

                    # Ask the user if the tool saves also the modified values from character parameters editor
                    msg = QMessageBox()
                    msg.setWindowTitle("Message")
                    msg.setWindowIcon(self.ico_image)
                    message = "Do you wish to save also the modified values from 'character parameters editor' " \
                              "into the unpacked files?"
                    answer = msg.question(self, '', message, msg.Yes | msg.No | msg.Cancel)

                    # Check if the user has selected something
                    if answer:

                        # The user wants to save also the modified values from 'character parameters editor'
                        if answer == msg.Yes:

                            # --- operate_character_XXX_m ---
                            # Check what type of character parameter editor is activated
                            # The user has opened the operate_character tab
                            if self.operate_character_xyz_m_frame.isEnabled():

                                # Ask the user if it is packing a vram or ioram file for Xbox
                                separator, separator_size = ask_pack_structure(self)

                                # Save all the info
                                print("Writing values in the file...")
                                self.run_save_operate_character_and_pack(path_output_file, separator, separator_size)

                            # --- operate_resident_param --- or --- db_font_pad ---
                            # If the user has opened the operate resident or db_font_pad and edited one character, we will save the file
                            elif self.operate_resident_param_frame.isEnabled() and GPV.character_list_edited:

                                # Ask the user if it is packing a vram or ioram file for Xbox
                                separator, separator_size = ask_pack_structure(self)

                                # pack file
                                self.run_save_operate_resident_param_db_font_pad_ps3_and_pack(path_output_file, separator, separator_size)

                            # --- cs_chip ---
                            # If the user has opened the cs_chip tab and edited one character, we will save the file
                            elif self.cs_chip.isEnabled() and REV.slots_edited:

                                # Ask the user if it is packing a vram or ioram file for Xbox
                                separator, separator_size = ask_pack_structure(self)

                                # Save all the info
                                print("Writing values in the file...")
                                self.run_save_cs_chip_and_pack(path_output_file, separator, separator_size)

                            else:
                                msg = QMessageBox()
                                msg.setWindowTitle("Warning")
                                msg.setWindowIcon(self.ico_image)
                                msg.setText("The file hasn't been modified.")
                                msg.exec()

                        # The user wants to save the values only from the 'pak explorer'
                        elif answer == msg.No:
                            # Ask the user if it is packing a vram or ioram file for Xbox
                            separator, separator_size = ask_pack_structure(self)

                            # pack file
                            self.run_save_pe_to_data(path_output_file, separator, separator_size)

                # We save the data from the 'pak explorer' tab
                elif self.pak_explorer.isEnabled():
                    # Ask the user if it is packing a vram or ioram file for Xbox
                    separator, separator_size = ask_pack_structure(self)

                    # pack file
                    self.run_save_pe_to_data(path_output_file, separator, separator_size)
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Warning")
                    msg.setWindowIcon(self.ico_image)
                    msg.setText("No pak file has been loaded.")
                    msg.exec()

    def action_SPA_to_JSON_logic(self):

        # Open the file
        path_file = QFileDialog.getOpenFileName(self, "Open spa file", MainWindow.old_path_file, "Special animation file (*.spa)")[0]

        if os.path.exists(path_file):

            # Save the path_file to our aux var old_path_file
            MainWindow.old_path_file = path_file

            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = WorkerMainWindow()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.worker.path_file = path_file
            self.worker.path_output_file = path_file
            self.worker.start_progress = 0.0
            self.worker.end_progress = 100.0
            self.thread.started.connect(self.worker.convert_SPA_to_JSON)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progressValue.connect(self.report_progress_value)
            self.worker.progressText.connect(self.report_progress_text)
            # Step 6: Start the thread
            self.progressBarWindow.show()
            self.thread.start()

            # Reset progressbar
            self.reset_progress_bar()

    def action_JSON_to_SPA_logic(self):

        # Open the file
        path_file = QFileDialog.getOpenFileName(self, "Open json file", MainWindow.old_path_file, "Json file (*.json)")[0]

        if os.path.exists(path_file):

            # Save the path_file to our aux var old_path_file
            MainWindow.old_path_file = path_file

            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = WorkerMainWindow()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.worker.path_file = path_file
            self.worker.path_output_file = path_file
            self.worker.start_progress = 0.0
            self.worker.end_progress = 100.0
            self.thread.started.connect(self.worker.convert_JSON_to_SPA)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progressValue.connect(self.report_progress_value)
            self.worker.progressText.connect(self.report_progress_text)
            # Step 6: Start the thread
            self.progressBarWindow.show()
            self.thread.start()

            # Reset progressbar
            self.reset_progress_bar()

    def action_multiple_SPA_to_multiple_JSON_logic(self):

        # Ask the user from where to import the files into the tool
        folder_import_path = QFileDialog.getExistingDirectory(self, "Folder where spa files are located")

        if folder_import_path:

            # Create output folder
            folder_output_path = folder_import_path + "_" + IPV.animation_bone_extension
            # If exists, we remove everything inside and create the folder again
            if os.path.exists(folder_output_path):
                shutil.rmtree(folder_output_path)
            os.mkdir(folder_output_path)

            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = WorkerMainWindow()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.worker.folder_path = folder_import_path
            self.worker.folder_output_path = folder_output_path
            self.worker.start_progress = 0.0
            self.worker.end_progress = 100.0
            self.thread.started.connect(self.worker.convert_multiple_SPA_to_multiple_JSON)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progressValue.connect(self.report_progress_value)
            self.worker.progressText.connect(self.report_progress_text)
            # Step 6: Start the thread
            self.progressBarWindow.show()
            self.thread.start()

            # Reset progressbar
            self.reset_progress_bar()

    def action_multiple_JSON_to_multiple_SPA_logic(self):

        # Ask the user from where to import the files into the tool
        folder_import_path = QFileDialog.getExistingDirectory(self, "Folder where json files are located")

        if folder_import_path:

            # Create output folder
            folder_output_path = folder_import_path + "_" + IPV.animation_extension
            # If exists, we remove everything inside and create the folder again
            if os.path.exists(folder_output_path):
                shutil.rmtree(folder_output_path)
            os.mkdir(folder_output_path)
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = WorkerMainWindow()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.worker.folder_path = folder_import_path
            self.worker.folder_output_path = folder_output_path
            self.worker.start_progress = 0.0
            self.worker.end_progress = 100.0
            self.thread.started.connect(self.worker.convert_multiple_JSON_to_multiple_SPA)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progressValue.connect(self.report_progress_value)
            self.worker.progressText.connect(self.report_progress_text)
            # Step 6: Start the thread
            self.progressBarWindow.show()
            self.thread.start()

            # Reset progressbar
            self.reset_progress_bar()

    def action_single_unpack_logic(self):

        # Open the file
        path_file = QFileDialog.getOpenFileName(self,
                                                "Open packed file", MainWindow.old_path_file,
                                                "Packed file "
                                                "(*.pak)")[0]
        if os.path.exists(path_file):

            # Save the path_file to our aux var old_path_file
            MainWindow.old_path_file = path_file

            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = WorkerMainWindow()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.worker.path_file = path_file
            self.worker.path_output_file = os.path.dirname(path_file)
            self.worker.start_progress = 0.0
            self.worker.end_progress = 100.0
            self.thread.started.connect(self.worker.single_unpack_file)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progressValue.connect(self.report_progress_value)
            self.worker.progressText.connect(self.report_progress_text)
            # Step 6: Start the thread
            self.progressBarWindow.show()
            self.thread.start()

            # Reset progressbar
            self.reset_progress_bar()

    def action_multiple_unpack_logic(self):

        # Ask the user from where to import the files into the tool
        folder_import_path = QFileDialog.getExistingDirectory(self, "Folder where unpacked files are located")

        if folder_import_path:

            # Create output folder
            folder_output_path = folder_import_path + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S")
            # If exists, we remove everything inside and create the folder again
            if os.path.exists(folder_output_path):
                shutil.rmtree(folder_output_path)
            os.mkdir(folder_output_path)

            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = WorkerMainWindow()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.worker.folder_path = folder_import_path
            self.worker.folder_output_path = folder_output_path
            self.worker.start_progress = 0.0
            self.worker.end_progress = 100.0
            self.thread.started.connect(self.worker.multiple_unpack_file)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progressValue.connect(self.report_progress_value)
            self.worker.progressText.connect(self.report_progress_text)
            # Step 6: Start the thread
            self.progressBarWindow.show()
            self.thread.start()

            # Reset progressbar
            self.reset_progress_bar()

    def action_single_pack_logic(self):

        # Ask the user from where to import the files into the tool
        folder_import_path = QFileDialog.getExistingDirectory(self, "Folder where files are located")

        if folder_import_path:
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = WorkerMainWindow()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.worker.path_file = folder_import_path
            self.worker.path_output_file = folder_import_path + ".pak"
            # Ask the user if it is packing a vram or ioram file for Xbox
            self.worker.separator, self.worker.separator_size = ask_pack_structure(self)
            self.worker.start_progress = 0.0
            self.worker.end_progress = 100.0
            self.thread.started.connect(self.worker.single_pack_file)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progressValue.connect(self.report_progress_value)
            self.worker.progressText.connect(self.report_progress_text)
            # Step 6: Start the thread
            self.progressBarWindow.show()
            self.thread.start()

            # Reset progressbar
            self.reset_progress_bar()

    def action_multiple_pack_logic(self):

        # Ask the user from where to import the files into the tool
        folder_import_path = QFileDialog.getExistingDirectory(self, "Folder where there are folders with files are located")

        if folder_import_path:

            # Ask the user if it is packing a vram or ioram file for Xbox
            self.worker.separator, self.worker.separator_size = ask_pack_structure(self)

            # Create output folder
            folder_output_path = folder_import_path + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S")
            # If exists, we remove everything inside and create the folder again
            if os.path.exists(folder_output_path):
                shutil.rmtree(folder_output_path)
            os.mkdir(folder_output_path)

            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = WorkerMainWindow()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.worker.folder_path = folder_import_path
            self.worker.folder_output_path = folder_output_path
            self.worker.start_progress = 0.0
            self.worker.end_progress = 100.0
            self.thread.started.connect(self.worker.multiple_pack_file)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progressValue.connect(self.report_progress_value)
            self.worker.progressText.connect(self.report_progress_text)
            # Step 6: Start the thread
            self.progressBarWindow.show()
            self.thread.start()

            # Reset progressbar
            self.reset_progress_bar()

    def action_single_encrypt_decrypt_logic(self):

        # Open the file
        path_file = QFileDialog.getOpenFileName(self,
                                                "Open encrypted or decrypted file", MainWindow.old_path_file,
                                                "Encrypted or decrypted file "
                                                "(*.zpak *.pak)")[0]
        if os.path.exists(path_file):

            # Save the path_file to our aux var old_path_file
            MainWindow.old_path_file = path_file

            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = WorkerMainWindow()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.worker.path_file = path_file

            basename = os.path.basename(path_file)
            basename_splited = basename.split(".")
            extension = ""
            if len(basename_splited) > 1:
                if basename_splited[1] == "zpak":
                    extension = "pak"
                else:
                    extension = "zpak"
                basename = basename_splited[0] + "." + extension
            else:
                basename = basename + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S")
            self.worker.extension_file = extension
            self.worker.path_output_file = os.path.join(os.path.dirname(path_file), basename)

            self.worker.start_progress = 0.0
            self.worker.end_progress = 100.0
            self.thread.started.connect(self.worker.encrypt_decrypt_file)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progressValue.connect(self.report_progress_value)
            self.worker.progressText.connect(self.report_progress_text)
            # Step 6: Start the thread
            self.progressBarWindow.show()
            self.thread.start()

            # Reset progressbar
            self.reset_progress_bar()

    def action_multiple_encrypt_decrypt_logic(self):

        # Ask the user from where to import the files into the tool
        folder_import_path = QFileDialog.getExistingDirectory(self, "Folder where encrypted or decrypted files are located")

        if folder_import_path:

            # Create output folder
            folder_output_path = folder_import_path + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S")
            # If exists, we remove everything inside and create the folder again
            if os.path.exists(folder_output_path):
                shutil.rmtree(folder_output_path)
            os.mkdir(folder_output_path)

            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = WorkerMainWindow()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.worker.folder_path = folder_import_path
            self.worker.folder_output_path = folder_output_path
            self.worker.start_progress = 0.0
            self.worker.end_progress = 100.0
            self.thread.started.connect(self.worker.convert_multiple_encrypted_decrypted_files)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progressValue.connect(self.report_progress_value)
            self.worker.progressText.connect(self.report_progress_text)
            # Step 6: Start the thread
            self.progressBarWindow.show()
            self.thread.start()

            # Reset progressbar
            self.reset_progress_bar()

    def closeEvent(self, event):
        if os.path.exists(PEV.temp_folder):
            rmtree(PEV.temp_folder, onerror=del_rw)
        event.accept()

    def action_author_logic(self):
        msg = QMessageBox()
        msg.setTextFormat(1)
        msg.setWindowTitle("Author")
        msg.setWindowIcon(self.ico_image)
        msg.setText(
            "<ul>"
            "<li><b>Raging tools 1.8.3</b> by "
            "<a href=https://www.youtube.com/channel/UCkZajFypIgQL6mI6OZLEGXw>adsl14</a></li>"
            "<li>The tutorial of how to work with the tool or get the source code, can be found here: "
            "<a href=https://github.com/adsl14/Raging-tools>Raging tools GitHub page</a><li>"
            "</ul>")
        msg.exec()

    def action_credits_logic(self):
        msg = QMessageBox()
        msg.setTextFormat(1)
        msg.setWindowTitle("Credits")
        msg.setWindowIcon(self.ico_image)
        msg.setText('<ul>' 
                    '<li>To <b>revelation (revel8n)</b> from <a href=https://forum.xentax.com>XeNTaX</a>'
                    ' forum who made the compress/uncompress tool <i>d'
                    'brb_compressor.exe</i> and for his contributions.</li>'
                    '<li>To <b><a href=https://github.com/ascomods>Ascomods</a></b> for his contributions.</li>'
                    '<li>To <b><a href=https://www.youtube.com/c/HiroTenkaichi>HiroTex</a></b>'
                    ' for his contributions.</li>'
                    '<li>To <b><a href=https://www.youtube.com/c/SamuelDBZMAM>SamuelDoesStuff</a></b>'
                    ' for his contributions.</li>'
                    '<li>To <b>316austin316</b> for his contributions.</li>'
                    '<li>To <b><a href=https://twitter.com/SSJLVegeta>SSJLVegeta</a></b> for his contributions.</li>'
                    '<li>To <b><a href=https://www.youtube.com/channel/UC4fHq0fbRMtkcW8ImfQO0Ew>LBFury</a></b>'
                    ' for his contributions.</li>'
                    '<li>To the <a href=https://discord.gg/nShbGxDQsx>Raging Blast Modding community</a>.</li>'
                    '</ul>')
        msg.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.setWindowIcon(window.ico_image)
    window.selectCharaWindow.setWindowIcon(window.ico_image)
    window.selectCharaPartnerWindow.setWindowIcon(window.ico_image)
    window.selectCharaRosterWindow.setWindowIcon(window.ico_image)
    window.MaterialChildEditorWindow.setWindowIcon(window.ico_image)
    window.progressBarWindow.setWindowIcon(window.ico_image)
    window.show()
    app.exec_()
