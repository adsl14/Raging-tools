from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from lib.packages import os, image, QImage, QPixmap, np
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.classes.SprpDataInfo import SprpDataInfo
from lib.vram_explorer.classes.Tx2Data import Tx2Data
from lib.vram_explorer.classes.Tx2dInfo import Tx2dInfo


def initialize_ve(main_window):

    # Buttons
    main_window.exportButton.clicked.connect(lambda: action_export_logic(main_window))
    main_window.exportAllButton.clicked.connect(lambda: action_export_all_logic(main_window))
    main_window.importButton.clicked.connect(lambda: action_import_logic(main_window))
    main_window.exportButton.setEnabled(False)
    main_window.exportAllButton.setEnabled(False)
    main_window.importButton.setEnabled(False)

    # Labels
    main_window.encodingImageText.setVisible(False)
    main_window.mipMapsImageText.setVisible(False)
    main_window.sizeImageText.setVisible(False)
    main_window.fileNameText.setVisible(False)


def load_data_to_ve(main_window):

    # Clean the variables
    VEV.sprpDatasInfo.clear()
    VEV.tx2_datas.clear()
    VEV.tx2d_infos.clear()
    VEV.textures_index_edited.clear()

    basename = os.path.basename(VEV.spr_file_path)

    # Open spr and vram
    open_spr_file(VEV.spr_file_path)
    open_vram_file(VEV.vram_file_path)

    # Add the names to the list view
    VEV.current_selected_texture = 0
    model = QStandardItemModel()
    main_window.listView.setModel(model)
    item_0 = QStandardItem(VEV.tx2_datas[0].name)
    item_0.setEditable(False)
    model.appendRow(item_0)
    main_window.listView.setCurrentIndex(model.indexFromItem(item_0))
    for tx2_data_element in VEV.tx2_datas[1:]:
        item = QStandardItem(tx2_data_element.name)
        item.setEditable(False)
        model.appendRow(item)
    main_window.listView.clicked.connect(
        lambda q_model_idx: action_item(q_model_idx, main_window.imageTexture, main_window.encodingImageText,
                                        main_window.mipMapsImageText,
                                        main_window.sizeImageText))

    # If the texture encoded is DXT1 or DXT5, we call the show dds function
    if VEV.tx2d_infos[0].dxt_encoding != 0:
        # Create the dds in disk and open it
        show_dds_image(main_window.imageTexture, VEV.tx2_datas[0].data, VEV.tx2d_infos[0].width,
                       VEV.tx2d_infos[0].height)
    else:
        if VEV.tx2_datas[0].extension != "png":
            show_bmp_image(main_window.imageTexture, VEV.tx2_datas[0].data, VEV.tx2d_infos[0].width,
                           VEV.tx2d_infos[0].height)
        else:
            show_bmp_image(main_window.imageTexture, VEV.tx2_datas[0].data_unswizzle, VEV.tx2d_infos[0].width,
                           VEV.tx2d_infos[0].height)

    # Enable the buttons
    main_window.exportButton.setEnabled(True)
    main_window.exportAllButton.setEnabled(True)
    main_window.importButton.setEnabled(True)

    # Show the text labels
    main_window.fileNameText.setText(basename.split(".")[0])
    main_window.fileNameText.setVisible(True)
    main_window.encodingImageText.setText(
        "Encoding: %s" % (get_encoding_name(VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding)))
    main_window.mipMapsImageText.setText("Mipmaps: %d" % VEV.tx2d_infos[VEV.current_selected_texture].mip_maps)
    main_window.sizeImageText.setText(
        "Resolution: %dx%d" % (VEV.tx2d_infos[VEV.current_selected_texture].width,
                               VEV.tx2d_infos[VEV.current_selected_texture]
                               .height))
    main_window.encodingImageText.setVisible(True)
    main_window.mipMapsImageText.setVisible(True)
    main_window.sizeImageText.setVisible(True)

    # Open the tab
    if main_window.tabWidget.currentIndex() != 0:
        main_window.tabWidget.setCurrentIndex(0)


def change_endian(data):

    data = data.hex()
    new_data = ""
    for i in range(0, len(data), 8):
        new_data = new_data + data[i+6:i+8] + data[i+4:i+6] + data[i+2:i+4] + data[i:i+2]

    return bytes.fromhex(new_data)


