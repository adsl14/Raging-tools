from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from pyglet.gl import GLException

from lib.packages import os, image, QImage, QPixmap, np
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.classes.MTRL.MtrlInfo import MtrlInfo
from lib.vram_explorer.classes.MTRL.MtrlLayer import MtrlLayer
from lib.vram_explorer.classes.SCNE.EyeData import EyeData
from lib.vram_explorer.classes.SCNE.ScneEyeInfo import ScneEyeInfo
from lib.vram_explorer.classes.SCNE.ScneMaterial import ScneMaterial
from lib.vram_explorer.classes.SCNE.ScneMaterialInfo import ScneMaterialInfo
from lib.vram_explorer.classes.SCNE.ScneModel import ScneModel
from lib.vram_explorer.classes.SPRP.SprpDataEntry import SprpDataEntry
from lib.vram_explorer.classes.SPRP.SprpDataInfo import SprpDataInfo
from lib.vram_explorer.classes.SPRP.SprpFile import SprpFile
from lib.vram_explorer.classes.SPRP.SprpTypeEntry import SprpTypeEntry
from lib.vram_explorer.classes.TX2D.Tx2dInfo import Tx2dInfo
from lib.vram_explorer.classes.TX2D.Tx2dVram import Tx2dVram


def initialize_ve(main_window):

    # Buttons
    main_window.exportAllButton.clicked.connect(lambda: action_export_all_logic(main_window))
    main_window.importAllButton.clicked.connect(lambda: action_import_all_logic(main_window))
    main_window.exportButton.clicked.connect(lambda: action_export_logic(main_window))
    main_window.importButton.clicked.connect(lambda: action_import_logic(main_window))
    main_window.removeButton.clicked.connect(lambda: action_remove_logic(main_window))
    main_window.addButton.clicked.connect(lambda: action_add_logic(main_window))
    main_window.exportAllButton.setEnabled(False)
    main_window.importAllButton.setEnabled(False)
    main_window.exportButton.setEnabled(False)
    main_window.importButton.setEnabled(False)
    main_window.removeButton.setEnabled(False)
    main_window.addButton.setEnabled(False)

    # Labels
    main_window.encodingImageText.setVisible(False)
    main_window.mipMapsImageText.setVisible(False)
    main_window.sizeImageText.setVisible(False)
    main_window.fileNameText.setVisible(False)


def load_data_to_ve(main_window):

    basename = os.path.basename(os.path.splitext(VEV.spr_file_path)[0])

    # Open spr and vram
    open_spr_file(VEV.spr_file_path)
    open_vram_file(VEV.vram_file_path)

    # Add the names to the list view
    model = QStandardItemModel()
    main_window.listView.setModel(model)
    item_0 = QStandardItem(VEV.sprp_file.type_entry[b'TX2D'].data_entry[0].data_info.name)
    item_0.setEditable(False)
    model.appendRow(item_0)
    main_window.listView.setCurrentIndex(model.indexFromItem(item_0))
    for data_entry in VEV.sprp_file.type_entry[b'TX2D'].data_entry[1:]:
        item = QStandardItem(data_entry.data_info.name)
        item.setEditable(False)
        model.appendRow(item)
    main_window.listView.selectionModel().currentChanged.connect(
        lambda q_model_idx: action_item(q_model_idx, main_window.imageTexture, main_window.encodingImageText,
                                        main_window.mipMapsImageText,
                                        main_window.sizeImageText))

    # If the texture encoded is DXT1 or DXT5, we call the show dds function
    if VEV.sprp_file.type_entry[b'TX2D'].data_entry[0].data_info.data.dxt_encoding != 0:
        # Create the dds in disk and open it
        show_dds_image(main_window.imageTexture, VEV.sprp_file.type_entry[b'TX2D'].data_entry[0]
                       .data_info.data.tx2d_vram.data, VEV.sprp_file.type_entry[b'TX2D']
                       .data_entry[0].data_info.data.width,
                       VEV.sprp_file.type_entry[b'TX2D'].data_entry[0].data_info.data.height)
    else:
        if VEV.sprp_file.type_entry[b'TX2D'].data_entry[0].data_info.extension != "png":
            show_bmp_image(main_window.imageTexture, VEV.sprp_file.type_entry[b'TX2D'].data_entry[0]
                           .data_info.data.tx2d_vram.data, VEV.sprp_file.type_entry[b'TX2D']
                           .data_entry[0].data_info.data.width,
                           VEV.sprp_file.type_entry[b'TX2D'].data_entry[0].data_info.data.height)
        else:
            show_bmp_image(main_window.imageTexture, VEV.sprp_file.type_entry[b'TX2D'].data_entry[0]
                           .data_info.data.tx2d_vram.data_unswizzle, VEV.sprp_file.type_entry[b'TX2D']
                           .data_entry[0].data_info.data.width,
                           VEV.sprp_file.type_entry[b'TX2D'].data_entry[0].data_info.data.height)

    # Enable the buttons
    main_window.exportAllButton.setEnabled(True)
    main_window.importAllButton.setEnabled(True)
    main_window.importButton.setEnabled(True)
    main_window.exportButton.setEnabled(True)
    main_window.removeButton.setEnabled(True)
    main_window.addButton.setEnabled(True)

    # Show the text labels
    main_window.fileNameText.setText(basename)
    main_window.fileNameText.setVisible(True)
    main_window.encodingImageText.setText(
        "Encoding: %s" % (get_encoding_name(VEV.sprp_file.type_entry[b'TX2D']
                                            .data_entry[VEV.current_selected_texture].data_info.data.dxt_encoding)))
    main_window.mipMapsImageText.setText("Mipmaps: %d" % VEV.sprp_file.type_entry[b'TX2D']
                                         .data_entry[VEV.current_selected_texture].data_info.data.mip_maps)
    main_window.sizeImageText.setText(
        "Resolution: %dx%d" % (VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]
                               .data_info.data.width,
                               VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]
                               .data_info.data.height))
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
        message = "<li> The original size is " + str(tx2d_info.width) \
            + "x" + str(tx2d_info.height) \
            + ". The imported texture is " + str(width) + "x" + str(height) + ".</li>"

    # Check mip_maps
    if tx2d_info.mip_maps != mip_maps:
        message = message + "<li> The original Mipmaps has " + str(tx2d_info.mip_maps) \
            + ". The imported texture has " + str(mip_maps) + ".</li>"

    # Check encoding
    dxt_encoding_text_original = get_encoding_name(tx2d_info.dxt_encoding)
    if dxt_encoding_text_original != dxt_encoding_text:
        message = message + "<li> The original encoding is " + dxt_encoding_text_original \
                  + ". The imported texture is " + dxt_encoding_text + ".</li>"

    return message


