from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QLineEdit
from pyglet.gl import GLException

from lib.packages import os, image, QImage, QPixmap
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

    # Material
    main_window.materialVal.currentIndexChanged.connect(lambda: action_material_val_changed(main_window))
    main_window.layerVal.currentIndexChanged.connect(lambda: action_layer_val_changed(main_window))
    main_window.typeVal.currentIndexChanged.connect(lambda: action_type_val_changed(main_window))
    main_window.textureVal.currentIndexChanged.connect(lambda: action_texture_val_changed(main_window))
    main_window.addMaterialButton.clicked.connect(lambda: action_add_material_logic(main_window))
    main_window.removeMaterialButton.clicked.connect(lambda: action_remove_material_logic(main_window))
    main_window.materialVal.setEnabled(False)
    main_window.layerVal.setEnabled(False)
    main_window.typeVal.setEnabled(False)
    main_window.textureVal.setEnabled(False)
    main_window.addMaterialButton.setEnabled(False)
    main_window.removeMaterialButton.setEnabled(False)

    # Model part
    main_window.modelPartVal.currentIndexChanged.connect(lambda: action_model_part_val_changed(main_window))
    main_window.materialModelPartVal.currentIndexChanged.connect(lambda:
                                                                 action_material_model_part_val_changed(main_window))
    main_window.modelPartVal.setEnabled(False)
    main_window.materialModelPartVal.setEnabled(False)

    # Labels
    main_window.encodingImageText.setVisible(False)
    main_window.mipMapsImageText.setVisible(False)
    main_window.sizeImageText.setVisible(False)
    main_window.fileNameText.setVisible(False)

    # Create a model for the list view of textures
    model = QStandardItemModel()
    main_window.listView.setModel(model)
    main_window.listView.selectionModel().currentChanged.connect(lambda: action_item(main_window.listView,
                                                                 main_window.imageTexture,
                                                                 main_window.encodingImageText,
                                                                 main_window.mipMapsImageText,
                                                                 main_window.sizeImageText))


def load_data_to_ve(main_window):

    # Reset boolean values
    VEV.enable_combo_box = False
    # Reset integer values
    VEV.unique_temp_name_offset = -1
    VEV.DbzCharMtrl_offset = 0
    # Reset combo box values
    main_window.materialVal.clear()
    main_window.typeVal.clear()
    main_window.typeVal.addItem("EMPTY", 0)
    main_window.textureVal.clear()
    main_window.textureVal.addItem("EMPTY", 0)
    main_window.modelPartVal.clear()
    main_window.materialModelPartVal.clear()
    main_window.materialModelPartVal.addItem("EMPTY", 0)
    # Reset model list view
    main_window.listView.model().clear()

    # Get basename from spr_file_path
    basename = os.path.basename(os.path.splitext(VEV.spr_file_path)[0])

    # Open spr and vram
    open_spr_file(main_window, main_window.listView.model(), VEV.spr_file_path)
    open_vram_file(VEV.vram_file_path)

    # Set the index of the list view to be always the first row when loading a new spr/vram file
    main_window.listView.setCurrentIndex(main_window.listView.model().index(0, 0))

    # If the texture encoded is DXT1 or DXT5, we call the show dds function
    data_entry_0 = VEV.sprp_file.type_entry[b'TX2D'].data_entry[0]
    if data_entry_0.data_info.data.dxt_encoding != 0:
        # Create the dds in disk and open it
        show_dds_image(main_window.imageTexture, data_entry_0.data_info.data.tx2d_vram.data,
                       data_entry_0.data_info.data.width, data_entry_0.data_info.data.height)
    else:
        if data_entry_0.data_info.extension != "png":
            show_bmp_image(main_window.imageTexture, data_entry_0.data_info.data.tx2d_vram.data,
                           data_entry_0.data_info.data.width, data_entry_0.data_info.data.height)
        else:
            show_bmp_image(main_window.imageTexture, data_entry_0.data_info.data.tx2d_vram.data_unswizzle,
                           data_entry_0.data_info.data.width, data_entry_0.data_info.data.height)

    # Enable the buttons
    main_window.exportAllButton.setEnabled(True)
    main_window.importAllButton.setEnabled(True)
    main_window.importButton.setEnabled(True)
    main_window.exportButton.setEnabled(True)
    main_window.removeButton.setEnabled(True)
    main_window.addButton.setEnabled(True)

    # Enable the buttons of material only if the spr holds mtrl section
    if b'MTRL' in VEV.sprp_file.type_entry:
        main_window.materialVal.setEnabled(True)
        main_window.layerVal.setEnabled(True)
        main_window.typeVal.setEnabled(True)
        main_window.textureVal.setEnabled(True)
        main_window.addMaterialButton.setEnabled(True)
        main_window.removeMaterialButton.setEnabled(True)

        main_window.modelPartVal.setEnabled(True)
        main_window.materialModelPartVal.setEnabled(True)

        # Enable combo box and set the values for the first layer of the first material
        VEV.enable_combo_box = True
        action_material_val_changed(main_window)
        action_model_part_val_changed(main_window)

    else:
        main_window.materialVal.setEnabled(False)
        main_window.layerVal.setEnabled(False)
        main_window.typeVal.setEnabled(False)
        main_window.textureVal.setEnabled(False)
        main_window.addMaterialButton.setEnabled(False)
        main_window.removeMaterialButton.setEnabled(False)

        main_window.modelPartVal.setEnabled(False)
        main_window.materialModelPartVal.setEnabled(False)

    # Show the text labels
    main_window.fileNameText.setText(basename)
    main_window.fileNameText.setVisible(True)
    main_window.encodingImageText.setText(
        "Encoding: %s" % (get_encoding_name(data_entry_0.data_info.data.dxt_encoding)))
    main_window.mipMapsImageText.setText("Mipmaps: %d" % data_entry_0.data_info.data.mip_maps)
    main_window.sizeImageText.setText(
        "Resolution: %dx%d" % (data_entry_0.data_info.data.width, data_entry_0.data_info.data.height))
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
        # Since a shader has height of 1, in order to show it more clearly, we ignore the scaling
        if height == 1:
            mpixmap = mpixmap.scaled(image_texture.width(), width)
        elif width > height:
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