def validation_dds_imported_texture(tx2d_info, width, height, mip_maps, dxt_encoding_text):

    message = ""

    # Check resolution
    if width != tx2d_info.width or height != tx2d_info.height:
        message = "<li> The size should be " + str(tx2d_info.width) \
            + "x" + str(tx2d_info.height) \
            + ". The imported texture is " + str(width) + "x" + str(height) + ".</li>"

    # Check mip_maps
    if tx2d_info.mip_maps != mip_maps:
        message = message + "<li> The Mipmaps should be " + str(tx2d_info.mip_maps) \
            + ". The imported texture has " + str(mip_maps) + ".</li>"

    # Check encoding
    dxt_encoding_text_original = get_encoding_name(tx2d_info.dxt_encoding)
    if dxt_encoding_text_original != dxt_encoding_text:
        message = message + "<li> The encoding should be " + dxt_encoding_text_original \
                  + ". The imported texture is " + dxt_encoding_text + ".</li>"

    return message


def validation_bmp_imported_texture(tx2d_info, width, height, number_bits):

    message = ""

    # Check resolution
    if width != tx2d_info.width or height != tx2d_info.height:
        message = "<li>The size has to be " + str(tx2d_info.width) \
            + "x" + str(tx2d_info.height) \
            + " and not " + str(width) + "x" + str(height) + ".</li>"

    # Check number of bits
    if 32 != number_bits:
        message = message + "<li>The number of bits has to be " + str(32) \
            + " and not " + str(number_bits) + " bits.</li>"

    return message


def show_dds_image(image_texture, texture_data, width, height, texture_path="temp.dds"):

    try:

        if texture_data is not None:
            # Create the dds in disk and open it
            file = open(texture_path, mode="wb")
            file.write(texture_data)
            file.close()

        img = read_dds_file(texture_path)

        mpixmap = QPixmap.fromImage(img)

        # If the image is higher in width or height from the imageTexture,
        # we will reduce the size maintaing the aspect ratio
        if width == height:
            if width > image_texture.width():
                mpixmap = mpixmap.scaled(image_texture.width(), image_texture.width())
        else:
            if width > height:
                if width > image_texture.width():
                    new_height = int((height / width) * image_texture.width())
                    mpixmap = mpixmap.scaled(image_texture.width(), new_height)
            else:
                if height > image_texture.height():
                    new_width = int((width / height) * image_texture.height())
                    mpixmap = mpixmap.scaled(new_width, image_texture.height())

        # Show the image
        image_texture.setPixmap(mpixmap)
    except OSError:
        image_texture.clear()

    if texture_data is not None:
        os.remove(texture_path)


def show_bmp_image(image_texture, texture_data, width, height):

    try:
        mpixmap = QPixmap()
        mpixmap.loadFromData(texture_data, "BMP")

        # If the image is higher in width or height from the imageTexture,
        # we will reduce the size maintaing the aspect ratio
        if width == height:
            if width > image_texture.width():
                mpixmap = mpixmap.scaled(image_texture.width(), image_texture.width())
        else:
            # Since a shader has height of 1, in order to show it more clearly, we ignore the scaling
            if height == 1:
                mpixmap = mpixmap.scaled(image_texture.width(), width)
            if width > height:
                if width > image_texture.width():
                    new_height = int((height / width) * image_texture.width())
                    mpixmap = mpixmap.scaled(image_texture.width(), new_height)
            else:
                if height > image_texture.height():
                    new_width = int((width / height) * image_texture.height())
                    mpixmap = mpixmap.scaled(new_width, image_texture.height())

        image_texture.setPixmap(mpixmap)
    except OSError:
        image_texture.clear()


def read_dds_file(file_path):
    try:
        _img = image.load(file_path)
    except OSError:
        print("The header of the image is not recognizable")
        raise OSError

    tex = _img.get_texture()
    tex = tex.get_image_data()
    _format = tex.format
    pitch = tex.width * len(_format)
    pixels = tex.get_data(_format, pitch)

    img = QImage(pixels, tex.width, tex.height, QImage.Format_ARGB32)
    img = img.rgbSwapped()

    return img