def validation_bmp_imported_texture(tx2d_info, width, height, number_bits, mip_maps, dxt_encoding_text):

    message = ""

    # Check resolution
    if width != tx2d_info.width or height != tx2d_info.height:
        message = "<li>The original size is " + str(tx2d_info.width) \
            + "x" + str(tx2d_info.height) \
            + ". The imported texture is " + str(width) + "x" + str(height) + ".</li>"

    # Check number of bits
    if 32 != number_bits:
        message = message + "<li>The original number of bits is " + str(32) \
            + ". The imported texture is " + str(number_bits) + " bits.</li>"

    # Check mip_maps
    if tx2d_info.mip_maps != mip_maps:
        message = message + "<li> The original Mipmaps has " + str(tx2d_info.mip_maps) \
            + ". The imported texture has " + str(mip_maps) + ".</li>"

    # Check encoding
    dxt_encoding_text_original = get_encoding_name(tx2d_info.dxt_encoding)
    if dxt_encoding_text_original != dxt_encoding_text:
        message = message + "<li> The original encoding is " + dxt_encoding_text_original \
                  + ". The imported texture is " + dxt_encoding_text + ".</li>"

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

        tex = _img.get_texture()
        tex = tex.get_image_data()
        _format = tex.format
        pitch = tex.width * len(_format)
        pixels = tex.get_data(_format, pitch)

        img = QImage(pixels, tex.width, tex.height, QImage.Format_ARGB32)
        img = img.rgbSwapped()

        return img

    except OSError:
        print("The header of the image is not recognizable")
        raise OSError
    except GLException:
        print("DDS image can't be shown")
        raise OSError


def get_name_from_spr(file, sprp_data_info):

    # Read the file until we find the '00' byte value
    while True:

        # Read one char
        data = file.read(1)

        # If the value is not 00, we store the char
        if data != b'\x00':

            # Some bytes can't be decoded directly, so we will add the string directly instead
            if data == b'\x82':
                data_decoded = ","
            elif data == b'\x8c':
                data_decoded = "Œ"
            else:
                data_decoded = data.decode('utf-8')

            sprp_data_info.name += data_decoded

        # The texture name is already stored. We clean it
        else:
            # Get the name splitted by '.'
            name_splitted = sprp_data_info.name.split(".")
            tam_name_splitted = len(name_splitted)
            sprp_data_info.name = ""

            # Get the name and extension separatelly
            if tam_name_splitted > 1:
                for i in range(0, tam_name_splitted - 1):
                    sprp_data_info.name += name_splitted[i] + ("." if i < tam_name_splitted - 2 else "")
                sprp_data_info.extension = name_splitted[-1]
            else:
                sprp_data_info.name = name_splitted[0]
                sprp_data_info.extension = ""

            # The max number of char for the name is 250
            name_size = len(sprp_data_info.name)
            if name_size > 250:
                sprp_data_info.name = sprp_data_info.name[name_size - 250:]

            # Finish the reading of the file
            break


def read_children(file, sprp_data_info, type_section):

    file.seek(sprp_data_info.child_offset + VEV.sprp_file.data_base)

    for _ in range(sprp_data_info.child_count):
        sprp_data_info_child = SprpDataInfo()

        sprp_data_info_child.name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
        sprp_data_info_child.data_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
        sprp_data_info_child.data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        sprp_data_info_child.child_count = int.from_bytes(file.read(VEV.bytes2Read), "big")
        sprp_data_info_child.child_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")

        # Get the name for the data_info
        aux_pointer_file = file.tell()
        file.seek(VEV.sprp_file.string_base + sprp_data_info_child.name_offset)
        get_name_from_spr(file, sprp_data_info_child)
        base_name_size = len(sprp_data_info_child.name)
        extension_size = len(sprp_data_info_child.extension)
        sprp_data_info_child.name_size = 1 + base_name_size + (extension_size + 1 if extension_size > 0 else 0)

        # Get the scene data
        if type_section == b'SCNE':

            # If the parent name is NODES, we store the scene model in the child data
            if sprp_data_info.name == "[NODES]":
                file.seek(VEV.sprp_file.data_base + sprp_data_info_child.data_offset)

                scne_model = ScneModel()
                scne_model.unk00 = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_model.unk04_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_model.unk08_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_model.unk0c_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_model.unk10_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")

                sprp_data_info_child.data = scne_model

            # If the children name is MATERIAL, we store the scene material in the child data
            elif sprp_data_info_child.name == "[MATERIAL]":
                file.seek(VEV.sprp_file.data_base + sprp_data_info_child.data_offset)

                scne_material = ScneMaterial()

                scne_material.name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_material.unk04 = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_material.material_info_count = int.from_bytes(file.read(VEV.bytes2Read), "big")

                for _ in range(0, scne_material.material_info_count):
                    scne_materia_info = ScneMaterialInfo()

                    scne_materia_info.unk00_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    scne_materia_info.unk04_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    scne_materia_info.unk08 = int.from_bytes(file.read(VEV.bytes2Read), "big")

                    scne_material.material_info.append(scne_materia_info)

                sprp_data_info_child.data = scne_material

            # If the children name is DbzEyeInfo, we store the scene eye info in the child data
            elif sprp_data_info_child.name == "DbzEyeInfo":
                file.seek(VEV.sprp_file.data_base + sprp_data_info_child.data_offset)

                scne_eye_info = ScneEyeInfo()

                # Get each eye_data
                for _ in range(0, 3):
                    eye_data = EyeData()
                    eye_data.unk00_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    file.seek(108, os.SEEK_CUR)

                    scne_eye_info.eyes_data.append(eye_data)
                    print(scne_eye_info.eyes_data[-1].unk00_name_offset)

                sprp_data_info_child.data = scne_eye_info

        # Restore the pointer of the file in order to read the following children
        file.seek(aux_pointer_file)

        # Get all the children sprp_data_info for the actual children in the loop section
        if sprp_data_info_child.child_count > 0:
            read_children(file, sprp_data_info_child, type_section)
            file.seek(aux_pointer_file)

        # Store each children to the array
        sprp_data_info.child_info.append(sprp_data_info_child)