def get_name_from_spr(file, offset):

    file.seek(offset)
    name = ""

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

            name += data_decoded

        # The texture name is already stored. We clean it
        else:
            # Get the name splitted by '.'
            name_splitted = name.split(".")
            tam_name_splitted = len(name_splitted)
            name = ""

            # Get the name and extension separatelly
            if tam_name_splitted > 1:
                for i in range(0, tam_name_splitted - 1):
                    name += name_splitted[i] + ("." if i < tam_name_splitted - 2 else "")
                extension = name_splitted[-1]
            else:
                name = name_splitted[0]
                extension = ""

            # The max number of char for the name is 250
            name_size = len(name)
            if name_size > 250:
                name = name[name_size - 250:]

            # Finish the reading of the file
            break

    return name, extension


def read_children(main_window, file, sprp_data_info, type_section):

    file.seek(sprp_data_info.child_offset + VEV.sprp_file.data_block_base)

    for _ in range(sprp_data_info.child_count):
        sprp_data_info_child = SprpDataInfo()

        sprp_data_info_child.name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
        sprp_data_info_child.data_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
        sprp_data_info_child.data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        sprp_data_info_child.child_count = int.from_bytes(file.read(VEV.bytes2Read), "big")
        sprp_data_info_child.child_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")

        # Get the name for the data_info
        aux_pointer_file = file.tell()
        sprp_data_info_child.name, sprp_data_info_child.extension = \
            get_name_from_spr(file, VEV.sprp_file.string_table_base + sprp_data_info_child.name_offset)
        base_name_size = len(sprp_data_info_child.name)
        extension_size = len(sprp_data_info_child.extension)
        sprp_data_info_child.name_size = 1 + base_name_size + (extension_size + 1 if extension_size > 0 else 0)

        if type_section == b'MTRL':

            # Save the data of the children from a material
            if sprp_data_info_child.name == "DbzCharMtrl":

                file.seek(sprp_data_info_child.data_offset + VEV.sprp_file.data_block_base)
                sprp_data_info_child.data = file.read(sprp_data_info_child.data_size)

        # Get the scene data
        elif type_section == b'SCNE':

            # If the parent name is NODES, we store the scene model in the child data
            if sprp_data_info.name == "[NODES]":
                file.seek(VEV.sprp_file.data_block_base + sprp_data_info_child.data_offset)

                scne_model = ScneModel()
                scne_model.unk00 = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_model.unk04_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_model.unk08_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_model.unk0c_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_model.unk10_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")

                sprp_data_info_child.data = scne_model

            # If the children name is MATERIAL, we store the scene material in the child data
            elif sprp_data_info_child.name == "[MATERIAL]":
                file.seek(VEV.sprp_file.data_block_base + sprp_data_info_child.data_offset)

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

                # Store in the combo box, the sprp_data_info children using as a key, the father's name
                main_window.modelPartVal.addItem(sprp_data_info.name, sprp_data_info_child)

            # If the children name is DbzEyeInfo, we store the scene eye info in the child data
            elif sprp_data_info_child.name == "DbzEyeInfo":
                file.seek(VEV.sprp_file.data_block_base + sprp_data_info_child.data_offset)

                scne_eye_info = ScneEyeInfo()

                # Get each eye_data
                for _ in range(0, 3):
                    eye_data = EyeData()
                    eye_data.unk00_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    file.seek(108, os.SEEK_CUR)

                    scne_eye_info.eyes_data.append(eye_data)

                sprp_data_info_child.data = scne_eye_info

        # Restore the pointer of the file in order to read the following children
        file.seek(aux_pointer_file)

        # Get all the children sprp_data_info for the actual children in the loop section
        if sprp_data_info_child.child_count > 0:
            read_children(main_window, file, sprp_data_info_child, type_section)
            file.seek(aux_pointer_file)

        # Store each children to the array
        sprp_data_info.child_info.append(sprp_data_info_child)


