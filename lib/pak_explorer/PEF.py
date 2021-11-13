import shutil

from PyQt5.QtGui import QStandardItem, QColor, QStandardItemModel, QPixmap
from PyQt5.QtWidgets import QFileDialog

from lib.character_parameters_editor.CPEF import read_character_parameters, action_change_character, \
    open_select_chara_window, read_single_character_parameters, read_cs_chip_file
from lib.packages import os, rmtree, re, copyfile, natsorted, move, QMessageBox
from lib.functions import del_rw
from lib.pak_explorer.PEV import PEV
from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.classes.Character import Character
from lib.packages import functools


def initialize_pe(main_window):

    # Open temp folder button
    main_window.openTempFolderButton.clicked.connect(action_open_temp_folder_button_logic)

    # Export all button
    main_window.exportAllButton_2.clicked.connect(lambda: action_export_all_2_logic(main_window))

    # Export button
    main_window.exportButton_2.clicked.connect(lambda: action_export_2_logic(main_window))

    # Import button
    main_window.importButton_2.clicked.connect(lambda: action_import_2_logic(main_window))

    # Disable pak explorer tab
    main_window.pak_explorer.setEnabled(False)


def load_data_to_pe_cpe(main_window):

    # Unpack pak file (pak explorer)
    # Prepare the list view 2 in order to add the names
    model = QStandardItemModel()
    main_window.listView_2.setModel(model)
    unpack(PEV.pak_file_path, os.path.basename(PEV.pak_file_path).split(".")[-1], PEV.temp_folder,
           main_window.listView_2)
    main_window.listView_2.setCurrentIndex(main_window.listView_2.model().index(0, 0))
    PEV.current_selected_subpak_file = main_window.listView_2.model().index(0, 0).row()
    main_window.listView_2.selectionModel().currentChanged.\
        connect(lambda q_model_idx: action_item_pak_explorer(q_model_idx))
    # Enable the pak explorer
    main_window.pak_explorer.setEnabled(True)
    # Add the title
    main_window.fileNameText_2.setText(os.path.basename(PEV.pak_file_path_original))
    
    # Read the pak file (character parameters editor)
    pak_file = open(PEV.pak_file_path, mode="rb")
    
    # Read the header (STPK)
    pak_file.seek(32)
    data = pak_file.read(32).decode('utf-8').split(".")[0]
    pak_file.close()

    # Check if the file is the operate_resident_param.pak
    if data == CPEV.operate_resident_param:
    
        # reset the values
        CPEV.character_list_edited.clear()
        CPEV.character_list.clear()
        CPEV.chara_selected = 0  # Index of the char selected in the program
    
        # Read all the data from the files
        # character_info and transformer_i
        CPEV.resident_character_inf_path = main_window.listView_2.model().item(3, 0).text()
        CPEV.resident_transformer_i_path = main_window.listView_2.model().item(11, 0).text()
        subpak_file_character_inf = open(CPEV.resident_character_inf_path, mode="rb")
        subpak_file_transformer_i = open(CPEV.resident_transformer_i_path, mode="rb")
    
        # Read the data from the files and store the parameters
        for i in range(0, 100):
            # Create a Character object
            character = Character()
    
            # Store the positions where the information is located
            character.position_visual_parameters = i * CPEV.sizeVisualParameters
            character.position_trans = i * CPEV.sizeTrans
    
            # Store the information in the object and append to a list
            read_character_parameters(character, subpak_file_character_inf, subpak_file_transformer_i)
            CPEV.character_list.append(character)
    
        # Close the files
        subpak_file_character_inf.close()
        subpak_file_transformer_i.close()
    
        # We're changing the character in the main panel (avoid combo box code)
        CPEV.change_character = True
    
        # Load the large portrait
        main_window.portrait.setPixmap(QPixmap(os.path.join(CPEV.path_large_images, "chara_up_chips_l_000.png")))
    
        # Show the transformations in the main panel
        main_window.label_trans_0.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_001.bmp")))
        main_window.label_trans_0.mousePressEvent = functools.partial(action_change_character, main_window=main_window,
                                                                      index=1, modify_slot_transform=False)
        main_window.label_trans_1.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_002.bmp")))
        main_window.label_trans_1.mousePressEvent = functools.partial(action_change_character, main_window=main_window,
                                                                      index=2, modify_slot_transform=False)
        main_window.label_trans_2.setPixmap(QPixmap(os.path.join(CPEV.path_small_images, "chara_chips_003.bmp")))
        main_window.label_trans_2.mousePressEvent = functools.partial(action_change_character, main_window=main_window,
                                                                      index=3, modify_slot_transform=False)
        main_window.label_trans_0.setVisible(True)
        main_window.label_trans_1.setVisible(True)
        main_window.label_trans_2.setVisible(True)
        main_window.label_trans_3.setVisible(False)
    
        # Get the values for the fist character of the list
        character_zero = CPEV.character_list[0]
    
        # Show the health
        main_window.health_value.setValue(character_zero.health)
    
        # Show the camera size
        main_window.camera_size_cutscene_value.setValue(character_zero.camera_size[0])
        main_window.camera_size_idle_value.setValue(character_zero.camera_size[1])
    
        # Show the hit box
        main_window.hit_box_value.setValue(character_zero.hit_box)
    
        # Show the aura size
        main_window.aura_size_idle_value.setValue(character_zero.aura_size[0])
        main_window.aura_size_dash_value.setValue(character_zero.aura_size[1])
        main_window.aura_size_charge_value.setValue(character_zero.aura_size[2])
    
        # Show the color lightnings parameter
        main_window.color_lightning_value.setCurrentIndex(main_window.color_lightning_value.findData
                                                          (character_zero.color_lightning))
    
        # Show the glow/lightnings parameter
        main_window.glow_lightning_value.setCurrentIndex(main_window.glow_lightning_value.findData
                                                         (character_zero.glow_lightning))
    
        # Show the transform panel
        main_window.transSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                   str(character_zero.transformations[0]).zfill(
                                                                    3) + ".png")))
        main_window.transSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window,
                                                                        main_window=main_window,
                                                                        index=character_zero.transformations[0],
                                                                        trans_slot_panel_index=0)
        main_window.transSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                   str(character_zero.transformations[1]).zfill(
                                                                    3) + ".png")))
        main_window.transSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window,
                                                                        main_window=main_window,
                                                                        index=character_zero.transformations[1],
                                                                        trans_slot_panel_index=1)
        main_window.transSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                   str(character_zero.transformations[2]).zfill(
                                                                    3) + ".png")))
        main_window.transSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window,
                                                                        main_window=main_window,
                                                                        index=character_zero.transformations[2],
                                                                        trans_slot_panel_index=2)
        main_window.transSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                   str(character_zero.transformations[3]).zfill(
                                                                    3) + ".png")))
        main_window.transSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window,
                                                                        main_window=main_window,
                                                                        index=character_zero.transformations[3],
                                                                        trans_slot_panel_index=3)
    
        # Show the transformation parameter
        main_window.transEffectValue.setCurrentIndex(main_window.transEffectValue.findData
                                                     (character_zero.transformation_effect))
    
        # Show the transformation partner
        main_window.transPartnerValue.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                     str(character_zero.transformation_partner).zfill(3)
                                                                     + ".png")))
        main_window.transPartnerValue.mousePressEvent = functools.partial(open_select_chara_window, 
                                                                          main_window=main_window,
                                                                          index=character_zero.transformation_partner,
                                                                          transformation_partner_flag=True)
    
        # Show amount ki per transformation
        main_window.amountKi_trans1_value.setValue(character_zero.amount_ki_transformations[0])
        main_window.amountKi_trans2_value.setValue(character_zero.amount_ki_transformations[1])
        main_window.amountKi_trans3_value.setValue(character_zero.amount_ki_transformations[2])
        main_window.amountKi_trans4_value.setValue(character_zero.amount_ki_transformations[3])
    
        # Show Animation per transformation
        main_window.trans1_animation_value.setCurrentIndex(main_window.trans1_animation_value.findData
                                                           (character_zero.transformations_animation[0]))
        main_window.trans2_animation_value.setCurrentIndex(main_window.trans2_animation_value.findData
                                                           (character_zero.transformations_animation[1]))
        main_window.trans3_animation_value.setCurrentIndex(main_window.trans3_animation_value.findData
                                                           (character_zero.transformations_animation[2]))
        main_window.trans4_animation_value.setCurrentIndex(main_window.trans4_animation_value.findData
                                                           (character_zero.transformations_animation[3]))
    
        # Show the fusion panel
        main_window.fusiSlotPanel0.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                  str(character_zero.fusions[0]).zfill(3) + ".png")))
        main_window.fusiSlotPanel0.mousePressEvent = functools.partial(open_select_chara_window,
                                                                       main_window=main_window,
                                                                       index=character_zero.fusions[0],
                                                                       fusion_slot_panel_index=0)
        main_window.fusiSlotPanel1.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                  str(character_zero.fusions[1]).zfill(3) + ".png")))
        main_window.fusiSlotPanel1.mousePressEvent = functools.partial(open_select_chara_window,
                                                                       main_window=main_window,
                                                                       index=character_zero.fusions[1],
                                                                       fusion_slot_panel_index=1)
        main_window.fusiSlotPanel2.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                  str(character_zero.fusions[2]).zfill(3) + ".png")))
        main_window.fusiSlotPanel2.mousePressEvent = functools.partial(open_select_chara_window,
                                                                       main_window=main_window,
                                                                       index=character_zero.fusions[2],
                                                                       fusion_slot_panel_index=2)
        main_window.fusiSlotPanel3.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                  str(character_zero.fusions[3]).zfill(3) + ".png")))
        main_window.fusiSlotPanel3.mousePressEvent = functools.partial(open_select_chara_window,
                                                                       main_window=main_window,
                                                                       index=character_zero.fusions[3],
                                                                       fusion_slot_panel_index=3)
    
        # Show the fusion partner (trigger)
        main_window.fusionPartnerTrigger_value.setPixmap(
            QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                 str(character_zero.fusion_partner[0]).zfill(3)
                                 + ".png")))
        main_window.fusionPartnerTrigger_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                   main_window=main_window,
                                                                                   index=character_zero.fusion_partner
                                                                                   [0],
                                                                                   fusion_partner_trigger_flag=True)
    
        # Show fusion partner visual
        main_window.fusionPartnerVisual_value.setPixmap(
            QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                 str(character_zero.fusion_partner[1]).zfill(3)
                                 + ".png")))
        main_window.fusionPartnerVisual_value.mousePressEvent = functools.partial(open_select_chara_window,
                                                                                  main_window=main_window,
                                                                                  index=character_zero.
                                                                                  fusion_partner[1],
                                                                                  fusion_partner_visual_flag=True)
    
        # Show amount ki per fusion
        main_window.amountKi_fusion1_value.setValue(character_zero.amount_ki_fusions[0])
        main_window.amountKi_fusion2_value.setValue(character_zero.amount_ki_fusions[1])
        main_window.amountKi_fusion3_value.setValue(character_zero.amount_ki_fusions[2])
        main_window.amountKi_fusion4_value.setValue(character_zero.amount_ki_fusions[3])
    
        # Show Animation per transformation
        main_window.fusion1_animation_value.setCurrentIndex(main_window.fusion1_animation_value.findData
                                                            (character_zero.fusions_animation[0]))
        main_window.fusion2_animation_value.setCurrentIndex(main_window.fusion2_animation_value.findData
                                                            (character_zero.fusions_animation[1]))
        main_window.fusion3_animation_value.setCurrentIndex(main_window.fusion3_animation_value.findData
                                                            (character_zero.fusions_animation[2]))
        main_window.fusion4_animation_value.setCurrentIndex(main_window.fusion4_animation_value.findData
                                                            (character_zero.fusions_animation[3]))
    
        # We're not changing the character in the main panel (play combo box code)
        CPEV.change_character = False

        # Open the tab (character parameters editor)
        if main_window.tabWidget.currentIndex() != 2:
            main_window.tabWidget.setCurrentIndex(2)

        # Open the tab operate_resident_param
        if main_window.tabWidget_2.currentIndex() != 0:
            main_window.tabWidget_2.setCurrentIndex(0)

        # Enable completely the tab character parameters editor
        if not main_window.character_parameters_editor.isEnabled():
            main_window.character_parameters_editor.setEnabled(True)
    
        # Enable all the buttons (character parameters editor -> operate_resident_param)
        if not main_window.operate_resident_param_frame.isEnabled():
            main_window.operate_resident_param_frame.setEnabled(True)
        # Disable all the buttons (character parameters editor -> operate_character_XXX_m)
        if main_window.operate_character_xyz_m_frame.isEnabled():
            main_window.operate_character_xyz_m_frame.setEnabled(False)
        # Disable all the buttons (character parameters editor -> cs_chip)
        if main_window.cs_chip.isEnabled():
            main_window.cs_chip.setEnabled(False)

    # Check if the file is an operate_character_XXX_m type
    elif re.search(CPEV.operate_character_XXX_m_regex, data):

        # Save the id of the character to the character parameters editor tab
        CPEV.character_id = data.split("_")[2]

        # Read all the data from the files and store it in the global_character from CPEV.
        read_single_character_parameters(main_window)

        # We're not changing the character in the main panel (play combo box code)
        CPEV.change_character = False

        # Open the tab (character parameters editor)
        if main_window.tabWidget.currentIndex() != 2:
            main_window.tabWidget.setCurrentIndex(2)

        # Open the tab operate_character_XXX_m
        if main_window.tabWidget_2.currentIndex() != 1:
            main_window.tabWidget_2.setCurrentIndex(1)

        # Enable completely the tab character parameters editor
        if not main_window.character_parameters_editor.isEnabled():
            main_window.character_parameters_editor.setEnabled(True)

        # Disable all the buttons (character parameters editor -> operate_resident_param)
        if main_window.operate_resident_param_frame.isEnabled():
            main_window.operate_resident_param_frame.setEnabled(False)
        # Enable all the buttons (character parameters editor -> operate_character_XXX_m)
        if not main_window.operate_character_xyz_m_frame.isEnabled():
            main_window.operate_character_xyz_m_frame.setEnabled(True)
        # Disable all the buttons (character parameters editor -> cs_chip)
        if main_window.cs_chip.isEnabled():
            main_window.cs_chip.setEnabled(False)

    # Check if the file is cs_chip
    elif data == CPEV.cs_chip:

        # Read all the data from the files and store it in the global vars from CPEV.
        read_cs_chip_file(main_window)

        # We're not changing the character in the main panel (play combo box code)
        CPEV.change_character = False

        # Open the tab (character parameters editor)
        if main_window.tabWidget.currentIndex() != 2:
            main_window.tabWidget.setCurrentIndex(2)

        # Open the tab operate_character_XXX_m
        if main_window.tabWidget_2.currentIndex() != 2:
            main_window.tabWidget_2.setCurrentIndex(2)

        # Enable completely the tab character parameters editor
        if not main_window.character_parameters_editor.isEnabled():
            main_window.character_parameters_editor.setEnabled(True)

        # Disable all the buttons (character parameters editor -> operate_resident_param)
        if main_window.operate_resident_param_frame.isEnabled():
            main_window.operate_resident_param_frame.setEnabled(False)
        # Disable all the buttons (character parameters editor -> operate_character_XXX_m)
        if main_window.operate_character_xyz_m_frame.isEnabled():
            main_window.operate_character_xyz_m_frame.setEnabled(False)
        # Disable all the buttons (character parameters editor -> cs_chip)
        if not main_window.cs_chip.isEnabled():
            main_window.cs_chip.setEnabled(True)

    # Generic pak file
    else:

        # Open the tab (pak explorer)
        if main_window.tabWidget.currentIndex() != 1:
            main_window.tabWidget.setCurrentIndex(1)
    
        # Disable completely the tab character parameters editor
        if main_window.character_parameters_editor.isEnabled():
            main_window.character_parameters_editor.setEnabled(False)