def write_children(file, sprp_data_info, type_section, relative_name_offset_quanty_accumulated,
                   relative_data_offset_quanty_accumulated):

    file.seek(sprp_data_info.child_offset + VEV.sprp_file.data_base)

    for i in range(sprp_data_info.child_count):
        sprp_data_info_child = sprp_data_info.child_info[i]

        # Update name_offset
        file.write(int(sprp_data_info_child.name_offset + relative_name_offset_quanty_accumulated)
                   .to_bytes(4, byteorder="big"))

        # Update data_offset (only when the data_offset of the data_entry is not 0)
        if sprp_data_info_child.data_size > 0:
            file.write(int(sprp_data_info_child.data_offset + relative_data_offset_quanty_accumulated)
                       .to_bytes(4, byteorder="big"))
        else:
            file.seek(4, os.SEEK_CUR)

        # Write the scene data
        if type_section == b'SCNE':

            # If the parent name is NODES, we write the scene model
            if sprp_data_info.name == "[NODES]":

                aux_pointer_file = file.tell()
                file.seek(VEV.sprp_file.data_base + sprp_data_info_child.data_offset)

                file.seek(4, os.SEEK_CUR)
                if sprp_data_info_child.data.unk04_name_offset > 0:
                    file.write(int(sprp_data_info_child.data.unk04_name_offset +
                                   relative_name_offset_quanty_accumulated)
                               .to_bytes(4, byteorder="big"))
                else:
                    file.seek(4, os.SEEK_CUR)
                if sprp_data_info_child.data.unk08_name_offset > 0:
                    file.write(int(sprp_data_info_child.data.unk08_name_offset +
                                   relative_name_offset_quanty_accumulated)
                               .to_bytes(4, byteorder="big"))
                else:
                    file.seek(4, os.SEEK_CUR)
                if sprp_data_info_child.data.unk0c_name_offset > 0:
                    file.write(int(sprp_data_info_child.data.unk0c_name_offset +
                                   relative_name_offset_quanty_accumulated)
                               .to_bytes(4, byteorder="big"))
                else:
                    file.seek(4, os.SEEK_CUR)
                if sprp_data_info_child.data.unk10_name_offset > 0:
                    file.write(int(sprp_data_info_child.data.unk10_name_offset +
                                   relative_name_offset_quanty_accumulated)
                               .to_bytes(4, byteorder="big"))
                else:
                    file.seek(4, os.SEEK_CUR)

                file.seek(aux_pointer_file)

            # If the children name is MATERIAL, we write the scene model
            elif sprp_data_info_child.name == "[MATERIAL]":

                aux_pointer_file = file.tell()
                file.seek(VEV.sprp_file.data_base + sprp_data_info_child.data_offset)

                # Write the name_offset of scne_material
                if sprp_data_info_child.data.name_offset > 0:
                    file.write(int(sprp_data_info_child.data.name_offset + relative_name_offset_quanty_accumulated)
                               .to_bytes(4, byteorder="big"))
                else:
                    file.seek(4, os.SEEK_CUR)
                file.seek(8, os.SEEK_CUR)

                for j in range(0, sprp_data_info_child.data.material_info_count):

                    if sprp_data_info_child.data.material_info[j].unk00_name_offset > 0:
                        file.write(int(sprp_data_info_child.data.material_info[j].unk00_name_offset +
                                       relative_name_offset_quanty_accumulated)
                                   .to_bytes(4, byteorder="big"))
                    else:
                        file.seek(4, os.SEEK_CUR)
                    if sprp_data_info_child.data.material_info[j].unk04_name_offset > 0:
                        file.write(
                            int(sprp_data_info_child.data.material_info[j].unk04_name_offset +
                                relative_name_offset_quanty_accumulated)
                            .to_bytes(4, byteorder="big"))
                    else:
                        file.seek(4, os.SEEK_CUR)
                    file.seek(4, os.SEEK_CUR)

                file.seek(aux_pointer_file)

            # If the children name is DbzEyeInfo, we write the scene model
            elif sprp_data_info_child.name == "DbzEyeInfo":

                aux_pointer_file = file.tell()
                file.seek(VEV.sprp_file.data_base + sprp_data_info_child.data_offset)

                # Write each eye_data
                for j in range(0, 3):

                    if sprp_data_info_child.data.eyes_data[j].unk00_name_offset > 0:
                        file.write(int(sprp_data_info_child.data.eyes_data[j].unk00_name_offset +
                                       relative_name_offset_quanty_accumulated)
                                   .to_bytes(4, byteorder="big"))
                    else:
                        file.seek(4, os.SEEK_CUR)
                    file.seek(108, os.SEEK_CUR)

                file.seek(aux_pointer_file)

        # Get all the children sprp_data_info
        file.seek(8, os.SEEK_CUR)
        if sprp_data_info_child.child_count > 0:
            file.write(int(sprp_data_info_child.child_offset + relative_data_offset_quanty_accumulated)
                       .to_bytes(4, byteorder="big"))
            aux_pointer_file = file.tell()
            write_children(file, sprp_data_info_child, type_section, relative_name_offset_quanty_accumulated,
                           relative_data_offset_quanty_accumulated)
            file.seek(aux_pointer_file)
        else:
            file.seek(4, os.SEEK_CUR)


def update_offset_data_info(file, data_entry, relative_name_offset_quanty_accumulated,
                            relative_data_offset_quanty_accumulated):
    # Update name_offset
    file.write(int(data_entry.data_info.name_offset +
                   relative_name_offset_quanty_accumulated)
               .to_bytes(4, byteorder="big"))

    # Update data_offset (only when the data_offset of the data_entry is not 0)
    if data_entry.data_info.data_size > 0:
        file.write(int(data_entry.data_info.data_offset +
                       relative_data_offset_quanty_accumulated).to_bytes(4, byteorder="big"))
    else:
        file.seek(4, os.SEEK_CUR)

    # Update child_offset
    file.seek(8, os.SEEK_CUR)
    if data_entry.data_info.child_count > 0:
        file.write(int(data_entry.data_info.child_offset +
                       relative_data_offset_quanty_accumulated).to_bytes(4, byteorder="big"))
        aux_pointer_file = file.tell()
        write_children(file, data_entry.data_info, data_entry.data_type,
                       relative_name_offset_quanty_accumulated, relative_data_offset_quanty_accumulated)
        file.seek(aux_pointer_file + 4)
    else:
        file.seek(8, os.SEEK_CUR)


def update_tx2d_data(file, index):

    # Change the size
    file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[index].
               data_info.data.data_size.to_bytes(4, byteorder="big"))
    # Change width
    file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[index].
               data_info.data.width.to_bytes(2, byteorder="big"))
    # Change height
    file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[index].
               data_info.data.height.to_bytes(2, byteorder="big"))
    # Change mip_maps
    file.seek(2, os.SEEK_CUR)
    file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[index].
               data_info.data.mip_maps.to_bytes(2, byteorder="big"))
    # Change dxt encoding
    file.seek(8, os.SEEK_CUR)
    file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[index].
               data_info.data.dxt_encoding.to_bytes(1, byteorder="big"))


