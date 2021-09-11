

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QInputDialog

from lib.design.Raging_tools import *
from lib.packages import datetime, os, functools, QPixmap, struct, rmtree, QStandardItem, QFileDialog, copyfile, \
    move, QMessageBox
from lib.functions import del_rw

# vram explorer
from lib.pak_explorer import PEF
from lib.pak_explorer.PEF import initialize_pe, action_item_pak_explorer, pack_and_save_file
from lib.pak_explorer.PEV import PEV
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.VEF import change_endian, get_dxt_value
from lib.vram_explorer.VEF import get_encoding_name, show_dds_image, validation_dds_imported_texture
from lib.vram_explorer.VEF import validation_bmp_imported_texture, show_bmp_image
from lib.vram_explorer.VEF import open_spr_file, open_vram_file, action_item, initialize_ve

# character parameters editor
from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.CPEF import store_character_parameters, initialize_cpe, action_change_character, \
    open_select_chara_window
from lib.character_parameters_editor.classes.Character import Character


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # File tab
        self.actionOpenSPRVRAM.triggered.connect(self.action_open_sprvram_logic)
        self.actionSaveSPRVRAM.triggered.connect(self.action_save_sprvram_logic)
        self.actionOpenPAK.triggered.connect(self.action_open_pak_logic)
        self.actionSavePAK.triggered.connect(self.action_save_pak_logic)
        self.actionClose.triggered.connect(self.close)

        # About tab
        self.actionAuthor.triggered.connect(self.action_author_logic)
        self.actionCredits.triggered.connect(self.action_credits_logic)

        # --- vram explorer ---
        initialize_ve(self)

        # --- pak explorer ---
        initialize_pe(self)

        # --- character parameters editor ---
        initialize_cpe(self, QtWidgets)

    # vram explorer methods
    def action_export_logic(self):

        # If the encoding is DXT5 or DXT1, we show the dds image
        if VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding != 0:
            # Save dds file
            export_path = QFileDialog.getSaveFileName(self, "Save file", os.path.join(os.path.abspath(os.getcwd()),
                                                                                      VEV.tx2_datas[
                                                                                          VEV.current_selected_texture]
                                                                                      .name + ".dds"),
                                                      "DDS file (*.dds)")[0]

            data = VEV.tx2_datas[VEV.current_selected_texture].data

        else:
            # Save bmp file
            export_path = QFileDialog.getSaveFileName(self, "Save file", os.path.join(os.path.abspath(os.getcwd()),
                                                                                      VEV.tx2_datas[
                                                                                          VEV.current_selected_texture]
                                                                                      .name + ".bmp"),
                                                      "BMP file (*.bmp)")[0]

            if VEV.tx2_datas[VEV.current_selected_texture].extension != "png":
                data = VEV.tx2_datas[VEV.current_selected_texture].data
            else:
                data = VEV.tx2_datas[VEV.current_selected_texture].data_unswizzle

        if export_path:
            file = open(export_path, mode="wb")
            file.write(data)
            file.close()

    def action_export_all_logic(self):

        # Create folder
        if not os.path.exists("textures"):
            os.mkdir("textures")
        name_folder = os.path.basename(VEV.vram_file_path_original).replace(".vram", "")
        folder_export_path = os.path.join(os.path.abspath(os.getcwd()), "textures", name_folder)
        if not os.path.exists(folder_export_path):
            os.mkdir(folder_export_path)

        for i in range(0, VEV.sprp_struct.data_count):
            # The image is dds
            if VEV.tx2d_infos[i].dxt_encoding != 0:

                file = open(os.path.join(folder_export_path, VEV.tx2_datas[i].name + ".dds"), mode="wb")

                file.write(VEV.tx2_datas[i].data)
                file.close()

            else:
                file = open(os.path.join(folder_export_path, VEV.tx2_datas[i].name + ".bmp"), mode="wb")
                if VEV.tx2_datas[i].extension != "png":
                    file.write(VEV.tx2_datas[i].data)
                else:
                    file.write(VEV.tx2_datas[i].data_unswizzle)
                file.close()

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        message = "All the textures were exported in: <b>" + folder_export_path \
                  + "</b><br><br> Do you wish to open the folder?"
        message_open_exported_files = msg.question(self, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + folder_export_path)

    def action_import_logic(self):

        # Open spr file
        # For DDS
        if VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding != 0:
            import_path = QFileDialog.getOpenFileName(self, "Open file",
                                                      os.path.join(os.path.abspath(VEV.spr_file_path),
                                                                   VEV.tx2_datas[VEV.current_selected_texture].name +
                                                                   ".dds"),
                                                      "DDS file (*.dds)")[0]
        # For BMP (rgba image)
        else:
            import_path = QFileDialog.getOpenFileName(self, "Open file",
                                                      os.path.join(os.path.abspath(VEV.spr_file_path),
                                                                   VEV.tx2_datas[VEV.current_selected_texture].name +
                                                                   ".bmp"),
                                                      "BMP file (*.bmp)")[0]
        # The user didn't cancel the file to import
        if import_path:
            with open(import_path, mode="rb") as file:
                header = file.read(2).hex()

                # It's a DDS modded image
                if header != "424d":
                    # It's a DDS file the selected texture
                    if VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding != 0:

                        # Get the height and width of the modified image
                        file.seek(12)
                        height = int.from_bytes(file.read(VEV.bytes2Read), 'little')
                        width = int.from_bytes(file.read(VEV.bytes2Read), 'little')
                        # Get the mipmaps
                        file.seek(28)
                        mip_maps = int.from_bytes(file.read(1), 'big')
                        # Get the dxtencoding
                        file.seek(84)
                        dxt_encoding = get_dxt_value(file.read(VEV.bytes2Read).decode())

                        message = validation_dds_imported_texture(VEV.tx2d_infos[VEV.current_selected_texture],
                                                                  width, height, mip_maps, dxt_encoding)

                        # If the message is empty, there is no differences between original and modified one
                        msg = QMessageBox()
                        if message:

                            # Concatenate the base message and the differences the tool has found
                            message = VEV.message_base_import_DDS_start + "<ul>" + message + "</ul>" \
                                      + VEV.message_base_import_DDS_end

                            # Ask to the user if he/she is sure that wants to replace the texture
                            msg.setWindowTitle("Warning")
                            message_import_result = msg.question(self, '', message, msg.Yes | msg.No)

                            # If the users click on 'No', the modified texture won't be imported
                            if message_import_result == msg.No:
                                return

                        # Get all the data
                        file.seek(0)
                        data = file.read()

                        # Importing the texture
                        # Get the difference in size between original and modified in order to change the offsets
                        len_data = len(data[128:])
                        difference = len_data - VEV.tx2d_infos[VEV.current_selected_texture].data_size
                        if difference != 0:
                            VEV.tx2d_infos[VEV.current_selected_texture].data_size = len_data
                            VEV.offset_quanty_difference[VEV.current_selected_texture] = difference

                        # Change width
                        if VEV.tx2d_infos[VEV.current_selected_texture].width != width:
                            VEV.tx2d_infos[VEV.current_selected_texture].width = width
                            self.sizeImageText.setText(
                                "Resolution: %dx%d" % (width, VEV.tx2d_infos[VEV.current_selected_texture].height))
                        # Change height
                        if VEV.tx2d_infos[VEV.current_selected_texture].height != height:
                            VEV.tx2d_infos[VEV.current_selected_texture].height = height
                            self.sizeImageText.setText(
                                "Resolution: %dx%d" % (VEV.tx2d_infos[VEV.current_selected_texture].width, height))

                        # Change mipMaps
                        if VEV.tx2d_infos[VEV.current_selected_texture].mip_maps != mip_maps:
                            VEV.tx2d_infos[VEV.current_selected_texture].mip_maps = mip_maps
                            self.mipMapsImageText.setText("Mipmaps: %s" % mip_maps)

                        # Change dxt encoding
                        if VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding != dxt_encoding:
                            VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding = dxt_encoding
                            self.encodingImageText.setText("Encoding: %s" %
                                                           (get_encoding_name(dxt_encoding)))

                        # Change texture in the array
                        VEV.tx2_datas[VEV.current_selected_texture].data = data

                        # Add the index texture that has been modified
                        # (if it was added before, we won't added twice)
                        if VEV.current_selected_texture not in VEV.textures_index_edited:
                            VEV.textures_index_edited.append(VEV.current_selected_texture)

                        try:
                            # Show texture in the program
                            show_dds_image(self.imageTexture, None, width, height, import_path)

                        except OSError:
                            self.imageTexture.clear()

                    else:
                        msg = QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setText("The image you're importing is DDS and should be BMP")
                        msg.exec()

                # it's a BMP modded image
                else:
                    # It's a BMP file the selected texture
                    if VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding == 0:

                        # Get the height and width of the modified image
                        file.seek(18)
                        width = int.from_bytes(file.read(VEV.bytes2Read), 'little')
                        height = int.from_bytes(file.read(VEV.bytes2Read), 'little')

                        # Get the number of bits
                        file.seek(28)
                        number_bits = int.from_bytes(file.read(2), 'little')

                        # Validate the BMP imported texture
                        message = validation_bmp_imported_texture(VEV.tx2d_infos[VEV.current_selected_texture],
                                                                  width, height, number_bits)

                        # If there is a message, it has detected differences
                        if message:
                            # If the imported texture is not png, we ask the user first to add it or not
                            if VEV.tx2_datas[VEV.current_selected_texture].extension != "png":

                                msg = QMessageBox()

                                # Concatenate the base message and the differences the tool has found
                                message = VEV.message_base_import_DDS_start + "<ul>" + message + "</ul>" \
                                    + VEV.message_base_import_DDS_end

                                # Ask to the user if he/she is sure that wants to replace the texture
                                msg.setWindowTitle("Warning")
                                message_import_result = msg.question(self, '', message, msg.Yes | msg.No)

                                # If the users click on 'NO', the modified texture won't be imported
                                if message_import_result == msg.No:
                                    return
                            else:
                                msg = QMessageBox()
                                msg.setWindowTitle("Error")
                                msg.setText(VEV.message_base_import_BMP_start + "<ul>" + message + "</ul>")
                                msg.exec()
                                return

                        # Get all the data
                        file.seek(0)
                        data = file.read()

                        # It's not png file
                        if VEV.tx2_datas[VEV.current_selected_texture].extension != "png":
                            # Importing the texture
                            # Get the difference in size between original and modified in order to change the offsets
                            len_data = len(data[54:])
                            difference = len_data - VEV.tx2d_infos[VEV.current_selected_texture].data_size
                            if difference != 0:
                                VEV.tx2d_infos[VEV.current_selected_texture].data_size = len_data
                                VEV.offset_quanty_difference[VEV.current_selected_texture] = difference

                            # Change width
                            if VEV.tx2d_infos[VEV.current_selected_texture].width != width:
                                VEV.tx2d_infos[VEV.current_selected_texture].width = width
                                self.sizeImageText.setText(
                                    "Resolution: %dx%d" % (width, VEV.tx2d_infos[VEV.current_selected_texture].height))
                            # Change height
                            if VEV.tx2d_infos[VEV.current_selected_texture].height != height:
                                VEV.tx2d_infos[VEV.current_selected_texture].height = height
                                self.sizeImageText.setText(
                                    "Resolution: %dx%d" % (VEV.tx2d_infos[VEV.current_selected_texture].width, height))

                            # Change texture in the array
                            VEV.tx2_datas[VEV.current_selected_texture].data = data

                        else:
                            # Importing the texture
                            # Change texture in the array
                            VEV.tx2_datas[VEV.current_selected_texture].data_unswizzle = data

                        # Add the index texture that has been modified (if it was added before,
                        # we won't added twice)
                        if VEV.current_selected_texture not in VEV.textures_index_edited:
                            VEV.textures_index_edited.append(VEV.current_selected_texture)

                        try:
                            # Show texture in the program
                            show_bmp_image(self.imageTexture, data, width, height)

                        except OSError:
                            self.imageTexture.clear()
                    else:
                        msg = QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setText("The image you're importing is BMP and should be DDS")
                        msg.exec()

    def action_open_sprvram_logic(self):

        # Open spr file
        VEV.spr_file_path_original = \
            QFileDialog.getOpenFileName(self, "Open file", os.path.abspath(os.getcwd()), "SPR files (*.spr)")[0]
        # Check if the user has selected an spr format file
        if not os.path.exists(VEV.spr_file_path_original):
            return
        # Check if the user has selected an spr stpz file
        with open(VEV.spr_file_path_original, mode="rb") as spr_file:
            type_file = spr_file.read(4).hex()
            if type_file == VEV.STPZ:
                VEV.stpz_file = True
            else:
                VEV.stpz_file = False

        # Open vram file
        VEV.vram_file_path_original = \
            QFileDialog.getOpenFileName(self, "Open file", os.path.abspath(VEV.spr_file_path_original),
                                        "Texture files (*.vram)")[0]
        if not os.path.exists(VEV.vram_file_path_original):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("A vram file is needed.")
            msg.exec()
            return

        # Clean the variables
        VEV.sprpDatasInfo.clear()
        VEV.tx2_datas.clear()
        VEV.tx2d_infos.clear()
        VEV.textures_index_edited.clear()

        basename = os.path.basename(VEV.spr_file_path_original)

        # Convert spr and vram files if we're dealing with stpz file
        if VEV.stpz_file:
            # Create a folder where we store the necessary files or delete it. If already exists,
            # we remove every files in it
            if os.path.exists(VEV.temp_folder):
                rmtree(VEV.temp_folder, onerror=del_rw)
            os.mkdir(VEV.temp_folder)

            # Execute the script in a command line for the spr file
            VEV.spr_file_path = os.path.join(os.path.abspath(os.getcwd()), VEV.temp_folder,
                                             basename.replace(".spr", "_u.spr"))
            args = os.path.join(VEV.dbrb_compressor_path) + " \"" + VEV.spr_file_path_original + "\" \"" + \
                VEV.spr_file_path + "\""
            os.system('cmd /c ' + args)

            # Execute the script in a command line for the vram file
            basename = os.path.basename(VEV.vram_file_path_original)
            VEV.vram_file_path = os.path.join(os.path.abspath(os.getcwd()), VEV.temp_folder,
                                              basename.replace(".vram", "_u.vram"))
            args = os.path.join(VEV.dbrb_compressor_path) + " \"" + \
                VEV.vram_file_path_original + "\" \"" + VEV.vram_file_path + "\""
            os.system('cmd /c ' + args)

            # Load the data from the files
            open_spr_file(VEV.spr_file_path, 16)

        # Generic spr file. Don't need to convert
        else:
            VEV.spr_file_path = VEV.spr_file_path_original
            VEV.vram_file_path = VEV.vram_file_path_original
            open_spr_file(VEV.spr_file_path, 12)

        open_vram_file(VEV.vram_file_path)

        # Add the names to the list view
        VEV.current_selected_texture = 0
        model = QStandardItemModel()
        self.listView.setModel(model)
        item_0 = QStandardItem(VEV.tx2_datas[0].name)
        item_0.setEditable(False)
        model.appendRow(item_0)
        self.listView.setCurrentIndex(model.indexFromItem(item_0))
        for tx2_data_element in VEV.tx2_datas[1:]:
            item = QStandardItem(tx2_data_element.name)
            item.setEditable(False)
            model.appendRow(item)
        self.listView.clicked.connect(
            lambda q_model_idx: action_item(q_model_idx, self.imageTexture, self.encodingImageText,
                                            self.mipMapsImageText,
                                            self.sizeImageText))

        # If the texture encoded is DXT1 or DXT5, we call the show dds function
        if VEV.tx2d_infos[0].dxt_encoding != 0:
            # Create the dds in disk and open it
            show_dds_image(self.imageTexture, VEV.tx2_datas[0].data, VEV.tx2d_infos[0].width, VEV.tx2d_infos[0].height)
        else:
            if VEV.tx2_datas[0].extension != "png":
                show_bmp_image(self.imageTexture, VEV.tx2_datas[0].data, VEV.tx2d_infos[0].width,
                               VEV.tx2d_infos[0].height)
            else:
                show_bmp_image(self.imageTexture, VEV.tx2_datas[0].data_unswizzle, VEV.tx2d_infos[0].width,
                               VEV.tx2d_infos[0].height)

        # Show the buttons
        self.exportButton.setVisible(True)
        self.exportAllButton.setVisible(True)
        self.importButton.setVisible(True)

        # Show the text labels
        self.fileNameText.setText(basename.split(".")[0])
        self.fileNameText.setVisible(True)
        self.encodingImageText.setText(
            "Encoding: %s" % (get_encoding_name(VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding)))
        self.mipMapsImageText.setText("Mipmaps: %d" % VEV.tx2d_infos[VEV.current_selected_texture].mip_maps)
        self.sizeImageText.setText(
            "Resolution: %dx%d" % (VEV.tx2d_infos[VEV.current_selected_texture].width,
                                   VEV.tx2d_infos[VEV.current_selected_texture]
                                   .height))
        self.encodingImageText.setVisible(True)
        self.mipMapsImageText.setVisible(True)
        self.sizeImageText.setVisible(True)

        # Open the tab
        self.tabWidget.setCurrentIndex(0)

    def action_save_sprvram_logic(self):

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
            basename = os.path.basename(VEV.vram_file_path_original) \
                .replace(".vram", datetime.now().strftime("_%d-%m-%Y_%H-%M-%S"))
            path_output_folder = os.path.join(os.path.abspath(os.getcwd()), "outputs")
            path_output_files = os.path.join(path_output_folder, basename)

            if not os.path.exists(path_output_folder):
                os.mkdir(path_output_folder)
            os.mkdir(path_output_files)

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
                output_file_spr.write(VEV.tx2d_infos[first_index_texture_edited].data_size.to_bytes(4, byteorder="big"))
                # Change width
                output_file_spr.write(VEV.tx2d_infos[first_index_texture_edited].width.to_bytes(2, byteorder="big"))
                # Change height
                output_file_spr.write(VEV.tx2d_infos[first_index_texture_edited].height.to_bytes(2, byteorder="big"))
                # Change mip_maps
                output_file_spr.seek(2, os.SEEK_CUR)
                output_file_spr.write(VEV.tx2d_infos[first_index_texture_edited].mip_maps.to_bytes(2, byteorder="big"))
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
                        output_file_spr.write(int(abs(VEV.tx2d_infos[i].data_offset)).to_bytes(4, byteorder="big"))
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

                        # Increment the difference only if the difference is not 0 and reset the offset differency array
                        if VEV.offset_quanty_difference[i] != 0:
                            quanty_aux += VEV.offset_quanty_difference[i]
                            VEV.offset_quanty_difference[i] = 0

            # replacing textures
            with open(vram_export_path, mode="wb") as output_file:
                with open(VEV.vram_file_path, mode="rb") as input_file:

                    # If we're dealing with a vram stpz file
                    if VEV.stpz_file:

                        # If we're dealing with a normal STPK
                        if VEV.single_stpk_header:
                            # Move to the position 16, where it tells the offset of the file where the texture starts
                            data = input_file.read(16)

                            output_file.write(data)

                            data = input_file.read(VEV.bytes2Read)
                            output_file.write(data)
                            texture_offset = int.from_bytes(data, "big")

                        # We're dealing with RB2 to RB1 port
                        else:
                            # Move to the position 16 + 64, where it tells the offset of the
                            # file where the texture starts
                            data = input_file.read(16 + 64)

                            output_file.write(data)

                            data = input_file.read(VEV.bytes2Read)
                            output_file.write(data)
                            texture_offset = int.from_bytes(data, "big") + 64

                    else:
                        texture_offset = 0

                    # Get each offset texture and write over the original file
                    for texture_index in VEV.textures_index_edited:
                        tx2d_info = VEV.tx2d_infos[texture_index]
                        tx2d_data = VEV.tx2_datas[texture_index]
                        data = input_file.read(abs(tx2d_info.data_offset_old + texture_offset - input_file.tell()))
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
                                args = os.path.join(VEV.swizzle_path) + " \"" + "tempSwizzledImage" + "\" \"" + \
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

            # Change the header of pos 256 in spr file because in that place indicates the size of the final output file
            with open(spr_export_path, mode="rb+") as output_file:
                output_file.seek(VEV.stpk_struct.data_offset + 48)
                output_file.write(vram_file_size.to_bytes(4, byteorder='big'))

            # If we're dealing with a vram stpz file
            if VEV.stpz_file:
                # Change the header of pos 20 in vram file because that place indicates the size of the final output
                # file
                with open(vram_export_path, mode="rb+") as output_file:
                    output_file.seek(20)
                    output_file.write(vram_file_size.to_bytes(4, byteorder='big'))

                # Generate the final files for the game
                # Output for the spr file
                basename_spr = os.path.basename(VEV.spr_file_path_original)
                VEV.spr_file_path_modified = os.path.join(path_output_files, basename_spr)
                args = os.path.join(VEV.dbrb_compressor_path) + " \"" + spr_export_path + "\" \"" \
                    + VEV.spr_file_path_modified + "\""
                os.system('cmd /c ' + args)

                # Output for the vram file
                basename_vram = os.path.basename(VEV.vram_file_path_original)
                VEV.vram_file_path_modified = os.path.join(path_output_files, basename_vram)
                args = os.path.join(VEV.dbrb_compressor_path) + " \"" + vram_export_path + "\" \"" \
                    + VEV.vram_file_path_modified + "\" "
                os.system('cmd /c ' + args)

                # Remove the uncompressed modified files
                os.remove(spr_export_path)
                os.remove(vram_export_path)

            else:

                basename_spr = os.path.basename(spr_export_path).replace("_m.", ".")
                basename_vram = os.path.basename(vram_export_path).replace("_m.", ".")
                VEV.spr_file_path_modified = os.path.join(path_output_files, basename_spr)
                VEV.vram_file_path_modified = os.path.join(path_output_files, basename_vram)

                move(spr_export_path, VEV.spr_file_path_modified)
                move(vram_export_path, VEV.vram_file_path_modified)

            msg = QMessageBox()
            msg.setWindowTitle("Message")
            message = "The files were saved and compressed in: <b>" + path_output_files \
                      + "</b><br><br> Do you wish to open the folder?"
            message_open_saved_files = msg.question(self, '', message, msg.Yes | msg.No)

            # If the users click on 'Yes', it will open the path where the files were saved
            if message_open_saved_files == msg.Yes:
                # Show the path folder to the user
                os.system('explorer.exe ' + path_output_files)

    # character parameters and pak explorer methods
    def action_open_pak_logic(self):

        # Open pak file
        PEV.pak_file_path_original = \
            QFileDialog.getOpenFileName(self, "Open file", os.path.abspath(os.getcwd()), "PAK files (*.pak *.zpak)")[0]

        # Check if the user has selected a pak format file
        if not os.path.exists(PEV.pak_file_path_original):
            return

        # Create a folder where we store the necessary files (always for pak explorer). If already exists,
        # we remove every files in it
        if os.path.exists(PEV.temp_folder):
            rmtree(PEV.temp_folder, onerror=del_rw)
        os.mkdir(PEV.temp_folder)

        # Check if the pak file is STPZ or STPK
        with open(PEV.pak_file_path_original, mode="rb") as pak_file:

            data = pak_file.read(4)

            # Check if the file is STPZ
            if data == PEV.STPZ:

                basename = os.path.basename(PEV.pak_file_path_original)
                extension = basename.split(".")[-1]

                # Execute the script in a command line for the pak file
                PEV.pak_file_path = os.path.join(os.path.abspath(os.getcwd()), PEV.temp_folder,
                                                 basename.replace("." + extension, "_d." + extension))
                args = os.path.join(PEV.dbrb_compressor_path) + " \"" + PEV.pak_file_path_original + "\" \"" + \
                    PEV.pak_file_path + "\""
                os.system('cmd /c ' + args)

                PEV.stpz_file = True

            # The file is STPK
            else:
                PEV.pak_file_path = PEV.pak_file_path_original

        # Unpack pak file (pak explorer)
        # Prepare the list view 2 in order to add the names
        model = QStandardItemModel()
        self.listView_2.setModel(model)
        PEF.unpack(PEV.pak_file_path, os.path.basename(PEV.pak_file_path).split(".")[-1], PEV.temp_folder,
                   self.listView_2)
        self.listView_2.setCurrentIndex(self.listView_2.model().index(0, 0))
        PEV.current_selected_subpak_file = self.listView_2.model().index(0, 0).row()
        self.listView_2.clicked.connect(lambda q_model_idx: action_item_pak_explorer(q_model_idx))
        # Enable the pak explorer
        self.pak_explorer.setEnabled(True)
        # Add the title
        self.fileNameText_2.setText(os.path.basename(PEV.pak_file_path_original))

        # Read the pak file (character parameters editor)
        with open(PEV.pak_file_path, mode="rb") as pak_file:

            # Read the filename (STPK) in the header
            pak_file.seek(32)
            data = pak_file.read(32).decode('utf-8').split(".")[0]

            # Check if the file is the operate_resident_param.pak
            if data == CPEV.operate_resident_param:

                # reset the values
                CPEV.character_list_edited.clear()
                CPEV.character_list.clear()
                CPEV.chara_selected = 0  # Index of the char selected in the program

                # Read the data from the file and store the parameters
                for i in range(0, 100):
                    # Create a Character object
                    character = Character()

                    # Store the positions where the information is located
                    character.position_visual_parameters = CPEV.base_pos_visual_parameters + (
                            i * CPEV.sizeVisualParameters)
                    character.position_trans = CPEV.base_pos_trans + (i * CPEV.sizeTrans)

                    # Store the information in the object and append to a list
                    store_character_parameters(character, pak_file)
                    CPEV.character_list.append(character)

                # Enable the characters portraits
                for i in range(0, 66):
                    CPEV.mini_portraits_image[i].setEnabled(True)

                # We're changing the character in the main panel (avoid combo box code)
                CPEV.change_character = True

                # Show the large portrait
                self.portrait.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_000.png")))
                self.portrait.setVisible(True)

                # Show the transformations in the main panel
                self.label_trans_0.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_001.bmp")))
                self.label_trans_0.mousePressEvent = functools.partial(action_change_character, main_window=self,
                                                                       index=1, modify_slot_transform=False)
                self.label_trans_1.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_002.bmp")))
                self.label_trans_1.mousePressEvent = functools.partial(action_change_character, main_window=self,
                                                                       index=2, modify_slot_transform=False)
                self.label_trans_2.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_003.bmp")))
                self.label_trans_2.mousePressEvent = functools.partial(action_change_character, main_window=self,
                                                                       index=3, modify_slot_transform=False)
                self.label_trans_0.setVisible(True)
                self.label_trans_1.setVisible(True)
                self.label_trans_2.setVisible(True)

                # Get the values for the fist character of the list
                character_zero = CPEV.character_list[0]

                # Show the health
                self.health_value.setValue(character_zero.health)

                # Show the camera size
                self.camera_size_cutscene_value.setValue(character_zero.camera_size[0])
                self.camera_size_idle_value.setValue(character_zero.camera_size[1])

                # Show the hit box
                self.hit_box_value.setValue(character_zero.hit_box)

                # Show the aura size
                self.aura_size_idle_value.setValue(character_zero.aura_size[0])
                self.aura_size_dash_value.setValue(character_zero.aura_size[1])
                self.aura_size_charge_value.setValue(character_zero.aura_size[2])

                # Show the color lightnings parameter
                self.color_lightning_value.setCurrentIndex(character_zero.glow_lightning)

                # Show the glow/lightnings parameter
                self.glow_lightning_value.setCurrentIndex(character_zero.glow_lightning)

                # Show the transform panel
                self.transSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                    str(character_zero.transformations[0]).zfill(
                                                                        3) + ".png")))
                self.transSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window, main_window=self,
                                                                         index=character_zero.transformations[0],
                                                                         trans_slot_panel_index=0)
                self.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                    str(character_zero.transformations[1]).zfill(
                                                                        3) + ".png")))
                self.transSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window, main_window=self,
                                                                         index=character_zero.transformations[1],
                                                                         trans_slot_panel_index=1)
                self.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                    str(character_zero.transformations[2]).zfill(
                                                                        3) + ".png")))
                self.transSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window, main_window=self,
                                                                         index=character_zero.transformations[2],
                                                                         trans_slot_panel_index=2)
                self.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                    str(character_zero.transformations[3]).zfill(
                                                                        3) + ".png")))
                self.transSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window, main_window=self,
                                                                         index=character_zero.transformations[3],
                                                                         trans_slot_panel_index=3)

                # Show the transformation parameter
                self.transEffectValue.setCurrentIndex(character_zero.transformation_effect)

                # Show the transformation partner
                self.transPartnerValue.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                      str(character_zero.transformation_partner).zfill(
                                                                          3)
                                                                      + ".png")))
                self.transPartnerValue.mousePressEvent = functools.partial(open_select_chara_window, main_window=self,
                                                                           index=character_zero.transformation_partner,
                                                                           transformation_partner_flag=True)

                # Show amount ki per transformation
                self.amountKi_trans1_value.setValue(character_zero.amount_ki_transformations[0])
                self.amountKi_trans2_value.setValue(character_zero.amount_ki_transformations[1])
                self.amountKi_trans3_value.setValue(character_zero.amount_ki_transformations[2])
                self.amountKi_trans4_value.setValue(character_zero.amount_ki_transformations[3])

                # Show Animation per transformation
                self.trans1_animation_value.setCurrentIndex(character_zero.transformations_animation[0])
                self.trans2_animation_value.setCurrentIndex(character_zero.transformations_animation[1])
                self.trans3_animation_value.setCurrentIndex(character_zero.transformations_animation[2])
                self.trans4_animation_value.setCurrentIndex(character_zero.transformations_animation[3])

                # Show the fusion panel
                self.fusiSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                   str(character_zero.fusions[0]).zfill(3) + ".png")))
                self.fusiSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window, main_window=self,
                                                                        index=character_zero.fusions[0],
                                                                        fusion_slot_panel_index=0)
                self.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                   str(character_zero.fusions[1]).zfill(3) + ".png")))
                self.fusiSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window, main_window=self,
                                                                        index=character_zero.fusions[1],
                                                                        fusion_slot_panel_index=1
                                                                        )
                self.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                   str(character_zero.fusions[2]).zfill(3) + ".png")))
                self.fusiSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window, main_window=self,
                                                                        index=character_zero.fusions[2],
                                                                        fusion_slot_panel_index=2)
                self.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                   str(character_zero.fusions[3]).zfill(3) + ".png")))
                self.fusiSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window, main_window=self,
                                                                        index=character_zero.fusions[3],
                                                                        fusion_slot_panel_index=3)

                # Show the fusion partner (trigger)
                self.fusionPartnerTrigger_value.setPixmap(
                    QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                         str(character_zero.fusion_partner[0]).zfill(3)
                                         + ".png")))
                self.fusionPartnerTrigger_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                    main_window=self,
                                                                                    index=character_zero.fusion_partner
                                                                                    [0],
                                                                                    fusion_partner_trigger_flag=True)

                # Show fusion partner visual
                self.fusionPartnerVisual_value.setPixmap(
                    QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                         str(character_zero.fusion_partner[1]).zfill(3)
                                         + ".png")))
                self.fusionPartnerVisual_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                   main_window=self,
                                                                                   index=character_zero.
                                                                                   fusion_partner[1],
                                                                                   fusion_partner_visual_flag=True)

                # Show amount ki per fusion
                self.amountKi_fusion1_value.setValue(character_zero.amount_ki_fusions[0])
                self.amountKi_fusion2_value.setValue(character_zero.amount_ki_fusions[1])
                self.amountKi_fusion3_value.setValue(character_zero.amount_ki_fusions[2])
                self.amountKi_fusion4_value.setValue(character_zero.amount_ki_fusions[3])

                # Show Animation per transformation
                self.fusion1_animation_value.setCurrentIndex(character_zero.fusions_animation[0])
                self.fusion2_animation_value.setCurrentIndex(character_zero.fusions_animation[1])
                self.fusion3_animation_value.setCurrentIndex(character_zero.fusions_animation[2])
                self.fusion4_animation_value.setCurrentIndex(character_zero.fusions_animation[3])

                # We're not changing the character in the main panel (play combo box code)
                CPEV.change_character = False

                # Enable the character parameters editor
                self.character_parameters_editor.setEnabled(True)
                # Open the tab (character parameters editor)
                self.tabWidget.setCurrentIndex(2)

            # Generic pak file
            else:
                # Open the tab (pak explorer)
                self.tabWidget.setCurrentIndex(1)
                # Disable the character parameters editor
                self.character_parameters_editor.setEnabled(False)

    def action_save_pak_logic(self):

        # Create the output name (STPZ)
        extension = PEV.pak_file_path_original.split(".")[-1]
        basename = os.path.basename(PEV.pak_file_path_original).replace("." + extension,
                                                                        datetime.now().
                                                                        strftime("_%d-%m-%Y_%H-%M-%S"))

        # Ask to the user where to save the file
        path_output_file = QFileDialog.getSaveFileName(self, "Save file",
                                                       os.path.abspath(os.path.join(os.getcwd(), basename)),
                                                       "PAK files (*.pak)")[0]

        # Check if the user has selected an output path
        if path_output_file:

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

                        # If the user has edited one character, we will save the file
                        if CPEV.character_list_edited:

                            pak_export_path = PEV.pak_file_path.replace("." + extension, "_m." + extension)
                            copyfile(PEV.pak_file_path, pak_export_path)

                            # We open the file decrypted
                            with open(pak_export_path, mode="rb+") as file:

                                # Change the transformations in the file
                                for character in CPEV.character_list_edited:

                                    # Save the visual parameters
                                    file.seek(character.position_visual_parameters)

                                    # Health
                                    file.write(character.health.to_bytes(4, byteorder="big"))

                                    # Camera size (cutscene)
                                    file.write(struct.pack('>f', character.camera_size[0]))
                                    # Camera size (idle)
                                    file.write(struct.pack('>f', character.camera_size[1]))

                                    # hit box
                                    file.write(struct.pack('>f', character.hit_box))

                                    # UNK data for now
                                    file.seek(12, 1)

                                    # Aura size (idle)
                                    file.write(struct.pack('>f', character.aura_size[0]))
                                    # Aura size (dash)
                                    file.write(struct.pack('>f', character.aura_size[1]))
                                    # Aura size (charge)
                                    file.write(struct.pack('>f', character.aura_size[2]))

                                    # UNK data for now
                                    file.seek(5, 1)
                                    # Color lightnining
                                    file.write(character.color_lightning.to_bytes(1, byteorder="big"))

                                    # UNK data for now
                                    file.seek(69, 1)
                                    # Glow/Lightning
                                    file.write(character.glow_lightning.to_bytes(1, byteorder="big"))

                                    # Save the transformation parameters
                                    file.seek(character.position_trans)

                                    file.write(character.character_id.to_bytes(1, byteorder="big"))

                                    file.write(character.transformation_effect.to_bytes(1, byteorder="big"))
                                    file.write(character.transformation_partner.to_bytes(1, byteorder="big"))
                                    for transformation in character.transformations:
                                        file.write(transformation.to_bytes(1, byteorder="big"))
                                    for trans_ki_ammount in character.amount_ki_transformations:
                                        file.write(trans_ki_ammount.to_bytes(1, byteorder="big"))
                                    for trans_animation in character.transformations_animation:
                                        file.write(trans_animation.to_bytes(1, byteorder="big"))

                                    # Move four positions because is unk data
                                    file.seek(4, 1)

                                    file.write(character.fusion_partner[0].to_bytes(1, byteorder="big"))
                                    file.write(character.fusion_partner[1].to_bytes(1, byteorder="big"))
                                    for fusion in character.fusions:
                                        file.write(fusion.to_bytes(1, byteorder="big"))
                                    for fusion_ki_ammount in character.amount_ki_fusions:
                                        file.write(fusion_ki_ammount.to_bytes(1, byteorder="big"))
                                    for fusion_animation in character.fusions_animation:
                                        file.write(fusion_animation.to_bytes(1, byteorder="big"))

                            # Generate the final file for the game
                            args = os.path.join(PEV.dbrb_compressor_path) + " \"" + pak_export_path + "\" \"" \
                                + path_output_file + "\""
                            os.system('cmd /c ' + args)

                            # Remove the uncompressed modified file
                            os.remove(pak_export_path)

                            msg = QMessageBox()
                            msg.setWindowTitle("Message")
                            message = "The file were saved and compressed in: <b>" + path_output_file \
                                      + "</b><br><br> Do you wish to open the folder?"
                            message_open_saved_files = msg.question(self, '', message, msg.Yes | msg.No)

                            # If the users click on 'Yes', it will open the path where the files were saved
                            if message_open_saved_files == msg.Yes:
                                # Show the path folder to the user
                                os.system('explorer.exe ' + os.path.dirname(path_output_file).replace("/", "\\"))

                        else:
                            msg = QMessageBox()
                            msg.setWindowTitle("Warning")
                            msg.setText("The file hasn't been modified.")
                            msg.exec()

                    # The user wants to save the pak file from the 'pak explorer'
                    else:
                        pack_and_save_file(self, path_output_file)
                        
            # We save the data from the 'pak explorer' tab
            elif self.pak_explorer.isEnabled():
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
            "Raging tools 1.0 by <a href=https://www.youtube.com/channel/UCkZajFypIgQL6mI6OZLEGXw>adsl14</a>")
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