def unpack(path_file, extension, main_temp_folder, list_view_2):

    # Open the file
    with open(path_file, mode="rb") as file:

        # Read the first four bytes
        data = file.read(4)

        # If data is STPK, means is a pak file that has inside multiple paks files
        if data == b'STPK':

            # Create a folder with the name of the file that is already opened (main pak)
            # If is the main pak of all paks, it will create the folder in the temp folder
            if not main_temp_folder:
                path_file_without_basename = os.path.dirname(path_file)
            else:
                path_file_without_basename = main_temp_folder
            folder_name = os.path.basename(path_file).split(".")[0]
            folder_path = os.path.join(path_file_without_basename, folder_name)
            if os.path.exists(folder_path):
                rmtree(folder_path, onerror=del_rw)
            os.mkdir(folder_path)

            # Get the number of subpak files that has the main pak file
            file.seek(4, 1)
            num_files = int.from_bytes(file.read(4), byteorder="big")
            file.seek(4, 1)

            # Write each subpak file
            for i in range(0, num_files):

                # Get the properties of the subpak file thas is inside of the main pak file
                offset = int.from_bytes(file.read(4), byteorder="big")
                size = int.from_bytes(file.read(4), byteorder="big")
                file.seek(8, 1)
                name = file.read(32).decode("utf-8").replace("\00", "")
                name_splitted = name.split(".")
                name = name_splitted[0] + ".pak"
                new_file_path = os.path.join(folder_path, str(i) + ";" + name)
                # There are some files that doesn't have extension, so we add a empty value
                if len(name_splitted) == 1:
                    name_splitted.append("")

                # Store the offset from the main pak file
                offset_aux = file.tell()

                # Write the subpak file
                file.seek(offset)
                data = file.read(size)
                with open(new_file_path, mode="wb") as output_file:
                    output_file.write(data)

                # Prepare the pointer of the main pak file for the next subpak file
                file.seek(offset_aux)

                # Call the function again
                unpack(new_file_path, name_splitted[1], "", list_view_2)

        # means the pak file doesn't have subpak.
        else:

            # Change the extension to his original one
            file.close()
            new_file_path = os.path.join(os.path.dirname(path_file),
                                         os.path.basename(path_file).split(".")[0] + "." + extension)
            os.rename(path_file, new_file_path)

            # Add to the listView_2
            item = QStandardItem(new_file_path)
            item.setData(os.path.basename(new_file_path).split(";")[1])
            item.setEditable(False)
            list_view_2.model().appendRow(item)