def open_spr_file(spr_path):

    # Clean vars
    VEV.sprp_file = SprpFile()

    with open(spr_path, mode='rb') as file:

        # Create SPRP_HEADER
        VEV.sprp_file.sprp_header.data_tag = file.read(VEV.bytes2Read)
        file.seek(4, os.SEEK_CUR)
        VEV.sprp_file.sprp_header.entry_count = int.from_bytes(file.read(VEV.bytes2Read), "big")
        file.seek(4, os.SEEK_CUR)
        VEV.sprp_file.sprp_header.name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.entry_info_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.string_table_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.data_info_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.data_block_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.ioram_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.ioram_data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.vram_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.vram_data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")

        # Create SPRP_FILE
        VEV.sprp_file.type_info_base = 64
        VEV.sprp_file.string_base = VEV.sprp_file.type_info_base + VEV.sprp_file.sprp_header.entry_info_size
        VEV.sprp_file.data_info_base = VEV.sprp_file.string_base + VEV.sprp_file.sprp_header.string_table_size
        VEV.sprp_file.data_base = VEV.sprp_file.data_info_base + VEV.sprp_file.sprp_header.data_info_size

        # Create each SPRP_TYPE_ENTRY
        file.seek(VEV.sprp_file.type_info_base)
        type_entry_offset = 0
        for i in range(0, VEV.sprp_file.sprp_header.entry_count):
            sprp_type_entry = SprpTypeEntry()
            sprp_type_entry.data_type = file.read(VEV.bytes2Read)
            file.seek(4, os.SEEK_CUR)
            sprp_type_entry.data_count = int.from_bytes(file.read(VEV.bytes2Read), "big")

            # Create each SPRP_DATA_ENTRY and under that, the SPRP_DATA_INFO
            aux_pointer_type_entry = file.tell()
            file.seek(VEV.sprp_file.data_info_base + type_entry_offset)
            for j in range(0, sprp_type_entry.data_count):

                sprp_data_entry = SprpDataEntry()
                sprp_data_entry.data_type = file.read(VEV.bytes2Read)
                sprp_data_entry.index = int.from_bytes(file.read(VEV.bytes2Read), "big")

                sprp_data_entry.data_info.name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                sprp_data_entry.data_info.data_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                sprp_data_entry.data_info.data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
                sprp_data_entry.data_info.child_count = int.from_bytes(file.read(VEV.bytes2Read), "big")
                sprp_data_entry.data_info.child_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                file.seek(4, os.SEEK_CUR)

                # Store the actual pointer in the file in order to read the following data_entry
                aux_pointer_data_entry = file.tell()

                # Store the name of the sprp_data_info
                file.seek(VEV.sprp_file.string_base + sprp_data_entry.data_info.name_offset)
                # Everything that is not SPR in the header, has names for each data
                if VEV.sprp_file.sprp_header.data_tag != b"SPR\x00":
                    get_name_from_spr(file, sprp_data_entry.data_info)
                    base_name_size = len(sprp_data_entry.data_info.name)
                    extension_size = len(sprp_data_entry.data_info.extension)
                    sprp_data_entry.data_info.name_size = 1 + base_name_size + (extension_size + 1
                                                                                if extension_size > 0 else 0)
                # If the data header is SPR, we create custom names
                else:
                    sprp_data_entry.data_info.name = sprp_type_entry.data_type.decode('utf-8') + "_" + str(j)

                # Get all the children sprp_data_info
                if sprp_data_entry.data_info.child_count > 0:
                    read_children(file, sprp_data_entry.data_info, sprp_data_entry.data_type)

                # Save the data when is the type TX2D
                if sprp_type_entry.data_type == b"TX2D":

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_base + sprp_data_entry.data_info.data_offset)

                    # Create the TX2D info
                    sprp_data_entry.data_info.data = Tx2dInfo()

                    file.seek(4, os.SEEK_CUR)
                    sprp_data_entry.data_info.data.data_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    sprp_data_entry.data_info.data.data_offset_old = sprp_data_entry.data_info.data.data_offset
                    file.seek(4, os.SEEK_CUR)
                    sprp_data_entry.data_info.data.data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    sprp_data_entry.data_info.data.data_size_old = sprp_data_entry.data_info.data.data_size
                    sprp_data_entry.data_info.data.width = int.from_bytes(file.read(2), "big")
                    sprp_data_entry.data_info.data.height = int.from_bytes(file.read(2), "big")
                    file.seek(2, os.SEEK_CUR)
                    sprp_data_entry.data_info.data.mip_maps = int.from_bytes(file.read(2), "big")
                    file.seek(8, os.SEEK_CUR)
                    sprp_data_entry.data_info.data.dxt_encoding = int.from_bytes(file.read(1), "big")

                    sprp_data_entry.data_info.data.tx2d_vram = Tx2dVram()

                # Save the data when is the type MTRL
                elif sprp_type_entry.data_type == b"MTRL":

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_base + sprp_data_entry.data_info.data_offset)

                    # Create the MTRL info
                    sprp_data_entry.data_info.data = MtrlInfo()

                    # Read unk data
                    sprp_data_entry.data_info.data.unk_00 = file.read(112)

                    # Read each layer (the max number is 10)
                    for _ in range(0, 10):
                        mtrlLayer = MtrlLayer()
                        mtrlLayer.layer_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                        mtrlLayer.source_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")

                        # Store the layer in the actual material
                        sprp_data_entry.data_info.data.layers.append(mtrlLayer)

                # Store all the info in the data_entry array
                sprp_type_entry.data_entry.append(sprp_data_entry)

                # Move to the next data_entry
                file.seek(aux_pointer_data_entry)

            # Store the type_entry to the dictionary of type_entries
            VEV.sprp_file.type_entry[sprp_type_entry.data_type] = sprp_type_entry

            file.seek(aux_pointer_type_entry)

            # Update the type_entry offset
            type_entry_offset += sprp_type_entry.data_count * 32