def open_spr_file(spr_path):

    with open(spr_path, mode='rb') as file:

        # Move the pointer to the pos 12 (SPR) and get the offset of the header
        file.seek(12)
        VEV.data_offset_header = int.from_bytes(file.read(VEV.bytes2Read), "big")

        # Create the VramExplorerVars.sprp_struct instance
        file.seek(VEV.data_offset_header + 20)
        VEV.sprp_struct.type_info_base = VEV.data_offset_header + 64
        VEV.sprp_struct.string_base = VEV.sprp_struct.type_info_base + int.from_bytes(file.read(VEV.bytes2Read), "big")
        file.seek(VEV.data_offset_header + 24)
        VEV.sprp_struct.data_info_base = VEV.sprp_struct.string_base + int.from_bytes(file.read(VEV.bytes2Read), "big")
        file.seek(VEV.data_offset_header + 28)
        VEV.sprp_struct.data_base = VEV.sprp_struct.data_info_base + int.from_bytes(file.read(VEV.bytes2Read), "big")
        file.seek(VEV.sprp_struct.type_info_base + 8)
        VEV.sprp_struct.data_count = int.from_bytes(file.read(VEV.bytes2Read), "big")

        # Read the first four bytes to check if the file is SPRP (50) or SPR (00).
        # SPR -> there is no names for each texture
        file.seek(3)
        data_type = file.read(1)
        if data_type != bytes.fromhex('00'):
            # Get the names of each texture
            file.seek(VEV.sprp_struct.string_base + 1)
            texture_name = ""
            counter = 0
            record_byte = True
            while True:
                data = file.read(1)
                if record_byte:
                    if data == bytes.fromhex('2E'):

                        # Get the extension
                        pointer = file.tell()
                        extension = ""
                        while True:
                            data = file.read(1)
                            if data != bytes.fromhex('00'):
                                extension = extension + data.decode('utf-8')
                            else:
                                file.seek(pointer)
                                break
                        # Store in a instance, the properties of the texture
                        tx2_data = Tx2Data()
                        tx2_data.extension = extension

                        # If the name of the texture has been already used, we add the string '_2', or '_3', etc
                        counter_name = 1
                        texture_name_aux = texture_name
                        for tx2_data_element in VEV.tx2_datas:
                            while True:
                                if texture_name_aux in tx2_data_element.name:
                                    counter_name += 1
                                    texture_name_aux = texture_name + "_" + str(counter_name)
                                else:
                                    break
                        texture_name = texture_name_aux

                        # If the name of the texture is greater than 250 (250 + 4 (.dds) = 254, we reduce the size
                        # of the string
                        if len(texture_name) > 250:
                            texture_name = texture_name[len(texture_name) - 250:]

                        # Clean the texture name from special characters
                        texture_name = texture_name.replace("|", "_")

                        # Store in a instance, the properties of the texture
                        tx2_data.name = texture_name
                        VEV.tx2_datas.append(tx2_data)
                        texture_name = ""
                        counter += 1
                        if counter == VEV.sprp_struct.data_count:
                            break
                        record_byte = False
                        continue

                    # If in the middle of the string there is a '00' value, we replace it with '_' in hex
                    elif data == bytes.fromhex('00'):
                        data = "_".encode()
                    # 82 is ‚
                    elif data == bytes.fromhex('82'):
                        data = "‚".encode()
                    # 8C is Œ
                    elif data == bytes.fromhex('8C'):
                        data = "Œ".encode()

                    # If the texture name has the value 'TX2D', it means that the .spr hasn't got all the textureNames.
                    # We will stop the loop and create defaults ones
                    if texture_name.__contains__("TX2D"):
                        VEV.tx2_datas.clear()
                        for i in range(0, VEV.sprp_struct.data_count):
                            tx2_data.name = "unknown_name_" + str(i + 1)
                            VEV.tx2_datas.append(tx2_data)
                        break

                    texture_name += data.decode('utf-8')
                else:
                    if data == bytes.fromhex('00'):
                        record_byte = True
        else:
            for i in range(0, VEV.sprp_struct.data_count):
                tx2_data = Tx2Data()
                tx2_data.name = "unknown_name_" + str(i + 1)
                VEV.tx2_datas.append(tx2_data)

        # Create a numpy array of zeros
        VEV.offset_quanty_difference = np.zeros(VEV.sprp_struct.data_count)

        # Get the data info (TX2D)
        file.seek(VEV.sprp_struct.data_info_base)
        for i in range(0, VEV.sprp_struct.data_count):
            sprp_data_info = SprpDataInfo()

            # Move where the information starts
            file.seek(8, os.SEEK_CUR)
            sprp_data_info.name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
            sprp_data_info.data_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
            sprp_data_info.dataSize = int.from_bytes(file.read(VEV.bytes2Read), "big")
            VEV.sprpDatasInfo.append(sprp_data_info)

            # Move to the next start offset
            file.seek(12, os.SEEK_CUR)

        # Get the data itself
        for sprpDataInfo in VEV.sprpDatasInfo:
            tx2_d_info = Tx2dInfo()

            # Move where the information starts
            file.seek(VEV.sprp_struct.data_base + sprpDataInfo.data_offset)

            # Move where the information starts
            file.seek(4, os.SEEK_CUR)
            tx2_d_info.data_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
            tx2_d_info.data_offset_old = tx2_d_info.data_offset
            file.seek(4, os.SEEK_CUR)
            tx2_d_info.data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
            tx2_d_info.data_size_old = tx2_d_info.data_size
            tx2_d_info.width = int.from_bytes(file.read(2), "big")
            tx2_d_info.height = int.from_bytes(file.read(2), "big")
            file.seek(2, os.SEEK_CUR)
            tx2_d_info.mip_maps = int.from_bytes(file.read(2), "big")
            file.seek(8, os.SEEK_CUR)
            tx2_d_info.dxt_encoding = int.from_bytes(file.read(1), "big")
            VEV.tx2d_infos.append(tx2_d_info)