def pack(path_folder, filenames, num_filenames, num_pak_files):

    # Create the headers and data vars
    header_0 = b'STPK' + bytes.fromhex("00 00 00 01") + num_pak_files.to_bytes(4, 'big') + bytes.fromhex("00 00 00 10")
    header = b''
    data = b''

    # Store the sizes
    acumulated_sizes = 0
    size_total_block_header_subpak = num_pak_files * 48
    stpk_header_size = 16

    # Final pak file
    pak_file = b''

    # Store all the data from a folder
    for i in range(0, num_filenames):

        filename = filenames[i]
        sub_folder_path = os.path.join(path_folder, filename)

        # We step in the first folder we find
        if os.path.isdir(sub_folder_path):

            # Get all the files inside the folder, with the number of files
            sub_filenames = natsorted(os.listdir(sub_folder_path), key=lambda y: y.lower())
            num_sub_filenames = len(sub_filenames)
            num_subpak_files = int(sub_filenames[-1].split(";")[0]) + 1

            pack(sub_folder_path, sub_filenames, num_sub_filenames, num_subpak_files)

        else:
            with open(os.path.join(path_folder, filename), mode="rb") as file_pointer:

                # Get the original data and size
                data_aux = file_pointer.read()
                size_o = len(data_aux)

                # Number of bytes in order to complete a 16 bytes line
                result = size_o % 16
                if result != 0:
                    num_bytes_mod_16 = 16 - result
                else:
                    num_bytes_mod_16 = result

                # Add the '00' to the end of data in order to append the full data to the pack file.
                # Also, change the size
                for j in range(0, num_bytes_mod_16):
                    data_aux = data_aux + bytes.fromhex("00")
                size = size_o + num_bytes_mod_16

            # Calculate offset fot the subpak (64 is because of the separator)
            offset = stpk_header_size + size_total_block_header_subpak + acumulated_sizes + 64

            # Increase the size for the next offset
            acumulated_sizes = acumulated_sizes + size

            # Number of bytes in order to complete a 32 bytes line for the name
            filename = filename.split(";")[1].encode('utf-8')
            extra_bytes = 32 - len(filename)
            if extra_bytes >= 0:
                for j in range(0, extra_bytes):
                    filename = filename + bytes.fromhex("00")
            else:
                filename = filename[:extra_bytes]

            header = header + offset.to_bytes(4, "big") + size_o.to_bytes(4, "big") + bytes.fromhex(
                "00 00 00 00 00 00 00 00") + filename
            data = data + data_aux

    # Add the last 112 bytes due to is the end of the file (maybe it's not necessary)
    for i in range(0, 112):
        data = data + bytes.fromhex("00")

    # Create the pak file
    pak_file = header_0 + header + PEV.separator + pak_file + data

    # Write the new pak file in the folder
    with open(path_folder + ".pak", mode="wb") as output_file:
        output_file.write(pak_file)


