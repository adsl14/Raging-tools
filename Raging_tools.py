from shutil import copyfile, rmtree, move

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from lib.design.Raging_tools import *
from lib.packages import datetime, os, functools, QPixmap
from lib.functions import del_rw

# vram explorer
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.VEF import change_endian, get_dxt_value
from lib.vram_explorer.VEF import get_encoding_name, show_dds_image, validation_dds_imported_texture
from lib.vram_explorer.VEF import validation_bmp_imported_texture, show_bmp_image
from lib.vram_explorer.VEF import open_spr_file, open_vram_file, action_item, initialize_ve

# character parameters editor
from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.CPEF import store_character_parameters, initialize_cpe
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

        # vram explorer
        initialize_ve(self)

        # character parameters editor
        initialize_cpe(self, QtWidgets)

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

    # vram explorer methods
    def action_open_sprvram_logic(self):

        # Open spr file
        VEV.spr_file_path_original = \
            QFileDialog.getOpenFileName(self, "Open file", os.path.abspath(os.getcwd()), "SPR files (*.spr)")[0]
        # Check if the user has selected an spr format file
        if not os.path.exists(VEV.spr_file_path_original):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("A spr file is needed.")
            msg.exec()
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

    # character parameters editor methods
    def action_open_pak_logic(self):

        # Open pak file
        CPEV.pak_file_path_original = \
            QFileDialog.getOpenFileName(self, "Open file", os.path.abspath(os.getcwd()), "PAK files (*.pak *.zpak)")[0]

        # Check if the user has selected a pak format file
        if not os.path.exists(CPEV.pak_file_path_original):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("A pak file is needed.")
            msg.exec()
            return

        # Check if the pak file is the correct one
        with open(CPEV.pak_file_path_original, mode="rb") as pak_file:
            pak_file.seek(78)
            data = pak_file.read(26)
            if data.decode('utf-8') != "operate_resident_param.pak":
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Selected file is not the correct one.")
                msg.exec()
                return

        basename = os.path.basename(CPEV.pak_file_path_original)

        # Create a folder where we store the necessary files or delete it. If already exists,
        # we remove every files in it
        if os.path.exists(CPEV.temp_folder):
            rmtree(CPEV.temp_folder, onerror=del_rw)
        os.mkdir(CPEV.temp_folder)

        # Execute the script in a command line for the pak file
        CPEV.pak_file_path = os.path.join(os.path.abspath(os.getcwd()), CPEV.temp_folder,
                                          basename.replace(".pak", "_d.pak"))
        args = os.path.join(CPEV.dbrb_compressor_path) + " \"" + CPEV.pak_file_path_original + "\" \"" + \
            CPEV.pak_file_path + "\""
        os.system('cmd /c ' + args)

        # reset the values
        CPEV.character_list_edited.clear()
        CPEV.character_list.clear()
        CPEV.chara_selected = 0  # Index of the char selected in the program

        # Read the file
        with open(CPEV.pak_file_path, mode="rb") as pak_file:

            # Read the data from the file and store the parameters
            for i in range(0, 100):
                # Create a Character object
                character = Character()

                # Move to the position where the information is located
                character.position_trans = CPEV.base_pos_trans + (i * CPEV.sizeTrans)
                pak_file.seek(character.position_trans)

                # Store the information in the object and append to a list
                store_character_parameters(character, pak_file)
                CPEV.character_list.append(character)

        # Enable the characters portraits
        for i in range(0, 62):
            CPEV.mini_portraits_image[i].setEnabled(True)

        # Show the large portrait
        self.portrait.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_000.png")))
        self.portrait.setVisible(True)

        # Show the transformations in the main panel
        self.label_trans_0.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_001.bmp")))
        self.label_trans_0.mousePressEvent = functools.partial(self.action_change_character,
                                                               index=1, modify_slot_transform=False)
        self.label_trans_1.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_002.bmp")))
        self.label_trans_1.mousePressEvent = functools.partial(self.action_change_character,
                                                               index=2, modify_slot_transform=False)
        self.label_trans_2.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_003.bmp")))
        self.label_trans_2.mousePressEvent = functools.partial(self.action_change_character,
                                                               index=3, modify_slot_transform=False)
        self.label_trans_0.setVisible(True)
        self.label_trans_1.setVisible(True)
        self.label_trans_2.setVisible(True)

        # Get the values for the fist character of the list
        character_zero = CPEV.character_list[0]

        # Show the transform panel
        self.transSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                            str(character_zero.transformations[0]).zfill(3) + ".png")))
        self.transSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                 index=character_zero.transformations[0],
                                                                 trans_slot_panel_index=0,
                                                                 fusion_slot_panel_index=-1)
        self.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                            str(character_zero.transformations[1]).zfill(3) + ".png")))
        self.transSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                 index=character_zero.transformations[1],
                                                                 trans_slot_panel_index=1,
                                                                 fusion_slot_panel_index=-1)
        self.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                            str(character_zero.transformations[2]).zfill(3) + ".png")))
        self.transSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                 index=character_zero.transformations[2],
                                                                 trans_slot_panel_index=2,
                                                                 fusion_slot_panel_index=-1)
        self.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                            str(character_zero.transformations[3]).zfill(3) + ".png")))
        self.transSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                 index=character_zero.transformations[3],
                                                                 trans_slot_panel_index=3,
                                                                 fusion_slot_panel_index=-1)
        self.transPanel.setEnabled(True)
        self.transText.setEnabled(True)

        # Show the destransformation parameter
        self.detransEffectText.setDisabled(False)
        self.detransEffectValue.setCurrentIndex(character_zero.destransformation_effect)
        self.detransEffectValue.setDisabled(False)

        # Show the transformation partner
        self.transPartnerText.setDisabled(False)
        self.transPartnerValue.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_" +
                                                              str(character_zero.transformation_partner).zfill(3)
                                                              + ".bmp")))
        self.transPartnerValue.setDisabled(False)

        # Show amount ki per transformation
        self.amount_ki_per_transformation_text.setDisabled(False)
        self.amountKi_trans1_text.setDisabled(False)
        self.amountKi_trans1_value.setValue(character_zero.amount_ki_transformations[0])
        self.amountKi_trans1_value.setDisabled(False)
        self.amountKi_trans2_text.setDisabled(False)
        self.amountKi_trans2_value.setValue(character_zero.amount_ki_transformations[1])
        self.amountKi_trans2_value.setDisabled(False)
        self.amountKi_trans3_text.setDisabled(False)
        self.amountKi_trans3_value.setValue(character_zero.amount_ki_transformations[2])
        self.amountKi_trans3_value.setDisabled(False)
        self.amountKi_trans4_text.setDisabled(False)
        self.amountKi_trans4_value.setValue(character_zero.amount_ki_transformations[3])
        self.amountKi_trans4_value.setDisabled(False)

        # Show Animation per transformation
        self.animation_per_transformation_text.setDisabled(False)
        self.animation_trans1_text.setDisabled(False)
        self.trans1_animation_value.setCurrentIndex(character_zero.transformations_animation[0])
        self.trans1_animation_value.setDisabled(False)
        self.animation_trans2_text.setDisabled(False)
        self.trans2_animation_value.setCurrentIndex(character_zero.transformations_animation[1])
        self.trans2_animation_value.setDisabled(False)
        self.animation_trans3_text.setDisabled(False)
        self.trans3_animation_value.setCurrentIndex(character_zero.transformations_animation[2])
        self.trans3_animation_value.setDisabled(False)
        self.animation_trans4_text.setDisabled(False)
        self.trans4_animation_value.setCurrentIndex(character_zero.transformations_animation[3])
        self.trans4_animation_value.setDisabled(False)

        # Show the fusion panel
        self.fusiSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                           str(character_zero.fusions[0]).zfill(3) + ".png")))
        self.fusiSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                index=character_zero.fusions[0],
                                                                trans_slot_panel_index=-1,
                                                                fusion_slot_panel_index=0)
        self.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                           str(character_zero.fusions[1]).zfill(3) + ".png")))
        self.fusiSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                index=character_zero.fusions[1],
                                                                trans_slot_panel_index=-1,
                                                                fusion_slot_panel_index=1
                                                                )
        self.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                           str(character_zero.fusions[2]).zfill(3) + ".png")))
        self.fusiSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                index=character_zero.fusions[2],
                                                                trans_slot_panel_index=-1,
                                                                fusion_slot_panel_index=2)
        self.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                           str(character_zero.fusions[3]).zfill(3) + ".png")))
        self.fusiSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                index=character_zero.fusions[3],
                                                                trans_slot_panel_index=-1,
                                                                fusion_slot_panel_index=3)
        self.fusiPanel.setEnabled(True)
        self.fusiPanelText.setEnabled(True)

        # Show the partner potara
        self.partnerPotara_text.setDisabled(False)
        self.partnerPotara_value.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_" +
                                                                str(character_zero.partner_potara).zfill(3)
                                                                + ".bmp")))
        self.partnerPotara_value.setDisabled(False)

        # Show  partner metamoran
        self.partnerMetamoran_text.setDisabled(False)
        self.partnerMetamoran_value.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_" +
                                                                   str(character_zero.partner_potara).zfill(3)
                                                                   + ".bmp")))
        self.partnerMetamoran_value.setDisabled(False)

        # Show amount ki per fusion
        self.amount_ki_per_fusion_text.setDisabled(False)
        self.amountKi_fusion1_text.setDisabled(False)
        self.amountKi_fusion1_value.setValue(character_zero.amount_ki_fusions[0])
        self.amountKi_fusion1_value.setDisabled(False)
        self.amountKi_fusion2_text.setDisabled(False)
        self.amountKi_fusion2_value.setValue(character_zero.amount_ki_fusions[1])
        self.amountKi_fusion2_value.setDisabled(False)
        self.amountKi_fusion3_text.setDisabled(False)
        self.amountKi_fusion3_value.setValue(character_zero.amount_ki_fusions[2])
        self.amountKi_fusion3_value.setDisabled(False)
        self.amountKi_fusion4_text.setDisabled(False)
        self.amountKi_fusion4_value.setValue(character_zero.amount_ki_fusions[3])
        self.amountKi_fusion4_value.setDisabled(False)

        # Show Animation per transformation
        self.animation_per_fusion_text.setDisabled(False)
        self.animation_fusion1_text.setDisabled(False)
        self.fusion1_animation_value.setCurrentIndex(character_zero.fusions_animation[0])
        self.fusion1_animation_value.setDisabled(False)
        self.animation_fusion2_text.setDisabled(False)
        self.fusion2_animation_value.setCurrentIndex(character_zero.fusions_animation[1])
        self.fusion2_animation_value.setDisabled(False)
        self.animation_fusion3_text.setDisabled(False)
        self.fusion3_animation_value.setCurrentIndex(character_zero.fusions_animation[2])
        self.fusion3_animation_value.setDisabled(False)
        self.animation_fusion4_text.setDisabled(False)
        self.fusion4_animation_value.setCurrentIndex(character_zero.fusions_animation[3])
        self.fusion4_animation_value.setDisabled(False)

        # Open the tab
        self.tabWidget.setCurrentIndex(1)

    def action_change_character(self, event, index=None, modify_slot_transform=False):

        # Change only if the char selected is other
        if CPEV.chara_selected != index:

            # Load the portrait
            self.portrait.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_" +
                                                         str(index).zfill(3) + ".png")))

            # Load the transformations for the panel transformations
            transformations = CPEV.character_list[index].transformations
            # Change panel transformations and their interactions
            if transformations[0] != 100:
                self.transSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                    str(transformations[0]).zfill(3) + ".png")))
                self.transSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=transformations[0],
                                                                         trans_slot_panel_index=0,
                                                                         fusion_slot_panel_index=-1)
                self.transSlotPanel0.setVisible(True)
            else:
                self.transSlotPanel0.setPixmap(QPixmap())
                self.transSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=100, trans_slot_panel_index=0,
                                                                         fusion_slot_panel_index=-1)
            if transformations[1] != 100:
                self.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                    str(transformations[1]).zfill(3) + ".png")))
                self.transSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=transformations[1],
                                                                         trans_slot_panel_index=1,
                                                                         fusion_slot_panel_index=-1)
                self.transSlotPanel1.setVisible(True)
            else:
                self.transSlotPanel1.setPixmap(QPixmap())
                self.transSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=100, trans_slot_panel_index=1,
                                                                         fusion_slot_panel_index=-1)
            if transformations[2] != 100:
                self.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                    str(transformations[2]).zfill(3) + ".png")))
                self.transSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=transformations[2],
                                                                         trans_slot_panel_index=2,
                                                                         fusion_slot_panel_index=-1)
                self.transSlotPanel2.setVisible(True)
            else:
                self.transSlotPanel2.setPixmap(QPixmap())
                self.transSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=100, trans_slot_panel_index=2,
                                                                         fusion_slot_panel_index=-1)
            if transformations[3] != 100:
                self.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                    str(transformations[3]).zfill(3) + ".png")))
                self.transSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=transformations[3],
                                                                         trans_slot_panel_index=3,
                                                                         fusion_slot_panel_index=-1)
                self.transSlotPanel3.setVisible(True)
            else:
                self.transSlotPanel3.setPixmap(QPixmap())
                self.transSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=100, trans_slot_panel_index=3,
                                                                         fusion_slot_panel_index=-1)

            # Modify the slots of the transformations in the main panel
            if modify_slot_transform:

                # Disable all the transformations of the slots if it has been activated in the main panel
                if self.label_trans_0.isVisible():
                    self.label_trans_0.setVisible(False)
                    self.label_trans_1.setVisible(False)
                    self.label_trans_2.setVisible(False)
                    self.label_trans_3.setVisible(False)

                # Get the original transformations for the character
                if index in CPEV.characters_with_trans:
                    transformations = CPEV.characters_with_trans_index[CPEV.characters_with_trans.index(index)]
                    num_transformations = len(transformations)
                    if num_transformations > 0:
                        self.label_trans_0.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_" +
                                                                          str(transformations[0]).zfill(3) + ".bmp")))
                        self.label_trans_0.mousePressEvent = functools.partial(self.action_change_character,
                                                                               index=transformations[0],
                                                                               modify_slot_transform=False)
                        self.label_trans_0.setVisible(True)
                        if num_transformations > 1:
                            self.label_trans_1.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_" +
                                                                              str(transformations[1]).zfill(3) +
                                                                              ".bmp")))
                            self.label_trans_1.mousePressEvent = functools.partial(self.action_change_character,
                                                                                   index=transformations[1],
                                                                                   modify_slot_transform=False)
                            self.label_trans_1.setVisible(True)
                            if num_transformations > 2:
                                self.label_trans_2.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "sc_chara_" +
                                                                                  str(transformations[2]).zfill(3) +
                                                                                  ".bmp")))
                                self.label_trans_2.mousePressEvent = functools.partial(self.action_change_character,
                                                                                       index=transformations[2],
                                                                                       modify_slot_transform=False)
                                self.label_trans_2.setVisible(True)
                                if num_transformations > 3:
                                    self.label_trans_3.setPixmap(QPixmap(os.path.join(CPEV.path_small_images,
                                                                                      "sc_chara_" +
                                                                                      str(transformations[3]).zfill(3) +
                                                                                      ".bmp")))
                                    self.label_trans_3.mousePressEvent = functools.partial(self.action_change_character,
                                                                                           index=transformations[3],
                                                                                           modify_slot_transform=False)
                                    self.label_trans_3.setVisible(True)                                                                

            # Store the actual index selected of the char
            CPEV.chara_selected = index

    def action_edit_trans_fusion_slot(self, event, char_selected_new):

        # Check if the user wants to edit the transformation slot
        if CPEV.trans_slot_panel_selected != -1:

            # If the selected character in the window is the same as in the panel transformations,
            # we assume there won't be any transformation in that slot
            # so it will be 100
            if CPEV.character_list[CPEV.chara_selected].transformations[CPEV.trans_slot_panel_selected] == \
                    char_selected_new:
                char_selected_new = 100

            # Change the transformation in our array of characters
            CPEV.character_list[CPEV.chara_selected].transformations[CPEV.trans_slot_panel_selected] = char_selected_new

            # Change the visual transformation
            if CPEV.trans_slot_panel_selected == 0:
                self.transSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                    str(char_selected_new).zfill(3) + ".png")))
                self.transSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=char_selected_new,
                                                                         trans_slot_panel_index=0,
                                                                         fusion_slot_panel_index=-1)
            elif CPEV.trans_slot_panel_selected == 1:
                self.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                    str(char_selected_new).zfill(3) + ".png")))
                self.transSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=char_selected_new,
                                                                         trans_slot_panel_index=1,
                                                                         fusion_slot_panel_index=-1)
            elif CPEV.trans_slot_panel_selected == 2:
                self.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                    str(char_selected_new).zfill(3) + ".png")))
                self.transSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=char_selected_new,
                                                                         trans_slot_panel_index=2,
                                                                         fusion_slot_panel_index=-1)
            elif CPEV.trans_slot_panel_selected == 3:
                self.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                    str(char_selected_new).zfill(3) + ".png")))
                self.transSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                         index=char_selected_new,
                                                                         trans_slot_panel_index=3,
                                                                         fusion_slot_panel_index=-1)

            # If the character was edited before, we won't append the index to our array of characters edited once
            if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
                CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])

        # fusion slot
        else:

            # If the selected character in the window is the same as in the panel fusions,
            # we assume there won't be any fusion in that slot
            # so it will be 100
            if CPEV.character_list[CPEV.chara_selected].fusions[CPEV.fusion_slot_panel_selected] == \
                    char_selected_new:
                char_selected_new = 100

            # Change the fusion in our array of characters
            CPEV.character_list[CPEV.chara_selected].fusions[CPEV.fusion_slot_panel_selected] = char_selected_new

            # Change the visual fusion
            if CPEV.fusion_slot_panel_selected == 0:
                self.fusiSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                   str(char_selected_new).zfill(3) + ".png")))
                self.fusiSlotPanel0.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                        index=char_selected_new,
                                                                        trans_slot_panel_index=-1,
                                                                        fusion_slot_panel_index=0)
            elif CPEV.fusion_slot_panel_selected == 1:
                self.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                   str(char_selected_new).zfill(3) + ".png")))
                self.fusiSlotPanel1.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                        index=char_selected_new,
                                                                        trans_slot_panel_index=-1,
                                                                        fusion_slot_panel_index=1)
            elif CPEV.fusion_slot_panel_selected == 2:
                self.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                   str(char_selected_new).zfill(3) + ".png")))
                self.fusiSlotPanel2.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                        index=char_selected_new,
                                                                        trans_slot_panel_index=-1,
                                                                        fusion_slot_panel_index=2)
            elif CPEV.fusion_slot_panel_selected == 3:
                self.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                   str(char_selected_new).zfill(3) + ".png")))
                self.fusiSlotPanel3.mousePressEvent = functools.partial(self.open_select_chara_window,
                                                                        index=char_selected_new,
                                                                        trans_slot_panel_index=-1,
                                                                        fusion_slot_panel_index=3)

            # If the character was edited before, we won't append the index to our array of characters edited once
            if CPEV.character_list[CPEV.chara_selected] not in CPEV.character_list_edited:
                CPEV.character_list_edited.append(CPEV.character_list[CPEV.chara_selected])


        self.selectCharaWindow.close()

    def open_select_chara_window(self, event, index, trans_slot_panel_index, fusion_slot_panel_index):

        # If trans_slot_panel_index is -1, means the user has selected the fusion panel
        if trans_slot_panel_index != -1:
            q_label_style = "QLabel {border : 3px solid red;}"
        else:
            q_label_style = "QLabel {border : 3px solid green;}"

        # Store in a global var what slot in the transformation and fusion panel has been selected
        CPEV.trans_slot_panel_selected = trans_slot_panel_index
        CPEV.fusion_slot_panel_selected = fusion_slot_panel_index

        # The character selected in the slot panel (trans or fusion) is not empty
        if index != 100:

            # The previous chara selected and the new are differents
            if CPEV.previous_chara_selected_character_window != index:

                # Add the color border to the character that has been selected in the trans/fusion slot
                CPEV.mini_portraits_image_select_chara_window[index].setStyleSheet(q_label_style)

                # Reset the previous character select if is not a empty character
                if CPEV.previous_chara_selected_character_window != 100:
                    CPEV.mini_portraits_image_select_chara_window[CPEV.previous_chara_selected_character_window] \
                        .setStyleSheet("QLabel {}")

                # Store the actual character selected in the select character window
                CPEV.previous_chara_selected_character_window = index

            # If the color border isn't the same, means the user has selected a different slot (trans or fusion)
            elif CPEV.mini_portraits_image_select_chara_window[index].styleSheet() != q_label_style:

                # Add the color border to the character that has been selected in the trans/fusion slot
                CPEV.mini_portraits_image_select_chara_window[index].setStyleSheet(q_label_style)

                # Store the actual character selected in the select character window
                CPEV.previous_chara_selected_character_window = index

        # If the index is 100 (means there's no character transformation),
        # we will remove the red/green border for the previous character transform panel
        elif CPEV.previous_chara_selected_character_window != index:
            CPEV.mini_portraits_image_select_chara_window[CPEV.previous_chara_selected_character_window] \
                .setStyleSheet("QLabel {}")

            CPEV.previous_chara_selected_character_window = index

        self.selectCharaWindow.show()

    def action_save_pak_logic(self):

        # If the user has edited one character, we will save
        if CPEV.character_list_edited:

            # Create the output name
            extension = CPEV.pak_file_path_original.split(".")[-1]
            basename = os.path.basename(CPEV.pak_file_path_original).replace("."+extension,
                                                                             datetime.now().
                                                                             strftime("_%d-%m-%Y_%H-%M-%S"))

            # Ask to the user where to save the file
            path_output_file = QFileDialog.getSaveFileName(self, "Save file",
                                                           os.path.abspath(os.path.join(os.getcwd(), basename)),
                                                           "PAK files (*.pak)")[0]

            if path_output_file:

                pak_export_path = CPEV.pak_file_path.replace("."+extension, "_m."+extension)
                copyfile(CPEV.pak_file_path, pak_export_path)

                # We open the file decrypted
                with open(pak_export_path, mode="rb+") as file:

                    # Change the transformations in the file
                    for character in CPEV.character_list_edited:
                        file.seek(character.position_trans)
                        for transformation in character.transformations:
                            file.write(transformation.to_bytes(1, byteorder="big"))

                # Generate the final file for the game
                args = os.path.join(CPEV.dbrb_compressor_path) + " \"" + pak_export_path + "\" \"" \
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

    def closeEvent(self, event):
        if os.path.exists(VEV.temp_folder):
            rmtree(VEV.temp_folder, onerror=del_rw)
        if os.path.exists(CPEV.temp_folder):
            rmtree(CPEV.temp_folder, onerror=del_rw)
        event.accept()

    @staticmethod
    def action_author_logic():
        msg = QMessageBox()
        msg.setTextFormat(1)
        msg.setWindowTitle("Author")
        msg.setText(
            "Raging tools 1.0 by <a href=https://www.youtube.com/channel/UCkZajFypIgQL6mI6OZLEGXw>adsl13</a>")
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