def open_vram_file(vram_path):

    with open(vram_path, mode="rb") as file:

        # Move to the position 0, where it tells the offset of the file where the texture starts
        texture_offset = 0

        # Get each texture
        header_1 = bytes.fromhex("44 44 53 20 7C 00 00 00 07 10 00 00")
        header_3_1 = "00000000"
        header_3_3 = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000"
        for i in range(0, len(VEV.tx2d_infos)):

            # Creating DXT5 and DXT1 heading
            if VEV.tx2d_infos[i].dxt_encoding != 0:

                header_2 = VEV.tx2d_infos[i].height.to_bytes(4, 'little') + \
                           VEV.tx2d_infos[i].width.to_bytes(4, 'little') + \
                           VEV.tx2d_infos[i].data_size.to_bytes(4, 'little')

                header_3_2 = VEV.tx2d_infos[i].mip_maps.to_bytes(4, 'little')

                header_3 = bytes.fromhex(header_3_1) + header_3_2 + bytes.fromhex(header_3_3)

                header_4, header_5, header_6 = create_header(VEV.tx2d_infos[i].dxt_encoding)
                header = header_1 + header_2 + header_3 + header_4 + header_5 + header_6

                # Store the data in memory
                file.seek(VEV.tx2d_infos[i].data_offset + texture_offset)
                data = file.read(VEV.tx2d_infos[i].data_size)
                VEV.tx2_datas[i].data = header + data

            # Creating RGBA heading
            else:

                header_1_bmp = "42 4D"
                header_2_bmp = (VEV.tx2d_infos[i].data_size + 54).to_bytes(4, 'little').hex()
                header_3_bmp = "00 00 00 00 36 00 00 00 28 00 00 00"
                header_4_1_bmp = VEV.tx2d_infos[i].width.to_bytes(4, 'little').hex()
                header_4_2_bmp = VEV.tx2d_infos[i].height.to_bytes(4, 'little').hex()
                header_4_bmp = header_4_1_bmp + header_4_2_bmp
                header_5_bmp = "01 00 20 00 00 00 00 00 00 00 00 00 12 0B 00 00 12 0B 00 00 00 00 00 00 00 00 00 00"
                header = bytes.fromhex(header_1_bmp + header_2_bmp + header_3_bmp + header_4_bmp + header_5_bmp)

                # Store the data in memory
                file.seek(VEV.tx2d_infos[i].data_offset + texture_offset)
                data = file.read(VEV.tx2d_infos[i].data_size)
                # We're dealing with a shader
                if VEV.tx2d_infos[i].height == 1:
                    data = change_endian(data)
                VEV.tx2_datas[i].data = header + data

                # Check if the extension is png, to unswizzle the image
                if VEV.tx2_datas[i].extension == "png":

                    # Write in disk the data swizzled
                    with open("tempSwizzledImage", mode="wb") as file_temp:
                        file_temp.write(VEV.tx2_datas[i].data)

                    # Run the exe file of 'swizzle.exe' with the option '-u' to unswizzle the image
                    args = os.path.join(VEV.swizzle_path) + " \"" + "tempSwizzledImage" + "\" \"" + "-u" + "\""
                    os.system('cmd /c ' + args)

                    # Get the data from the .exe
                    with open("tempUnSwizzledImage", mode="rb") as file_temp:
                        VEV.tx2_datas[i].data_unswizzle = file_temp.read()
                    with open("Indexes.txt", mode="r") as file_temp:
                        VEV.tx2_datas[i].indexes_unswizzle_algorithm = file_temp.read().split(";")[:-1]
                        # [:-1] because swizzle.exe saves an '' element in the end

                    # Remove the temp files
                    os.remove("tempSwizzledImage")
                    os.remove("tempUnSwizzledImage")
                    os.remove("Indexes.txt")

                    VEV.tx2_datas[i].data_unswizzle = header + VEV.tx2_datas[i].data_unswizzle