def open_vram_file(vram_path):

    # Clean vars
    # Current selected texture in the list view
    VEV.current_selected_texture = 0
    # The texture indexes that are edited
    VEV.textures_index_edited.clear()
    VEV.textures_index_removed.clear()
    # Acumulated size difference for the data_info offset
    VEV.relative_data_info_offset_quanty = 0
    # A numpy array of zeros for the differences in size for the name_offset
    VEV.relative_name_offset_quanty = np.zeros(VEV.sprp_file.type_entry[b'TX2D'].data_count)
    # A numpy array of zeros for the differences in size for the data_offset
    VEV.relative_data_offset_quanty = np.zeros(VEV.sprp_file.type_entry[b'TX2D'].data_count)
    # A numpy array of zeros for the differences in size of the data (vram)
    VEV.vram_offset_quanty_difference = np.zeros(VEV.sprp_file.type_entry[b'TX2D'].data_count)

    with open(vram_path, mode="rb") as file:

        # Get each texture
        header_1 = bytes.fromhex("44 44 53 20 7C 00 00 00 07 10 00 00")
        header_3_1 = "00000000"
        header_3_3 = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000"
        for i in range(0, VEV.sprp_file.type_entry[b'TX2D'].data_count):

            # Creating DXT5 and DXT1 heading
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.dxt_encoding != 0:

                header_2 = VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.height.\
                               to_bytes(4, 'little') + \
                               VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.width.\
                               to_bytes(4, 'little') + \
                               VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.data_size.\
                               to_bytes(4, 'little')

                header_3_2 = VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.mip_maps.\
                    to_bytes(4, 'little')

                header_3 = bytes.fromhex(header_3_1) + header_3_2 + bytes.fromhex(header_3_3)

                header_4, header_5, header_6 = create_header(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i]
                                                             .data_info.data.dxt_encoding)
                header = header_1 + header_2 + header_3 + header_4 + header_5 + header_6

                # Store the data in memory
                file.seek(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.data_offset)
                data = file.read(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.data_size)
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.tx2d_vram.data = header + data

            # Creating RGBA heading
            else:

                header_1_bmp = "42 4D"
                header_2_bmp = (VEV.sprp_file.type_entry[b'TX2D'].data_entry[i]
                                .data_info.data.data_size + 54).to_bytes(4, 'little').hex()
                header_3_bmp = "00 00 00 00 36 00 00 00 28 00 00 00"
                header_4_1_bmp = VEV.sprp_file.type_entry[b'TX2D'].data_entry[i]\
                    .data_info.data.width.to_bytes(4, 'little').hex()
                header_4_2_bmp = VEV.sprp_file.type_entry[b'TX2D'].data_entry[i]\
                    .data_info.data.height.to_bytes(4, 'little').hex()
                header_4_bmp = header_4_1_bmp + header_4_2_bmp
                header_5_bmp = "01 00 20 00 00 00 00 00 00 00 00 00 12 0B 00 00 12 0B 00 00 00 00 00 00 00 00 00 00"
                header = bytes.fromhex(header_1_bmp + header_2_bmp + header_3_bmp + header_4_bmp + header_5_bmp)

                # Store the data in memory
                file.seek(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.data_offset)
                data = file.read(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.data_size)
                # We're dealing with a shader
                if VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.height == 1:
                    data = change_endian(data)
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.tx2d_vram.data = header + data

                # Check if the extension is png, to unswizzle the image
                if VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.extension == "png":

                    # Write in disk the data swizzled
                    with open("tempSwizzledImage", mode="wb") as file_temp:
                        file_temp.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.tx2d_vram.data)

                    # Run the exe file of 'swizzle.exe' with the option '-u' to unswizzle the image
                    args = os.path.join(VEV.swizzle_path) + " \"" + "tempSwizzledImage" + "\" \"" + "-u" + "\""
                    os.system('cmd /c ' + args)

                    # Get the data from the .exe
                    with open("tempUnSwizzledImage", mode="rb") as file_temp:
                        VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info\
                            .data.tx2d_vram.data_unswizzle = file_temp.read()
                    with open("Indexes.txt", mode="r") as file_temp:
                        VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.tx2d_vram\
                            .indexes_unswizzle_algorithm = file_temp.read().split(";")[:-1]
                        # [:-1] because swizzle.exe saves an '' element in the end

                    # Remove the temp files
                    os.remove("tempSwizzledImage")
                    os.remove("tempUnSwizzledImage")
                    os.remove("Indexes.txt")

                    VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data\
                        .tx2d_vram.data_unswizzle = header + VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info\
                        .data.tx2d_vram.data_unswizzle


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

        # Only shows the texture when the size is different from 0
        if VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].data_info.data.data_size != 0:

            # If the encoding is DXT5 or DXT1, we show the dds image
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].data_info.data.dxt_encoding \
               != 0:
                # Create the dds in disk and open it
                show_dds_image(image_texture, VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]
                               .data_info.data.tx2d_vram.data,
                               VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].data_info.
                               data.width,
                               VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].data_info.
                               data.height)
            else:
                if VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].data_info.extension \
                   != "png":
                    show_bmp_image(image_texture, VEV.sprp_file.type_entry[b'TX2D'].
                                   data_entry[VEV.current_selected_texture]
                                   .data_info.data.tx2d_vram.data,
                                   VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]
                                   .data_info.data.width,
                                   VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]
                                   .data_info.data.height)
                else:
                    show_bmp_image(image_texture, VEV.sprp_file.type_entry[b'TX2D'].
                                   data_entry[VEV.current_selected_texture]
                                   .data_info.data.tx2d_vram.data_unswizzle,
                                   VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]
                                   .data_info.data.width,
                                   VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]
                                   .data_info.data.height)
        else:
            # Remove image in the tool view
            image_texture.clear()

        encoding_image_text.setText(
            "Encoding: %s" % (get_encoding_name(VEV.sprp_file.type_entry[b'TX2D']
                                                .data_entry[VEV.current_selected_texture].data_info.data.dxt_encoding)))
        mip_maps_image_text.setText("Mipmaps: %s" % VEV.sprp_file.type_entry[b'TX2D']
                                    .data_entry[VEV.current_selected_texture].data_info.data.mip_maps)
        size_image_text.setText(
            "Resolution: %dx%d" % (VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]
                                   .data_info.data.width,
                                   VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]
                                   .data_info.data.height))


def action_export_logic(main_window):

    # If the encoding is DXT5 or DXT1, we show the dds image
    if VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].data_info.data.dxt_encoding != 0:
        # Save dds file
        export_path = QFileDialog.getSaveFileName(main_window, "Export texture", os.path.join(
            VEV.spr_file_path, VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].data_info.name
            + ".dds"), "DDS file (*.dds)")[0]

        data = VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].data_info.data.tx2d_vram.data

    else:
        # Save bmp file
        export_path = QFileDialog.getSaveFileName(main_window, "Export texture", os.path.join(
            VEV.spr_file_path, VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].data_info.name
            + ".bmp"), "BMP file (*.bmp)")[0]

        if VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].data_info.extension != "png":
            data = VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].data_info.data.\
                tx2d_vram.data
        else:
            data = VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]\
                .data_info.data.tx2d_vram.data_unswizzle

    if export_path:
        file = open(export_path, mode="wb")
        file.write(data)
        file.close()


def action_export_all_logic(main_window):

    # Ask to the user where to save the files
    folder_export_path = QFileDialog.getSaveFileName(main_window, "Export textures", os.path.splitext(
        VEV.spr_file_path)[0])[0]

    # Check if the user selected the folder
    if folder_export_path:

        # Create the folder
        if not os.path.exists(folder_export_path):
            os.mkdir(folder_export_path)

        for i in range(0, VEV.sprp_file.type_entry[b'TX2D'].data_count):
            # The image is dds
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.dxt_encoding != 0:

                file = open(os.path.join(folder_export_path, VEV.sprp_file.type_entry[b'TX2D'].data_entry[i]
                                         .data_info.name + ".dds"), mode="wb")

                file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.tx2d_vram.data)
                file.close()

            else:
                file = open(os.path.join(folder_export_path, VEV.sprp_file.type_entry[b'TX2D']
                                         .data_entry[i].data_info.name + ".bmp"), mode="wb")
                if VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.extension != "png":
                    file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.tx2d_vram.data)
                else:
                    file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.tx2d_vram.data_unswizzle)
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


