from PyQt5.QtWidgets import QInputDialog

from lib.design.Raging_tools import *
from lib.packages import os, rmtree, QFileDialog, copyfile, \
    move, QMessageBox
from lib.functions import del_rw

# vram explorer
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.VEF import change_endian, load_data_to_ve
from lib.vram_explorer.VEF import initialize_ve

# pak explorer
from lib.pak_explorer.PEF import initialize_pe, pack_and_save_file, load_data_to_pe_cpe
from lib.pak_explorer.PEV import PEV

# character parameters editor
from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.CPEF import initialize_cpe, write_single_character_parameters, \
    write_character_parameters


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

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
                                                "Open file", os.path.abspath(os.getcwd()), "Supported files "
                                                                                           "(*.pak *.zpak *.spr *.vram)"
                                                                                           ";;Packed files "
                                                                                           "(*.pak *.zpak)"
                                                                                           ";;Info files (*.spr)"
                                                                                           ";;Texture files "
                                                                                           "(*.vram)")[0]
        # Check if the user has selected a file
        if os.path.exists(path_file):

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

                # Load all the data from pak file to pak_explorer/character_parameters_editor
                load_data_to_pe_cpe(self)

            # spr file
            elif header_type == b'SPRP' or header_type == b'SPR\x00':

                # Open vram file
                path_file_2 = QFileDialog.getOpenFileName(self, "Open file", os.path.abspath(path_file),
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
                path_file_2 = QFileDialog.getOpenFileName(self, "Open file", os.path.abspath(path_file),
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

        extension_pak = "Pack files (*.zpak)"
        extension_spr_vram = "Info/Texture files (folder)"

        # Ask to the user where to save the file
        path_output_file, extension = QFileDialog.getSaveFileName(self,
                                                                  "Save file", os.path.abspath(os.getcwd()),
                                                                  extension_pak + ";;" + extension_spr_vram)

        # The user has selected a path
        if path_output_file:

            # Save spr_vram in a folder
            if extension == extension_spr_vram:

                # Remove the extension in order to get the path as a folder
                path_output_file = os.path.splitext(path_output_file)[0]

                if not VEV.tx2_datas:
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

                    # Update the offsets
                    with open(spr_export_path, mode="rb+") as output_file_spr:
                        first_index_texture_edited = VEV.textures_index_edited[0]
                        # Move where the information starts to the first modified texture
                        output_file_spr.seek(VEV.sprp_struct.data_base +
                                             VEV.sprpDatasInfo[first_index_texture_edited].data_offset + 12)
                        # Change the size
                        output_file_spr.write(VEV.tx2d_infos[first_index_texture_edited].
                                              data_size.to_bytes(4, byteorder="big"))
                        # Change width
                        output_file_spr.write(VEV.tx2d_infos[first_index_texture_edited]
                                              .width.to_bytes(2, byteorder="big"))
                        # Change height
                        output_file_spr.write(VEV.tx2d_infos[first_index_texture_edited]
                                              .height.to_bytes(2, byteorder="big"))
                        # Change mip_maps
                        output_file_spr.seek(2, os.SEEK_CUR)
                        output_file_spr.write(VEV.tx2d_infos[first_index_texture_edited].
                                              mip_maps.to_bytes(2, byteorder="big"))
                        # Change dxt encoding
                        output_file_spr.seek(8, os.SEEK_CUR)
                        output_file_spr.write(VEV.tx2d_infos[first_index_texture_edited].
                                              dxt_encoding.to_bytes(1, byteorder="big"))

                        # Check if is the last texture modified and there is no more textures in the bottom
                        if first_index_texture_edited + 1 < VEV.sprp_struct.data_count:
                            quanty_aux = int(VEV.offset_quanty_difference[first_index_texture_edited])
                            # Reset offset difference for the first texture edited
                            VEV.offset_quanty_difference[first_index_texture_edited] = 0
                            first_index_texture_edited += 1
                            for i in range(first_index_texture_edited, VEV.sprp_struct.data_count):

                                # Move where the information starts to the next textures
                                output_file_spr.seek(VEV.sprp_struct.data_base + VEV.sprpDatasInfo[i].data_offset + 4)
                                # Update the offset
                                VEV.tx2d_infos[i].data_offset += quanty_aux
                                output_file_spr.write(int(abs(VEV.tx2d_infos[i].data_offset)).
                                                      to_bytes(4, byteorder="big"))
                                output_file_spr.seek(4, os.SEEK_CUR)

                                # Write the new data size
                                output_file_spr.write(VEV.tx2d_infos[i].data_size.to_bytes(4, byteorder="big"))
                                # Write the new  width
                                output_file_spr.write(VEV.tx2d_infos[i].width.to_bytes(2, byteorder="big"))
                                # Write the new  height
                                output_file_spr.write(VEV.tx2d_infos[i].height.to_bytes(2, byteorder="big"))
                                # Write the new  mip_maps
                                output_file_spr.seek(2, os.SEEK_CUR)
                                output_file_spr.write(VEV.tx2d_infos[i].mip_maps.to_bytes(2, byteorder="big"))
                                # Write the new  dxt encoding
                                output_file_spr.seek(8, os.SEEK_CUR)
                                output_file_spr.write(VEV.tx2d_infos[i].dxt_encoding.to_bytes(1, byteorder="big"))

                                # Increment the difference only if the difference is not 0 and reset the
                                # offset differency array
                                if VEV.offset_quanty_difference[i] != 0:
                                    quanty_aux += VEV.offset_quanty_difference[i]
                                    VEV.offset_quanty_difference[i] = 0

                    # replacing textures
                    with open(vram_export_path, mode="wb") as output_file:
                        with open(VEV.vram_file_path, mode="rb") as input_file:

                            # SPR header
                            texture_offset = 0

                            # Get each offset texture and write over the original file
                            for texture_index in VEV.textures_index_edited:
                                tx2d_info = VEV.tx2d_infos[texture_index]
                                tx2d_data = VEV.tx2_datas[texture_index]
                                data = input_file.read(
                                    abs(tx2d_info.data_offset_old + texture_offset - input_file.tell()))
                                output_file.write(data)
                                input_file.seek(tx2d_info.data_size_old, os.SEEK_CUR)

                                # It's a DDS image
                                if tx2d_info.dxt_encoding != 0:
                                    output_file.write(VEV.tx2_datas[texture_index].data[128:])
                                else:

                                    if tx2d_data.extension != "png":
                                        # We're dealing with a shader. We have to change the endian
                                        if tx2d_info.height == 1:
                                            output_file.write(change_endian(VEV.tx2_datas[texture_index].data[54:]))
                                        else:
                                            output_file.write(VEV.tx2_datas[texture_index].data[54:])
                                    else:
                                        # Write in disk the data swizzled
                                        with open("tempSwizzledImage", mode="wb") as file:
                                            file.write(VEV.tx2_datas[texture_index].data)

                                        # Write in disk the data unswizzled
                                        with open("tempUnSwizzledImage", mode="wb") as file:
                                            file.write(VEV.tx2_datas[texture_index].data_unswizzle[54:])

                                        # Write in disk the indexes
                                        with open("Indexes.txt", mode="w") as file:
                                            for index in VEV.tx2_datas[texture_index].indexes_unswizzle_algorithm:
                                                file.write(index + ";")

                                        # Run the exe file of 'swizzle.exe' with the option '-s' to swizzle the image
                                        args = os.path.join(VEV.swizzle_path) + " \"" + \
                                            "tempSwizzledImage" + "\" \"" + \
                                            "tempUnSwizzledImage" + "\" \"" + "Indexes.txt" + "\" \"" + "-s" + "\""
                                        os.system('cmd /c ' + args)

                                        # Get the data from the .exe
                                        with open("tempSwizzledImageModified", mode="rb") as file:
                                            VEV.tx2_datas[texture_index].data = file.read()

                                        # Remove the temp files
                                        os.remove("tempSwizzledImage")
                                        os.remove("tempUnSwizzledImage")
                                        os.remove("Indexes.txt")
                                        os.remove("tempSwizzledImageModified")

                                        output_file.write(VEV.tx2_datas[texture_index].data)

                            data = input_file.read()
                            output_file.write(data)

                            # Modify the bytes in pos 20 that indicates the size of the file
                            vram_file_size = abs(VEV.vram_file_size_old + output_file.tell() - input_file.tell())

                    # Change the header of pos 256 in spr file because in that place indicates the size of the
                    # final output file
                    with open(spr_export_path, mode="rb+") as output_file:
                        output_file.seek(VEV.data_offset_header + 48)
                        output_file.write(vram_file_size.to_bytes(4, byteorder='big'))

                    # SPR file. We won't compress

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
                        os.system('explorer.exe ' + path_output_file)

            # Save pak file
            else:

                # Check if character parameters editor is enabled in order to save the parameters from that tab
                if self.character_parameters_editor.isEnabled():

                    # Ask to the user, from what tab he wants to gather and save the data
                    msg = QMessageBox()
                    msg.setWindowTitle("Message")
                    message = "From what tab do you wish to save the file?"
                    options = ["character parameters editor", "pak explorer"]
                    answer = QInputDialog.getItem(self, "Select option", message, options, editable=False)

                    # Check if the user has selected something
                    if answer[1]:

                        # The user wants to save the file from the 'character parameters editor'
                        if answer[0] == options[0]:

                            # Check what type of character parameter editor is activated
                            # --- operate_character_XXX_m ---
                            if self.ki_values.isVisible():

                                # Save all the info
                                print("Writing values in the file...")
                                write_single_character_parameters(self)

                                # Pack the files
                                print("Packing the file...")
                                pack_and_save_file(self, path_output_file)

                            # --- operate_resident_param ---
                            # If the user has edited one character, we will save the file
                            elif CPEV.character_list_edited:

                                # Open the files
                                subpak_file_character_inf = open(CPEV.resident_character_inf_path, mode="rb+")
                                subpak_file_transformer_i = open(CPEV.resident_transformer_i_path, mode="rb+")

                                print("Writing values in the file...")
                                # Change the transformations in the file
                                for character in CPEV.character_list_edited:
                                    # Save all the info for each character
                                    write_character_parameters(character, subpak_file_character_inf,
                                                               subpak_file_transformer_i)

                                # Close the files
                                subpak_file_character_inf.close()
                                subpak_file_transformer_i.close()

                                # Pack the files
                                print("Packing the file...")
                                pack_and_save_file(self, path_output_file)

                            else:
                                msg = QMessageBox()
                                msg.setWindowTitle("Warning")
                                msg.setText("The file hasn't been modified.")
                                msg.exec()

                        # The user wants to save the pak file from the 'pak explorer'
                        else:
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
            "<li><b>Raging tools 1.3.2</b> by "
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
                    '<li>To <b>revelation (revel8n) </b> from <a ''href=https://forum.xentax.com>XeNTaX</a> '
                    'forum who made the compress/uncompress tool <i>dbrb_compressor.exe</i>.</li>'
                    '<li>To <b>316austin316</b> for reporting bugs.</li>'
                    '<li>To the <a ''href=https://discord.gg/tBmcwkGUE6>Raging Blast Modding community</a>.</li>'
                    '</ul>')
        msg.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