def write_children(file, sprp_data_info, type_section, relative_name_offset_quanty_accumulated,
                   relative_data_offset_quanty_accumulated):

    file.seek(sprp_data_info.child_offset + VEV.sprp_file.data_block_base)

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
                file.seek(VEV.sprp_file.data_block_base + sprp_data_info_child.data_offset)

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
                file.seek(VEV.sprp_file.data_block_base + sprp_data_info_child.data_offset)

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
                file.seek(VEV.sprp_file.data_block_base + sprp_data_info_child.data_offset)

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


def open_spr_file(main_window, model, spr_path):

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
        VEV.sprp_file.entry_info_base = 64
        VEV.sprp_file.string_table_base = VEV.sprp_file.entry_info_base + VEV.sprp_file.sprp_header.entry_info_size
        VEV.sprp_file.data_info_base = VEV.sprp_file.string_table_base + VEV.sprp_file.sprp_header.string_table_size
        VEV.sprp_file.data_block_base = VEV.sprp_file.data_info_base + VEV.sprp_file.sprp_header.data_info_size
        VEV.sprp_file.file_size = VEV.sprp_file.data_block_base + VEV.sprp_file.sprp_header.data_block_size

        # Create each SPRP_TYPE_ENTRY
        file.seek(VEV.sprp_file.entry_info_base)
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
                # Everything that is not SPR in the header, has names for each data
                if VEV.sprp_file.sprp_header.data_tag != b"SPR\x00":
                    sprp_data_entry.data_info.name,  sprp_data_entry.data_info.extension = \
                        get_name_from_spr(file, VEV.sprp_file.string_table_base + sprp_data_entry.data_info.name_offset)
                    base_name_size = len(sprp_data_entry.data_info.name)
                    extension_size = len(sprp_data_entry.data_info.extension)
                    sprp_data_entry.data_info.name_size = base_name_size + (1 + extension_size
                                                                            if extension_size > 0 else 0)
                # If the data header is SPR, we create custom names
                else:
                    sprp_data_entry.data_info.name = sprp_type_entry.data_type.decode('utf-8') + "_" + str(j)

                # Get all the children sprp_data_info
                if sprp_data_entry.data_info.child_count > 0:
                    read_children(main_window, file, sprp_data_entry.data_info, sprp_data_entry.data_type)

                # Save the data when is the type TX2D
                if sprp_type_entry.data_type == b"TX2D":

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Create the TX2D info
                    sprp_data_entry.data_info.data = Tx2dInfo()

                    sprp_data_entry.data_info.data.unk0x00 = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    sprp_data_entry.data_info.data.data_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    sprp_data_entry.data_info.data.unk0x08 = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    sprp_data_entry.data_info.data.data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    sprp_data_entry.data_info.data.width = int.from_bytes(file.read(2), "big")
                    sprp_data_entry.data_info.data.height = int.from_bytes(file.read(2), "big")
                    sprp_data_entry.data_info.data.unk0x14 = int.from_bytes(file.read(2), "big")
                    sprp_data_entry.data_info.data.mip_maps = int.from_bytes(file.read(2), "big")
                    sprp_data_entry.data_info.data.unk0x18 = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    sprp_data_entry.data_info.data.unk0x1c = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    sprp_data_entry.data_info.data.dxt_encoding = int.from_bytes(file.read(1), "big")

                    sprp_data_entry.data_info.data.tx2d_vram = Tx2dVram()

                    # Add the tx2d_data_entry to the combo box (material section)
                    main_window.textureVal.addItem(sprp_data_entry.data_info.name,
                                                   sprp_data_entry.data_info.name_offset)

                    # Add the texture to the listView
                    item = QStandardItem(sprp_data_entry.data_info.name)
                    item.setData(sprp_data_entry)
                    item.setEditable(False)
                    model.appendRow(item)

                # Save the data when is the type MTRL
                elif sprp_type_entry.data_type == b"MTRL":

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Create the MTRL info
                    sprp_data_entry.data_info.data = MtrlInfo()

                    # Read unk data
                    sprp_data_entry.data_info.data.unk_00 = file.read(112)

                    # Read each layer (the max number is 10)
                    for k in range(0, 10):
                        mtrlLayer = MtrlLayer()
                        mtrlLayer.layer_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                        mtrlLayer.source_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")

                        # Get the names for each mtrlLayer
                        aux_mtrl_pointer = file.tell()
                        mtrlLayer.layer_name, extension = \
                            get_name_from_spr(file, mtrlLayer.layer_name_offset + VEV.sprp_file.string_table_base)
                        file.seek(aux_mtrl_pointer)

                        # Store the layer in the actual material
                        sprp_data_entry.data_info.data.layers.append(mtrlLayer)

                    # Add the material to the combo box
                    main_window.materialVal.addItem(sprp_data_entry.data_info.name, sprp_data_entry)
                    main_window.materialModelPartVal.addItem(sprp_data_entry.data_info.name,
                                                             sprp_data_entry.data_info.name_offset)

                elif sprp_type_entry.data_type == b'TXAN':

                    # Add the txan_data_entry to the combo box (material section) but only the name and name_offset
                    main_window.textureVal.addItem(sprp_data_entry.data_info.name,
                                                   sprp_data_entry.data_info.name_offset)

                # Store all the info in the data_entry array
                sprp_type_entry.data_entry.append(sprp_data_entry)

                # Move to the next data_entry
                file.seek(aux_pointer_data_entry)

            # Store the type_entry to the dictionary of type_entries
            VEV.sprp_file.type_entry[sprp_type_entry.data_type] = sprp_type_entry

            file.seek(aux_pointer_type_entry)

            # Update the type_entry offset
            type_entry_offset += sprp_type_entry.data_count * 32

        # If there is material in the spr file, we try to find specific names
        if b'MTRL' in VEV.sprp_file.type_entry:
            offset = 161
            stop_offset = VEV.sprp_file.sprp_header.string_table_size + 160
            while True:
                name, extension = get_name_from_spr(file, offset)

                # We found the offset of DbzCharMtrl
                if name == "DbzCharMtrl":
                    VEV.DbzCharMtrl_offset = offset - VEV.sprp_file.string_table_base
                # Find the type effects
                elif name in VEV.layer_type_effects:
                    main_window.typeVal.addItem(name, offset - VEV.sprp_file.string_table_base)
                # We reached the end of the string base section
                if file.tell() > stop_offset:
                    break

                offset = file.tell()


