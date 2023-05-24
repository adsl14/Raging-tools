from lib.packages import os, QFileDialog, QInputDialog, QLineEdit, QMessageBox
from lib.vram_explorer import VEF
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.classes.MTRL.MtrlInfo import MtrlInfo
from lib.vram_explorer.classes.MTRL.MtrlLayer import MtrlLayer
from lib.vram_explorer.classes.MTRL.MtrlProp import MtrlProp
from lib.vram_explorer.classes.SPRP.SprpDataEntry import SprpDataEntry
from lib.vram_explorer.classes.SPRP.SprpDataInfo import SprpDataInfo
from lib.vram_explorer.functions.auxiliary import get_encoding_name


def show_texture(list_view, image_texture, encoding_image_text, mip_maps_image_text, size_image_text):

    current_selected_index = list_view.currentIndex().row()

    # There is no texture to show if the index is negative
    if current_selected_index >= 0:

        data_entry = list_view.model().item(current_selected_index, 0).data()

        # Only shows the texture when the size is different from 0
        if data_entry.data_info.data.data_size != 0:

            # If the encoding is DXT5 or DXT1, we show the dds image
            if data_entry.data_info.data.dxt_encoding != 0:
                # If we're dealing with an Xbox spr file and the encoding of the texture is ATI2 (normal texture)
                # we won't show anything in the tool view
                if VEV.header_type_spr_file != b'SPR3' or data_entry.data_info.data.dxt_encoding != 32:
                    # Create the dds in disk and open it
                    VEF.show_dds_image(image_texture, data_entry.data_info.data.tx2d_vram.data,
                                       data_entry.data_info.data.width,
                                       data_entry.data_info.data.height)
                else:
                    # Remove image in the tool view
                    image_texture.clear()
            else:
                if not data_entry.data_info.data.tx2d_vram.data_unswizzle_ps3:
                    VEF.show_bmp_image(image_texture, data_entry.data_info.data.tx2d_vram.data,
                                       data_entry.data_info.data.width,
                                       data_entry.data_info.data.height)
                else:
                    VEF.show_bmp_image(image_texture, data_entry.data_info.data.tx2d_vram.data_unswizzle_ps3,
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

        if not data_entry.data_info.data.tx2d_vram.data_unswizzle_ps3:
            data = data_entry.data_info.data.tx2d_vram.data
        else:
            data = data_entry.data_info.data.tx2d_vram.data_unswizzle_ps3

    if export_path:
        file = open(export_path, mode="wb")
        file.write(data)
        file.close()


def action_export_all_logic(main_window):

    # Ask the user where to save the files
    folder_export_path = QFileDialog.getSaveFileName(main_window, "Export textures", os.path.splitext(
        VEV.spr_file_path)[0] + "_textures")[0]

    # Check if the user selected the folder
    if folder_export_path:

        # Create the folder
        if not os.path.exists(folder_export_path):
            os.mkdir(folder_export_path)

        num_textures = main_window.listView.model().rowCount()
        for i in range(0, num_textures):
            data_entry = main_window.listView.model().item(i, 0).data()
            # The image is dds
            if data_entry.data_info.data.dxt_encoding != 0:

                file = open(os.path.join(folder_export_path, data_entry.data_info.name + ".dds"), mode="wb")

                file.write(data_entry.data_info.data.tx2d_vram.data)
                file.close()

            else:
                file = open(os.path.join(folder_export_path, data_entry.data_info.name + ".bmp"), mode="wb")
                if not data_entry.data_info.data.tx2d_vram.data_unswizzle_ps3:
                    file.write(data_entry.data_info.data.tx2d_vram.data)
                else:
                    file.write(data_entry.data_info.data.tx2d_vram.data_unswizzle_ps3)
                file.close()

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setWindowIcon(main_window.ico_image)
        message = "All the textures were exported in: <b>" + folder_export_path \
                  + "</b><br><br> Do you wish to open the folder?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + folder_export_path.replace("/", "\\"))


def action_import_all_logic(main_window):

    # Ask the user from where to import the files into the tool
    folder_import_path = QFileDialog.getExistingDirectory(main_window, "Import textures")

    if folder_import_path:

        # Message to show
        message = ""
        # Flag that will be used to show the texture modified in the tool
        show_texture_flag = False
        # Get the current texture selected
        current_selected_texture = main_window.listView.selectionModel().currentIndex().row()
        # Get all the textures name from memory
        num_textures = main_window.listView.model().rowCount()

        for i in range(0, num_textures):
            data_entry = main_window.listView.model().item(i, 0).data()

            # Check if is the texture that the user is currently selected, to show it in the tool
            if i == current_selected_texture:
                show_texture_flag = True
            elif show_texture_flag:
                show_texture_flag = False

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
                output_message = VEF.import_texture(main_window, path_file, False, show_texture_flag, data_entry)
                if output_message:
                    message = message + texture_name_extension + "<ul>" + output_message + "</ul>"
            else:
                message = message + texture_name_extension + "<ul><li>" + "Texture <b>not found!</b>" + "</li></ul>"

        # If there is a message, it has detected differences
        if message:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setWindowIcon(main_window.ico_image)
            msg.setText("Found the following errors while importing: <br><br>" + message)
            msg.exec()
            return


def action_import_logic(main_window):

    # Open texture file
    import_path = QFileDialog.getOpenFileName(main_window, "Import texture", os.path.join(main_window.old_path_file,
                                                                                          ""),
                                              "Supported files (*.dds *.bmp) "
                                              ";; DDS file (*.dds) "
                                              ";; BMP file (*.bmp)")[0]
    # The user didn't cancel the file to import
    if os.path.exists(import_path):
        data_entry = main_window.listView.model().item(main_window.listView.selectionModel().currentIndex().row(), 0)\
            .data()
        VEF.import_texture(main_window, import_path, True, True, data_entry)

        # Change old path
        main_window.old_path_file = import_path


def action_remove_logic(main_window):

    # Ask the user if is sure to remove the texture
    msg = QMessageBox()
    msg.setWindowTitle("Message")
    msg.setWindowIcon(main_window.ico_image)
    message = "The texture will be removed. Are you sure to continue?"
    answer = msg.question(main_window, '', message, msg.Yes | msg.No | msg.Cancel)

    # Check if the user has selected something
    if answer:

        # The user wants to remove the selected texture
        if answer == msg.Yes:

            # Update the index for the data_entry
            current_index_list_view = main_window.listView.selectionModel().currentIndex().row()

            # Remove from the array of textures in the window list
            main_window.listView.model().removeRow(current_index_list_view)

            # Remove from the array of textures in the material section
            VEF.listen_events_logic(main_window, False)
            current_index_material_texture_index = current_index_list_view + 1

            # Search the material layer that is using the texture removed to assign the empty offset one
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
            VEF.listen_events_logic(main_window, True)

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
        VEF.add_texture(main_window, import_path)

        # Enable some the buttons if there won't be any more texture
        if not main_window.removeButton.isEnabled():
            # Enable the buttons
            main_window.exportAllButton.setEnabled(True)
            main_window.importAllButton.setEnabled(True)
            main_window.importButton.setEnabled(True)
            main_window.exportButton.setEnabled(True)
            main_window.removeButton.setEnabled(True)


def action_material_val_changed(main_window):

    # Get the mtrl entry
    mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
    mtrl_data = mtrl_data_entry.data_info.data

    # Get the layer index
    layer = mtrl_data.layers[0]

    # Get the index to 0. This will call the other methods
    if main_window.layerVal.currentIndex() != 0:
        main_window.layerVal.setCurrentIndex(0)
    # If the index is 0, we call by our self the methods of the type and texture material
    else:
        # Get the type of layer (index 0)
        main_window.typeVal.setCurrentIndex(main_window.typeVal.findText(layer.layer_name))

        # Get the effect of layer (index 0)
        main_window.effectVal.setCurrentIndex(main_window.effectVal.findText(layer.effect_name))

        # Get the texture for the layer (index 0)
        main_window.textureVal.setCurrentIndex(main_window.textureVal.findData(layer.source_name_offset))

    # Change the material children (if any)
    if mtrl_data_entry.data_info.child_count > 0:

        # Get the material children
        mtrl_child = mtrl_data_entry.data_info.child_info[0]

        # Raging Blast 2 material children
        if mtrl_child.data_size == 96:
            if not main_window.editMaterialChildrenButton.isEnabled():
                main_window.editMaterialChildrenButton.setEnabled(True)
            # Load the material children to the window
            VEF.load_material_children_to_window(main_window, mtrl_child.data)
        else:
            if main_window.editMaterialChildrenButton.isEnabled():
                main_window.editMaterialChildrenButton.setEnabled(False)

    else:
        # Close material children window and disable button for material children edition
        if main_window.editMaterialChildrenButton.isEnabled():
            main_window.editMaterialChildrenButton.setEnabled(False)
            main_window.MaterialChildEditorWindow.close()


def action_layer_val_changed(main_window):

    # Get the mtrl entry
    mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
    mtrl_data = mtrl_data_entry.data_info.data

    # Get the layer index
    layer = mtrl_data.layers[main_window.layerVal.currentIndex()]

    # Get the type of layer
    main_window.typeVal.setCurrentIndex(main_window.typeVal.findText(layer.layer_name))

    # Get the effect of layer
    main_window.effectVal.setCurrentIndex(main_window.effectVal.findText(layer.effect_name))

    # Get the texture for the layer
    main_window.textureVal.setCurrentIndex(main_window.textureVal.findData(layer.source_name_offset))


def action_type_val_changed(main_window):

    # Get the mtrl entry
    mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
    mtrl_data = mtrl_data_entry.data_info.data

    # Get the layer index
    layer = mtrl_data.layers[main_window.layerVal.currentIndex()]

    # Store the selected type of layer
    layer.layer_name = main_window.typeVal.itemText(main_window.typeVal.currentIndex())


def action_effect_val_changed(main_window):

    # Get the mtrl entry
    mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
    mtrl_data = mtrl_data_entry.data_info.data

    # Get the layer index
    layer = mtrl_data.layers[main_window.layerVal.currentIndex()]

    # Store the selected effect of layer
    layer.effect_name = main_window.effectVal.itemText(main_window.effectVal.currentIndex())


def action_texture_val_changed(main_window):

    # Get the mtrl entry
    mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
    mtrl_data = mtrl_data_entry.data_info.data

    # Get the layer index
    layer = mtrl_data.layers[main_window.layerVal.currentIndex()]

    # Store the texture for the layer
    layer.source_name_offset = main_window.textureVal.itemData(main_window.textureVal.currentIndex())


def action_add_material_logic(main_window):

    # Ask the user the name of the material
    text, ok_pressed = QInputDialog.getText(main_window, "Material", "Insert a material name:", QLineEdit.Normal, "")

    # If the user write the name and is not empty, we create a new material
    if ok_pressed and text != '':

        # Create the data_entry for the material
        sprp_data_entry = SprpDataEntry()
        sprp_data_entry.data_type = b'MTRL'
        sprp_data_entry.index = main_window.materialVal.count()

        # Store the data_info properties
        # The name offset value will be unique and temporal for now
        sprp_data_entry.data_info.name_offset = VEV.unique_temp_name_offset
        VEV.unique_temp_name_offset += 1
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
        sprp_data_info_children.name = "DbzCharMtrl"
        sprp_data_info_children.data_size = 96

        # Create a default material properties for the new material
        mtrl_prop = MtrlProp()
        mtrl_prop.Ilumination_Shadow_orientation = 0.1
        mtrl_prop.Ilumination_Light_orientation_glow = 0.17
        mtrl_prop.unk0x04[0] = 1.0
        mtrl_prop.unk0x04[1] = 0.7
        mtrl_prop.Brightness_purple_light_glow = 0.7
        mtrl_prop.Saturation_glow = 0.8
        mtrl_prop.Saturation_base = 0.0
        mtrl_prop.Brightness_toonmap_active_some_positions = 0.0
        mtrl_prop.Brightness_toonmap = 0.0
        mtrl_prop.Brightness_toonmap_active_other_positions = 0.0
        mtrl_prop.Brightness_incandescence_active_some_positions = 0.4
        mtrl_prop.Brightness_incandescence = 1.0
        mtrl_prop.Brightness_incandescence_active_other_positions = 0.0
        mtrl_prop.Border_RGBA[0] = 0.4
        mtrl_prop.Border_RGBA[1] = 0.4
        mtrl_prop.Border_RGBA[2] = 0.4
        mtrl_prop.Border_RGBA[3] = 0.8
        mtrl_prop.unk0x44[0] = 0.2
        mtrl_prop.unk0x44[1] = 0.2
        mtrl_prop.unk0x44[2] = 0.2
        mtrl_prop.unk0x50[0] = 0.0
        mtrl_prop.unk0x50[1] = 0.0
        mtrl_prop.unk0x50[2] = 0.0
        mtrl_prop.unk0x50[3] = 0.0
        sprp_data_info_children.data = mtrl_prop
        sprp_data_entry.data_info.child_info.append(sprp_data_info_children)

        # Add the material to the combo box
        VEF.listen_events_logic(main_window, False)
        main_window.materialVal.addItem(sprp_data_entry.data_info.name, sprp_data_entry)
        main_window.materialModelPartVal.addItem(sprp_data_entry.data_info.name, sprp_data_entry.data_info.name_offset)
        VEF.listen_events_logic(main_window, True)


def action_remove_material_logic(main_window):

    # Ask the user if is sure to remove the texture
    msg = QMessageBox()
    msg.setWindowTitle("Message")
    msg.setWindowIcon(main_window.ico_image)
    message = "The material will be removed. Are you sure to continue?"
    answer = msg.question(main_window, '', message, msg.Yes | msg.No | msg.Cancel)

    # Check if the user has selected something
    if answer:

        # The user wants to remove the selected texture
        if answer == msg.Yes:

            # Remove the material
            current_index_material_model = main_window.materialVal.currentIndex()
            material_name_offset = main_window.materialVal.itemData(current_index_material_model).data_info.name_offset
            main_window.materialVal.removeItem(current_index_material_model)

            # Search the model part that is using the material removed to assign the empty offset one
            VEF.listen_events_logic(main_window, False)
            for i in range(0, main_window.modelPartVal.count()):
                data_info_children = main_window.modelPartVal.itemData(i)
                if data_info_children.data.name_offset == material_name_offset:
                    data_info_children.data.name_offset = 0

            # Remove the offset material name from the model part material section
            # If the current material is selected in the combo box is the same index as the material we're removing
            # we leave the combo box to be in the index 0
            if main_window.materialModelPartVal.currentIndex() == current_index_material_model+1:
                main_window.materialModelPartVal.setCurrentIndex(0)

            main_window.materialModelPartVal.removeItem(current_index_material_model + 1)

            VEF.listen_events_logic(main_window, True)


def action_material_export_logic(main_window):

    # Get the current mtrl entry
    mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())

    # Ask the path
    export_path = QFileDialog.getSaveFileName(main_window, "Export material", os.path.join(
        main_window.old_path_file, mtrl_data_entry.data_info.name))[0]

    # If the user has selected a path, we export the material
    if export_path:
        VEF.export_material(export_path, mtrl_data_entry)