# main_window -> instance of the main program
# import_file_path -> path where the file is located
# texture_index_list -> index of the texture where is located in the array list of the program
# ask_user -> flag that will activate or deactive a pop up message when the imported texture has differences with
# the original texture
def import_texture(main_window, import_file_path, texture_index_list, ask_user):

    with open(import_file_path, mode="rb") as file:
        header = file.read(4)

        # It's a DDS modded image
        if header == b'DDS ':

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

            message = validation_dds_imported_texture(VEV.sprp_file.type_entry[b'TX2D']
                                                      .data_entry[texture_index_list].data_info.data, width,
                                                      height, mip_maps, dxt_encoding_text)

            # If the message is empty, there is no differences between original and modified one
            if message:

                # It's an image that originally is swizzled. It's mandatory that the modified texture has the same
                # properties as the original texture due to the swizzled algorithm
                if VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.extension == "png" \
                    and VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data\
                        .dxt_encoding == 0:

                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setText(VEV.message_base_import_BMP_start + "<ul>" + message + "</ul>")
                    msg.exec()
                    return

                # This will be used to ask the user if he/she wants to replace the texture eventhough it has
                # differences between original texture and modified one
                elif ask_user:
                    msg = QMessageBox()

                    # Concatenate the base message and the differences the tool has found
                    message = VEV.message_base_import_texture_start + "<ul>" + message + "</ul>" + \
                        VEV.message_base_import_texture_end

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
            difference = len_data - VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list]\
                .data_info.data.data_size_old
            if difference != 0 or VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].\
               data_info.data.data_size == 0:
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.data_size = len_data
                VEV.vram_offset_quanty_difference[texture_index_list] = difference

            # Change width
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.width != width:
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.width = width
                main_window.sizeImageText.setText(
                    "Resolution: %dx%d" % (width, VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list]
                                           .data_info.data.height))
            # Change height
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.height != height:
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.height = height
                main_window.sizeImageText.setText(
                    "Resolution: %dx%d" % (VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list]
                                           .data_info.data.width, height))

            # Change mipMaps
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.mip_maps != mip_maps:
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.mip_maps = mip_maps
                main_window.mipMapsImageText.setText("Mipmaps: %s" % mip_maps)

            # Change dxt encoding
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list]\
                    .data_info.data.dxt_encoding != dxt_encoding:
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list]\
                    .data_info.data.dxt_encoding = dxt_encoding
                main_window.encodingImageText.setText("Encoding: %s" %
                                                      (get_encoding_name(dxt_encoding)))

            # Change texture in the array
            VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.tx2d_vram.data = data

            # Add the index texture that has been modified
            # (if it was added before, we won't added twice)
            # Also, if the texture was removed before, we drop the index from the array of textures removed
            if texture_index_list not in VEV.textures_index_edited:
                # Only add to the textures array the ones that are actually in the spr/vram file
                if VEV.current_selected_texture < VEV.sprp_file.type_entry[b'TX2D'].data_count:
                    VEV.textures_index_edited.append(texture_index_list)
            elif texture_index_list in VEV.textures_index_removed:
                VEV.textures_index_removed.remove(texture_index_list)

            try:
                # Show texture in the program
                if VEV.current_selected_texture == texture_index_list:
                    show_dds_image(main_window.imageTexture, None, width, height, import_file_path)

            except OSError:
                main_window.imageTexture.clear()

        # it's a BMP modded image
        elif header[:2] == b'BM':

            # Get the height and width of the modified image
            file.seek(18)
            width = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            height = int.from_bytes(file.read(VEV.bytes2Read), 'little')

            # Get the number of bits
            file.seek(28)
            number_bits = int.from_bytes(file.read(2), 'little')

            # Validate the BMP imported texture
            message = validation_bmp_imported_texture(VEV.sprp_file.type_entry[b'TX2D']
                                                      .data_entry[texture_index_list].data_info.data,
                                                      width, height, number_bits, 1, "RGBA")

            # If there is a message, it has detected differences
            if message:

                # It's an image that originally is swizzled. It's mandatory that the modified texture has the same
                # properties as the original texture due to the swizzled algorithm
                if VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.extension == "png" \
                    and VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data\
                        .dxt_encoding == 0:

                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setText(VEV.message_base_import_BMP_start + "<ul>" + message + "</ul>")
                    msg.exec()
                    return

                # This will be used to ask the user if he/she wants to replace the texture eventhough it has
                # differences between original texture and modified one
                elif ask_user:
                    msg = QMessageBox()

                    # Concatenate the base message and the differences the tool has found
                    message = VEV.message_base_import_texture_start + "<ul>" + message + "</ul>" + \
                        VEV.message_base_import_texture_end

                    # Ask to the user if he/she is sure that wants to replace the texture
                    msg.setWindowTitle("Warning")
                    message_import_result = msg.question(main_window, '', message, msg.Yes | msg.No)

                    # If the users click on 'No', the modified texture won't be imported
                    if message_import_result == msg.No:
                        return

            # Get all the data
            file.seek(0)
            data = file.read()

            # We gather the data modified but only a number of bytes that the mod of 4 is 0, so always will have
            # blocks of four bytes. Doing this, we avoid to corrupt the file
            len_data = len(data[54:])
            mod_4 = len_data % 4
            if mod_4 != 0:
                len_data = len_data - mod_4
            data = data[:len_data + 54]

            # Get the difference in size between original and modified in order to change the offsets
            difference = len_data - VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list]\
                .data_info.data.data_size_old
            if difference != 0 or VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].\
               data_info.data.data_size == 0:
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.data_size = len_data
                VEV.vram_offset_quanty_difference[texture_index_list] = difference

            # Change width
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.width != width:
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.width = width
                main_window.sizeImageText.setText(
                    "Resolution: %dx%d" % (width, VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list]
                                           .data_info.data.height))
            # Change height
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.height != height:
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.height = height
                main_window.sizeImageText.setText(
                    "Resolution: %dx%d" % (VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list]
                                           .data_info.data.width, height))

            # Change mipMaps
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.mip_maps != 1:
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data.mip_maps = 1
                main_window.mipMapsImageText.setText("Mipmaps: %s" % 1)

            # Change dxt encoding
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list]\
                    .data_info.data.dxt_encoding != 0:
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list]\
                    .data_info.data.dxt_encoding = 0
                main_window.encodingImageText.setText("Encoding: %s" %
                                                      (get_encoding_name(0)))

            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.extension != "png":
                # Importing the texture
                # Change texture in the array
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list].data_info.data \
                    .tx2d_vram.data = data
            # It's png swizzled texture file
            else:
                # Importing the texture
                # Change texture in the array
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[texture_index_list] \
                    .data_info.data.tx2d_vram.data_unswizzle = data

            # Add the index texture that has been modified
            # (if it was added before, we won't added twice)
            # Also, if the texture was removed before, we drop the index from the array of textures removed
            if texture_index_list not in VEV.textures_index_edited:
                # Only add to the textures array the ones that are actually in the spr/vram file
                if VEV.current_selected_texture < VEV.sprp_file.type_entry[b'TX2D'].data_count:
                    VEV.textures_index_edited.append(texture_index_list)
            elif texture_index_list in VEV.textures_index_removed:
                VEV.textures_index_removed.remove(texture_index_list)

            try:
                # Show texture in the program
                if VEV.current_selected_texture == texture_index_list:
                    show_bmp_image(main_window.imageTexture, data, width, height)

            except OSError:
                main_window.imageTexture.clear()

        else:
            # Wrong texture file
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Invalid texture file.")
            msg.exec()
            return

    return ""