def action_item_pak_explorer(q_model_index):
    if PEV.current_selected_subpak_file != q_model_index.row():
        PEV.current_selected_subpak_file = q_model_index.row()


def action_open_temp_folder_button_logic():

    # Show the path folder to the user
    os.system('explorer.exe ' + PEV.temp_folder.replace("/", "\\"))


def action_export_all_2_logic(main_window):

    # Ask to the user in what folder wants to save the files
    name_folder = os.path.basename(os.path.splitext(PEV.pak_file_path_original)[0])
    folder_export_path = QFileDialog.getSaveFileName(main_window, "Export files", name_folder, "")[0]

    # Check if the user has selected the path
    if folder_export_path:

        # Copy all the files to the folder
        shutil.copytree(PEV.temp_folder, folder_export_path)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        message = "All the files were exported in: <b>" + folder_export_path \
                  + "</b><br><br> Do you wish to open the folder?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + folder_export_path.replace("/", "\\"))


def action_export_2_logic(main_window):

    # Ask to the user where to save the file
    item = main_window.listView_2.model().item(PEV.current_selected_subpak_file, 0)
    path_original_file = item.text()
    path_copy_file = QFileDialog.getSaveFileName(main_window, "Export file", item.data(), "")[0]

    if path_copy_file:
        copyfile(path_original_file, path_copy_file)