def action_material_import_logic(main_window):

    # Ask the user from what file wants to open the camera files
    file_import_path = QFileDialog.getOpenFileName(main_window, "Import material", main_window.old_path_file, "")[0]

    if os.path.exists(file_import_path):
        mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
        message = VEF.import_material(main_window, file_import_path, mtrl_data_entry, False, True)

        # Check if there is an error
        if message:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setWindowIcon(main_window.ico_image)
            msg.setText(message)
            msg.exec()

        # Change old path
        main_window.old_path_file = file_import_path


def action_material_export_all_logic(main_window):

    # Ask the user where to save the files
    folder_export_path = QFileDialog.getSaveFileName(main_window, "Export materials", os.path.splitext(
        VEV.spr_file_path)[0] + "_materials")[0]

    # Check if the user selected the folder
    if folder_export_path:

        # Create the folder
        if not os.path.exists(folder_export_path):
            os.mkdir(folder_export_path)

        num_materials = main_window.materialVal.count()
        for i in range(0, num_materials):
            # Get the mtrl entry
            mtrl_data_entry = main_window.materialVal.itemData(i)
            # Export the material
            VEF.export_material(os.path.join(folder_export_path, mtrl_data_entry.data_info.name), mtrl_data_entry)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setWindowIcon(main_window.ico_image)
        message = "All the materials were exported in: <b>" + folder_export_path \
                  + "</b><br><br> Do you wish to open the folder?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + folder_export_path.replace("/", "\\"))