def open_vram_file(vram_path):

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


def write_separator_vram(output_vram_file, data_entry):

    extra = output_vram_file.tell() % 16
    if extra > 0:
        for _ in range(0, extra):
            output_vram_file.write(b'\x00')
    if data_entry.data_info.data.width == data_entry.data_info.data.height:
        if data_entry.data_info.data.dxt_encoding == 8:
            output_vram_file.write(VEV.vram_separator_80)
        else:
            output_vram_file.write(VEV.vram_separator_48)
    else:
        # If the encoding is dxt1, we write a separator of 32 bytes
        if data_entry.data_info.data.dxt_encoding == 8:
            output_vram_file.write(VEV.vram_separator_32)
        else:
            output_vram_file.write(VEV.vram_separator_80)


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


def replace_texture_properties(main_window, data_entry, len_data, width, height, mip_maps, dxt_encoding):

    # Get the difference in size between actual and modified texture to check if is necessary to update offsets
    difference = len_data - data_entry.data_info.data.data_size

    # Change size
    if difference != 0:
        data_entry.data_info.data.data_size = len_data

    # Change width
    if data_entry.data_info.data.width != width:
        data_entry.data_info.data.width = width
        main_window.sizeImageText.setText("Resolution: %dx%d" % (width, data_entry.data_info.data.height))
    # Change height
    if data_entry.data_info.data.height != height:
        data_entry.data_info.data.height = height
        main_window.sizeImageText.setText("Resolution: %dx%d" % (data_entry.data_info.data.width, height))

    # Change mipMaps
    if data_entry.data_info.data.mip_maps != mip_maps:
        data_entry.data_info.data.mip_maps = mip_maps
        main_window.mipMapsImageText.setText("Mipmaps: %s" % mip_maps)

    # Change dxt encoding
    if data_entry.data_info.data.dxt_encoding != dxt_encoding:
        data_entry.data_info.data.dxt_encoding = dxt_encoding
        main_window.encodingImageText.setText("Encoding: %s" % (get_encoding_name(dxt_encoding)))