# This method will prepare a new sprp_data_entry (the comun values between dds and bmp image)
def prepare_data_entry(main_window, import_file_path, sprp_data_entry):

    # Create a new spr_data_entry
    sprp_data_entry.data_type = b'TX2D'
    sprp_data_entry.index = VEV.sprp_file.type_entry[b'TX2D'].data_count + VEV.num_new_tx2d_entries_to_add

    # Store the necessary data_info from the data_entry
    sprp_data_entry.data_info.name = os.path.basename(import_file_path).split(".")[0]
    sprp_data_entry.data_info.extension = "tga"
    sprp_data_entry.data_info.name_size = 1 + len(sprp_data_entry.data_info.name) + 4
    sprp_data_entry.data_info.data_size = 32

    # Store the offset
    sprp_data_entry.data_info.data.data_offset = VEV.sprp_file.sprp_header.vram_data_size + VEV.vram_quanty_size_to_add
    sprp_data_entry.data_info.data.data_offset_old = sprp_data_entry.data_info.data.data_offset

    # Add the number of tx2d entries we have to add in the spr file header
    VEV.num_new_tx2d_entries_to_add += 1

    # Add the quanty of size we need to add to the total of vram
    VEV.vram_quanty_size_to_add += sprp_data_entry.data_info.data.data_size

    # Append to the array of data_entries
    VEV.sprp_file.type_entry[b'TX2D'].data_entry.append(sprp_data_entry)
    # Append to the array of quanty difference in vram offset (this won't be used when saving, but to avoid to
    # reestructure the code when importing a new texture in the added ones)
    VEV.vram_offset_quanty_difference = np.append(VEV.vram_offset_quanty_difference, 0)

    # Append to the array of textures in the window list
    item = QStandardItem(sprp_data_entry.data_info.name)
    item.setEditable(False)
    main_window.listView.model().appendRow(item)


# Will add a new texture to the list view, creating a new sprp_data_entry
def add_texture(main_window, import_file_path):

    with open(import_file_path, mode="rb") as file:

        # Read the type of file
        header = file.read(4)

        # It's a DDS modded image
        if header == b'DDS ':

            # Create a new spr_data_entry
            sprp_data_entry = SprpDataEntry()
            # Create a new tx2d_info instance
            sprp_data_entry.data_info.data = Tx2dInfo()
            # Create a new tx2d_vram instance
            sprp_data_entry.data_info.data.tx2d_vram = Tx2dVram()

            # Get the height and width of the modified image
            file.seek(12)
            sprp_data_entry.data_info.data.height = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            sprp_data_entry.data_info.data.width = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            # Get the mipmaps
            file.seek(28)
            sprp_data_entry.data_info.data.mip_maps = int.from_bytes(file.read(1), 'big')
            # Get the dxtencoding
            file.seek(84)
            sprp_data_entry.data_info.data.dxt_encoding = get_dxt_value(file.read(VEV.bytes2Read).decode())

            # Get all the data
            file.seek(0)
            data = file.read()

            # Store the data and size
            sprp_data_entry.data_info.data.tx2d_vram.data = data
            sprp_data_entry.data_info.data.data_size = len(data[128:])
            sprp_data_entry.data_info.data.data_size_old = sprp_data_entry.data_info.data.data_size

            prepare_data_entry(main_window, import_file_path, sprp_data_entry)

        # it's a BMP modded image
        elif header[:2] == b'BM':

            # Create a new spr_data_entry
            sprp_data_entry = SprpDataEntry()
            # Create a new tx2d_info instance
            sprp_data_entry.data_info.data = Tx2dInfo()
            # Create a new tx2d_vram instance
            sprp_data_entry.data_info.data.tx2d_vram = Tx2dVram()

            # Get the height and width of the modified image
            file.seek(18)
            sprp_data_entry.data_info.data.width = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            sprp_data_entry.data_info.data.height = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            # Get the mipmaps
            sprp_data_entry.data_info.data.mip_maps = 1
            # Get the dxtencoding
            sprp_data_entry.data_info.data.dxt_encoding = 0

            # Get all the data
            file.seek(0)
            data = file.read()

            # Store the data and size
            sprp_data_entry.data_info.data.tx2d_vram.data = data
            sprp_data_entry.data_info.data.data_size = len(data[54:])
            sprp_data_entry.data_info.data.data_size_old = sprp_data_entry.data_info.data.data_size

            prepare_data_entry(main_window, import_file_path, sprp_data_entry)
        else:
            # Wrong texture file
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Invalid texture file.")
            msg.exec()
            return


def action_import_all_logic(main_window):

    # Ask to the user from where to import the files into the tool
    folder_import_path = QFileDialog.getExistingDirectory(main_window, "Import textures", VEV.spr_file_path)

    message = ""

    if folder_import_path:
        # Get all the textures name from memory
        for i in range(0, VEV.sprp_file.type_entry[b'TX2D'].data_count):

            # Get the output extension
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.dxt_encoding != 0:
                extension = ".dds"
            else:
                extension = ".bmp"

            # Get the full name
            texture_name_extension = VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.name + extension

            # Get the path and check in the folder the texture. If the tool find the texture, we import it
            # If the tool finds errors, it won't import the texture and will add a message at the end with the errors
            path_file = os.path.join(folder_import_path, texture_name_extension)
            if os.path.exists(path_file):
                message = message + import_texture(main_window, path_file, i, False)
            else:
                message = message + "<li>" + texture_name_extension + " not found!" + "</li>"

        # If there is a message, it has detected differences
        if message:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Found the following errors while importing:" + "<ul>" + message + "</ul>")
            msg.exec()
            return