def action_material_import_all_logic(main_window):

    # Ask the user from where to import the files into the tool
    folder_import_path = QFileDialog.getExistingDirectory(main_window, "Import materials")

    if folder_import_path:

        # Message to show
        message = ""
        # Get the current index material that the user is watching
        current_index = main_window.materialVal.currentIndex()
        # This flag will be used to show the current child values of the material that the user is watching
        show_edited_child = False
        # Get all the textures name from memory
        num_materials = main_window.materialVal.count()

        for i in range(0, num_materials):
            # Get the mtrl name
            mtrl_data_entry = main_window.materialVal.itemData(i)

            if i == current_index:
                show_edited_child = True
            elif show_edited_child:
                show_edited_child = False

            # Get the path and check in the folder the material. If the tool find the material, we import it
            # If the tool finds errors, it won't import the material and will add a message at the end with the errors
            path_file = os.path.join(folder_import_path, mtrl_data_entry.data_info.name)
            if os.path.exists(path_file):
                message = message + VEF.import_material(main_window, path_file, mtrl_data_entry, True,
                                                        show_edited_child)
            else:
                message = message + "<li>" + mtrl_data_entry.data_info.name + " not found!" + "</li>"

        # If there is a message, it has detected differences
        if message:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setWindowIcon(main_window.ico_image)
            msg.setText("Found the following errors while importing:" + "<ul>" + message + "</ul>")
            msg.exec()
            return