# main_window -> instance of the main program
# import_file_path -> path where the file is located
# ask_user -> flag that will activate or deactive a pop up message when the imported texture has differences with
# the original texture
def import_texture(main_window, import_file_path, ask_user):

    with open(import_file_path, mode="rb") as file:
        header = file.read(4)

        current_selected_index = main_window.listView.selectionModel().currentIndex().row()
        data_entry = main_window.listView.model().item(current_selected_index, 0).data()

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

            message = validation_dds_imported_texture(data_entry.data_info.data, width,
                                                      height, mip_maps, dxt_encoding_text)

            # If the message is empty, there is no differences between original and modified one
            if message:

                # It's an image that originally is swizzled. It's mandatory that the modified texture has the same
                # properties as the original texture due to the swizzled algorithm
                if data_entry.data_info.extension == "png" and data_entry.data_info.data.dxt_encoding == 0:

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
            len_data = len(data[128:])

            # --- Importing the texture ---
            # Change texture in the array
            data_entry.data_info.data.tx2d_vram.data = data

            # Replace the texture properties in memory
            replace_texture_properties(main_window, data_entry, len_data, width, height, mip_maps, dxt_encoding)

            try:
                # Show texture in the program
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
            message = validation_bmp_imported_texture(data_entry.data_info.data, width, height, number_bits, 1, "RGBA")

            # If there is a message, it has detected differences
            if message:

                # It's an image that originally is swizzled. It's mandatory that the modified texture has the same
                # properties as the original texture due to the swizzled algorithm
                if data_entry.data_info.extension == "png" and data_entry.data_info.data.dxt_encoding == 0:

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

            # --- Importing the texture ---
            # Change texture in the array
            if data_entry.data_info.extension != "png":
                data_entry.data_info.data.tx2d_vram.data = data
            # It's png swizzled texture file
            else:
                data_entry.data_info.data.tx2d_vram.data_unswizzle = data

            # Replace the texture properties in memory
            replace_texture_properties(main_window, data_entry, len_data, width, height, 1, 0)

            try:
                # Show texture in the program
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
def prepare_sprp_data_entry(main_window, import_file_path, sprp_data_entry):

    # Create a new spr_data_entry
    sprp_data_entry.data_type = b'TX2D'
    sprp_data_entry.index = main_window.listView.model().rowCount()
    sprp_data_entry.new_entry = True

    # Store the data_info from the data_entry
    # The name offset value will be unique and temporal for now
    sprp_data_entry.data_info.name_offset = VEV.unique_temp_name_offset
    VEV.unique_temp_name_offset -= 1
    sprp_data_entry.data_info.name = os.path.basename(import_file_path).split(".")[0]
    sprp_data_entry.data_info.extension = "tga"
    sprp_data_entry.data_info.name_size = len(sprp_data_entry.data_info.name) + 1 + \
        len(sprp_data_entry.data_info.extension)
    sprp_data_entry.data_info.data_size = 36

    # Append to the array of textures in the window list
    item = QStandardItem(sprp_data_entry.data_info.name)
    item.setData(sprp_data_entry)
    item.setEditable(False)
    main_window.listView.model().appendRow(item)

    # Append to the array of textures in the material section
    VEV.enable_combo_box = False
    main_window.textureVal.addItem(sprp_data_entry.data_info.name, sprp_data_entry.data_info.name_offset)
    VEV.enable_combo_box = True


# Will add a new texture to the list view, creating a new sprp_data_entry
def add_texture(main_window, import_file_path):

    with open(import_file_path, mode="rb") as file:

        # Create a new spr_data_entry
        sprp_data_entry = SprpDataEntry()
        # Create a new tx2d_info instance
        sprp_data_entry.data_info.data = Tx2dInfo()
        # Create a new tx2d_vram instance
        sprp_data_entry.data_info.data.tx2d_vram = Tx2dVram()

        # Read the type of file
        header = file.read(4)

        # It's a DDS modded image
        if header == b'DDS ':

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

            prepare_sprp_data_entry(main_window, import_file_path, sprp_data_entry)

        # it's a BMP modded image
        elif header[:2] == b'BM':

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

            prepare_sprp_data_entry(main_window, import_file_path, sprp_data_entry)

        else:
            # Wrong texture file
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Invalid texture file.")
            msg.exec()
            return


def action_item(list_view, image_texture, encoding_image_text, mip_maps_image_text, size_image_text):

    current_selected_index = list_view.selectionModel().currentIndex().row()

    # There is no texture to show if the index is negative
    if current_selected_index >= 0:

        data_entry = list_view.model().item(current_selected_index, 0).data()

        # Only shows the texture when the size is different from 0
        if data_entry.data_info.data.data_size != 0:

            # If the encoding is DXT5 or DXT1, we show the dds image
            if data_entry.data_info.data.dxt_encoding \
               != 0:
                # Create the dds in disk and open it
                show_dds_image(image_texture, data_entry.data_info.data.tx2d_vram.data,
                               data_entry.data_info.data.width,
                               data_entry.data_info.data.height)
            else:
                if data_entry.data_info.extension \
                   != "png":
                    show_bmp_image(image_texture, data_entry.data_info.data.tx2d_vram.data,
                                   data_entry.data_info.data.width,
                                   data_entry.data_info.data.height)
                else:
                    show_bmp_image(image_texture, data_entry.data_info.data.tx2d_vram.data_unswizzle,
                                   data_entry.data_info.data.width,
                                   data_entry.data_info.data.height)
        else:
            # Remove image in the tool view
            image_texture.clear()

        encoding_image_text.setText("Encoding: %s" % (get_encoding_name(data_entry.data_info.data.dxt_encoding)))
        mip_maps_image_text.setText("Mipmaps: %s" % data_entry.data_info.data.mip_maps)
        size_image_text.setText("Resolution: %dx%d" % (data_entry.data_info.data.width,
                                                       data_entry.data_info.data.height))
    else:
        encoding_image_text.setText("")
        mip_maps_image_text.setText("")
        size_image_text.setText("")
        image_texture.clear()