def create_header(value):
    if value == 8:
        return bytes.fromhex("04000000"), "DXT1".encode(), bytes.fromhex(
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
            "00 00 00 00 00 00 ".strip())
    elif value == 24 or value == 32:
        return bytes.fromhex("04000000"), "DXT5".encode(), bytes.fromhex(
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 10 00 00 00 00 00 00 00 00 00 00 00 00 "
            "00 00 00 00 00 00 ".strip())


def get_encoding_name(value):
    # 0x00 RGBA, 0x08 DXT1, 0x24 and 0x32 as DXT5
    if value == 8:
        return "DXT1"
    elif value == 24 or value == 32:
        return "DXT5"
    elif value == 0:
        return "RGBA"
    else:
        return "UNKNOWN"


def get_dxt_value(encoding_name):
    # 0x00 RGBA, 0x08 DXT1, 0x24 and 0x32 as DXT5
    if encoding_name == "DXT1":
        return 8
    elif encoding_name == "DXT5":
        return 24


def action_item(q_model_index, image_texture, encoding_image_text, mip_maps_image_text, size_image_text):

    if VEV.current_selected_texture != q_model_index.row():
        VEV.current_selected_texture = q_model_index.row()

        # If the encoding is DXT5 or DXT1, we show the dds image
        if VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding != 0:
            # Create the dds in disk and open it
            show_dds_image(image_texture, VEV.tx2_datas[VEV.current_selected_texture].data,
                           VEV.tx2d_infos[VEV.current_selected_texture].width,
                           VEV.tx2d_infos[VEV.current_selected_texture].height)
        else:
            if VEV.tx2_datas[VEV.current_selected_texture].extension != "png":
                show_bmp_image(image_texture, VEV.tx2_datas[VEV.current_selected_texture].data,
                               VEV.tx2d_infos[VEV.current_selected_texture].width,
                               VEV.tx2d_infos[VEV.current_selected_texture].height)
            else:
                show_bmp_image(image_texture, VEV.tx2_datas[VEV.current_selected_texture].data_unswizzle,
                               VEV.tx2d_infos[VEV.current_selected_texture].width,
                               VEV.tx2d_infos[VEV.current_selected_texture].height)

        encoding_image_text.setText(
            "Encoding: %s" % (get_encoding_name(VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding)))
        mip_maps_image_text.setText("Mipmaps: %s" % VEV.tx2d_infos[VEV.current_selected_texture].mip_maps)
        size_image_text.setText(
            "Resolution: %dx%d" % (VEV.tx2d_infos[VEV.current_selected_texture].width,
                                   VEV.tx2d_infos[VEV.current_selected_texture]
                                   .height))


def action_export_logic(main_window):

    # If the encoding is DXT5 or DXT1, we show the dds image
    if VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding != 0:
        # Save dds file
        export_path = QFileDialog.getSaveFileName(main_window, "Save file", os.path.join(os.path.abspath(os.getcwd()),
                                                                                         VEV.tx2_datas[
                                                                                         VEV.current_selected_texture]
                                                                                         .name + ".dds"),
                                                  "DDS file (*.dds)")[0]

        data = VEV.tx2_datas[VEV.current_selected_texture].data

    else:
        # Save bmp file
        export_path = QFileDialog.getSaveFileName(main_window, "Export texture",
                                                  os.path.join(os.path.abspath(os.getcwd()),
                                                               VEV.tx2_datas[VEV.current_selected_texture].name +
                                                               ".bmp"), "BMP file (*.bmp)")[0]

        if VEV.tx2_datas[VEV.current_selected_texture].extension != "png":
            data = VEV.tx2_datas[VEV.current_selected_texture].data
        else:
            data = VEV.tx2_datas[VEV.current_selected_texture].data_unswizzle

    if export_path:
        file = open(export_path, mode="wb")
        file.write(data)
        file.close()