def action_material_children_logic(main_window):

    # Disable check 'A' value for border color apply to all materials
    main_window.MaterialChildEditorUI.border_color_A_apply_all_materials.setChecked(False)

    # Show the material editor window
    main_window.MaterialChildEditorWindow.show()


def action_model_part_val_changed(main_window):

    # Get the scene data info
    scene_data_info = main_window.modelPartVal.itemData(main_window.modelPartVal.currentIndex())

    # Get the material that the model is using by searching the name offset
    main_window.materialModelPartVal.setCurrentIndex(main_window.materialModelPartVal.findData(scene_data_info.data.name_offset))


def action_material_model_part_val_changed(main_window):

    # Get the scene data info children
    data_info_children = main_window.modelPartVal.itemData(main_window.modelPartVal.currentIndex())

    # Change the material that is using the model
    data_info_children.data.name_offset = main_window.materialModelPartVal.itemData(main_window.materialModelPartVal.currentIndex())


def action_rgb_changed_logic(main_window):

    # Get each value RGBA
    border_rgba = ""
    border_rgba = border_rgba + str(main_window.MaterialChildEditorUI.border_color_R_value.value()) + ","
    border_rgba = border_rgba + str(main_window.MaterialChildEditorUI.border_color_G_value.value()) + ","
    border_rgba = border_rgba + str(main_window.MaterialChildEditorUI.border_color_B_value.value()) + ","
    border_rgba = border_rgba + str(main_window.MaterialChildEditorUI.border_color_A_value.value())

    # Change the color
    main_window.MaterialChildEditorUI.border_color_color.setStyleSheet("background-color: rgba(" + border_rgba + ");")