def action_export_logic(main_window):

    current_selected_index = main_window.listView.selectionModel().currentIndex().row()
    data_entry = main_window.listView.model().item(current_selected_index, 0).data()

    # If the encoding is DXT5 or DXT1, we show the dds image
    if data_entry.data_info.data.dxt_encoding != 0:
        # Save dds file
        export_path = QFileDialog.getSaveFileName(main_window, "Export texture", os.path.join(
            VEV.spr_file_path, data_entry.data_info.name
            + ".dds"), "DDS file (*.dds)")[0]

        data = data_entry.data_info.data.tx2d_vram.data

    else:
        # Save bmp file
        export_path = QFileDialog.getSaveFileName(main_window, "Export texture", os.path.join(
            VEV.spr_file_path, data_entry.data_info.name
            + ".bmp"), "BMP file (*.bmp)")[0]

        if data_entry.data_info.extension != "png":
            data = data_entry.data_info.data.tx2d_vram.data
        else:
            data = data_entry.data_info.data.tx2d_vram.data_unswizzle

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

        for i in range(0, main_window.listView.model().rowCount()):
            data_entry = main_window.listView.model().item(i, 0).data()
            # The image is dds
            if data_entry.data_info.data.dxt_encoding != 0:

                file = open(os.path.join(folder_export_path, data_entry.data_info.name + ".dds"), mode="wb")

                file.write(data_entry.data_info.data.tx2d_vram.data)
                file.close()

            else:
                file = open(os.path.join(folder_export_path, data_entry.data_info.name + ".bmp"), mode="wb")
                if data_entry.data_info.extension != "png":
                    file.write(data_entry.data_info.data.tx2d_vram.data)
                else:
                    file.write(data_entry.data_info.data.tx2d_vram.data_unswizzle)
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


def action_import_all_logic(main_window):

    # Ask to the user from where to import the files into the tool
    folder_import_path = QFileDialog.getExistingDirectory(main_window, "Import textures", VEV.spr_file_path)

    message = ""

    if folder_import_path:
        # Get all the textures name from memory
        for i in range(0, main_window.listView.model().rowCount()):
            data_entry = main_window.listView.model().item(i, 0).data()

            # Get the output extension
            if data_entry.data_info.data.dxt_encoding != 0:
                extension = ".dds"
            else:
                extension = ".bmp"

            # Get the full name
            texture_name_extension = data_entry.data_info.name + extension

            # Get the path and check in the folder the texture. If the tool find the texture, we import it
            # If the tool finds errors, it won't import the texture and will add a message at the end with the errors
            path_file = os.path.join(folder_import_path, texture_name_extension)
            if os.path.exists(path_file):
                message = message + import_texture(main_window, path_file, False)
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
        import_texture(main_window, import_path, True)


def action_remove_logic(main_window):

    # Ask to the user if is sure to remove the texture
    msg = QMessageBox()
    msg.setWindowTitle("Message")
    message = "The texture will be removed. Are you sure to continue?"
    answer = msg.question(main_window, '', message, msg.Yes | msg.No | msg.Cancel)

    # Check if the user has selected something
    if answer:

        # The user wants to remove the selected texture
        if answer == msg.Yes:

            # Update the index for the data_entry. If we're dealing with new added textures, we recalculate their
            # offsets
            current_index_list_view = main_window.listView.selectionModel().currentIndex().row()
            for i in range(current_index_list_view + 1,  main_window.listView.model().rowCount()):

                # Get the data entry
                data_entry = main_window.listView.model().item(i, 0).data()

                # Reduce their index
                data_entry.index -= 1

            # Remove from the array of textures in the window list
            main_window.listView.model().removeRow(current_index_list_view)

            # Remove from the array of textures in the material section
            VEV.enable_combo_box = False
            current_index_material_texture_index = current_index_list_view + 1

            # Search the material layer that is using the texture removed to assing the empty offset one
            # in the material layer
            name_offset_removed = main_window.textureVal.itemData(current_index_material_texture_index)
            for i in range(0, main_window.materialVal.count()):
                mtrl_entry_data = main_window.materialVal.itemData(i)
                for j in range(0, main_window.layerVal.count()):
                    layer = mtrl_entry_data.data_info.data.layers[j]
                    if layer.source_name_offset == name_offset_removed:
                        layer.source_name_offset = 0

            # Remove the offset texture name from the texture material section
            # If the current texture selected in the combo box is the same index as the texture we're removing
            # we leave the combo box to be in the index 0
            if main_window.textureVal.currentIndex() == current_index_material_texture_index:
                main_window.textureVal.setCurrentIndex(0)
            main_window.textureVal.removeItem(current_index_material_texture_index)
            VEV.enable_combo_box = True

            # Disable some the buttons if there won't be any more texture
            if main_window.listView.model().rowCount() == 0 and main_window.removeButton.isEnabled():
                # Disable the buttons
                main_window.exportAllButton.setEnabled(False)
                main_window.importAllButton.setEnabled(False)
                main_window.importButton.setEnabled(False)
                main_window.exportButton.setEnabled(False)
                main_window.removeButton.setEnabled(False)