def action_import_2_logic(main_window):

    # Ask to the user what file wants to import
    item = main_window.listView_2.model().item(PEV.current_selected_subpak_file, 0)
    path_original_file = item.text()
    path_new_file = QFileDialog.getOpenFileName(main_window, "Import file", item.data(), main_window.old_path_file)[0]

    if os.path.exists(path_new_file):
        # Copy the new file
        copyfile(path_new_file, path_original_file)

        # Changed background color in order to show that file has been changed
        item.setBackground(QColor('#7fc97f'))

        # Change old path
        main_window.old_path_file = path_new_file


def pack_and_save_file(main_window, path_output_file):

    # Due to we have issues with the permissions in the SPTK file from  drb_compressor, we move the pak file
    # to the folder 'old_pak', so we can create a new packed file
    old_pak_folder = ""
    if PEV.stpz_file:
        old_pak_folder = os.path.join(PEV.temp_folder, "old_pak")
        if not os.path.exists(old_pak_folder):
            os.mkdir(old_pak_folder)
        move(PEV.pak_file_path, os.path.join(old_pak_folder, os.path.basename(PEV.pak_file_path)))

    # Path where we'll save the stpk  packed file
    path_output_packed_file = os.path.join(PEV.temp_folder,
                                           os.path.basename(PEV.pak_file_path).split(".")[0])

    # Get the list of files inside the folder unpacked in order to pak the folder
    filenames = natsorted(os.listdir(path_output_packed_file), key=lambda y: y.lower())
    num_filenames = len(filenames)
    num_pak_files = int(filenames[-1].split(";")[0]) + 1
    pack(path_output_packed_file, filenames, num_filenames, num_pak_files)

    path_output_packed_file = path_output_packed_file + ".pak"

    # Generate the final file for the game
    args = os.path.join(PEV.dbrb_compressor_path) + " \"" + path_output_packed_file + "\" \"" \
        + path_output_file + "\""
    os.system('cmd /c ' + args)

    # Remove the 'old_pak' folder
    if PEV.stpz_file:
        rmtree(old_pak_folder, onerror=del_rw)

    msg = QMessageBox()
    msg.setWindowTitle("Message")
    message = "The file were saved and compressed in: <b>" + path_output_file \
              + "</b><br><br> Do you wish to open the folder?"
    message_open_saved_files = msg.question(main_window, '', message, msg.Yes | msg.No)

    # If the users click on 'Yes', it will open the path where the files were saved
    if message_open_saved_files == msg.Yes:
        # Show the path folder to the user
        os.system('explorer.exe ' + os.path.dirname(path_output_file).replace("/", "\\"))