def action_import_logic(main_window):

    # Open texture file
    import_path = QFileDialog.getOpenFileName(main_window, "Import texture", os.path.join(VEV.spr_file_path, ""),
                                              "Supported files (*.dds *.bmp) "
                                              ";; DDS file (*.dds) "
                                              ";; BMP file (*.bmp)")[0]
    # The user didn't cancel the file to import
    if os.path.exists(import_path):
        import_texture(main_window, import_path, VEV.current_selected_texture, True)


def action_remove_logic(main_window):

    # Ask to the user if is sure to remove the texture
    msg = QMessageBox()

    # The texture selected is not removed
    if VEV.current_selected_texture not in VEV.textures_index_removed:

        msg.setWindowTitle("Message")
        message = "The texture will be removed. Are you sure to continue?"
        answer = msg.question(main_window, '', message, msg.Yes | msg.No | msg.Cancel)

        # Check if the user has selected something
        if answer:

            # The user wants to remove the selected texture
            if answer == msg.Yes:

                # The texture that we will remove is from the spr file
                if VEV.current_selected_texture < VEV.sprp_file.type_entry[b'TX2D'].data_count:

                    data = VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].\
                        data_info.data.tx2d_vram.data

                    # The encoding is RGBA
                    if VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].\
                            data_info.data.dxt_encoding == 0:

                        header = data[:54]
                        data_texture = b''

                        # The extension is png. It's a swizzle image. We only replace the data with 'FF'
                        if VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture].\
                           data_info.extension == "png":

                            # Change texture in the array
                            VEV.sprp_file.type_entry[b'TX2D'].data_entry[
                                VEV.current_selected_texture].data_info.data.tx2d_vram.data_unswizzle = b''

                            data_size = VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]\
                                .data_info.data.data_size
                            for _ in range(0, data_size):
                                data_texture += b'\xFF'

                            # Change texture in the array
                            VEV.sprp_file.type_entry[b'TX2D'].data_entry[
                                VEV.current_selected_texture].data_info.data.tx2d_vram.data_unswizzle = header + \
                                data_texture

                        # It's not a swizzle image
                        else:

                            # The texture size will be 1024
                            VEV.sprp_file.type_entry[b'TX2D'].data_entry[
                                VEV.current_selected_texture].data_info.data.data_size = 1024

                            # Get the difference in size between original and modified in order to change the offsets
                            data_size_old = VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]\
                                .data_info.data.data_size_old
                            VEV.vram_offset_quanty_difference[VEV.current_selected_texture] = 1024 - data_size_old

                            # Change width and height
                            VEV.sprp_file.type_entry[b'TX2D'].data_entry[
                                VEV.current_selected_texture].data_info.data.width = 256
                            VEV.sprp_file.type_entry[b'TX2D'].data_entry[
                                VEV.current_selected_texture].data_info.data.height = 1
                            main_window.sizeImageText.setText("Resolution: %dx%d" % (256, 1))

                            # Change texture in the array
                            VEV.sprp_file.type_entry[b'TX2D'].data_entry[
                                VEV.current_selected_texture].data_info.data.tx2d_vram.data = b''

                            data_size = VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]\
                                .data_info.data.data_size
                            for _ in range(0, data_size):
                                data_texture += b'\xFF'

                            # Change texture in the array
                            VEV.sprp_file.type_entry[b'TX2D'].data_entry[
                                VEV.current_selected_texture].data_info.data.tx2d_vram.data = header + data_texture

                    # It's a DDS image
                    else:

                        header = data[:128]
                        data_texture = b''

                        # The texture size will be 1024
                        VEV.sprp_file.type_entry[b'TX2D'].data_entry[
                            VEV.current_selected_texture].data_info.data.data_size = 1024

                        # Get the difference in size between original and modified in order to change the offsets
                        data_size_old = VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture] \
                            .data_info.data.data_size_old
                        VEV.vram_offset_quanty_difference[VEV.current_selected_texture] = 1024 - data_size_old

                        # Change width and height
                        VEV.sprp_file.type_entry[b'TX2D'].data_entry[
                            VEV.current_selected_texture].data_info.data.width = 256
                        VEV.sprp_file.type_entry[b'TX2D'].data_entry[
                            VEV.current_selected_texture].data_info.data.height = 1
                        main_window.sizeImageText.setText("Resolution: %dx%d" % (256, 1))

                        # Change texture in the array
                        VEV.sprp_file.type_entry[b'TX2D'].data_entry[
                            VEV.current_selected_texture].data_info.data.tx2d_vram.data = b''
                        data_size = VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]\
                            .data_info.data.data_size
                        for _ in range(0, data_size):
                            data_texture += b'\xFF'

                        # Change texture in the array
                        VEV.sprp_file.type_entry[b'TX2D'].data_entry[
                            VEV.current_selected_texture].data_info.data.tx2d_vram.data = header + data_texture

                    # Add the texture index to the array of textures edited (but only the ones that are actually in the
                    # file
                    # and not the new that are added by the user)
                    # Also add the removed texture to the array of removed textures
                    if VEV.current_selected_texture not in VEV.textures_index_edited:
                        VEV.textures_index_edited.append(VEV.current_selected_texture)
                    VEV.textures_index_removed.append(VEV.current_selected_texture)

                    # Remove image in the tool view
                    main_window.imageTexture.clear()

                # Remove entirely the texture (added for the user)
                else:

                    # Remove the number of tx2d entries
                    VEV.num_new_tx2d_entries_to_add -= 1

                    # Remove the quanty of size we need to add to the total of vram
                    VEV.vram_quanty_size_to_add -= VEV.sprp_file.type_entry[b'TX2D']\
                        .data_entry[VEV.current_selected_texture].data_info.data.data_size

                    # Remove from the array of differences
                    VEV.vram_offset_quanty_difference = np.delete(VEV.vram_offset_quanty_difference,
                                                                  VEV.current_selected_texture)

                    # Remove from the array of data_entries
                    del VEV.sprp_file.type_entry[b'TX2D'].data_entry[VEV.current_selected_texture]
                    # Remove from the array of textures in the window list
                    main_window.listView.model().removeRow(VEV.current_selected_texture)
    else:
        msg.setWindowTitle("Error")
        message = "There is no texture to remove"
        msg.setText(message)
        msg.exec()


def action_add_logic(main_window):

    # Open texture file
    import_path = QFileDialog.getOpenFileName(main_window, "Import texture", os.path.join(VEV.spr_file_path, ""),
                                              "Supported files (*.dds *.bmp) "
                                              ";; DDS file (*.dds) "
                                              ";; BMP file (*.bmp)")[0]
    # The user didn't cancel the file to import
    if os.path.exists(import_path):
        add_texture(main_window, import_path)
