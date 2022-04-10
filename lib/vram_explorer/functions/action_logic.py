from lib.packages import os, QFileDialog, QInputDialog, QLineEdit, QMessageBox
from lib.vram_explorer import VEF
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.classes.MTRL.MtrlInfo import MtrlInfo
from lib.vram_explorer.classes.MTRL.MtrlLayer import MtrlLayer
from lib.vram_explorer.classes.MTRL.MtrlProp import MtrlProp
from lib.vram_explorer.classes.SPRP.SprpDataEntry import SprpDataEntry
from lib.vram_explorer.classes.SPRP.SprpDataInfo import SprpDataInfo
from lib.vram_explorer.functions.auxiliary import get_encoding_name


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
                VEF.show_dds_image(image_texture, data_entry.data_info.data.tx2d_vram.data,
                                   data_entry.data_info.data.width,
                                   data_entry.data_info.data.height)
            else:
                if data_entry.data_info.extension \
                   != "png":
                    VEF.show_bmp_image(image_texture, data_entry.data_info.data.tx2d_vram.data,
                                       data_entry.data_info.data.width,
                                       data_entry.data_info.data.height)
                else:
                    VEF.show_bmp_image(image_texture, data_entry.data_info.data.tx2d_vram.data_unswizzle,
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
        msg.setWindowIcon(main_window.ico_image)
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
                message = message + VEF.import_texture(main_window, path_file, False)
            else:
                message = message + "<li>" + texture_name_extension + " not found!" + "</li>"

        # If there is a message, it has detected differences
        if message:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setWindowIcon(main_window.ico_image)
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
        VEF.import_texture(main_window, import_path, True)


def action_remove_logic(main_window):

    # Ask to the user if is sure to remove the texture
    msg = QMessageBox()
    msg.setWindowTitle("Message")
    msg.setWindowIcon(main_window.ico_image)
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

            # Reduce the increment of the string table size only if it was a brand new texture
            data_entry = main_window.listView.model().item(current_index_list_view, 0).data()
            if data_entry.new_entry:
                VEV.string_table_size_increment += - 1 - data_entry.data_info.name_size
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
            if main_window.editMaterialChildrenButton.isEnabled():
                main_window.editMaterialChildrenButton.setEnabled(False)


def action_layer_val_changed(main_window):

    if VEV.enable_combo_box:

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

    if VEV.enable_combo_box:
        # Get the mtrl entry
        mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
        mtrl_data = mtrl_data_entry.data_info.data

        # Get the layer index
        layer = mtrl_data.layers[main_window.layerVal.currentIndex()]

        # Store the selected type of layer
        layer.layer_name_offset = main_window.typeVal.itemData(main_window.typeVal.currentIndex())
        layer.layer_name = main_window.typeVal.itemText(main_window.typeVal.currentIndex())


def action_effect_val_changed(main_window):

    if VEV.enable_combo_box:
        # Get the mtrl entry
        mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
        mtrl_data = mtrl_data_entry.data_info.data

        # Get the layer index
        layer = mtrl_data.layers[main_window.layerVal.currentIndex()]

        # Store the selected effect of layer
        layer.effect_name_offset = main_window.effectVal.itemData(main_window.effectVal.currentIndex())
        layer.effect_name = main_window.effectVal.itemText(main_window.effectVal.currentIndex())


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
    text, ok_pressed = QInputDialog.getText(main_window, "Material", "Insert a material name:", QLineEdit.Normal, "")

    # If the user write the name and is not empty, we create a new material
    if ok_pressed and text != '':

        # Create the data_entry for the material
        sprp_data_entry = SprpDataEntry()
        sprp_data_entry.data_type = b'MTRL'
        sprp_data_entry.index = main_window.materialVal.count()
        sprp_data_entry.new_entry = True

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
        sprp_data_info_children.name_offset = VEV.DbzCharMtrl_offset
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
        VEV.enable_combo_box = False
        main_window.materialVal.addItem(sprp_data_entry.data_info.name, sprp_data_entry)
        main_window.materialModelPartVal.addItem(sprp_data_entry.data_info.name, sprp_data_entry.data_info.name_offset)
        VEV.enable_combo_box = True

        # Increment the string_table_size difference
        VEV.string_table_size_increment += 1 + sprp_data_entry.data_info.name_size


def action_remove_material_logic(main_window):

    # Ask to the user if is sure to remove the texture
    msg = QMessageBox()
    msg.setWindowTitle("Message")
    msg.setWindowIcon(main_window.ico_image)
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
            # Reduce the increment of the string table size only if it was a brand new material
            data_entry = main_window.materialVal.itemData(current_index_list_view)
            if data_entry.new_entry:
                VEV.string_table_size_increment += - 1 - data_entry.data_info.name_size
            main_window.materialVal.removeItem(current_index_material_model)
            main_window.materialModelPartVal.removeItem(current_index_material_model + 1)

            VEV.enable_combo_box = True


def action_material_children_logic(main_window):

    # Show the material editor window
    main_window.MaterialChildEditorWindow.show()


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


def action_rgb_changed_logic(main_window):

    if VEV.enable_combo_box:
        # Get each value RGBA
        border_rgba = ""
        border_rgba = border_rgba + str(main_window.MaterialChildEditorUI.border_color_R_value.value()) + ","
        border_rgba = border_rgba + str(main_window.MaterialChildEditorUI.border_color_G_value.value()) + ","
        border_rgba = border_rgba + str(main_window.MaterialChildEditorUI.border_color_B_value.value()) + ","
        border_rgba = border_rgba + str(main_window.MaterialChildEditorUI.border_color_A_value.value())

        # Change the color
        main_window.MaterialChildEditorUI.border_color_color\
            .setStyleSheet("background-color: rgba(" + border_rgba + ");")


def action_save_material_logic(main_window):

    # Get the mtrl entry
    mtrl_data_entry = main_window.materialVal.itemData(main_window.materialVal.currentIndex())
    # Get the mtrl child data
    mtrl_child_data = mtrl_data_entry.data_info.child_info[0].data

    mtrl_child_data.Ilumination_Shadow_orientation = \
        float(main_window.MaterialChildEditorUI.shadow_orienation_value.value()/100)
    mtrl_child_data.Ilumination_Light_orientation_glow = \
        float(main_window.MaterialChildEditorUI.light_orientation_glow_value.value()/100)
    mtrl_child_data.Saturation_base = float(main_window.MaterialChildEditorUI.saturation_base_value.value()/100)
    mtrl_child_data.Saturation_glow = float(main_window.MaterialChildEditorUI.saturation_glow_value.value()/100)
    mtrl_child_data.Brightness_toonmap = float(main_window.MaterialChildEditorUI.brightness_base_value.value()/100)
    mtrl_child_data.Brightness_toonmap_active_some_positions = mtrl_child_data.Brightness_toonmap
    mtrl_child_data.Brightness_toonmap_active_other_positions = mtrl_child_data.Brightness_toonmap
    mtrl_child_data.Brightness_incandescence = \
        float(main_window.MaterialChildEditorUI.brightness_glow_value.value()/100)
    mtrl_child_data.Brightness_incandescence_active_some_positions = mtrl_child_data.Brightness_incandescence
    mtrl_child_data.Brightness_incandescence_active_other_positions = mtrl_child_data.Brightness_incandescence
    mtrl_child_data.Border_RGBA[0] = float(main_window.MaterialChildEditorUI.border_color_R_value.value()/255)
    mtrl_child_data.Border_RGBA[1] = float(main_window.MaterialChildEditorUI.border_color_G_value.value()/255)
    mtrl_child_data.Border_RGBA[2] = float(main_window.MaterialChildEditorUI.border_color_B_value.value()/255)
    mtrl_child_data.Border_RGBA[3] = float(main_window.MaterialChildEditorUI.border_color_A_value.value()/255)

    # Close the Material children editor window
    main_window.MaterialChildEditorWindow.close()


def action_cancel_material_logic(main_window):

    # Close the Material children editor window
    main_window.MaterialChildEditorWindow.close()