def action_save_material_logic(main_window):

    # Apply the changes with the current material
    if not main_window.MaterialChildEditorUI.border_color_A_apply_all_materials.isChecked():
        # Get the mtrl entry
        mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())

        # Replace children material values
        VEF.replace_material_children_values(main_window, mtrl_data_entry)

        # Close the Material children editor window
        main_window.MaterialChildEditorWindow.close()

    # Replace the 'A' value for border color to all the children materials
    else:

        # Create the message window
        msg = QMessageBox()
        message = "Do you wish to replace the current 'A' border color value to all materials?"
        # Ask the user if he/she is sure that wants to replace the current border color values to all the materials
        msg.setWindowIcon(main_window.ico_image)
        message_import_result = msg.question(main_window, 'Warning', message, msg.Yes | msg.No)

        # If the user says yes, then we replace the current border color values to all the children materials values
        if message_import_result == msg.Yes:
            # Get the number of materials
            num_material = main_window.materialVal.count()

            # Get each material from comboBox
            for i in range(0, num_material):
                # Get the mtrl entry
                mtrl_data_entry = main_window.materialVal.itemData(i)

                # If there is a material that doesn't have children, we won't modify anything
                if mtrl_data_entry.data_info.child_count > 0:
                    # Replace 'A' border color value
                    if i != main_window.materialVal.currentIndex():
                        mtrl_data_entry.data_info.child_info[0].data.Border_RGBA[3] = \
                            float(main_window.MaterialChildEditorUI.border_color_A_value.value() / 255)
                    # While we're iterating in the comboBox, we find the current material that the user has selected,
                    # we edit not only the 'A' border color value but all the current material children values
                    else:
                        VEF.replace_material_children_values(main_window, mtrl_data_entry)

            # Close the Material children editor window
            main_window.MaterialChildEditorWindow.close()
        else:
            # Bring material children window to front again
            main_window.MaterialChildEditorWindow.activateWindow()


def action_cancel_material_logic(main_window):

    # Close the Material children editor window
    main_window.MaterialChildEditorWindow.close()