def action_export_all_logic(main_window):

    # Ask to the user where to save the files
    name_folder = os.path.splitext(VEV.vram_file_path)[0]
    folder_export_path = QFileDialog.getSaveFileName(main_window, "Export textures", os.path.join(
                                                   os.path.abspath(os.getcwd()), name_folder))[0]

    # Check if the user selected the folder
    if folder_export_path:

        # Create the folder
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
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + folder_export_path.replace("/", "\\"))


def action_import_logic(main_window):

    # Open spr file
    # For DDS
    if VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding != 0:
        import_path = QFileDialog.getOpenFileName(main_window, "Import texture",
                                                  os.path.join(os.path.abspath(VEV.spr_file_path),
                                                               VEV.tx2_datas[VEV.current_selected_texture].name +
                                                               ".dds"),
                                                  "DDS file (*.dds)")[0]
    # For BMP (rgba image)
    else:
        import_path = QFileDialog.getOpenFileName(main_window, "Import texture",
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
                    dxt_encoding_text = file.read(VEV.bytes2Read).decode()
                    dxt_encoding = get_dxt_value(dxt_encoding_text)

                    message = validation_dds_imported_texture(VEV.tx2d_infos[VEV.current_selected_texture],
                                                              width, height, mip_maps, dxt_encoding_text)

                    # If the message is empty, there is no differences between original and modified one
                    if message:

                        msg = QMessageBox()

                        # Concatenate the base message and the differences the tool has found
                        message = VEV.message_base_import_DDS_start + "<ul>" + message + "</ul>" \
                            + VEV.message_base_import_DDS_end

                        # Ask to the user if he/she is sure that wants to replace the texture
                        msg.setWindowTitle("Warning")
                        message_import_result = msg.question(main_window, '', message, msg.Yes | msg.No)

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
                        main_window.sizeImageText.setText(
                            "Resolution: %dx%d" % (width, VEV.tx2d_infos[VEV.current_selected_texture].height))
                    # Change height
                    if VEV.tx2d_infos[VEV.current_selected_texture].height != height:
                        VEV.tx2d_infos[VEV.current_selected_texture].height = height
                        main_window.sizeImageText.setText(
                            "Resolution: %dx%d" % (VEV.tx2d_infos[VEV.current_selected_texture].width, height))

                    # Change mipMaps
                    if VEV.tx2d_infos[VEV.current_selected_texture].mip_maps != mip_maps:
                        VEV.tx2d_infos[VEV.current_selected_texture].mip_maps = mip_maps
                        main_window.mipMapsImageText.setText("Mipmaps: %s" % mip_maps)

                    # Change dxt encoding
                    if VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding != dxt_encoding:
                        VEV.tx2d_infos[VEV.current_selected_texture].dxt_encoding = dxt_encoding
                        main_window.encodingImageText.setText("Encoding: %s" %
                                                              (get_encoding_name(dxt_encoding)))

                    # Change texture in the array
                    VEV.tx2_datas[VEV.current_selected_texture].data = data

                    # Add the index texture that has been modified
                    # (if it was added before, we won't added twice)
                    if VEV.current_selected_texture not in VEV.textures_index_edited:
                        VEV.textures_index_edited.append(VEV.current_selected_texture)

                    try:
                        # Show texture in the program
                        show_dds_image(main_window.imageTexture, None, width, height, import_path)

                    except OSError:
                        main_window.imageTexture.clear()

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
                        msg = QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setText(VEV.message_base_import_BMP_start + "<ul>" + message + "</ul>")
                        msg.exec()
                        return

                    # Get all the data
                    file.seek(0)
                    data = file.read()

                    # Get the difference in size between original and modified. If the size in each of one is
                    # different, we gather the data modified but only the exact number of bytes from the original
                    # in order to avoid the corruption of the files
                    len_data = len(data[54:])
                    difference = abs(len_data - VEV.tx2d_infos[VEV.current_selected_texture].data_size)
                    if difference != 0:
                        data = data[:-difference]

                    # It's not png file
                    if VEV.tx2_datas[VEV.current_selected_texture].extension != "png":
                        # Importing the texture
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
                        show_bmp_image(main_window.imageTexture, data, width, height)

                    except OSError:
                        main_window.imageTexture.clear()
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setText("The image you're importing is BMP and should be DDS")
                    msg.exec()
