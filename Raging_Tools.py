from PyQt5.QtWidgets import QInputDialog

from lib.character_parameters_editor.IPF import write_single_character_parameters
from lib.character_parameters_editor.GPF import write_operate_resident_param, write_db_font_pad_ps3
from lib.character_parameters_editor.REF import write_cs_chip_file
from lib.character_parameters_editor.GPV import GPV
from lib.character_parameters_editor.REV import REV
from lib.design.Raging_Tools.Raging_Tools import *
from lib.packages import os, rmtree, QFileDialog, QMessageBox, stat
from lib.functions import del_rw

# vram explorer
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.VEF import load_data_to_ve, write_children, generate_tx2d_entry
from lib.vram_explorer.classes.SPRP.SprpTypeEntry import SprpTypeEntry
from lib.vram_explorer.functions.auxiliary import check_entry_module, search_texture
from lib.vram_explorer.VEF import initialize_ve

# pak explorer
from lib.pak_explorer.PEF import initialize_pe, pack_and_save_file, load_data_to_pe_cpe
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
        self.setupUi(self)

        # File tab
        self.actionOpen.triggered.connect(self.action_open_logic)
        self.actionSave.triggered.connect(self.action_save_logic)
        self.actionClose.triggered.connect(self.close)

        # About tab
        self.actionAuthor.triggered.connect(self.action_author_logic)
        self.actionCredits.triggered.connect(self.action_credits_logic)

        # --- vram explorer ---
        initialize_ve(self, QtWidgets)

        # --- pak explorer ---
        initialize_pe(self)

        # --- character parameters editor ---
        CPEV.change_character = True  # Starting the tool (avoid combo box code)
        initialize_cpe(self, QtWidgets)

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
                load_data_to_pe_cpe(self)

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
                load_data_to_pe_cpe(self)

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
                load_data_to_ve(self)

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
                load_data_to_ve(self)

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

                        # Default paths
                        VEV.spr_file_path_modified = os.path.join(path_output_file, os.path.basename(VEV.spr_file_path))
                        VEV.vram_file_path_modified = os.path.join(path_output_file,
                                                                   os.path.basename(VEV.vram_file_path))

                        # Vars used in order to create the spr from scratch
                        num_textures, entry_count, name_offset, entry_info_size, ioram_name_offset, ioram_data_size, \
                            vram_name_offset, vram_data_size = self.listView.model().rowCount(), 0, 0, 0, 0, 0, 0, 0
                        string_name_offset = 1
                        string_table_size, data_entry_size, data_offset, data_size = 0, 0, 0, 0
                        entry_info, header, string_table, data_entry, data = b'', b'', b'', b'', b''
                        # Vars used of the mtrl
                        num_material = 0
                        # Vars used for the txan
                        txan_name_offset_assigned = []
                        txan_entry = SprpTypeEntry()
                        # We will save in this class, some special name offsets
                        special_names_dict = {}

                        # It will generate the spr from scratch
                        if VEV.enable_spr_scratch:

                            # Get each type entry and write the data
                            for type_entry in VEV.sprp_file.type_entry:

                                # ------------------
                                # --- Write TX2D ---
                                # ------------------
                                if b'TX2D' == type_entry:
                                    entry_info, entry_info_size, entry_count, string_table, string_table_size, \
                                        string_name_offset, data_entry, data_entry_size, data, data_size, data_offset, \
                                        vram_data_size = \
                                        generate_tx2d_entry(self, VEV.vram_file_path_modified, entry_info,
                                                            entry_info_size, entry_count, string_table,
                                                            string_table_size, string_name_offset, data_entry,
                                                            data_entry_size, data, data_size, data_offset,
                                                            vram_separator, num_textures)

                                # ------------------
                                # --- Write VSHD ---
                                # ------------------
                                if b'VSHD' == type_entry:
                                    # Get the type entry vshd
                                    vshd_type_entry = VEV.sprp_file.type_entry[b'VSHD']

                                    # Get each vshd data entry
                                    for i in range(0, vshd_type_entry.data_count):
                                        # Get the data entry for the VSHD
                                        vshd_data_entry = vshd_type_entry.data_entry[i]

                                        # Get the data for the vshd
                                        vshd_data = vshd_data_entry.data_info.data

                                        # Write the name for each vshd
                                        vshd_data_entry.data_info.new_name_offset = string_name_offset
                                        string_table += b'\x00' + vshd_data_entry.data_info.name.encode('utf-8')
                                        string_table_size += 1 + len(vshd_data_entry.data_info.name)

                                        # Write the data_entry for each vshd
                                        data_entry += vshd_data_entry.data_type
                                        data_entry += i.to_bytes(4, 'big')
                                        data_entry += string_name_offset.to_bytes(4, 'big')
                                        data_entry += (data_offset + vshd_data.data_size).to_bytes(4, 'big')
                                        data_entry += vshd_data_entry.data_info.data_size.to_bytes(4, 'big')
                                        data_entry += vshd_data_entry.data_info.child_count.to_bytes(4, 'big')
                                        # We write the child offset later

                                        # Write the data for each vshd
                                        data += vshd_data.data
                                        data += vshd_data.unk0x00
                                        data += vshd_data.data_size.to_bytes(4, 'big')
                                        data += vshd_data.unk0x10
                                        data_size += vshd_data.data_size + vshd_data_entry.data_info.data_size

                                        # Write children (if any)
                                        if vshd_data_entry.data_info.child_count > 0:
                                            string_table_child, string_table_child_size, string_name_offset, \
                                                data_child, data_child_size, data_offset = \
                                                write_children(self, num_material, num_textures,
                                                               vshd_data_entry.data_info, b'VSHD',
                                                               string_table_size + 1, data_size, special_names_dict)

                                            # Update the string_name and string_table_size
                                            string_table += string_table_child
                                            string_table_size += string_table_child_size

                                            # Update the data and data_size
                                            data += data_child
                                            data_size += data_child_size

                                            # Write in the data entry, the children offset
                                            data_entry += data_offset.to_bytes(4, 'big')
                                        else:
                                            # Child offset
                                            data_entry += b'\x00\x00\x00\x00'
                                        data_entry += b'\x00\x00\x00\x00'
                                        data_entry_size += 32

                                        # Check if the data, the module of 16 is 0
                                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                                        # Update offsets for the next entry
                                        string_name_offset = 1 + string_table_size
                                        data_offset = data_size

                                    # Update the entry info
                                    entry_info += b'VSHD' + b'\x00\x00\x00\x08' + \
                                                  vshd_type_entry.data_count.to_bytes(4, 'big')
                                    # Update the sizes
                                    entry_count += 1
                                    entry_info_size += 12

                                # ------------------
                                # --- Write PSHD ---
                                # ------------------
                                if b'PSHD' == type_entry:
                                    # Get the type entry pshd
                                    pshd_type_entry = VEV.sprp_file.type_entry[b'PSHD']

                                    # Get each pshd data entry
                                    for i in range(0, pshd_type_entry.data_count):
                                        # Get the data entry for the PSHD
                                        pshd_data_entry = pshd_type_entry.data_entry[i]

                                        # Get the data for the pshd
                                        pshd_data = pshd_data_entry.data_info.data

                                        # Write the name for each pshd
                                        pshd_data_entry.data_info.new_name_offset = string_name_offset
                                        string_table += b'\x00' + pshd_data_entry.data_info.name.encode('utf-8')
                                        string_table_size += 1 + len(pshd_data_entry.data_info.name)

                                        # Write the data_entry for each pshd
                                        data_entry += pshd_data_entry.data_type
                                        data_entry += i.to_bytes(4, 'big')
                                        data_entry += string_name_offset.to_bytes(4, 'big')
                                        data_entry += (data_offset + pshd_data.data_size).to_bytes(4, 'big')
                                        data_entry += pshd_data_entry.data_info.data_size.to_bytes(4, 'big')
                                        data_entry += pshd_data_entry.data_info.child_count.to_bytes(4, 'big')
                                        # We write the child offset later

                                        # Write the data for each vshd
                                        data += pshd_data.data
                                        data += pshd_data.unk0x00
                                        data += pshd_data.data_size.to_bytes(4, 'big')
                                        data_size += pshd_data.data_size + pshd_data_entry.data_info.data_size

                                        # Write children (if any)
                                        if pshd_data_entry.data_info.child_count > 0:
                                            string_table_child, string_table_child_size, string_name_offset, \
                                                data_child, data_child_size, data_offset = \
                                                write_children(self, num_material, num_textures,
                                                               pshd_data_entry.data_info, b'PSHD',
                                                               string_table_size + 1, data_size, special_names_dict)

                                            # Update the string_name and string_table_size
                                            string_table += string_table_child
                                            string_table_size += string_table_child_size

                                            # Update the data and data_size
                                            data += data_child
                                            data_size += data_child_size

                                            # Write in the data entry, the children offset
                                            data_entry += data_offset.to_bytes(4, 'big')
                                        else:
                                            # Child offset
                                            data_entry += b'\x00\x00\x00\x00'
                                        data_entry += b'\x00\x00\x00\x00'
                                        data_entry_size += 32

                                        # Check if the data, the module of 16 is 0
                                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                                        # Update offsets for the next entry
                                        string_name_offset = 1 + string_table_size
                                        data_offset = data_size

                                    # Update the entry info
                                    entry_info += b'PSHD' + b'\x00\x00\x00\x08' + \
                                                  pshd_type_entry.data_count.to_bytes(4, 'big')
                                    # Update the sizes
                                    entry_count += 1
                                    entry_info_size += 12

                                # ------------------
                                # --- Write MTRL ---
                                # ------------------
                                if b'MTRL' == type_entry:
                                    num_material = self.materialVal.count()

                                    # TXAN values (will be used to know if the txan entries name offset are
                                    # already added to the spr)
                                    if b'TXAN' in VEV.sprp_file.type_entry:
                                        txan_entry = VEV.sprp_file.type_entry[b"TXAN"]
                                        for _ in range(0, txan_entry.data_count):
                                            txan_name_offset_assigned.append(False)

                                    # Write each material
                                    for i in range(0, num_material):
                                        # Get the material from the tool
                                        mtrl_data_entry = self.materialVal.itemData(i)

                                        # Write the name for each material
                                        mtrl_data_entry.data_info.new_name_offset = string_name_offset
                                        string_table += b'\x00' + mtrl_data_entry.data_info.name.encode('utf-8')
                                        string_table_size += 1 + len(mtrl_data_entry.data_info.name)

                                        # Write the data_entry for each material
                                        data_entry += mtrl_data_entry.data_type
                                        data_entry += i.to_bytes(4, 'big')
                                        mtrl_data_entry.data_info.new_name_offset = string_name_offset
                                        data_entry += mtrl_data_entry.data_info.new_name_offset.to_bytes(4, 'big')
                                        data_entry += data_offset.to_bytes(4, 'big')
                                        data_entry += mtrl_data_entry.data_info.data_size.to_bytes(4, 'big')
                                        data_entry += mtrl_data_entry.data_info.child_count.to_bytes(4, 'big')
                                        # The child offset will be calculated later

                                        # Write the data for each material
                                        mtrl_info = mtrl_data_entry.data_info.data
                                        data += mtrl_info.unk_00
                                        for layer in mtrl_info.layers:

                                            # Assing to the spr, the layer type
                                            if layer.layer_name == "":
                                                data += b'\00\00\00\00'
                                            else:
                                                # The special name wasn't added to the string name, so the name
                                                # offset will be calculated
                                                if layer.layer_name not in special_names_dict:
                                                    # Write the name for the special name
                                                    special_names_dict[layer.layer_name] = 1 + string_table_size
                                                    string_table += b'\x00' + layer.layer_name.encode('utf-8')
                                                    string_table_size += 1 + len(layer.layer_name)

                                                data += special_names_dict[layer.layer_name].to_bytes(4, 'big')

                                            # Search for the texture assigned to the material
                                            if layer.source_name_offset == 0:
                                                data += b'\00\00\00\00'
                                            else:
                                                # Search the texture
                                                found, data = search_texture(self, data, layer.source_name_offset,
                                                                             num_textures)
                                                # Search in the TXAN entries
                                                if not found:
                                                    for j in range(0, txan_entry.data_count):
                                                        txan_data_entry = txan_entry.data_entry[j]
                                                        if txan_data_entry.data_info.name_offset == layer.\
                                                                source_name_offset:
                                                            # The TXAN wasn't added to the string name, so the name
                                                            # offset will be calculated
                                                            if not txan_name_offset_assigned[j]:
                                                                name = txan_data_entry.data_info.name + \
                                                                       ("." + txan_data_entry.data_info.extension
                                                                        if txan_data_entry.data_info.extension else "")
                                                                txan_data_entry.data_info.new_name_offset = \
                                                                    1 + string_table_size
                                                                string_table += b'\x00' + name.encode('utf-8')
                                                                string_table_size += 1 + len(name)
                                                                txan_name_offset_assigned[j] = True
                                                            data += txan_data_entry.data_info.new_name_offset.\
                                                                to_bytes(4, 'big')
                                                            found = True
                                                            break
                                                # If we didn't find anything, we add it to the special names var.
                                                if not found:
                                                    # The special name wasn't added to the string name, so the name
                                                    # offset will be calculated
                                                    if layer.source_name not in special_names_dict:
                                                        # Write the name for the special name
                                                        special_names_dict[layer.source_name] = 1 + string_table_size
                                                        string_table += b'\x00' + layer.source_name.encode('utf-8')
                                                        string_table_size += 1 + len(layer.source_name)

                                                    data += special_names_dict[layer.source_name].to_bytes(4, 'big')

                                        data_size += mtrl_data_entry.data_info.data_size

                                        # Write the children material (if any)
                                        if mtrl_data_entry.data_info.child_count > 0:
                                            string_table_child, string_table_child_size, string_name_offset, \
                                                data_child, data_child_size, data_offset = \
                                                write_children(self, num_material, num_textures,
                                                               mtrl_data_entry.data_info, b'MTRL',
                                                               string_table_size + 1, data_size, special_names_dict)

                                            # Update the string_name and string_table_size
                                            string_table += string_table_child
                                            string_table_size += string_table_child_size

                                            # Update the data and data_size
                                            data += data_child
                                            data_size += data_child_size

                                            # Write in the data entry, the children offset
                                            data_entry += data_offset.to_bytes(4, 'big')
                                        else:
                                            # Child offset
                                            data_entry += b'\00\00\00\00'
                                        data_entry += b'\00\00\00\00'
                                        data_entry_size += 32

                                        # Check if the data, the module of 16 is 0
                                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                                        # Update offsets for the next entry
                                        string_name_offset = 1 + string_table_size
                                        data_offset = data_size

                                    # Update the entry info
                                    entry_info += b'MTRL' + b'\x00\x00\x00\x08' + num_material.to_bytes(4, 'big')
                                    # Update the sizes
                                    entry_count += 1
                                    entry_info_size += 12

                                # ------------------
                                # --- Write SHAP ---
                                # ------------------
                                if b'SHAP' == type_entry:
                                    # Get the type entry shap
                                    shap_type_entry = VEV.sprp_file.type_entry[b'SHAP']

                                    # Get each shape data entry
                                    for i in range(0, shap_type_entry.data_count):
                                        # Get the data entry for the SHAP
                                        shap_data_entry = shap_type_entry.data_entry[i]

                                        # Write the name for each shape
                                        shap_data_entry.data_info.new_name_offset = string_name_offset
                                        string_table += b'\x00' + shap_data_entry.data_info.name.encode('utf-8')
                                        string_table_size += 1 + len(shap_data_entry.data_info.name)

                                        # Write the data_entry for each shape
                                        data_entry += shap_data_entry.data_type
                                        data_entry += i.to_bytes(4, 'big')
                                        data_entry += string_name_offset.to_bytes(4, 'big')
                                        data_entry += data_offset.to_bytes(4, 'big')
                                        data_entry += shap_data_entry.data_info.data_size.to_bytes(4, 'big')
                                        data_entry += shap_data_entry.data_info.child_count.to_bytes(4, 'big')
                                        # We write the child offset later

                                        # Write the data for each shape
                                        shap_info = shap_data_entry.data_info.data
                                        data += shap_info.data
                                        data_size += shap_data_entry.data_info.data_size

                                        # Write children (if any)
                                        if shap_data_entry.data_info.child_count > 0:
                                            string_table_child, string_table_child_size, string_name_offset, \
                                                data_child, data_child_size, data_offset = \
                                                write_children(self, num_material, num_textures,
                                                               shap_data_entry.data_info, b'SHAP',
                                                               string_table_size + 1, data_size, special_names_dict)

                                            # Update the string_name and string_table_size
                                            string_table += string_table_child
                                            string_table_size += string_table_child_size

                                            # Update the data and data_size
                                            data += data_child
                                            data_size += data_child_size

                                            # Write in the data entry, the children offset
                                            data_entry += data_offset.to_bytes(4, 'big')
                                        else:
                                            # Child offset
                                            data_entry += b'\x00\x00\x00\x00'
                                        data_entry += b'\x00\x00\x00\x00'
                                        data_entry_size += 32

                                        # Check if the data, the module of 16 is 0
                                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                                        # Update offsets for the next entry
                                        string_name_offset = 1 + string_table_size
                                        data_offset = data_size

                                    # Update the entry info
                                    entry_info += b'SHAP' + b'\x00\x00\x00\x05' + \
                                                  shap_type_entry.data_count.to_bytes(4, 'big')
                                    # Update the sizes
                                    entry_count += 1
                                    entry_info_size += 12

                                # ------------------
                                # --- Write VBUF ---
                                # ------------------
                                if b'VBUF' == type_entry:
                                    # Get the type entry vbuf
                                    vbuf_type_entry = VEV.sprp_file.type_entry[b'VBUF']

                                    # Get each vbuf data entry
                                    for i in range(0, vbuf_type_entry.data_count):
                                        # Get the data entry for the VBUF
                                        vbuf_data_entry = vbuf_type_entry.data_entry[i]

                                        # Write the name for each vbuf
                                        vbuf_data_entry.data_info.new_name_offset = string_name_offset
                                        string_table += b'\x00' + vbuf_data_entry.data_info.name.encode('utf-8')
                                        string_table_size += 1 + len(vbuf_data_entry.data_info.name)

                                        # Write each vertexDecl first
                                        vbuf_info = vbuf_data_entry.data_info.data
                                        data_offset_vertex_decl = data_size
                                        for j in range(0, vbuf_info.decl_count_0):

                                            vertex_decl = vbuf_info.vertex_decl[j]

                                            # Read all the data
                                            data += vertex_decl.unk0x00

                                            # Search what effect is using the vertex declaration for the mesh
                                            # If we don't find anything, we write 0
                                            if vertex_decl.resource_name == "":
                                                data += b'\00\00\00\00'
                                            else:
                                                # The special name wasn't added to the string name, so the name
                                                # offset will be calculated
                                                if vertex_decl.resource_name not in special_names_dict:
                                                    # Write the name for the special name
                                                    special_names_dict[vertex_decl.resource_name] = 1 + \
                                                                                                    string_table_size
                                                    string_table += b'\x00' + vertex_decl.resource_name.encode('utf-8')
                                                    string_table_size += 1 + len(vertex_decl.resource_name)

                                                data += special_names_dict[vertex_decl.resource_name].to_bytes(4, 'big')

                                            data += vertex_decl.vertex_usage.to_bytes(2, 'big')
                                            data += vertex_decl.index.to_bytes(2, 'big')
                                            data += vertex_decl.vertex_format
                                            data += vertex_decl.stride.to_bytes(2, 'big')
                                            data += vertex_decl.offset.to_bytes(4, 'big')
                                            data_size += 20

                                        # Check if the data, the module of 16 is 0
                                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                                        # If we check the size of the vbuf data due to Game Assets Converter
                                        # store the size as 'header + data' instead of 'header'. If the size is
                                        # different from 32, we modify the original size
                                        if vbuf_data_entry.data_info.data_size != 32:
                                            vbuf_data_entry.data_info.data_size = 32

                                        # Write the data_entry for each vbuf
                                        data_offset = data_size
                                        data_entry += vbuf_data_entry.data_type
                                        data_entry += i.to_bytes(4, 'big')
                                        data_entry += string_name_offset.to_bytes(4, 'big')
                                        data_entry += data_offset.to_bytes(4, 'big')
                                        data_entry += vbuf_data_entry.data_info.data_size.to_bytes(4, 'big')
                                        data_entry += vbuf_data_entry.data_info.child_count.to_bytes(4, 'big')
                                        # We write the child offset later

                                        # Write the data for each vbuf
                                        data += vbuf_info.unk0x00
                                        data += vbuf_info.unk0x04
                                        data += vbuf_info.data_offset.to_bytes(4, 'big')
                                        data += vbuf_info.data_size.to_bytes(4, 'big')
                                        data += vbuf_info.vertex_count.to_bytes(4, 'big')
                                        data += vbuf_info.unk0x14
                                        data += vbuf_info.unk0x16
                                        data += vbuf_info.decl_count_0.to_bytes(2, 'big')
                                        data += vbuf_info.decl_count_1.to_bytes(2, 'big')
                                        data += data_offset_vertex_decl.to_bytes(4, 'big')
                                        data_size += vbuf_data_entry.data_info.data_size

                                        # Child offset
                                        data_entry += b'\x00\x00\x00\x00'
                                        data_entry += b'\x00\x00\x00\x00'
                                        data_entry_size += 32

                                        # Check if the data, the module of 16 is 0
                                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                                        # Update offsets for the next entry
                                        string_name_offset = 1 + string_table_size
                                        data_offset = data_size

                                    # Update the entry info
                                    entry_info += b'VBUF' + b'\x00\x00\x00\x0A' + \
                                                  vbuf_type_entry.data_count.to_bytes(4, 'big')
                                    # Update the sizes
                                    entry_count += 1
                                    entry_info_size += 12

                                # ------------------
                                # --- Write SCNE ---
                                # ------------------
                                if b'SCNE' == type_entry:

                                    # Get the type entry scne
                                    scne_type_entry = VEV.sprp_file.type_entry[b'SCNE']

                                    # Get each SCNE entry
                                    for i in range(0, scne_type_entry.data_count):
                                        scne_data_entry = scne_type_entry.data_entry[i]

                                        # Write children (if any)
                                        if scne_data_entry.data_info.child_count > 0:
                                            string_table_child, string_table_child_size, string_name_offset, \
                                                data_child, data_child_size, data_offset = \
                                                write_children(self, num_material, num_textures,
                                                               scne_data_entry.data_info, b'SCNE',
                                                               string_table_size + 1, data_size, special_names_dict)

                                            # Reset all the [NODES] children name offset calculated
                                            nodes = scne_data_entry.data_info.child_info[1].child_info
                                            for node in nodes:
                                                if node.name_offset_calculated:
                                                    node.name_offset_calculated = False

                                            # Update the string_name and string_table_size
                                            string_table += string_table_child
                                            string_table_size += string_table_child_size

                                            # Update the data and data_size
                                            data += data_child
                                            data_size += data_child_size

                                        # Write the name for the scne
                                        name = "scene_" + self.fileNameText.text() + ".mb"
                                        string_table += b'\x00' + name.encode('utf-8')
                                        string_table_size += 1 + len(name)

                                        # Write the data_entry
                                        data_entry += scne_data_entry.data_type
                                        data_entry += i.to_bytes(4, 'big')
                                        data_entry += string_name_offset.to_bytes(4, 'big')
                                        data_entry += data_offset.to_bytes(4, 'big')
                                        data_entry += scne_data_entry.data_info.data_size.to_bytes(4, 'big')
                                        data_entry += scne_data_entry.data_info.child_count.to_bytes(4, 'big')
                                        data_entry += data_offset.to_bytes(4, 'big')
                                        data_entry += b'\x00\x00\x00\x00'
                                        data_entry_size += 32

                                        # Check if the data, the module of 16 is 0
                                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                                        # Update offsets for the next entry
                                        string_name_offset = 1 + string_table_size
                                        data_offset = data_size

                                    # Update the entry info
                                    entry_info += b'SCNE' + b'\x00\x00\x00\x07' + \
                                                  scne_type_entry.data_count.to_bytes(4, 'big')
                                    # Update the sizes
                                    entry_count += 1
                                    entry_info_size += 12

                                # ------------------
                                # --- Write BONE ---
                                # ------------------
                                if b'BONE' == type_entry:
                                    # Get the type entry bone
                                    bone_type_entry = VEV.sprp_file.type_entry[b'BONE']

                                    # Get each bone data entry
                                    for i in range(0, bone_type_entry.data_count):
                                        # Get the data entry for the BONE
                                        bone_data_entry = bone_type_entry.data_entry[i]

                                        # Write the name for each bone
                                        string_table += b'\x00' + bone_data_entry.data_info.name.encode('utf-8')
                                        string_table_size += 1 + len(bone_data_entry.data_info.name)

                                        # Write the data_entry for each bone
                                        data_entry += bone_data_entry.data_type
                                        data_entry += i.to_bytes(4, 'big')
                                        data_entry += string_name_offset.to_bytes(4, 'big')
                                        data_entry += data_offset.to_bytes(4, 'big')
                                        data_entry += bone_data_entry.data_info.data_size.to_bytes(4, 'big')
                                        data_entry += bone_data_entry.data_info.child_count.to_bytes(4, 'big')
                                        # We write the child offset later

                                        # Write the data for each bone
                                        data += bone_data_entry.data_info.data
                                        data_size += bone_data_entry.data_info.data_size

                                        # Write children (if any)
                                        if bone_data_entry.data_info.child_count > 0:
                                            string_table_child, string_table_child_size, string_name_offset, \
                                                data_child, data_child_size, data_offset = \
                                                write_children(self, num_material, num_textures,
                                                               bone_data_entry.data_info, b'BONE',
                                                               string_table_size + 1, data_size, special_names_dict)

                                            # Update the string_name and string_table_size
                                            string_table += string_table_child
                                            string_table_size += string_table_child_size

                                            # Update the data and data_size
                                            data += data_child
                                            data_size += data_child_size

                                            # Write in the data entry, the children offset
                                            data_entry += data_offset.to_bytes(4, 'big')
                                        else:
                                            # Child offset
                                            data_entry += b'\x00\x00\x00\x00'
                                        data_entry += b'\x00\x00\x00\x00'
                                        data_entry_size += 32

                                        # Check if the data, the module of 16 is 0
                                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                                        # Update offsets for the next entry
                                        string_name_offset = 1 + string_table_size
                                        data_offset = data_size

                                    # Update the entry info
                                    entry_info += b'BONE' + b'\x00\x00\x00\x03' + \
                                                  bone_type_entry.data_count.to_bytes(4, 'big')
                                    # Update the sizes
                                    entry_count += 1
                                    entry_info_size += 12

                                # ------------------
                                # --- Write DRVN ---
                                # ------------------
                                if b'DRVN' == type_entry:
                                    # Get the type entry drvn
                                    drvn_type_entry = VEV.sprp_file.type_entry[b'DRVN']

                                    # Get each drvn data entry
                                    for i in range(0, drvn_type_entry.data_count):
                                        # Get the data entry for the DRVN
                                        drvn_data_entry = drvn_type_entry.data_entry[i]

                                        # Write the name for each drvn
                                        name = "driven_" + self.fileNameText.text() + ".mb"
                                        string_table += b'\x00' + name.encode('utf-8')
                                        string_table_size += 1 + len(name)

                                        # Write the data_entry for each devn
                                        data_entry += drvn_data_entry.data_type
                                        data_entry += i.to_bytes(4, 'big')
                                        data_entry += string_name_offset.to_bytes(4, 'big')
                                        data_entry += data_offset.to_bytes(4, 'big')
                                        data_entry += drvn_data_entry.data_info.data_size.to_bytes(4, 'big')
                                        data_entry += drvn_data_entry.data_info.child_count.to_bytes(4, 'big')
                                        # We write the child offset later

                                        # Write the data for each drvn
                                        data += drvn_data_entry.data_info.data
                                        data_size += drvn_data_entry.data_info.data_size

                                        # Write children (if any)
                                        if drvn_data_entry.data_info.child_count > 0:
                                            string_table_child, string_table_child_size, string_name_offset, \
                                                data_child, data_child_size, data_offset = \
                                                write_children(self, num_material, num_textures,
                                                               drvn_data_entry.data_info, b'DRVN',
                                                               string_table_size + 1, data_size, special_names_dict)

                                            # Update the string_name and string_table_size
                                            string_table += string_table_child
                                            string_table_size += string_table_child_size

                                            # Update the data and data_size
                                            data += data_child
                                            data_size += data_child_size

                                            # Write in the data entry, the children offset
                                            data_entry += data_offset.to_bytes(4, 'big')
                                        else:
                                            # Child offset
                                            data_entry += b'\x00\x00\x00\x00'
                                        data_entry += b'\x00\x00\x00\x00'
                                        data_entry_size += 32

                                        # Check if the data, the module of 16 is 0
                                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                                        # Update offsets for the next entry
                                        string_name_offset = 1 + string_table_size
                                        data_offset = data_size

                                    # Update the entry info
                                    entry_info += b'DRVN' + b'\x00\x00\x00\x01' + \
                                                  drvn_type_entry.data_count.to_bytes(4, 'big')
                                    # Update the sizes
                                    entry_count += 1
                                    entry_info_size += 12

                                # ------------------
                                # --- Write TXAN ---
                                # ------------------
                                if b'TXAN' == type_entry:
                                    # Get the type entry txan
                                    txan_type_entry = VEV.sprp_file.type_entry[b'TXAN']

                                    # Get each txan data entry
                                    for i in range(0, txan_type_entry.data_count):
                                        # Get the data entry for the TXAN
                                        txan_data_entry = txan_type_entry.data_entry[i]

                                        # Write the data_entry for each txan
                                        data_entry += txan_type_entry.data_type
                                        data_entry += i.to_bytes(4, 'big')

                                        if txan_name_offset_assigned[i]:
                                            data_entry += txan_data_entry.data_info.new_name_offset.to_bytes(4, 'big')
                                        else:
                                            # Write the name for each txan
                                            string_table += b'\x00' + txan_data_entry.data_info.name.encode('utf-8')
                                            string_table_size += 1 + len(txan_data_entry.data_info.name)
                                            data_entry += string_name_offset.to_bytes(4, 'big')
                                            # Update offset for the string table
                                            string_name_offset = 1 + string_table_size

                                        data_entry += data_offset.to_bytes(4, 'big')
                                        data_entry += txan_data_entry.data_info.data_size.to_bytes(4, 'big')
                                        data_entry += txan_data_entry.data_info.child_count.to_bytes(4, 'big')
                                        # We write the child offset later

                                        # Write the data for each txan
                                        data += txan_data_entry.data_info.data
                                        data_size += txan_data_entry.data_info.data_size

                                        # Write children (if any)
                                        if txan_data_entry.data_info.child_count > 0:
                                            string_table_child, string_table_child_size, string_name_offset, \
                                                data_child, data_child_size, data_offset = \
                                                write_children(self, num_material, num_textures,
                                                               txan_data_entry.data_info, b'TXAN',
                                                               string_table_size + 1, data_size, special_names_dict)

                                            # Update the string_name and string_table_size
                                            string_table += string_table_child
                                            string_table_size += string_table_child_size

                                            # Update the data and data_size
                                            data += data_child
                                            data_size += data_child_size

                                            # Write in the data entry, the children offset
                                            data_entry += data_offset.to_bytes(4, 'big')
                                        else:
                                            # Child offset
                                            data_entry += b'\x00\x00\x00\x00'
                                        data_entry += b'\x00\x00\x00\x00'
                                        data_entry_size += 32

                                        # Check if the data, the module of 16 is 0
                                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                                        # Update offsets for the next entry
                                        data_offset = data_size

                                    # Update the entry info
                                    entry_info += b'TXAN' + b'\x00\x00\x00\x01' + \
                                                  txan_type_entry.data_count.to_bytes(4, 'big')
                                    # Update the sizes
                                    entry_count += 1
                                    entry_info_size += 12

                                # ------------------
                                # --- Write ANIM ---
                                # ------------------
                                if b'ANIM' == type_entry:
                                    # Get the type entry anim
                                    anim_type_entry = VEV.sprp_file.type_entry[b'ANIM']

                                    # Get each anim data entry
                                    for i in range(0, anim_type_entry.data_count):
                                        # Get the data entry for the ANIM
                                        anim_data_entry = anim_type_entry.data_entry[i]

                                        # Write the name for each anim
                                        string_table += b'\x00' + anim_data_entry.data_info.name.encode('utf-8')
                                        string_table_size += 1 + len(anim_data_entry.data_info.name)

                                        # Write the data_entry for each anim
                                        data_entry += anim_data_entry.data_type
                                        data_entry += i.to_bytes(4, 'big')
                                        data_entry += string_name_offset.to_bytes(4, 'big')
                                        data_entry += data_offset.to_bytes(4, 'big')
                                        data_entry += anim_data_entry.data_info.data_size.to_bytes(4, 'big')
                                        data_entry += anim_data_entry.data_info.child_count.to_bytes(4, 'big')
                                        # We write the child offset later

                                        # Write the data for each anim
                                        data += anim_data_entry.data_info.data
                                        data_size += anim_data_entry.data_info.data_size

                                        # Write children (if any)
                                        if anim_data_entry.data_info.child_count > 0:
                                            string_table_child, string_table_child_size, string_name_offset, \
                                                data_child, data_child_size, data_offset = \
                                                write_children(self, num_material, num_textures,
                                                               anim_data_entry.data_info, b'ANIM',
                                                               string_table_size + 1, data_size, special_names_dict)

                                            # Update the string_name and string_table_size
                                            string_table += string_table_child
                                            string_table_size += string_table_child_size

                                            # Update the data and data_size
                                            data += data_child
                                            data_size += data_child_size

                                            # Write in the data entry, the children offset
                                            data_entry += data_offset.to_bytes(4, 'big')
                                        else:
                                            # Child offset
                                            data_entry += b'\x00\x00\x00\x00'
                                        data_entry += b'\x00\x00\x00\x00'
                                        data_entry_size += 32

                                        # Check if the data, the module of 16 is 0
                                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                                        # Update offsets for the next entry
                                        string_name_offset = 1 + string_table_size
                                        data_offset = data_size

                                    # Update the entry info
                                    entry_info += b'ANIM' + b'\x00\x00\x00\x03' + \
                                                  anim_type_entry.data_count.to_bytes(4, 'big')
                                    # Update the sizes
                                    entry_count += 1
                                    entry_info_size += 12

                            # Write the basename, ioram and vram offsets names
                            # If the spr doesn't have an ioram file, we won't write the name on it
                            if VEV.sprp_file.sprp_header.ioram_data_size > 0:

                                # Write the xmb extension
                                name_offset = 1 + string_table_size
                                name = self.fileNameText.text() + ".xmb"
                                string_table += b'\x00' + name.encode('utf-8')
                                string_table_size += 1 + len(name)

                                ioram_name_offset = 1 + string_table_size
                                ioram_data_size = VEV.sprp_file.sprp_header.ioram_data_size
                                name = self.fileNameText.text() + ".ioram"
                                string_table += b'\x00' + name.encode('utf-8')
                                string_table_size += 1 + len(name)
                            else:

                                # Write the spr extension
                                name_offset = 1 + string_table_size
                                name = self.fileNameText.text() + ".spr"
                                string_table += b'\x00' + name.encode('utf-8')
                                string_table_size += 1 + len(name)

                                ioram_name_offset = 0
                                ioram_data_size = 0
                            vram_name_offset = 1 + string_table_size
                            name = self.fileNameText.text() + ".vram"
                            string_table += b'\x00' + name.encode('utf-8')
                            string_table_size += 1 + len(name)

                            # Write the watermark
                            string_table += b'\x00' + VEV.watermark_message.encode('utf-8')
                            string_table_size += 1 + len(VEV.watermark_message)

                            # Check if the entry_info, the module of 16 is 0
                            entry_info, entry_info_size, padding_size = check_entry_module(entry_info, entry_info_size,
                                                                                           16)

                            # Check if the string_table_size, the module of 16 is 0
                            string_table, string_table_size, padding_size = check_entry_module(string_table,
                                                                                               string_table_size, 16)

                            # Create the header
                            header = VEV.sprp_file.sprp_header.data_tag + b'\00\01\00\01' + \
                                entry_count.to_bytes(4, 'big') + b'\00\00\00\00' + name_offset.to_bytes(4, 'big') + \
                                entry_info_size.to_bytes(4, 'big') + \
                                string_table_size.to_bytes(4, 'big') + data_entry_size.to_bytes(4, 'big') + \
                                data_size.to_bytes(4, 'big') + ioram_name_offset.to_bytes(4, 'big') + \
                                ioram_data_size.to_bytes(4, 'big') + vram_name_offset.to_bytes(4, 'big') + \
                                vram_data_size.to_bytes(4, 'big') + b'\00\00\00\00\00\00\00\00\00\00\00\00'

                        # The spr output will be a copy from the original one, the difference will be only the
                        # tx2d entry
                        else:

                            with open(VEV.spr_file_path, mode='rb') as input_spr_file:

                                # Store the entry_info
                                input_spr_file.seek(64)
                                entry_info = input_spr_file.read(VEV.sprp_file.sprp_header.entry_info_size)

                                # Store the string table
                                string_table = input_spr_file.read(VEV.sprp_file.sprp_header.string_table_size)
                                string_table_size = VEV.sprp_file.sprp_header.string_table_size
                                # Write the watermark
                                string_table += b'\x00' + VEV.watermark_message.encode('utf-8')
                                string_table_size += 1 + len(VEV.watermark_message)
                                # Check if the string_table_size, the module of 16 is 0
                                string_table, string_table_size, padding_size = check_entry_module(string_table,
                                                                                                   string_table_size,
                                                                                                   16)

                                # Write the data entry
                                # Write the TX2D entry only
                                null, null, null, null, null, null, null, null, data, null, null, vram_data_size = \
                                    generate_tx2d_entry(self, VEV.vram_file_path_modified, entry_info,
                                                        entry_info_size, entry_count, string_table,
                                                        string_table_size, string_name_offset, data_entry,
                                                        data_entry_size, data, data_size, data_offset, vram_separator,
                                                        num_textures)
                                data_entry = input_spr_file.read(VEV.sprp_file.sprp_header.data_info_size)

                                # Write the data
                                tx2d_data_size = 48 * num_textures
                                input_spr_file.seek(tx2d_data_size, os.SEEK_CUR)
                                data = data + input_spr_file.read()

                            # Write the header
                            header = VEV.sprp_file.sprp_header.data_tag + b'\00\01\00\01' + \
                                VEV.sprp_file.sprp_header.entry_count.to_bytes(4, 'big') + b'\00\00\00\00' + \
                                VEV.sprp_file.sprp_header.name_offset.to_bytes(4, 'big') + \
                                VEV.sprp_file.sprp_header.entry_info_size.to_bytes(4, 'big') + \
                                string_table_size.to_bytes(4, 'big') + \
                                VEV.sprp_file.sprp_header.data_info_size.to_bytes(4, 'big') + \
                                VEV.sprp_file.sprp_header.data_block_size.to_bytes(4, 'big') + \
                                VEV.sprp_file.sprp_header.ioram_name_offset.to_bytes(4, 'big') + \
                                VEV.sprp_file.sprp_header.ioram_data_size.to_bytes(4, 'big') + \
                                VEV.sprp_file.sprp_header.vram_name_offset.to_bytes(4, 'big') + \
                                vram_data_size.to_bytes(4, 'big') + b'\00\00\00\00\00\00\00\00\00\00\00\00'

                        # Write the spr
                        with open(VEV.spr_file_path_modified, mode="wb") as output_spr_file:
                            output_spr_file.write(header + entry_info + string_table + data_entry + data)

                        message = "The files were saved in: <b>" + path_output_file \
                                  + "</b><br><br> Do you wish to open the folder?"

                        msg = QMessageBox()
                        msg.setWindowTitle("Message")
                        msg.setWindowIcon(self.ico_image)
                        message_open_saved_files = msg.question(self, '', message, msg.Yes | msg.No)

                        # If the users click on 'Yes', it will open the path where the files were saved
                        if message_open_saved_files == msg.Yes:
                            # Show the path folder to the user
                            os.system('explorer.exe ' + path_output_file.replace("/", "\\"))

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

                            # Check what type of character parameter editor is activated
                            # --- operate_character_XXX_m ---
                            if self.operate_character_xyz_m_frame.isEnabled():

                                # Save all the info
                                print("Writing values in the file...")
                                write_single_character_parameters(self)

                                # Pack the files
                                print("Packing the file...")
                                pack_and_save_file(self, path_output_file, PEV.separator_size_64, PEV.separator_64)

                            # If the user has edited one character, we will save the file
                            elif GPV.character_list_edited:

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
                                        # Save all the info for each character
                                        write_db_font_pad_ps3(character, subpak_file_resident_character_param)

                                    # Close the files
                                    subpak_file_resident_character_param.close()

                                # Pack the files
                                print("Packing the file...")
                                pack_and_save_file(self, path_output_file, PEV.separator_size_64, PEV.separator_64)

                            # --- cs_chip ---
                            # If the user has edited one character, we will save the file
                            elif REV.slots_edited:

                                # Save all the info
                                print("Writing values in the file...")
                                write_cs_chip_file()

                                # Pack the files
                                print("Packing the file...")
                                pack_and_save_file(self, path_output_file, PEV.separator_size_64, PEV.separator_64)

                            else:
                                msg = QMessageBox()
                                msg.setWindowTitle("Warning")
                                msg.setWindowIcon(self.ico_image)
                                msg.setText("The file hasn't been modified.")
                                msg.exec()

                        # The user wants to save the values only from the 'pak explorer'
                        elif answer == msg.No:
                            print("Packing the file...")
                            pack_and_save_file(self, path_output_file, PEV.separator_size_64, PEV.separator_64)

                # We save the data from the 'pak explorer' tab
                elif self.pak_explorer.isEnabled():

                    # Ask to the user if is packing a vram or ioram file for Xbox. If is for Xbox,
                    # we have to change the separator size that is written between header and data. Otherwise
                    # will crash or make an output with bugs and errors
                    msg = QMessageBox()
                    msg.setWindowTitle("Message")
                    msg.setWindowIcon(self.ico_image)
                    message = "Do you wish to pack the file with Xbox compatibility?"
                    answer = msg.question(self, '', message, msg.Yes | msg.No)

                    if answer == msg.Yes:
                        # Packing file with Xbox compatibility (this is only when packing .vram or .ioram files, but
                        # it looks like it's working for any other files)
                        print("Packing the file with Xbox compatibility...")
                        pack_and_save_file(self, path_output_file, PEV.separator_size_4032, PEV.separator_4032)
                    else:
                        print("Packing the file...")
                        pack_and_save_file(self, path_output_file, PEV.separator_size_64, PEV.separator_64)
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
    window.ico_image = QtGui.QIcon("lib/design/Raging_Tools/Raging_Tools.ico")
    window.setWindowIcon(window.ico_image)
    window.selectCharaWindow.setWindowIcon(window.ico_image)
    window.selectCharaPartnerWindow.setWindowIcon(window.ico_image)
    window.selectCharaRosterWindow.setWindowIcon(window.ico_image)
    window.MaterialChildEditorWindow.setWindowIcon(window.ico_image)
    window.show()
    app.exec_()