def action_add_logic(main_window):

    # Open texture file
    import_path = QFileDialog.getOpenFileName(main_window, "Import texture", os.path.join(VEV.spr_file_path, ""),
                                              "Supported files (*.dds *.bmp) "
                                              ";; DDS file (*.dds) "
                                              ";; BMP file (*.bmp)")[0]
    # The user didn't cancel the file to import
    if os.path.exists(import_path):
        add_texture(main_window, import_path)

        # Enable some the buttons if there won't be any more texture
        if not main_window.removeButton.isEnabled():
            # Enable the buttons
            main_window.exportAllButton.setEnabled(True)
            main_window.importAllButton.setEnabled(True)
            main_window.importButton.setEnabled(True)
            main_window.exportButton.setEnabled(True)
            main_window.removeButton.setEnabled(True)


def action_material_val_changed(main_window):

    if VEV.enable_combo_box:
        # Get the mtrl entry
        mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
        mtrl_data = mtrl_data_entry.data_info.data

        # Get the layer index
        layer = mtrl_data.layers[0]

        # Get the index to 0. This will call the other methods
        if main_window.layerVal.currentIndex() != 0:
            main_window.layerVal.setCurrentIndex(0)
        # If the index is 0, we call by ourselfs the methods of the type and texture material
        else:
            # Get the type of layer (index 0)
            main_window.typeVal.setCurrentIndex(main_window.typeVal.findData(layer.layer_name_offset))

            # Get the texture for the layer (index 0)
            main_window.textureVal.setCurrentIndex(main_window.textureVal.findData(layer.source_name_offset))


def action_layer_val_changed(main_window):

    if VEV.enable_combo_box:

        # Get the mtrl entry
        mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
        mtrl_data = mtrl_data_entry.data_info.data

        # Get the layer index
        layer = mtrl_data.layers[main_window.layerVal.currentIndex()]

        # Get the type of layer
        main_window.typeVal.setCurrentIndex(main_window.typeVal.findData(layer.layer_name_offset))

        # Get the texture for the layer
        main_window.textureVal.setCurrentIndex(main_window.textureVal.findData(layer.source_name_offset))


def action_type_val_changed(main_window):

    if VEV.enable_combo_box:
        # Get the mtrl entry
        mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
        mtrl_data = mtrl_data_entry.data_info.data

        # Get the layer index
        layer = mtrl_data.layers[main_window.layerVal.currentIndex()]

        # Store the selected type of layer
        layer.layer_name_offset = main_window.typeVal.itemData(main_window.typeVal.currentIndex())


def action_texture_val_changed(main_window):

    if VEV.enable_combo_box:
        # Get the mtrl entry
        mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
        mtrl_data = mtrl_data_entry.data_info.data

        # Get the layer index
        layer = mtrl_data.layers[main_window.layerVal.currentIndex()]

        # Store the texture for the layer
        layer.source_name_offset = main_window.textureVal.itemData(main_window.textureVal.currentIndex())


