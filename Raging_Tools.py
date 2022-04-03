from lib.character_parameters_editor.IPF import write_single_character_parameters
from lib.character_parameters_editor.GPF import write_operate_resident_param, write_db_font_pad_ps3
from lib.character_parameters_editor.REF import write_cs_chip_file
from lib.character_parameters_editor.GPV import GPV
from lib.character_parameters_editor.REV import REV
from lib.design.Raging_Tools.Raging_Tools import *
from lib.packages import os, rmtree, QFileDialog, QMessageBox
from lib.functions import del_rw

# vram explorer
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.VEF import change_endian, load_data_to_ve, write_children
from lib.vram_explorer.functions.auxiliary import write_separator_vram, check_entry_module
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
            elif header_type == b'SPRP' or header_type == b'SPR\x00':

                # Open vram file
                path_file_2 = QFileDialog.getOpenFileName(self, "Open file", path_file,
                                                          "Texture files (*.vram)")[0]

                if os.path.exists(path_file_2):
                    # Get the header of the new file
                    with open(path_file_2, mode="rb") as input_file:
                        header_type = input_file.read(4)

                    # Check if the type of file is vram
                    if header_type == b'STPZ' or header_type == b'STPK' or header_type == b'SPRP' \
                            or header_type == b'SPR\x00':
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
                        header_type = input_file.read(4)

                    # Check if the type of file is vram
                    if header_type != b'SPRP' and header_type != b'SPR\x00':
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

                if not VEV.sprp_file.type_entry:
                    msg = QMessageBox()
                    msg.setWindowTitle("Warning")
                    msg.setWindowIcon(self.ico_image)
                    msg.setText("There is no file loaded.")
                    msg.exec()
                else:

                    # Create the folder where we save the modified files
                    if not os.path.exists(path_output_file):
                        os.mkdir(path_output_file)

                    # Default paths
                    VEV.spr_file_path_modified = os.path.join(path_output_file, os.path.basename(VEV.spr_file_path))
                    VEV.vram_file_path_modified = os.path.join(path_output_file, os.path.basename(VEV.vram_file_path))

                    # Vars used in order to create the spr from scratch
                    num_textures, entry_count, name_offset, entry_info_size, ioram_name_offset, ioram_data_size, \
                        vram_name_offset, vram_data_size, string_name_offset, string_table_size, data_entry_size, \
                        data_offset, data_size, dbz_char_mtrl_offset, map1_offset, dbz_edge_info_offset, \
                        dbz_shape_info_offset = 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0
                    entry_info, header, string_table, data_entry, data = b'', b'', b'', b'', b''
                    # MTRL layer values
                    type_layer_new_offsets = [0, 0, 0, 0, 0, 0, 0, 0]
                    # TXAN values
                    txan_entry = VEV.sprp_file.type_entry[b"TXAN"]
                    txan_name_offset_assigned = []
                    for _ in range(0, txan_entry.data_count):
                        txan_name_offset_assigned.append(False)

                    # ------------------
                    # --- Write TX2D ---
                    # ------------------
                    with open(VEV.vram_file_path_modified, mode="wb") as output_vram_file:

                        # Get the number of textures
                        num_textures = self.listView.model().rowCount()

                        # Get each data_entry (TX2D) and store the texture properties
                        for i in range(0, num_textures):

                            # Get the texture from the tool
                            tx2d_data_entry = self.listView.model().item(i, 0).data()

                            # Write the name for each texture
                            name = tx2d_data_entry.data_info.name + "." + tx2d_data_entry.data_info.extension
                            string_table += b'\x00' + name.encode('utf-8')
                            string_table_size += 1 + len(name)

                            # Write the data_entry for each texture
                            data_entry += tx2d_data_entry.data_type
                            data_entry += i.to_bytes(4, 'big')
                            tx2d_data_entry.data_info.new_name_offset = string_name_offset
                            data_entry += tx2d_data_entry.data_info.new_name_offset.to_bytes(4, 'big')
                            data_entry += data_offset.to_bytes(4, 'big')
                            data_entry += tx2d_data_entry.data_info.data_size.to_bytes(4, 'big')
                            data_entry += b'\x00\x00\x00\x00'
                            data_entry += b'\x00\x00\x00\x00'
                            data_entry += b'\x00\x00\x00\x00'
                            data_entry_size += 32

                            # Write the data for each texture
                            # Get the tx2d info
                            tx2d_info = tx2d_data_entry.data_info.data
                            data += tx2d_info.unk0x00.to_bytes(4, 'big')
                            data += output_vram_file.tell().to_bytes(4, 'big')
                            data += tx2d_info.unk0x08.to_bytes(4, 'big')
                            data += tx2d_info.data_size.to_bytes(4, 'big')
                            data += tx2d_info.width.to_bytes(2, 'big')
                            data += tx2d_info.height.to_bytes(2, 'big')
                            data += tx2d_info.unk0x14.to_bytes(2, 'big')
                            data += tx2d_info.mip_maps.to_bytes(2, 'big')
                            data += tx2d_info.unk0x18.to_bytes(4, 'big')
                            data += tx2d_info.unk0x1c.to_bytes(4, 'big')
                            data += tx2d_info.dxt_encoding.to_bytes(1, 'big')
                            data += b'\00\00\00'
                            data_size += tx2d_data_entry.data_info.data_size

                            # Check if the data, the module of 16 is 0
                            data, data_size = check_entry_module(data, data_size, 16)

                            # Update offsets for the next entry
                            string_name_offset = 1 + string_table_size
                            data_offset = data_size

                            # Write the textures in the vram file
                            # It's a DDS image
                            if tx2d_info.dxt_encoding != 0:
                                output_vram_file.write(tx2d_info.tx2d_vram.data[128:])
                                # Write the vram separator
                                if i < num_textures - 1:
                                    write_separator_vram(output_vram_file, tx2d_data_entry)
                            # It's a BMP image
                            else:

                                if tx2d_data_entry.data_info.extension != "png":
                                    # We're dealing with a shader. We have to change the endian
                                    if tx2d_info.height == 1:
                                        output_vram_file.write(change_endian(tx2d_info.
                                                                             tx2d_vram.data[54:]))
                                    else:
                                        output_vram_file.write(tx2d_info.tx2d_vram.data[54:])
                                else:
                                    # Write in disk the data swizzled
                                    with open("tempSwizzledImage", mode="wb") as file:
                                        file.write(tx2d_info.tx2d_vram.data)

                                    # Write in disk the data unswizzled
                                    with open("tempUnSwizzledImage", mode="wb") as file:
                                        file.write(tx2d_info.tx2d_vram.data_unswizzle[54:])

                                    # Write in disk the indexes
                                    with open("Indexes.txt", mode="w") as file:
                                        for index in tx2d_info.tx2d_vram.\
                                                indexes_unswizzle_algorithm:
                                            file.write(index + ";")

                                    # Run the exe file of 'swizzle.exe' with the option '-s' to swizzle the image
                                    args = os.path.join(VEV.swizzle_path) + " \"" + \
                                        "tempSwizzledImage" + "\" \"" + \
                                        "tempUnSwizzledImage" + "\" \"" + "Indexes.txt" + "\" \"" + "-s" + "\""
                                    os.system('cmd /c ' + args)

                                    # Get the data from the .exe
                                    with open("tempSwizzledImageModified", mode="rb") as file:
                                        tx2d_info.tx2d_vram.data = file.read()

                                    # Remove the temp files
                                    os.remove("tempSwizzledImage")
                                    os.remove("tempUnSwizzledImage")
                                    os.remove("Indexes.txt")
                                    os.remove("tempSwizzledImageModified")

                                    output_vram_file.write(tx2d_info.tx2d_vram.data)

                        # Get the new vram size by getting the position of the pointer in the output file
                        # since it's in the end of the file
                        vram_data_size = output_vram_file.tell()

                        # Update the entry info
                        entry_info += b'TX2D' + b'\x00\x01\x00\x00' + num_textures.to_bytes(4, 'big')
                        # Update the sizes
                        entry_count += 1
                        entry_info_size += 12

                    # ------------------
                    # --- Write MTRL ---
                    # ------------------
                    # If there is MTRL, we write SHAP, VBUF, SCNE, BONE, DRVN and TXAN
                    if b'MTRL' in VEV.sprp_file.type_entry:
                        num_material = self.materialVal.count()
                        num_layer_effect = self.typeVal.count()

                        # Write each type layer effect
                        for i in range(1, num_layer_effect):
                            # Get the layer from the tool
                            layer_effect_name = self.typeVal.itemText(i)

                            # Write the name for each layer effect
                            type_layer_new_offsets[i] = string_name_offset
                            string_table += b'\x00' + layer_effect_name.encode('utf-8')
                            string_table_size += 1 + len(layer_effect_name)

                            # Update the offset
                            string_name_offset = 1 + string_table_size

                        # Write the 'DbzCharMtrl'
                        dbz_char_mtrl_offset = string_name_offset
                        string_table += b'\x00' + "DbzCharMtrl".encode('utf-8')
                        string_table_size += 1 + len("DbzCharMtrl")
                        # Update the offset
                        string_name_offset = 1 + string_table_size

                        # Write each material
                        for i in range(0, num_material):
                            # Get the material from the tool
                            mtrl_data_entry = self.materialVal.itemData(i)

                            # Write the name for each material
                            string_table += b'\x00' + mtrl_data_entry.data_info.name.encode('utf-8')
                            string_table_size += 1 + len(mtrl_data_entry.data_info.name)

                            # Write the data_entry for each material
                            data_entry += mtrl_data_entry.data_type
                            data_entry += i.to_bytes(4, 'big')
                            data_entry += string_name_offset.to_bytes(4, 'big')
                            data_entry += data_offset.to_bytes(4, 'big')
                            data_entry += mtrl_data_entry.data_info.data_size.to_bytes(4, 'big')
                            data_entry += mtrl_data_entry.data_info.child_count.to_bytes(4, 'big')
                            # The child offset will be calculated later

                            # Write the data for each material
                            mtrl_info = mtrl_data_entry.data_info.data
                            data += mtrl_info.unk_00
                            for layer in mtrl_info.layers:
                                # Search for the layer type assigned to the material
                                data += type_layer_new_offsets[self.typeVal.findData(layer.layer_name_offset)]\
                                    .to_bytes(4, 'big')
                                # Search for the texture assigned to the material
                                if layer.source_name_offset == 0:
                                    data += b'\00\00\00\00'
                                else:
                                    found = False
                                    # Search the texture
                                    for j in range(0, num_textures):
                                        tx2d_data_entry = self.listView.model().item(j, 0).data()
                                        if tx2d_data_entry.data_info.name_offset == layer.source_name_offset:
                                            data += tx2d_data_entry.data_info.new_name_offset.to_bytes(4, 'big')
                                            break
                                    # Search in the TXAN entries
                                    if not found:
                                        txan_entry = VEV.sprp_file.type_entry[b"TXAN"]
                                        for j in range(0, txan_entry.data_count):
                                            txan_data_entry = txan_entry.data_entry[j]
                                            if txan_data_entry.data_info.name_offset == layer.source_name_offset:
                                                # The TXAN wasn't added to the string name, so the name offset
                                                # will be calculated
                                                if not txan_name_offset_assigned[j]:
                                                    name = txan_data_entry.data_info.name + "." + \
                                                           txan_data_entry.data_info.extension
                                                    string_name_offset = 1 + string_table_size
                                                    txan_data_entry.data_info.new_name_offset = string_name_offset
                                                    string_table += b'\x00' + name.encode('utf-8')
                                                    string_table_size += 1 + len(name)
                                                    txan_name_offset_assigned[j] = True
                                                data += txan_data_entry.data_info.new_name_offset.to_bytes(4, 'big')
                                                break
                            data_size += mtrl_data_entry.data_info.data_size

                            # Write the children material (if any)
                            if mtrl_data_entry.data_info.child_count > 0:
                                data_child, data_child_size, data_offset = write_children(mtrl_data_entry.data_info,
                                                                                          b'MTRL', data_size,
                                                                                          map1_offset,
                                                                                          dbz_char_mtrl_offset,
                                                                                          dbz_edge_info_offset,
                                                                                          dbz_shape_info_offset)

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
                            data, data_size = check_entry_module(data, data_size, 16)

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
                        # Get the type entry shap
                        shap_type_entry = VEV.sprp_file.type_entry[b'SHAP']

                        # Write the 'map1'
                        map1_offset = string_name_offset
                        string_table += b'\x00' + "map1".encode('utf-8')
                        string_table_size += 1 + len("map1")
                        # Update the offset
                        string_name_offset = 1 + string_table_size

                        # Write the 'DbzEdgeInfo'
                        dbz_edge_info_offset = string_name_offset
                        string_table += b'\x00' + "DbzEdgeInfo".encode('utf-8')
                        string_table_size += 1 + len("DbzEdgeInfo")
                        # Update the offset
                        string_name_offset = 1 + string_table_size

                        # Write the 'DbzShapeInfo'
                        dbz_shape_info_offset = string_name_offset
                        string_table += b'\x00' + "DbzShapeInfo".encode('utf-8')
                        string_table_size += 1 + len("DbzShapeInfo")
                        # Update the offset
                        string_name_offset = 1 + string_table_size

                        # Get each shape data entry
                        for i in range(0, shap_type_entry.data_count):
                            # Get the data entry for the SHAP
                            shap_data_entry = shap_type_entry.data_entry[i]

                            # Write the name for each shape
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
                                data_child, data_child_size, data_offset = write_children(shap_data_entry.data_info,
                                                                                          b'SHAP', data_size,
                                                                                          map1_offset,
                                                                                          dbz_char_mtrl_offset,
                                                                                          dbz_edge_info_offset,
                                                                                          dbz_shape_info_offset)

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
                            data, data_size = check_entry_module(data, data_size, 16)

                            # Update offsets for the next entry
                            string_name_offset = 1 + string_table_size
                            data_offset = data_size

                        # Update the entry info
                        entry_info += b'SHAP' + b'\x00\x00\x00\x05' + shap_type_entry.data_count.to_bytes(4, 'big')
                        # Update the sizes
                        entry_count += 1
                        entry_info_size += 12

                        # ------------------
                        # --- Write VBUF ---
                        # ------------------
                        # Get the type entry shap
                        vbuf_type_entry = VEV.sprp_file.type_entry[b'VBUF']

                        # Get each vbuf data entry
                        for i in range(0, vbuf_type_entry.data_count):
                            # Get the data entry for the VBUF
                            vbuf_data_entry = vbuf_type_entry.data_entry[i]

                            # Write the name for each vbuf
                            string_table += b'\x00' + vbuf_data_entry.data_info.name.encode('utf-8')
                            string_table_size += 1 + len(vbuf_data_entry.data_info.name)

                            # Write each vertexDecl first
                            vbuf_info = vbuf_data_entry.data_info.data
                            data_offset_vertex_decl = data_size
                            for j in range(0, vbuf_info.decl_count_0):

                                vertex_decl = vbuf_info.vertex_decl[j]

                                # Read all the data
                                data += vertex_decl.unk0x00
                                data += vertex_decl.resource_name_offset.to_bytes(4, 'big')
                                data += vertex_decl.vertex_usage
                                data += vertex_decl.index.to_bytes(2, 'big')
                                data += vertex_decl.vertex_format
                                data += vertex_decl.stride.to_bytes(2, 'big')
                                data += vertex_decl.offset.to_bytes(4, 'big')
                                data_size += 20

                            # Check if the data, the module of 16 is 0
                            data, data_size = check_entry_module(data, data_size, 16)

                            # Write the data_entry for each vbuf
                            data_offset = data_size
                            data_entry += vbuf_data_entry.data_type
                            data_entry += i.to_bytes(4, 'big')
                            data_entry += string_name_offset.to_bytes(4, 'big')
                            data_entry += data_offset.to_bytes(4, 'big')
                            data_entry += vbuf_data_entry.data_info.data_size.to_bytes(4, 'big')
                            data_entry += b'\x00\x00\x00\x00'
                            data_entry += b'\x00\x00\x00\x00'
                            data_entry += b'\x00\x00\x00\x00'
                            data_entry_size += 32

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

                            # Check if the data, the module of 16 is 0
                            data, data_size = check_entry_module(data, data_size, 16)

                            # Update offsets for the next entry
                            string_name_offset = 1 + string_table_size
                            data_offset = data_size

                        # Update the entry info
                        entry_info += b'VBUF' + b'\x00\x00\x00\x0A' + vbuf_type_entry.data_count.to_bytes(4, 'big')
                        # Update the sizes
                        entry_count += 1
                        entry_info_size += 12

                    # Write the basename, ioram and vram offsets names
                    name_offset = 1 + string_table_size
                    name = self.fileNameText.text() + ".spr"
                    string_table += b'\x00' + name.encode('utf-8')
                    string_table_size += 1 + len(name)
                    # If the spr doesn't have an ioram file, we won't write the name on it
                    if VEV.sprp_file.sprp_header.ioram_data_size > 0:
                        ioram_name_offset = 1 + string_table_size
                        ioram_data_size = VEV.sprp_file.sprp_header.ioram_data_size
                        name = self.fileNameText.text() + ".ioram"
                        string_table += b'\x00' + name.encode('utf-8')
                        string_table_size += 1 + len(name)
                    else:
                        ioram_name_offset = 0
                        ioram_data_size = 0
                    vram_name_offset = 1 + string_table_size
                    name = self.fileNameText.text() + ".vram"
                    string_table += b'\x00' + name.encode('utf-8')
                    string_table_size += 1 + len(name)

                    # Check if the entry_info, the module of 16 is 0
                    entry_info, entry_info_size = check_entry_module(entry_info, entry_info_size, 16)

                    # Check if the string_table_size, the module of 16 is 0
                    string_table, string_table_size = check_entry_module(string_table, string_table_size, 16)

                    # Create the header
                    header = VEV.sprp_file.sprp_header.data_tag + b'\00\01\00\01' + entry_count.to_bytes(4, 'big') + \
                        b'\00\00\00\00' + name_offset.to_bytes(4, 'big') + entry_info_size.to_bytes(4, 'big') + \
                        string_table_size.to_bytes(4, 'big') + data_entry_size.to_bytes(4, 'big') + \
                        data_size.to_bytes(4, 'big') + ioram_name_offset.to_bytes(4, 'big') + \
                        ioram_data_size.to_bytes(4, 'big') + vram_name_offset.to_bytes(4, 'big') + \
                        vram_data_size.to_bytes(4, 'big') + b'\00\00\00\00\00\00\00\00\00\00\00\00'

                    # Write the spr
                    with open(VEV.spr_file_path_modified, mode="wb") as output_spr_file:
                        output_spr_file.write(header + entry_info + string_table + data_entry + data)

                    '''
                    # Get all the necessary info from the original spr. The new info from spr and vram will be
                    # written from scratch (except the data itself stored in spr file)
                    with open(VEV.spr_file_path, mode="rb") as input_sprp_file:

                        # Header of the spr file (64 first bytes)
                        header = input_sprp_file.read(VEV.sprp_file.entry_info_base)

                        # Where the entries are located
                        entry_info = input_sprp_file.read(VEV.sprp_file.sprp_header.entry_info_size)

                        # Where the names are located.
                        string_table = input_sprp_file.read(VEV.sprp_file.sprp_header.string_table_size)
                        string_table_size = VEV.sprp_file.sprp_header.string_table_size

                        # Get each data entry divided in tx2d, mtrl and the rest of data entries
                        tx2d_data_info_size = VEV.sprp_file.type_entry[b'TX2D'].data_count * 32
                        num_textures = self.listView.model().rowCount()
                        # Update the entry_info_base for tx2d
                        entry_info = entry_info[:8] + num_textures.to_bytes(4, 'big') + entry_info[12:]
                        if b'MTRL' in VEV.sprp_file.type_entry:
                            mtrl_data_info_size = VEV.sprp_file.type_entry[b'MTRL'].data_count * 32
                            num_material = self.materialVal.count()
                            # Update the entry_info_base for mtrl
                            entry_info = entry_info[:20] + num_material.to_bytes(4, 'big') + entry_info[24:]
                        else:
                            mtrl_data_info_size = 0
                            num_material = 0
                        input_sprp_file.seek(tx2d_data_info_size + mtrl_data_info_size, os.SEEK_CUR)
                        rest_data_info_size = VEV.sprp_file.sprp_header.data_info_size - (tx2d_data_info_size +
                                                                                          mtrl_data_info_size)
                        rest_data_info = input_sprp_file.read(rest_data_info_size)

                        # Get all the data
                        input_sprp_file.seek(VEV.sprp_file.data_block_base)
                        data_block = input_sprp_file.read()
                        data_block_size = input_sprp_file.tell() - VEV.sprp_file.data_block_base

                    # Create the new vram
                    tx2d_data_entry = b''
                    mtrl_data_entry = b''
                    data_info_size = ((num_textures + num_material) * 32) + rest_data_info_size
                    data_block_base = VEV.string_table_size_increment + VEV.sprp_file.data_info_base + data_info_size
                    spr_new_size = data_block_base + data_block_size
                    with open(VEV.vram_file_path_modified, mode="wb") as output_vram_file:

                        # Get each data_entry (TX2D) and store the texture properties
                        for i in range(0, num_textures):

                            # Get the texture from the tool
                            data_entry = self.listView.model().item(i, 0).data()

                            # Create the tx2d_data_entry for each texture
                            tx2d_data_entry += data_entry.data_type
                            tx2d_data_entry += data_entry.index.to_bytes(4, 'big')

                            # Calculate the name_offset and data_offset only when is a brand new texture
                            # Also calculate the new size of the spr
                            if data_entry.new_entry:

                                aux_name_offset = data_entry.data_info.name_offset

                                # Calculate the name offset for the file
                                data_entry.data_info.name_offset = 1 + string_table_size

                                # Change the offset also in the combo box
                                self.textureVal.setItemData(self.textureVal.findData(aux_name_offset),
                                                            data_entry.data_info.name_offset)

                                # Search the material layer that is using this brand new texture (if exists)
                                for j in range(0, num_material):
                                    temp_mtrl_data_entry = self.materialVal.itemData(j)
                                    for k in range(0, 10):
                                        # Get the layer from one material and check if the texture is aiming is the
                                        # same as the brand new texture
                                        layer = temp_mtrl_data_entry.data_info.data.layers[k]
                                        if layer.source_name_offset == aux_name_offset:
                                            layer.source_name_offset = data_entry.data_info.name_offset

                                # Calculate the data offset
                                data_entry.data_info.data_offset = data_block_size
                                string_table_size += 1 + data_entry.data_info.name_size
                                data_block_size += data_entry.data_info.data_size + 12
                                spr_new_size += data_entry.data_info.data_size + 12

                            tx2d_data_entry += data_entry.data_info.name_offset.to_bytes(4, 'big')
                            tx2d_data_entry += data_entry.data_info.data_offset.to_bytes(4, 'big')
                            tx2d_data_entry += data_entry.data_info.data_size.to_bytes(4, 'big')
                            tx2d_data_entry += data_entry.data_info.child_count.to_bytes(4, 'big')
                            tx2d_data_entry += data_entry.data_info.child_offset.to_bytes(4, 'big')
                            for _ in range(4):
                                tx2d_data_entry += b'\x00'

                            # Create the tx2d_data for each texture
                            tx2d_data = b''
                            tx2d_data += data_entry.data_info.data.unk0x00.to_bytes(4, 'big')
                            tx2d_data += output_vram_file.tell().to_bytes(4, 'big')
                            tx2d_data += data_entry.data_info.data.unk0x08.to_bytes(4, 'big')
                            tx2d_data += data_entry.data_info.data.data_size.to_bytes(4, 'big')
                            tx2d_data += data_entry.data_info.data.width.to_bytes(2, 'big')
                            tx2d_data += data_entry.data_info.data.height.to_bytes(2, 'big')
                            tx2d_data += data_entry.data_info.data.unk0x14.to_bytes(2, 'big')
                            tx2d_data += data_entry.data_info.data.mip_maps.to_bytes(2, 'big')
                            tx2d_data += data_entry.data_info.data.unk0x18.to_bytes(4, 'big')
                            tx2d_data += data_entry.data_info.data.unk0x1c.to_bytes(4, 'big')
                            tx2d_data += data_entry.data_info.data.dxt_encoding.to_bytes(1, 'big')
                            for _ in range(15):
                                tx2d_data += b'\x00'
                            # Replace the tx2d_data in the original spr file
                            if not data_entry.new_entry:
                                data_block = data_block[:data_entry.data_info.data_offset] + tx2d_data + \
                                    data_block[data_entry.data_info.data_offset + 48:]
                            # The texture is a new one for the spr, we append it to the end of the file
                            else:
                                name = data_entry.data_info.name + "." + data_entry.data_info.extension
                                string_table += b'\x00' + name.encode('utf-8')
                                data_block += tx2d_data

                            # Write the textures in the vram file
                            # It's a DDS image
                            if data_entry.data_info.data.dxt_encoding != 0:
                                output_vram_file.write(data_entry.data_info.data.tx2d_vram.data[128:])
                                # Write the vram separator
                                if i < num_textures - 1:
                                    write_separator_vram(output_vram_file, data_entry)
                            # It's a BMP image
                            else:

                                if data_entry.data_info.extension != "png":
                                    # We're dealing with a shader. We have to change the endian
                                    if data_entry.data_info.data.height == 1:
                                        output_vram_file.write(change_endian(data_entry.data_info.data.
                                                                             tx2d_vram.data[54:]))
                                    else:
                                        output_vram_file.write(data_entry.data_info.data.tx2d_vram.data[54:])
                                else:
                                    # Write in disk the data swizzled
                                    with open("tempSwizzledImage", mode="wb") as file:
                                        file.write(data_entry.data_info.data.tx2d_vram.data)

                                    # Write in disk the data unswizzled
                                    with open("tempUnSwizzledImage", mode="wb") as file:
                                        file.write(data_entry.data_info.data.tx2d_vram.data_unswizzle[54:])

                                    # Write in disk the indexes
                                    with open("Indexes.txt", mode="w") as file:
                                        for index in data_entry.data_info.data.tx2d_vram.indexes_unswizzle_algorithm:
                                            file.write(index + ";")

                                    # Run the exe file of 'swizzle.exe' with the option '-s' to swizzle the image
                                    args = os.path.join(VEV.swizzle_path) + " \"" + \
                                        "tempSwizzledImage" + "\" \"" + \
                                        "tempUnSwizzledImage" + "\" \"" + "Indexes.txt" + "\" \"" + "-s" + "\""
                                    os.system('cmd /c ' + args)

                                    # Get the data from the .exe
                                    with open("tempSwizzledImageModified", mode="rb") as file:
                                        data_entry.data_info.data.tx2d_vram.data = file.read()

                                    # Remove the temp files
                                    os.remove("tempSwizzledImage")
                                    os.remove("tempUnSwizzledImage")
                                    os.remove("Indexes.txt")
                                    os.remove("tempSwizzledImageModified")

                                    output_vram_file.write(data_entry.data_info.data.tx2d_vram.data)

                        # Get the new vram size by getting the position of the pointer in the output file
                        # since it's in the end of the file
                        vram_new_size = output_vram_file.tell()

                    # Get each data_entry (MTRL) and store the material properties
                    for i in range(0, num_material):

                        # Get the material from the tool
                        data_entry = self.materialVal.itemData(i)

                        # Create the mtrl_data_entry for each material
                        mtrl_data_entry += data_entry.data_type
                        mtrl_data_entry += data_entry.index.to_bytes(4, 'big')

                        # Calculate the name_offset and data_offset only when is a brand new material
                        # Also calculate the new size of the spr
                        if data_entry.new_entry:

                            aux_name_offset = data_entry.data_info.name_offset

                            # Calculate the name offset for the file
                            data_entry.data_info.name_offset = 1 + string_table_size

                            # Change the offset also in the combo box
                            self.materialModelPartVal.setItemData(
                                self.materialModelPartVal.findData(aux_name_offset),
                                data_entry.data_info.name_offset)

                            # Search the model part that is using this brand new material (if exists)
                            for j in range(0, self.modelPartVal.count()):
                                scene_data_info_children = self.modelPartVal.itemData(j)
                                if scene_data_info_children.data.name_offset == aux_name_offset:
                                    scene_data_info_children.data.name_offset = data_entry.data_info.name_offset

                            # Calculate the offsets for the new material
                            data_entry.data_info.data_offset = data_block_size
                            data_entry.data_info.child_offset = data_entry.data_info.data_offset + \
                                data_entry.data_info.data_size + data_entry.data_info.child_info[0].data_size

                            string_table_size += 1 + data_entry.data_info.name_size
                            data_block_size += data_entry.data_info.data_size + \
                                data_entry.data_info.child_info[0].data_size + 32
                            spr_new_size += data_entry.data_info.data_size + \
                                data_entry.data_info.child_info[0].data_size + 32

                        mtrl_data_entry += data_entry.data_info.name_offset.to_bytes(4, 'big')
                        mtrl_data_entry += data_entry.data_info.data_offset.to_bytes(4, 'big')
                        mtrl_data_entry += data_entry.data_info.data_size.to_bytes(4, 'big')
                        mtrl_data_entry += data_entry.data_info.child_count.to_bytes(4, 'big')
                        mtrl_data_entry += data_entry.data_info.child_offset.to_bytes(4, 'big')
                        for _ in range(4):
                            mtrl_data_entry += b'\x00'

                        # Create the mtrl_data for each material layer
                        mtrl_data = b''
                        mtrl_data += data_entry.data_info.data.unk_00
                        # Write each layer from one material
                        for j in range(0, 10):
                            layer = data_entry.data_info.data.layers[j]
                            mtrl_data += layer.layer_name_offset.to_bytes(4, 'big')
                            mtrl_data += layer.source_name_offset.to_bytes(4, 'big')

                        # Write the children material (if any)
                        if data_entry.data_info.child_count > 0:
                            # Get the data_info from the parent data_info
                            data_info_children = data_entry.data_info.child_info[0]

                            # Raging Blast 2 material children
                            if data_info_children.data_size == 96:
                                mtrl_prop = data_info_children.data
                                mtrl_data += struct.pack('>f', mtrl_prop.Ilumination_Shadow_orientation)
                                mtrl_data += struct.pack('>f', mtrl_prop.Ilumination_Light_orientation_glow)
                                for k in range(len(mtrl_prop.unk0x04)):
                                    mtrl_data += struct.pack('>f', mtrl_prop.unk0x04[k])
                                mtrl_data += struct.pack('>f', mtrl_prop.Brightness_purple_light_glow)
                                mtrl_data += struct.pack('>f', mtrl_prop.Saturation_glow)
                                mtrl_data += struct.pack('>f', mtrl_prop.Saturation_base)
                                mtrl_data += \
                                    struct.pack('>f', mtrl_prop.Brightness_toonmap_active_some_positions)
                                mtrl_data += struct.pack('>f', mtrl_prop.Brightness_toonmap)
                                mtrl_data += \
                                    struct.pack('>f', mtrl_prop.Brightness_toonmap_active_other_positions)
                                mtrl_data += \
                                    struct.pack('>f', mtrl_prop.Brightness_incandescence_active_some_positions)
                                mtrl_data += struct.pack('>f', mtrl_prop.Brightness_incandescence)
                                mtrl_data += \
                                    struct.pack('>f', mtrl_prop.Brightness_incandescence_active_other_positions)
                                for k in range(len(mtrl_prop.Border_RGBA)):
                                    mtrl_data += struct.pack('>f', mtrl_prop.Border_RGBA[k])
                                for k in range(len(mtrl_prop.unk0x44)):
                                    mtrl_data += struct.pack('>f', mtrl_prop.unk0x44[k])
                                for k in range(len(mtrl_prop.unk0x50)):
                                    mtrl_data += struct.pack('>f', mtrl_prop.unk0x50[k])
                            else:
                                mtrl_data += data_info_children.data

                            mtrl_data += VEV.DbzCharMtrl_offset.to_bytes(4, 'big')
                            mtrl_data += (data_entry.data_info.data_offset + 192).to_bytes(4, 'big')
                            mtrl_data += data_info_children.data_size.to_bytes(4, 'big')
                            mtrl_data += data_info_children.child_count.to_bytes(4, 'big')
                            mtrl_data += data_info_children.child_offset.to_bytes(4, 'big')
                            for _ in range(12):
                                mtrl_data += b'\x00'
                            material_total_size = data_entry.data_info.data_size + data_info_children.data_size + 32
                        else:
                            material_total_size = data_entry.data_info.data_size

                        if not data_entry.new_entry:
                            data_block = data_block[:data_entry.data_info.data_offset] + mtrl_data + \
                                         data_block[data_entry.data_info.data_offset + material_total_size:]
                        else:
                            string_table += b'\x00' + data_entry.data_info.name.encode('utf-8')
                            data_block += mtrl_data

                    # Write the scne material data info name offset to the file
                    for i in range(0, self.modelPartVal.count()):
                        data_info_children = self.modelPartVal.itemData(i)
                        data_offset = data_info_children.data_offset
                        data_block = data_block[:data_offset] + \
                            data_info_children.data.name_offset.to_bytes(4, 'big') + data_block[data_offset+4:]

                    # Create the new spr file
                    # Check if the string_table_size, the module of 16 is 0
                    rest = 16 - (string_table_size % 16)
                    if rest != 16:
                        for i in range(rest):
                            string_table += b'\00'
                            string_table_size += 1
                    # Update the header
                    header = header[:24] + string_table_size.to_bytes(4, 'big') + data_info_size.to_bytes(4, 'big') + \
                        data_block_size.to_bytes(4, 'big') + header[36:48] + vram_new_size.to_bytes(4, 'big') + \
                        header[52:]
                    with open(VEV.spr_file_path_modified, mode="wb") as output_spr_file:
                        output_spr_file.write(header + entry_info + string_table + tx2d_data_entry + mtrl_data_entry +
                                              rest_data_info + data_block)

                    '''
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
                                pack_and_save_file(self, path_output_file)

                            # If the user has edited one character, we will save the file
                            elif GPV.character_list_edited:

                                # --- operate_resident_param ---
                                if GPV.operate_resident_param_file:
                                    # Open the files
                                    subpak_file_character_inf = open(GPV.resident_character_inf_path, mode="rb+")
                                    subpak_file_transformer_i = open(GPV.resident_transformer_i_path, mode="rb+")

                                    print("Writing values in the file...")
                                    # Change the transformations in the file
                                    for character in GPV.character_list_edited:
                                        # Save all the info for each character
                                        write_operate_resident_param(character, subpak_file_character_inf,
                                                                     subpak_file_transformer_i)

                                    # Close the files
                                    subpak_file_character_inf.close()
                                    subpak_file_transformer_i.close()

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
                                pack_and_save_file(self, path_output_file)

                            # --- cs_chip ---
                            # If the user has edited one character, we will save the file
                            elif REV.slots_edited:

                                # Save all the info
                                print("Writing values in the file...")
                                write_cs_chip_file()

                                # Pack the files
                                print("Packing the file...")
                                pack_and_save_file(self, path_output_file)

                            else:
                                msg = QMessageBox()
                                msg.setWindowTitle("Warning")
                                msg.setWindowIcon(self.ico_image)
                                msg.setText("The file hasn't been modified.")
                                msg.exec()

                        # The user wants to save the values only from the 'pak explorer'
                        elif answer == msg.No:
                            print("Packing the file...")
                            pack_and_save_file(self, path_output_file)

                # We save the data from the 'pak explorer' tab
                elif self.pak_explorer.isEnabled():
                    print("Packing the file...")
                    pack_and_save_file(self, path_output_file)
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Warning")
                    msg.setWindowIcon(self.ico_image)
                    msg.setText("No pak file has been loaded.")
                    msg.exec()

    def closeEvent(self, event):
        if os.path.exists(VEV.temp_folder):
            rmtree(VEV.temp_folder, onerror=del_rw)
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
            "<li><b>Raging tools 1.6.1</b> by "
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
                    '<li>To <b>revelation (revel8n) </b> from <a href=https://forum.xentax.com>XeNTaX</a> '
                    'forum who made the compress/uncompress tool <i>dbrb_compressor.exe</i>.</li>'
                    '<li>To <b>316austin316</b> for contributing to the tool.</li>'
                    '<li>To <b>SSJLVegeta</b> for contributing to the tool.</li>'
                    '<li>To the <a ''href=https://discord.gg/JpCvDCgpnb>Raging Blast Modding community</a>.</li>'
                    '</ul>')
        msg.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.ico_image = QtGui.QIcon("lib/design/Raging_Tools/Raging_Tools.ico")
    window.setWindowIcon(window.ico_image)
    window.selectCharaWindow.setWindowIcon(window.ico_image)
    window.selectCharaRosterWindow.setWindowIcon(window.ico_image)
    window.MaterialChildEditorWindow.setWindowIcon(window.ico_image)
    window.show()
    app.exec_()
