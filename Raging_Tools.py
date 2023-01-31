from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QInputDialog

from lib.character_parameters_editor.GPV import GPV
from lib.character_parameters_editor.REV import REV
from lib.design.Raging_Tools.Raging_Tools import *
from lib.design.material_children.material_children import Material_Child_Editor
from lib.design.progress_bar.progress_bar import Progress_Bar
from lib.design.select_chara.select_chara import Select_Chara
from lib.design.select_chara.select_chara_roster import Select_Chara_Roster
from lib.packages import os, rmtree, QFileDialog, QMessageBox, stat
from lib.functions import del_rw, ask_pack_structure
# vram explorer
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.VEF import WorkerVef
from lib.vram_explorer.VEF import initialize_ve

# pak explorer
from lib.pak_explorer.PEF import initialize_pe, WorkerPef
from lib.pak_explorer.PEV import PEV

# character parameters editor
from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.CPEF import initialize_cpe


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
        initialize_ve(self)

        # --- pak explorer ---
        initialize_pe(self)

        # --- character parameters editor ---
        CPEV.disable_logic_events_combobox = True  # Starting the tool (avoid combo box code)
        initialize_cpe(self)

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

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = WorkerVef()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(lambda: self.worker.load_spr_vram_file(self))
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

    def run_save_ve_to_data(self, vram_separator, path_output_file):

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = WorkerVef()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(lambda: self.worker.save_spr_vram_file(self, vram_separator, path_output_file))
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

    def run_load_data_to_pe_cpe(self):

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = WorkerPef()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(lambda: self.worker.load_data_to_pe_cpe(self))
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

    def run_save_operate_character_and_pack(self, path_output_file, separator, separator_size):

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = WorkerPef()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(lambda: self.worker.save_operate_character_and_pack(self, path_output_file, separator, separator_size))
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
        self.worker = WorkerPef()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(lambda: self.worker.save_cs_chip_and_pack(path_output_file, separator, separator_size))
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
        self.worker = WorkerPef()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(lambda: self.worker.save_operate_resident_param_db_font_pad_ps3_and_pack(path_output_file, separator,
                                                                                                             separator_size))
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
        self.worker = WorkerPef()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(lambda: self.worker.pack_and_save_file(0.0, 100.0, path_output_file, separator, separator_size))
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
                # we remove every files in it
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
                # we remove every files in it
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

        # Ask to the user where to save the file
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

                    # Ask to the user the format for the vram file (only when is saving a vram and spr for PS3)
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

                    # Ask to the user if the tool saves also the modified values from character parameters editor
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

                                # Ask to the user if is packing a vram or ioram file for Xbox
                                separator, separator_size = ask_pack_structure(self)

                                # Save all the info
                                print("Writing values in the file...")
                                self.run_save_operate_character_and_pack(path_output_file, separator, separator_size)

                            # --- operate_resident_param --- or --- db_font_pad ---
                            # If the user has opened the operate resident or db_font_pad and edited one character, we will save the file
                            elif self.operate_resident_param_frame.isEnabled() and GPV.character_list_edited:

                                # Ask to the user if is packing a vram or ioram file for Xbox
                                separator, separator_size = ask_pack_structure(self)

                                # pack file
                                self.run_save_operate_resident_param_db_font_pad_ps3_and_pack(path_output_file, separator, separator_size)

                            # --- cs_chip ---
                            # If the user has opened the cs_chip tab and edited one character, we will save the file
                            elif self.cs_chip.isEnabled() and REV.slots_edited:

                                # Ask to the user if is packing a vram or ioram file for Xbox
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
                            # Ask to the user if is packing a vram or ioram file for Xbox
                            separator, separator_size = ask_pack_structure(self)

                            # pack file
                            self.run_save_pe_to_data(path_output_file, separator, separator_size)

                # We save the data from the 'pak explorer' tab
                elif self.pak_explorer.isEnabled():
                    # Ask to the user if is packing a vram or ioram file for Xbox
                    separator, separator_size = ask_pack_structure(self)

                    # pack file
                    self.run_save_pe_to_data(path_output_file, separator, separator_size)
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Warning")
                    msg.setWindowIcon(self.ico_image)
                    msg.setText("No pak file has been loaded.")
                    msg.exec()

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
            "<li><b>Raging tools 1.8</b> by "
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
                    '<li>To <b>SSJLVegeta</b> for his contributions.</li>'
                    '<li>To <b><a href=https://www.youtube.com/channel/UC4fHq0fbRMtkcW8ImfQO0Ew>LBFury</a></b>'
                    ' for his contributions.</li>'
                    '<li>To the <a href=https://discord.gg/JpCvDCgpnb>Raging Blast Modding community</a>.</li>'
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