def action_add_material_logic(main_window):

    # Ask to the user the name of the material
    text, okPressed = QInputDialog.getText(main_window, "Material", "Insert a material name:", QLineEdit.Normal, "")

    # If the user write the name and is not empty, we create a new material
    if okPressed and text != '':

        # Create the data_entry for the material
        sprp_data_entry = SprpDataEntry()
        sprp_data_entry.data_type = b'MTRL'
        sprp_data_entry.index = main_window.materialVal.count()
        sprp_data_entry.new_entry = True

        # Store the data_info properties
        # The name offset value will be unique and temporal for now
        sprp_data_entry.data_info.name_offset = VEV.unique_temp_name_offset
        VEV.unique_temp_name_offset -= 1
        sprp_data_entry.data_info.data_size = 192
        sprp_data_entry.data_info.child_count = 1
        sprp_data_entry.data_info.name = text
        sprp_data_entry.data_info.name_size = len(text)

        # Create the mtrl_info
        sprp_data_entry.data_info.data = MtrlInfo()
        # We don't know for now what kind of values are these for the material. When adding, this will be the default
        sprp_data_entry.data_info.data.unk_00 = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x80\x00\x00' \
                                                b'\x3F\x24\xDD\x2F\x3E\xD1\x7A\x54\x3E\xC2\x8A\x1E\x3F\x80\x00\x00' \
                                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x80\x00\x00' \
                                                b'\x3F\x36\xC8\xB4\x3E\x6C\x28\x2D\x3E\x6C\x28\x2D\x3F\x80\x00\x00' \
                                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                                                b'\x3E\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        # Create the layers
        for i in range(0, 10):
            mtrl_layer = MtrlLayer()
            mtrl_layer.layer_name_offset = 0
            mtrl_layer.source_name_offset = 0
            sprp_data_entry.data_info.data.layers.append(mtrl_layer)

        # Create the children sprp_data_info
        sprp_data_info_children = SprpDataInfo()
        sprp_data_info_children.name_offset = VEV.DbzCharMtrl_offset
        sprp_data_info_children.data_size = 96
        sprp_data_info_children.data = b'\x3D\xCC\xCC\xCD\x3E\x2E\x14\x7B\x3F\x80\x00\x00\x3F\x33\x33\x33\x3F\x33\x33' \
                                       b'\x33\x3E\x4C\xCC\xCD\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                                       b'\x00\x00\x3E\xCC\xCC\xCD\x3F\x80\x00\x00\x00\x00\x00\x00\x3E\xCC\xCC\xCD\x3E' \
                                       b'\xCC\xCC\xCD\x3E\xCC\xCC\xCD\x3F\x4C\xCC\xCD\x3E\x4C\xCC\xCD\x3E\x4C\xCC\xCD' \
                                       b'\x3E\x4C\xCC\xCD\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                                       b'\x00'
        sprp_data_entry.data_info.child_info.append(sprp_data_info_children)

        # Add the material to the combo box
        VEV.enable_combo_box = False
        main_window.materialVal.addItem(sprp_data_entry.data_info.name, sprp_data_entry)
        main_window.materialModelPartVal.addItem(sprp_data_entry.data_info.name, sprp_data_entry.data_info.name_offset)
        VEV.enable_combo_box = True


def action_remove_material_logic(main_window):

    # Ask to the user if is sure to remove the texture
    msg = QMessageBox()
    msg.setWindowTitle("Message")
    message = "The material will be removed. Are you sure to continue?"
    answer = msg.question(main_window, '', message, msg.Yes | msg.No | msg.Cancel)

    # Check if the user has selected something
    if answer:

        # The user wants to remove the selected texture
        if answer == msg.Yes:

            # Update the index for the data_entry. If we're dealing with new added material, we recalculate their
            # offsets
            current_index_list_view = main_window.materialVal.currentIndex()
            for i in range(current_index_list_view + 1,  main_window.materialVal.count()):

                # Get the mtrl data_entry
                data_entry = main_window.materialVal.itemData(i)

                # Reduce their index
                data_entry.index -= 1

            # Search the model part that is using the material removed to assing the empty offset one
            VEV.enable_combo_box = False
            current_index_material_model = main_window.materialVal.currentIndex()
            material_name_offset = main_window.materialVal.itemData(current_index_material_model).data_info.name_offset
            for i in range(0, main_window.modelPartVal.count()):
                data_info_children = main_window.modelPartVal.itemData(i)
                if data_info_children.data.name_offset == material_name_offset:
                    data_info_children.data.name_offset = 0

            # Remove the offset material name from the model part material section
            # If the current material is selected in the combo box is the same index as the material we're removing
            # we leave the combo box to be in the index 0
            if main_window.materialModelPartVal.currentIndex() == current_index_material_model+1:
                main_window.materialModelPartVal.setCurrentIndex(0)
            main_window.materialVal.removeItem(current_index_material_model)
            main_window.materialModelPartVal.removeItem(current_index_material_model + 1)

            VEV.enable_combo_box = True


def action_model_part_val_changed(main_window):

    if VEV.enable_combo_box:

        # Get the scene data info
        scene_data_info = main_window.modelPartVal.itemData(main_window.modelPartVal.currentIndex())

        # Get the material that the model is using by searching the name offset
        main_window.materialModelPartVal.setCurrentIndex(main_window.materialModelPartVal.
                                                         findData(scene_data_info.data.name_offset))


def action_material_model_part_val_changed(main_window):

    if VEV.enable_combo_box:

        # Get the scene data info children
        data_info_children = main_window.modelPartVal.itemData(main_window.modelPartVal.currentIndex())

        # Change the material that is using the model
        data_info_children.data.name_offset = main_window.materialModelPartVal.\
            itemData(main_window.materialModelPartVal.currentIndex())
