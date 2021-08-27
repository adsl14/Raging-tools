from shutil import copyfile, rmtree, move

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from lib.design.Raging_tools import *
from lib.packages import datetime
from lib.functions import *
from lib.vram_explorer.VramExplorerFunctions import *


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        #
        # File tab
        self.actionOpen.triggered.connect(self.action_open_logic)
        self.actionSave.triggered.connect(self.action_save_logic)
        self.actionClose.triggered.connect(self.close)

        # About tab
        self.actionAuthor.triggered.connect(self.action_author_logic)
        self.actionCredits.triggered.connect(self.action_credits_logic)

        # Buttons
        self.exportButton.clicked.connect(self.action_export_logic)
        self.exportAllButton.clicked.connect(self.action_export_all_logic)
        self.importButton.clicked.connect(self.action_import_logic)
        self.exportButton.setVisible(False)
        self.exportAllButton.setVisible(False)
        self.importButton.setVisible(False)

        # Labels
        self.encodingImageText.setVisible(False)
        self.mipMapsImageText.setVisible(False)
        self.sizeImageText.setVisible(False)
        self.fileNameText.setVisible(False)

    # vram explorer methods
    def action_export_logic(self):

        # If the encoding is DXT5 or DXT1, we show the dds image
        if VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].dxt_encoding != 0:
            # Save dds file
            export_path = QFileDialog.getSaveFileName(self, "Save file", os.path.join(os.path.abspath(os.getcwd()),
                                                                                      VramExplorerVars.tx2_datas[
                                                                                          VramExplorerVars.current_selected_texture]
                                                                                      .name + ".dds"),
                                                      "DDS file (*.dds)")[0]

            data = VramExplorerVars.tx2_datas[VramExplorerVars.current_selected_texture].data

        else:
            # Save bmp file
            export_path = QFileDialog.getSaveFileName(self, "Save file", os.path.join(os.path.abspath(os.getcwd()),
                                                                                      VramExplorerVars.tx2_datas[
                                                                                          VramExplorerVars.current_selected_texture]
                                                                                      .name + ".bmp"),
                                                      "BMP file (*.bmp)")[0]

            if VramExplorerVars.tx2_datas[VramExplorerVars.current_selected_texture].extension != "png":
                data = VramExplorerVars.tx2_datas[VramExplorerVars.current_selected_texture].data
            else:
                data = VramExplorerVars.tx2_datas[VramExplorerVars.current_selected_texture].data_unswizzle

        if export_path:
            file = open(export_path, mode="wb")
            file.write(data)
            file.close()

    def action_export_all_logic(self):

        # Create folder
        if not os.path.exists("textures"):
            os.mkdir("textures")
        name_folder = os.path.basename(VramExplorerVars.vram_file_path_original).replace(".vram", "")
        folder_export_path = os.path.join(os.path.abspath(os.getcwd()), "textures", name_folder)
        if not os.path.exists(folder_export_path):
            os.mkdir(folder_export_path)

        for i in range(0, VramExplorerVars.sprp_struct.data_count):
            # The image is dds
            if VramExplorerVars.tx2d_infos[i].dxt_encoding != 0:

                file = open(os.path.join(folder_export_path, VramExplorerVars.tx2_datas[i].name + ".dds"), mode="wb")

                file.write(VramExplorerVars.tx2_datas[i].data)
                file.close()

            else:
                file = open(os.path.join(folder_export_path, VramExplorerVars.tx2_datas[i].name + ".bmp"), mode="wb")
                if VramExplorerVars.tx2_datas[i].extension != "png":
                    file.write(VramExplorerVars.tx2_datas[i].data)
                else:
                    file.write(VramExplorerVars.tx2_datas[i].data_unswizzle)
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
        if VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].dxt_encoding != 0:
            import_path = QFileDialog.getOpenFileName(self, "Open file",
                                                      os.path.join(os.path.abspath(VramExplorerVars.spr_file_path),
                                                                   VramExplorerVars.tx2_datas[VramExplorerVars.current_selected_texture].name + ".dds"),
                                                      "DDS file (*.dds)")[0]
        # For BMP (rgba image)
        else:
            import_path = QFileDialog.getOpenFileName(self, "Open file",
                                                      os.path.join(os.path.abspath(VramExplorerVars.spr_file_path),
                                                                   VramExplorerVars.tx2_datas[VramExplorerVars.current_selected_texture].name + ".bmp"),
                                                      "BMP file (*.bmp)")[0]
        # The user didn't cancel the file to import
        if import_path:
            with open(import_path, mode="rb") as file:
                header = file.read(2).hex()

                # It's a DDS modded image
                if header != "424d":
                    # It's a DDS file the selected texture
                    if VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].dxt_encoding != 0:

                        # Get the height and width of the modified image
                        file.seek(12)
                        height = int.from_bytes(file.read(VramExplorerVars.bytes2Read), 'little')
                        width = int.from_bytes(file.read(VramExplorerVars.bytes2Read), 'little')
                        # Get the mipmaps
                        file.seek(28)
                        mip_maps = int.from_bytes(file.read(1), 'big')
                        # Get the dxtencoding
                        file.seek(84)
                        dxt_encoding = get_dxt_value(file.read(VramExplorerVars.bytes2Read).decode())

                        message = validation_dds_imported_texture(VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture],
                                                                  width, height, mip_maps, dxt_encoding)

                        # If the message is empty, there is no differences between original and modified one
                        msg = QMessageBox()
                        if message:

                            # Concatenate the base message and the differences the tool has found
                            message = VramExplorerVars.message_base_import_DDS_start + "<ul>" + message + "</ul>" \
                                      + VramExplorerVars.message_base_import_DDS_end

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
                        difference = len_data - VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].data_size
                        if difference != 0:
                            VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].data_size = len_data
                            VramExplorerVars.offset_quanty_difference[VramExplorerVars.current_selected_texture] = difference

                        # Change width
                        if VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].width != width:
                            VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].width = width
                            self.sizeImageText.setText(
                                "Resolution: %dx%d" % (width, VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].height))
                        # Change height
                        if VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].height != height:
                            VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].height = height
                            self.sizeImageText.setText(
                                "Resolution: %dx%d" % (VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].width, height))

                        # Change mipMaps
                        if VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].mip_maps != mip_maps:
                            VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].mip_maps = mip_maps
                            self.mipMapsImageText.setText("Mipmaps: %s" % mip_maps)

                        # Change dxt encoding
                        if VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].dxt_encoding != dxt_encoding:
                            VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].dxt_encoding = dxt_encoding
                            self.encodingImageText.setText("Encoding: %s" %
                                                           (get_encoding_name(dxt_encoding)))

                        # Change texture in the array
                        VramExplorerVars.tx2_datas[VramExplorerVars.current_selected_texture].data = data

                        # Add the index texture that has been modified
                        # (if it was added before, we won't added twice)
                        if VramExplorerVars.current_selected_texture not in VramExplorerVars.textures_index_edited:
                            VramExplorerVars.textures_index_edited.append(VramExplorerVars.current_selected_texture)

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
                    if VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].dxt_encoding == 0:

                        # Get the height and width of the modified image
                        file.seek(18)
                        width = int.from_bytes(file.read(VramExplorerVars.bytes2Read), 'little')
                        height = int.from_bytes(file.read(VramExplorerVars.bytes2Read), 'little')

                        # Get the number of bits
                        file.seek(28)
                        number_bits = int.from_bytes(file.read(2), 'little')

                        # Validate the BMP imported texture
                        message = validation_bmp_imported_texture(VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture],
                                                                  width, height, number_bits)

                        # If there is a message, it has detected differences
                        if message:
                            # If the imported texture is not png, we ask the user first to add it or not
                            if VramExplorerVars.tx2_datas[VramExplorerVars.current_selected_texture].extension != "png":

                                msg = QMessageBox()

                                # Concatenate the base message and the differences the tool has found
                                message = VramExplorerVars.message_base_import_DDS_start + "<ul>" + message + "</ul>" \
                                    + VramExplorerVars.message_base_import_DDS_end

                                # Ask to the user if he/she is sure that wants to replace the texture
                                msg.setWindowTitle("Warning")
                                message_import_result = msg.question(self, '', message, msg.Yes | msg.No)

                                # If the users click on 'NO', the modified texture won't be imported
                                if message_import_result == msg.No:
                                    return
                            else:
                                msg = QMessageBox()
                                msg.setWindowTitle("Error")
                                msg.setText(VramExplorerVars.message_base_import_BMP_start + "<ul>" + message + "</ul>")
                                msg.exec()
                                return

                        # Get all the data
                        file.seek(0)
                        data = file.read()

                        # It's not png file
                        if VramExplorerVars.tx2_datas[VramExplorerVars.current_selected_texture].extension != "png":
                            # Importing the texture
                            # Get the difference in size between original and modified in order to change the offsets
                            len_data = len(data[54:])
                            difference = len_data - VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].data_size
                            if difference != 0:
                                VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].data_size = len_data
                                VramExplorerVars.offset_quanty_difference[VramExplorerVars.current_selected_texture] = difference

                            # Change width
                            if VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].width != width:
                                VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].width = width
                                self.sizeImageText.setText(
                                    "Resolution: %dx%d" % (width, VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].height))
                            # Change height
                            if VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].height != height:
                                VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].height = height
                                self.sizeImageText.setText(
                                    "Resolution: %dx%d" % (VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].width, height))

                            # Change texture in the array
                            VramExplorerVars.tx2_datas[VramExplorerVars.current_selected_texture].data = data

                        else:
                            # Importing the texture
                            # Change texture in the array
                            VramExplorerVars.tx2_datas[VramExplorerVars.current_selected_texture].data_unswizzle = data

                        # Add the index texture that has been modified (if it was added before,
                        # we won't added twice)
                        if VramExplorerVars.current_selected_texture not in VramExplorerVars.textures_index_edited:
                            VramExplorerVars.textures_index_edited.append(VramExplorerVars.current_selected_texture)

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

    def action_open_logic(self):

        # Open spr file
        VramExplorerVars.spr_file_path_original = \
            QFileDialog.getOpenFileName(self, "Open file", os.path.abspath(os.getcwd()), "SPR files (*.spr)")[0]
        # Check if the user has selected an spr format file
        if not os.path.exists(VramExplorerVars.spr_file_path_original):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("A spr file is needed.")
            msg.exec()
            return
        # Check if the user has selected an spr stpz file
        with open(VramExplorerVars.spr_file_path_original, mode="rb") as spr_file:
            type_file = spr_file.read(4).hex()
            if type_file == VramExplorerVars.STPZ:
                VramExplorerVars.stpz_file = True
            else:
                VramExplorerVars.stpz_file = False

        # Open vram file
        VramExplorerVars.vram_file_path_original = \
            QFileDialog.getOpenFileName(self, "Open file", os.path.abspath(VramExplorerVars.spr_file_path_original),
                                        "Texture files (*.vram)")[0]
        if not os.path.exists(VramExplorerVars.vram_file_path_original):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("A vram file is needed.")
            msg.exec()
            return

        # Clean the variables
        VramExplorerVars.sprpDatasInfo.clear()
        VramExplorerVars.tx2_datas.clear()
        VramExplorerVars.tx2d_infos.clear()
        VramExplorerVars.textures_index_edited.clear()

        basename = os.path.basename(VramExplorerVars.spr_file_path_original)

        # Convert spr and vram files if we're dealing with stpz file
        if VramExplorerVars.stpz_file:
            # Create a folder where we store the necessary files or delete it. If already exists,
            # we remove every files in it
            if os.path.exists(VramExplorerVars.temp_folder):
                rmtree(VramExplorerVars.temp_folder, onerror=del_rw)
            os.mkdir(VramExplorerVars.temp_folder)

            # Execute the script in a command line for the spr file
            VramExplorerVars.spr_file_path = os.path.join(os.path.abspath(os.getcwd()), VramExplorerVars.temp_folder, basename.replace(".spr", "_u.spr"))
            args = os.path.join(VramExplorerVars.dbrb_compressor_path) + " \"" + VramExplorerVars.spr_file_path_original + "\" \"" + VramExplorerVars.spr_file_path + "\""
            os.system('cmd /c ' + args)

            # Execute the script in a command line for the vram file
            basename = os.path.basename(VramExplorerVars.vram_file_path_original)
            VramExplorerVars.vram_file_path = os.path.join(os.path.abspath(os.getcwd()), VramExplorerVars.temp_folder,
                                          basename.replace(".vram", "_u.vram"))
            args = os.path.join(VramExplorerVars.dbrb_compressor_path) + " \"" + \
                VramExplorerVars.vram_file_path_original + "\" \"" + VramExplorerVars.vram_file_path + "\""
            os.system('cmd /c ' + args)

            # Load the data from the files
            open_spr_file(VramExplorerVars.spr_file_path, 16)

        # Generic spr file. Don't need to convert
        else:
            VramExplorerVars.spr_file_path = VramExplorerVars.spr_file_path_original
            VramExplorerVars.vram_file_path = VramExplorerVars.vram_file_path_original
            open_spr_file(VramExplorerVars.spr_file_path, 12)

        open_vram_file(VramExplorerVars.vram_file_path)

        # Add the names to the list view
        VramExplorerVars.current_selected_texture = 0
        model = QStandardItemModel()
        self.listView.setModel(model)
        item_0 = QStandardItem(VramExplorerVars.tx2_datas[0].name)
        item_0.setEditable(False)
        model.appendRow(item_0)
        self.listView.setCurrentIndex(model.indexFromItem(item_0))
        for tx2_data_element in VramExplorerVars.tx2_datas[1:]:
            item = QStandardItem(tx2_data_element.name)
            item.setEditable(False)
            model.appendRow(item)
        self.listView.clicked.connect(
            lambda q_model_idx: action_item(q_model_idx, self.imageTexture, self.encodingImageText,
                                            self.mipMapsImageText,
                                            self.sizeImageText))

        # If the texture encoded is DXT1 or DXT5, we call the show dds function
        if VramExplorerVars.tx2d_infos[0].dxt_encoding != 0:
            # Create the dds in disk and open it
            show_dds_image(self.imageTexture, VramExplorerVars.tx2_datas[0].data, VramExplorerVars.tx2d_infos[0].width, VramExplorerVars.tx2d_infos[0].height)
        else:
            if VramExplorerVars.tx2_datas[0].extension != "png":
                show_bmp_image(self.imageTexture, VramExplorerVars.tx2_datas[0].data, VramExplorerVars.tx2d_infos[0].width, VramExplorerVars.tx2d_infos[0].height)
            else:
                show_bmp_image(self.imageTexture, VramExplorerVars.tx2_datas[0].data_unswizzle, VramExplorerVars.tx2d_infos[0].width,
                               VramExplorerVars.tx2d_infos[0].height)

        # Show the buttons
        self.exportButton.setVisible(True)
        self.exportAllButton.setVisible(True)
        self.importButton.setVisible(True)

        # Show the text labels
        self.fileNameText.setText(basename.split(".")[0])
        self.fileNameText.setVisible(True)
        self.encodingImageText.setText(
            "Encoding: %s" % (get_encoding_name(VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].dxt_encoding)))
        self.mipMapsImageText.setText("Mipmaps: %d" % VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].mip_maps)
        self.sizeImageText.setText(
            "Resolution: %dx%d" % (VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture].width, VramExplorerVars.tx2d_infos[VramExplorerVars.current_selected_texture]
                                   .height))
        self.encodingImageText.setVisible(True)
        self.mipMapsImageText.setVisible(True)
        self.sizeImageText.setVisible(True)

    def action_save_logic(self):

        if not VramExplorerVars.tx2_datas:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText("There is no file loaded.")
            msg.exec()
        elif not VramExplorerVars.textures_index_edited:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText("The file hasn't been modified.")
            msg.exec()
        else:

            # Create the folder where we save the modified files
            basename = os.path.basename(VramExplorerVars.vram_file_path_original) \
                .replace(".vram", datetime.now().strftime("_%d-%m-%Y_%H-%M-%S"))
            path_output_folder = os.path.join(os.path.abspath(os.getcwd()), "outputs")
            path_output_files = os.path.join(path_output_folder, basename)

            if not os.path.exists(path_output_folder):
                os.mkdir(path_output_folder)
            os.mkdir(path_output_files)

            # Default paths
            spr_export_path = VramExplorerVars.spr_file_path.replace(".spr", "_m.spr")
            vram_export_path = VramExplorerVars.vram_file_path.replace(".vram", "_m.vram")

            # Sort the indexes of the modified textures
            VramExplorerVars.textures_index_edited.sort()

            # Create a copy of the original file
            copyfile(VramExplorerVars.spr_file_path, spr_export_path)

            # Update the offsets
            with open(spr_export_path, mode="rb+") as output_file_spr:
                first_index_texture_edited = VramExplorerVars.textures_index_edited[0]
                # Move where the information starts to the first modified texture
                output_file_spr.seek(VramExplorerVars.sprp_struct.data_base + VramExplorerVars.sprpDatasInfo[first_index_texture_edited].data_offset + 12)
                # Change the size
                output_file_spr.write(VramExplorerVars.tx2d_infos[first_index_texture_edited].data_size.to_bytes(4, byteorder="big"))
                # Change width
                output_file_spr.write(VramExplorerVars.tx2d_infos[first_index_texture_edited].width.to_bytes(2, byteorder="big"))
                # Change height
                output_file_spr.write(VramExplorerVars.tx2d_infos[first_index_texture_edited].height.to_bytes(2, byteorder="big"))
                # Change mip_maps
                output_file_spr.seek(2, os.SEEK_CUR)
                output_file_spr.write(VramExplorerVars.tx2d_infos[first_index_texture_edited].mip_maps.to_bytes(2, byteorder="big"))
                # Change dxt encoding
                output_file_spr.seek(8, os.SEEK_CUR)
                output_file_spr.write(VramExplorerVars.tx2d_infos[first_index_texture_edited].dxt_encoding.to_bytes(1, byteorder="big"))

                # Check if is the last texture modified and there is no more textures in the bottom
                if first_index_texture_edited + 1 < VramExplorerVars.sprp_struct.data_count:
                    quanty_aux = int(VramExplorerVars.offset_quanty_difference[first_index_texture_edited])
                    # Reset offset difference for the first texture edited
                    VramExplorerVars.offset_quanty_difference[first_index_texture_edited] = 0
                    first_index_texture_edited += 1
                    for i in range(first_index_texture_edited, VramExplorerVars.sprp_struct.data_count):

                        # Move where the information starts to the next textures
                        output_file_spr.seek(VramExplorerVars.sprp_struct.data_base + VramExplorerVars.sprpDatasInfo[i].data_offset + 4)
                        # Update the offset
                        VramExplorerVars.tx2d_infos[i].data_offset += quanty_aux
                        output_file_spr.write(int(abs(VramExplorerVars.tx2d_infos[i].data_offset)).to_bytes(4, byteorder="big"))
                        output_file_spr.seek(4, os.SEEK_CUR)

                        # Write the new data size
                        output_file_spr.write(VramExplorerVars.tx2d_infos[i].data_size.to_bytes(4, byteorder="big"))
                        # Write the new  width
                        output_file_spr.write(VramExplorerVars.tx2d_infos[i].width.to_bytes(2, byteorder="big"))
                        # Write the new  height
                        output_file_spr.write(VramExplorerVars.tx2d_infos[i].height.to_bytes(2, byteorder="big"))
                        # Write the new  mip_maps
                        output_file_spr.seek(2, os.SEEK_CUR)
                        output_file_spr.write(VramExplorerVars.tx2d_infos[i].mip_maps.to_bytes(2, byteorder="big"))
                        # Write the new  dxt encoding
                        output_file_spr.seek(8, os.SEEK_CUR)
                        output_file_spr.write(VramExplorerVars.tx2d_infos[i].dxt_encoding.to_bytes(1, byteorder="big"))

                        # Increment the difference only if the difference is not 0 and reset the offset differency array
                        if VramExplorerVars.offset_quanty_difference[i] != 0:
                            quanty_aux += VramExplorerVars.offset_quanty_difference[i]
                            VramExplorerVars.offset_quanty_difference[i] = 0

            # replacing textures
            with open(vram_export_path, mode="wb") as output_file:
                with open(VramExplorerVars.vram_file_path, mode="rb") as input_file:

                    # If we're dealing with a vram stpz file
                    if VramExplorerVars.stpz_file:

                        # If we're dealing with a normal STPK
                        if VramExplorerVars.single_stpk_header:
                            # Move to the position 16, where it tells the offset of the file where the texture starts
                            data = input_file.read(16)

                            output_file.write(data)

                            data = input_file.read(VramExplorerVars.bytes2Read)
                            output_file.write(data)
                            texture_offset = int.from_bytes(data, "big")

                        # We're dealing with RB2 to RB1 port
                        else:
                            # Move to the position 16 + 64, where it tells the offset of the
                            # file where the texture starts
                            data = input_file.read(16 + 64)

                            output_file.write(data)

                            data = input_file.read(VramExplorerVars.bytes2Read)
                            output_file.write(data)
                            texture_offset = int.from_bytes(data, "big") + 64

                    else:
                        texture_offset = 0

                    # Get each offset texture and write over the original file
                    for texture_index in VramExplorerVars.textures_index_edited:
                        tx2d_info = VramExplorerVars.tx2d_infos[texture_index]
                        tx2d_data = VramExplorerVars.tx2_datas[texture_index]
                        data = input_file.read(abs(tx2d_info.data_offset_old + texture_offset - input_file.tell()))
                        output_file.write(data)
                        input_file.seek(tx2d_info.data_size_old, os.SEEK_CUR)

                        # It's a DDS image
                        if tx2d_info.dxt_encoding != 0:
                            output_file.write(VramExplorerVars.tx2_datas[texture_index].data[128:])
                        else:

                            if tx2d_data.extension != "png":
                                # We're dealing with a shader. We have to change the endian
                                if tx2d_info.height == 1:
                                    output_file.write(change_endian(VramExplorerVars.tx2_datas[texture_index].data[54:]))
                                else:
                                    output_file.write(VramExplorerVars.tx2_datas[texture_index].data[54:])
                            else:
                                # Write in disk the data swizzled
                                with open("tempSwizzledImage", mode="wb") as file:
                                    file.write(VramExplorerVars.tx2_datas[texture_index].data)

                                # Write in disk the data unswizzled
                                with open("tempUnSwizzledImage", mode="wb") as file:
                                    file.write(VramExplorerVars.tx2_datas[texture_index].data_unswizzle[54:])

                                # Write in disk the indexes
                                with open("Indexes.txt", mode="w") as file:
                                    for index in VramExplorerVars.tx2_datas[texture_index].indexes_unswizzle_algorithm:
                                        file.write(index + ";")    

                                # Run the exe file of 'swizzle.exe' with the option '-s' to swizzle the image
                                args = os.path.join(VramExplorerVars.swizzle_path) + " \"" + "tempSwizzledImage" + "\" \"" + \
                                    "tempUnSwizzledImage" + "\" \"" + "Indexes.txt" + "\" \"" + "-s" + "\""
                                os.system('cmd /c ' + args)

                                # Get the data from the .exe
                                with open("tempSwizzledImageModified", mode="rb") as file:
                                    VramExplorerVars.tx2_datas[texture_index].data = file.read()

                                # Remove the temp files
                                os.remove("tempSwizzledImage")
                                os.remove("tempUnSwizzledImage")
                                os.remove("Indexes.txt")
                                os.remove("tempSwizzledImageModified")

                                output_file.write(VramExplorerVars.tx2_datas[texture_index].data)

                    data = input_file.read()
                    output_file.write(data)

                    # Modify the bytes in pos 20 that indicates the size of the file
                    vram_file_size = abs(VramExplorerVars.vram_file_size_old + output_file.tell() - input_file.tell())

            # Change the header of pos 256 in spr file because in that place indicates the size of the final output file
            with open(spr_export_path, mode="rb+") as output_file:
                output_file.seek(VramExplorerVars.stpk_struct.data_offset + 48)
                output_file.write(vram_file_size.to_bytes(4, byteorder='big'))

            # If we're dealing with a vram stpz file
            if VramExplorerVars.stpz_file:
                # Change the header of pos 20 in vram file because that place indicates the size of the final output
                # file
                with open(vram_export_path, mode="rb+") as output_file:
                    output_file.seek(20)
                    output_file.write(vram_file_size.to_bytes(4, byteorder='big'))

                # Generate the final files for the game
                # Output for the spr file
                basename_spr = os.path.basename(VramExplorerVars.spr_file_path_original)
                VramExplorerVars.spr_file_path_modified = os.path.join(path_output_files, basename_spr)
                args = os.path.join(VramExplorerVars.dbrb_compressor_path) + " \"" + spr_export_path + "\" \"" \
                    + VramExplorerVars.spr_file_path_modified + "\""
                os.system('cmd /c ' + args)

                # Output for the vram file
                basename_vram = os.path.basename(VramExplorerVars.vram_file_path_original)
                VramExplorerVars.vram_file_path_modified = os.path.join(path_output_files, basename_vram)
                args = os.path.join(VramExplorerVars.dbrb_compressor_path) + " \"" + vram_export_path + "\" \"" \
                    + VramExplorerVars.vram_file_path_modified + "\" "
                os.system('cmd /c ' + args)

                # Remove the uncompressed modified files
                os.remove(spr_export_path)
                os.remove(vram_export_path)

            else:

                basename_spr = os.path.basename(spr_export_path).replace("_m.", ".")
                basename_vram = os.path.basename(vram_export_path).replace("_m.", ".")
                VramExplorerVars.spr_file_path_modified = os.path.join(path_output_files, basename_spr)
                VramExplorerVars.vram_file_path_modified = os.path.join(path_output_files, basename_vram)

                move(spr_export_path, VramExplorerVars.spr_file_path_modified)
                move(vram_export_path, VramExplorerVars.vram_file_path_modified)

            msg = QMessageBox()
            msg.setWindowTitle("Message")
            message = "The files were saved and compressed in: <b>" + path_output_files \
                      + "</b><br><br> Do you wish to open the folder?"
            message_open_saved_files = msg.question(self, '', message, msg.Yes | msg.No)

            # If the users click on 'Yes', it will open the path where the files were saved
            if message_open_saved_files == msg.Yes:
                # Show the path folder to the user
                os.system('explorer.exe ' + path_output_files)

    def closeEvent(self, event):
        if os.path.exists(VramExplorerVars.temp_folder):
            rmtree(VramExplorerVars.temp_folder, onerror=del_rw)
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
