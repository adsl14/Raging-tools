from lib.character_parameters_editor.IPF import write_single_character_parameters
from lib.character_parameters_editor.GPF import write_character_parameters
from lib.character_parameters_editor.REF import write_cs_chip_file
from lib.character_parameters_editor.GPV import GPV
from lib.character_parameters_editor.REV import REV
from lib.design.Raging_tools import *
from lib.packages import os, rmtree, QFileDialog, copyfile, \
    move, QMessageBox
from lib.functions import del_rw

# vram explorer
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.VEF import change_endian, load_data_to_ve, update_tx2d_data
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
        initialize_ve(self)

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
                    msg.setText("A spr file is needed.")
                    msg.exec()
                    return

                # Load all the data to the vram_explorer from the spr and vram files
                load_data_to_ve(self)

    def action_save_logic(self):

        extension_pak = "Pack files ()"
        extension_spr_vram = "Info/Texture files ()"

        # Ask to the user where to save the file
        path_output_file = os.path.splitext(MainWindow.old_path_file)[0]
        path_output_file, extension = QFileDialog.getSaveFileName(self,
                                                                  "Save file", path_output_file,
                                                                  extension_pak + ";;" + extension_spr_vram)

        # The user has selected a path
        if path_output_file:

            # Save spr_vram in a folder
            if extension == extension_spr_vram:

                if not VEV.sprp_file.type_entry:
                    msg = QMessageBox()
                    msg.setWindowTitle("Warning")
                    msg.setText("There is no file loaded.")
                    msg.exec()
                elif not VEV.textures_index_edited:
                    msg = QMessageBox()
                    msg.setWindowTitle("Warning")
                    msg.setText("The file hasn't been modified.")
                    msg.exec()
                else:

                    # Create the folder where we save the modified files
                    if not os.path.exists(path_output_file):
                        os.mkdir(path_output_file)

                    # Default paths
                    spr_export_path = VEV.spr_file_path.replace(".spr", "_m.spr")
                    vram_export_path = VEV.vram_file_path.replace(".vram", "_m.vram")

                    # Sort the indexes of the modified textures
                    VEV.textures_index_edited.sort()

                    # Create a copy of the original file
                    copyfile(VEV.spr_file_path, spr_export_path)

                    # replacing textures (vram)
                    with open(vram_export_path, mode="wb") as output_file:
                        with open(VEV.vram_file_path, mode="rb") as input_file:

                            # Get each offset texture and write over the original file
                            for texture_index in VEV.textures_index_edited:
                                tx2d_info = VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index].data_info.data
                                data = input_file.read(tx2d_info.data_offset_old - input_file.tell())
                                output_file.write(data)
                                input_file.seek(tx2d_info.data_size_old, os.SEEK_CUR)

                                # It's a DDS image
                                if tx2d_info.dxt_encoding != 0:
                                    output_file.write(VEV.sprp_file.type_entry[b'TX2D']
                                                      .data_entry[texture_index].data_info.data.tx2d_vram.data[128:])
                                else:

                                    if VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index].data_info\
                                     .extension != "png":
                                        # We're dealing with a shader. We have to change the endian
                                        if tx2d_info.height == 1:
                                            output_file.write(change_endian(VEV.sprp_file.type_entry[b'TX2D']
                                                                            .data_entry[texture_index].data_info
                                                                            .data.tx2d_vram.data[54:]))
                                        else:
                                            output_file.write(VEV.sprp_file.type_entry[b'TX2D']
                                                              .data_entry[texture_index].data_info.
                                                              data.tx2d_vram.data[54:])
                                    else:
                                        # Write in disk the data swizzled
                                        with open("tempSwizzledImage", mode="wb") as file:
                                            file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index]
                                                       .data_info.data.tx2d_vram.data)

                                        # Write in disk the data unswizzled
                                        with open("tempUnSwizzledImage", mode="wb") as file:
                                            file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index]
                                                       .data_info.data.tx2d_vram.data_unswizzle[54:])

                                        # Write in disk the indexes
                                        with open("Indexes.txt", mode="w") as file:
                                            for index in VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index]\
                                                 .data_info.data.tx2d_vram.indexes_unswizzle_algorithm:
                                                file.write(index + ";")

                                        # Run the exe file of 'swizzle.exe' with the option '-s' to swizzle the image
                                        args = os.path.join(VEV.swizzle_path) + " \"" + \
                                            "tempSwizzledImage" + "\" \"" + \
                                            "tempUnSwizzledImage" + "\" \"" + "Indexes.txt" + "\" \"" + "-s" + "\""
                                        os.system('cmd /c ' + args)

                                        # Get the data from the .exe
                                        with open("tempSwizzledImageModified", mode="rb") as file:
                                            VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index].data_info.data\
                                                .tx2d_vram.data = file.read()

                                        # Remove the temp files
                                        os.remove("tempSwizzledImage")
                                        os.remove("tempUnSwizzledImage")
                                        os.remove("Indexes.txt")
                                        os.remove("tempSwizzledImageModified")

                                        output_file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index]
                                                          .data_info.data.tx2d_vram.data)

                            # Write the rest of the data to the new file
                            data = input_file.read()
                            output_file.write(data)

                            # Get the new vram size by getting the position of the pointer in the output file
                            # since it's in the end of the file
                            vram_new_size = output_file.tell()

                    # Update the offsets (spr)
                    with open(spr_export_path, mode="rb+") as output_file_spr:

                        first_index_texture_edited = VEV.textures_index_edited[0]

                        # Move where the information starts to the first modified texture
                        output_file_spr.seek(VEV.sprp_file.data_base +
                                             VEV.sprp_file.type_entry[b'TX2D'].
                                             data_entry[first_index_texture_edited]
                                             .data_info.data_offset + 12)

                        # Update tx2d_data
                        update_tx2d_data(output_file_spr, first_index_texture_edited)

                        # Check if is the last texture modified and there is no more textures in the bottom
                        if first_index_texture_edited + 1 < VEV.sprp_file.type_entry[b'TX2D'].data_count:
                            # Get the quanty difference for the first texture modified
                            quanty_aux = VEV.vram_offset_quanty_difference[first_index_texture_edited]
                            for i in range(first_index_texture_edited+1, VEV.sprp_file.type_entry[b'TX2D'].data_count):

                                # Move where the information starts to the next textures
                                output_file_spr.seek(VEV.sprp_file.data_base + VEV.sprp_file.type_entry[b'TX2D']
                                                     .data_entry[i].data_info.data_offset + 4)
                                # Update the offset
                                output_file_spr.write(int(abs(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i]
                                                              .data_info
                                                              .data.data_offset + quanty_aux))
                                                      .to_bytes(4, byteorder="big"))
                                output_file_spr.seek(4, os.SEEK_CUR)

                                # Update tx2d_data
                                update_tx2d_data(output_file_spr, i)

                                # Increment the difference only if the difference is not 0 and reset the
                                # offset differency array
                                if VEV.vram_offset_quanty_difference[i] != 0:
                                    quanty_aux += VEV.vram_offset_quanty_difference[i]

                        # Change the header of pos 48 in spr file because in that place indicates the size of the
                        # final output file
                        output_file_spr.seek(48)
                        output_file_spr.write(vram_new_size.to_bytes(4, byteorder='big'))

                        # --- Update the data_info offsets when we remove a texture (this won't be used for now) ---
                        '''if VEV.textures_index_removed:

                            # Update each data_info
                            output_file_spr.seek(VEV.sprp_file.data_info_base)
                            reduce_index_quanty = 0
                            name_offset_quanty = 0
                            name_offsets_quanty_per_txt = {}
                            data_offset_quanty = 0
                            for type_entry in VEV.sprp_file.type_entry:
                                for i in range(0, VEV.sprp_file.type_entry[type_entry].data_count):

                                    data_entry = VEV.sprp_file.type_entry[type_entry].data_entry[i]

                                    if type_entry != b'TX2D':

                                        output_file_spr.seek(8, os.SEEK_CUR)

                                        # Update data_offset and child_offset
                                        update_offset_data_info(output_file_spr, data_entry,
                                                                name_offset_quanty,
                                                                data_offset_quanty)

                                        # Update the offsets of each layer
                                        if type_entry == b'MTRL':

                                            # Get the actual position of the file
                                            aux_pointer = output_file_spr.tell()

                                            # Move to the position where is located all the layers for the material
                                            # We add 112 at the end because the first 112 bytes are unk data
                                            output_file_spr.seek(data_entry.data_info.data_offset +
                                                                 VEV.sprp_file.data_base + 112)

                                            # Get one material
                                            mtrl_info = data_entry.data_info.data

                                            # Get each layer for the material
                                            for j in range(0, 10):

                                                # Get the layer
                                                layer = mtrl_info.layers[j]

                                                # Update source name offset only when the output his offset is not
                                                # 0
                                                if layer.source_name_offset != 0:

                                                    # is aiming to a texture
                                                    if layer.source_name_offset in name_offsets_quanty_per_txt:

                                                        relative_name_offset_per_txt = \
                                                            name_offsets_quanty_per_txt[layer.source_name_offset]

                                                        # We write the new offset only
                                                        new_offset = layer.source_name_offset + \
                                                            relative_name_offset_per_txt
                                                        # if it's positive, means we have to update the offsets since
                                                        # this materials are using textures that won't get removed
                                                        if new_offset > 0:
                                                            # Update layer name offset only when the output is positive
                                                            output_file_spr.write(int(layer.layer_name_offset +
                                                                                      name_offset_quanty)
                                                                                  .to_bytes(4, byteorder="big"))

                                                            output_file_spr.write(int(new_offset)
                                                                                  .to_bytes(4, byteorder="big"))
                                                        else:
                                                            output_file_spr.write(b'\00\00\00\00')
                                                            output_file_spr.write(b'\00\00\00\00')
                                                    else:
                                                        # Update layer name offset only when the output is positive
                                                        output_file_spr.write(int(layer.layer_name_offset +
                                                                                  name_offset_quanty)
                                                                              .to_bytes(4, byteorder="big"))
                                                        output_file_spr.seek(4, os.SEEK_CUR)
                                                else:
                                                    output_file_spr.seek(8, os.SEEK_CUR)

                                            # Restore the position of the file
                                            output_file_spr.seek(aux_pointer)

                                    else:

                                        # Save the accumulated offset for the name_offset.
                                        # Also, save the accumulated offset
                                        # but for each texture in a dictionary of name_offsets
                                        name_offset_quanty += VEV.relative_name_offset_quanty[i]
                                        name_offsets_quanty_per_txt[data_entry.data_info.name_offset] = \
                                            name_offset_quanty
                                        # Save the accumulated offset for the data_offset
                                        data_offset_quanty += VEV.relative_data_offset_quanty[i]

                                        # Update only the 'TX2D' entries that won't be removed
                                        if i not in VEV.textures_index_removed:

                                            if i > first_index_texture_edited:
                                                output_file_spr.seek(4, os.SEEK_CUR)
                                                # Update index
                                                output_file_spr.write((data_entry.index + reduce_index_quanty).
                                                                      to_bytes(4, byteorder="big"))

                                                # Update data_offset and child_offset
                                                update_offset_data_info(output_file_spr, data_entry,
                                                                        name_offset_quanty,
                                                                        data_offset_quanty)
                                            else:
                                                output_file_spr.seek(32, os.SEEK_CUR)

                                        else:
                                            reduce_index_quanty -= 1
                                            output_file_spr.seek(32, os.SEEK_CUR)

                            # Update the name_offset
                            output_file_spr.seek(16)
                            output_file_spr.write(int((VEV.sprp_file.sprp_header.name_offset +
                                                       name_offset_quanty))
                                                  .to_bytes(4, byteorder="big"))
                            # Update the string_table_size
                            output_file_spr.seek(4, os.SEEK_CUR)
                            output_file_spr.write(int((VEV.sprp_file.sprp_header.string_table_size +
                                                       name_offset_quanty))
                                                  .to_bytes(4, byteorder="big"))

                            # Update the data_info_size
                            output_file_spr.write(int((VEV.sprp_file.sprp_header.data_info_size +
                                                       VEV.relative_data_info_offset_quanty))
                                                  .to_bytes(4, byteorder="big"))

                            # Update the data_block_size
                            output_file_spr.write(int((VEV.sprp_file.sprp_header.data_block_size +
                                                       data_offset_quanty))
                                                  .to_bytes(4, byteorder="big"))

                            # Update the ioram_name_offset and vram_name_offset
                            output_file_spr.write(int((VEV.sprp_file.sprp_header.ioram_name_offset +
                                                       name_offset_quanty))
                                                  .to_bytes(4, byteorder="big"))
                            output_file_spr.seek(4, os.SEEK_CUR)
                            output_file_spr.write(int((VEV.sprp_file.sprp_header.vram_name_offset +
                                                       name_offset_quanty))
                                                  .to_bytes(4, byteorder="big"))

                            # Update type_entry data_count
                            output_file_spr.seek(VEV.sprp_file.type_info_base)
                            output_file_spr.seek(8, os.SEEK_CUR)
                            output_file_spr.write(int((VEV.sprp_file.type_entry[b'TX2D'].data_count -
                                                       len(VEV.textures_index_removed)))
                                                  .to_bytes(4, byteorder="big"))

                            # Recreate a new spr file with the removed data
                            output_file_spr.seek(0)
                            spr_export_path_rewrited = VEV.spr_file_path.replace(".spr", "_r.spr")
                            with open(spr_export_path_rewrited, mode="wb") as output_file_spr_r:

                                # New header
                                header = output_file_spr.read(VEV.sprp_file.string_base)

                                # New data
                                data_name = b''
                                data_info = b''
                                data = b''

                                # Create the new names for the textures
                                aux_pointer_data_name = VEV.sprp_file.string_base
                                aux_pointer_data_info = VEV.sprp_file.data_info_base
                                aux_pointer_data = VEV.sprp_file.data_base
                                for i in range(0, VEV.sprp_file.type_entry[b'TX2D'].data_count):

                                    name_size = VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.name_size

                                    if i not in VEV.textures_index_removed:
                                        # Store the name
                                        output_file_spr.seek(aux_pointer_data_name)
                                        data_name += output_file_spr.read(name_size)
                                        aux_pointer_data_name = output_file_spr.tell()

                                        # Store the data info
                                        output_file_spr.seek(aux_pointer_data_info)
                                        data_info += output_file_spr.read(32)
                                        aux_pointer_data_info = output_file_spr.tell()

                                        # Store the data
                                        data_size = VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data_size
                                        output_file_spr.seek(aux_pointer_data)
                                        data += output_file_spr.read(data_size + 12)
                                        aux_pointer_data = output_file_spr.tell()
                                    else:

                                        # Increase data_name offset aux
                                        aux_pointer_data_name += name_size

                                        # Increase data_info offset aux
                                        aux_pointer_data_info += 32

                                        # Store only the 12 bytes of data the texture
                                        data_size = VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data_size
                                        output_file_spr.seek(aux_pointer_data + data_size)
                                        data += output_file_spr.read(12)
                                        aux_pointer_data = output_file_spr.tell()

                                # Store the rest of the data_name
                                output_file_spr.seek(aux_pointer_data_name)
                                data_name += output_file_spr.read(VEV.sprp_file.data_info_base - output_file_spr.tell())

                                # Store the rest of the type_entries sections
                                output_file_spr.seek(aux_pointer_data_info)
                                data_info += output_file_spr.read(VEV.sprp_file.data_base - output_file_spr.tell())

                                # Store the rest of the data sections
                                output_file_spr.seek(aux_pointer_data)
                                data += output_file_spr.read()

                                # Write the new reestructured spr
                                output_file_spr_r.write(header + data_name + data_info + data)

                            # Get the new spr rewritted
                            output_file_spr.close()
                            os.remove(spr_export_path)
                            os.rename(spr_export_path_rewrited, spr_export_path)'''

                    basename_spr = os.path.basename(spr_export_path).replace("_m.", ".")
                    basename_vram = os.path.basename(vram_export_path).replace("_m.", ".")
                    VEV.spr_file_path_modified = os.path.join(path_output_file, basename_spr)
                    VEV.vram_file_path_modified = os.path.join(path_output_file, basename_vram)

                    move(spr_export_path, VEV.spr_file_path_modified)
                    move(vram_export_path, VEV.vram_file_path_modified)

                    message = "The files were saved in: <b>" + path_output_file \
                              + "</b><br><br> Do you wish to open the folder?"

                    msg = QMessageBox()
                    msg.setWindowTitle("Message")
                    message_open_saved_files = msg.question(self, '', message, msg.Yes | msg.No)

                    # If the users click on 'Yes', it will open the path where the files were saved
                    if message_open_saved_files == msg.Yes:
                        # Show the path folder to the user
                        os.system('explorer.exe ' + path_output_file.replace("/", "\\"))

            # Save pak file
            else:

                # Add the extension .zpak
                path_output_file = path_output_file + ".zpak"

                # Check if character parameters editor is enabled in order to save the parameters from that tab
                if self.character_parameters_editor.isEnabled():

                    # Ask to the user if the tool saves also the modified values from character parameters editor
                    msg = QMessageBox()
                    msg.setWindowTitle("Message")
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

                            # --- operate_resident_param ---
                            # If the user has edited one character, we will save the file
                            elif GPV.character_list_edited:

                                # Open the files
                                subpak_file_character_inf = open(GPV.resident_character_inf_path, mode="rb+")
                                subpak_file_transformer_i = open(GPV.resident_transformer_i_path, mode="rb+")

                                print("Writing values in the file...")
                                # Change the transformations in the file
                                for character in GPV.character_list_edited:
                                    # Save all the info for each character
                                    write_character_parameters(character, subpak_file_character_inf,
                                                               subpak_file_transformer_i)

                                # Close the files
                                subpak_file_character_inf.close()
                                subpak_file_transformer_i.close()

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
                    msg.setText("No pak file has been loaded.")
                    msg.exec()

    def closeEvent(self, event):
        if os.path.exists(VEV.temp_folder):
            rmtree(VEV.temp_folder, onerror=del_rw)
        if os.path.exists(PEV.temp_folder):
            rmtree(PEV.temp_folder, onerror=del_rw)
        event.accept()

    @staticmethod
    def action_author_logic():
        msg = QMessageBox()
        msg.setTextFormat(1)
        msg.setWindowTitle("Author")
        msg.setText(
            "<ul>"
            "<li><b>Raging tools 1.4</b> by "
            "<a href=https://www.youtube.com/channel/UCkZajFypIgQL6mI6OZLEGXw>adsl14</a></li>"
            "<li>If you want to support the tool, you can get the source code in the "
            "<a href=https://github.com/adsl14/Raging-tools>GitHub</a> page <li>"
            "</ul>")
        msg.exec()

    @staticmethod
    def action_credits_logic():
        msg = QMessageBox()
        msg.setTextFormat(1)
        msg.setWindowTitle("Credits")
        msg.setText('<ul>'
                    '<li>To <b>revelation (revel8n) </b> from <a href=https://forum.xentax.com>XeNTaX</a> '
                    'forum who made the compress/uncompress tool <i>dbrb_compressor.exe</i>.</li>'
                    '<li>To <b>316austin316</b> for contributing to the tool.</li>'
                    '<li>To <b>SSJLVegeta</b> for contributing to the tool.</li>'
                    '<li>To the <a ''href=https://discord.gg/tBmcwkGUE6>Raging Blast Modding community</a>.</li>'
                    '</ul>')
        msg.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
