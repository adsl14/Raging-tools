from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from lib.character_parameters_editor.functions.IP.auxiliary import read_transformation_effect
from lib.packages import natsorted, os, QFileDialog, QMessageBox

from lib.character_parameters_editor import IPF
from lib.character_parameters_editor.IPV import IPV
from lib.character_parameters_editor.CPEV import CPEV


def action_export_camera_button_logic(main_window):
    # Ask to the user the file output
    name_file = CPEV.file_character_id + "_" + str(main_window.camera_type_key.currentIndex()) + "_" + \
                main_window.camera_type_key.currentText().replace(" ", "_") + "." + IPV.camera_extension
    file_export_path = QFileDialog.getSaveFileName(main_window, "Export camera",
                                                   os.path.join(main_window.old_path_file, name_file), "")[0]

    if file_export_path:

        camera_cutscene = main_window.camera_type_key.currentData()

        IPF.export_camera(file_export_path, camera_cutscene)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setWindowIcon(main_window.ico_image)
        message = "The camera file was exported in: <b>" + file_export_path \
                  + "</b><br><br> Do you wish to open the path?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + os.path.dirname(file_export_path).replace("/", "\\"))


def action_import_camera_button_logic(main_window):

    # Ask to the user from what file wants to open the camera files
    name_file = CPEV.file_character_id + "_" + str(main_window.camera_type_key.currentIndex()) + "_" + \
                main_window.camera_type_key.currentText().replace(" ", "_") + "." + IPV.camera_extension
    file_export_path = QFileDialog.getOpenFileName(main_window, "Import camera",
                                                   os.path.join(main_window.old_path_file, name_file), "")[0]

    if os.path.exists(file_export_path):

        with open(file_export_path, mode="rb") as file:

            size_file = len(file.read())

            # The file of the camera has to be 52 bytes length
            if size_file == IPV.size_each_camera_cutscene:
                file.seek(0)
            else:
                # Wrong camera file
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setWindowIcon(main_window.ico_image)
                msg.setText("Invalid camera file.")
                msg.exec()
                return

            # Get the instance of the combo box
            camera_cutscene = main_window.camera_type_key.currentData()

            # Import camera to memory
            IPF.import_camera(camera_cutscene, file)

        # Set camera values to current combo box and show them in the tool
        IPF.change_camera_cutscene_values(main_window, camera_cutscene)

        # Change old path
        main_window.old_path_file = file_export_path


def action_export_all_camera_button_logic(main_window):
    # Ask to the user the folder output
    name_folder = CPEV.file_character_id + "_cameras"
    folder_export_path = QFileDialog.getSaveFileName(main_window, "Export cameras",
                                                     os.path.join(main_window.old_path_file, name_folder), "")[0]

    if folder_export_path:

        # Create the folder
        if not os.path.exists(folder_export_path):
            os.mkdir(folder_export_path)

        # Export all the files to the folder
        for i in range(0, main_window.camera_type_key.count()):
            name_file = CPEV.file_character_id + "_" + str(i) + "_" + \
                        main_window.camera_type_key.itemText(i).replace(" ", "_") + "." + IPV.camera_extension
            file_export_path = os.path.join(folder_export_path, name_file)

            camera_cutscene = main_window.camera_type_key.itemData(i)

            IPF.export_camera(file_export_path, camera_cutscene)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setWindowIcon(main_window.ico_image)
        message = "The camera files were exported in: <b>" + folder_export_path \
                  + "</b><br><br> Do you wish to open the path?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + folder_export_path.replace("/", "\\"))


def action_import_all_camera_button_logic(main_window):
    # Ask to the user from what file wants to open the camera files
    folder_import = QFileDialog.getExistingDirectory(main_window, "Import cameras", main_window.old_path_file)

    cameras_files_error = []

    if folder_import:

        cameras_files = natsorted(os.listdir(folder_import), key=lambda y: y.lower())
        # Get the filename of each camera
        for i in range(0, len(cameras_files)):

            # Read all the data
            file_export_path = os.path.join(folder_import, cameras_files[i])
            with open(file_export_path, mode="rb") as file:

                size_file = len(file.read())
                file.seek(0)

                # Check if camera has the correct size
                if size_file == IPV.size_each_camera_cutscene:

                    # Create an instance of cameraCutscene
                    camera_cutscene = main_window.camera_type_key.itemData(i)

                    # Import camera to memory
                    IPF.import_camera(camera_cutscene, file)

                    # Change the values in the tool only for the current selected item
                    if main_window.camera_type_key.currentIndex() == i:
                        IPF.change_camera_cutscene_values(main_window, camera_cutscene)

                else:
                    cameras_files_error.append(cameras_files[i])

        # We show a message with the cameras files that couldn't get imported
        if cameras_files_error:

            message = ""

            for cameras_file_error in cameras_files_error:
                message = message + "<li>" + cameras_file_error + "</li>"
            message = "The following cameras couldn't get imported <ul>" + message + "</ul>"

            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(main_window.ico_image)
            msg.setText(message)
            msg.exec()


def action_export_animation_button_logic(main_window, animation_type_index, properties_text=""):
    # Ask to the user the file output
    name_file = CPEV.file_character_id + "_" + str(main_window.animation_type_value.currentIndex()) + "_" + \
                main_window.animation_type_value.currentText().replace(" ", "_") + properties_text + "." + \
                IPV.animations_extension
    file_export_path = QFileDialog.getSaveFileName(main_window, "Export animation",
                                                   os.path.join(main_window.old_path_file, name_file), "")[0]

    # The user has selected an output
    if file_export_path:

        # Get from the combo box, the array of animations ([[keyframes, effect], [keyframes, effects]])
        animation_array = main_window.animation_type_value.currentData()

        IPF.export_animation(animation_array, file_export_path, animation_type_index)


def action_export_all_animation_button_logic(main_window, animation_type_index, properties_text=""):
    # Ask to the user the folder output
    name_folder = CPEV.file_character_id + "_animations" + properties_text
    folder_export_path = QFileDialog.getSaveFileName(main_window,
                                                     "Export animations" + properties_text,
                                                     os.path.join(main_window.old_path_file, name_folder), "")[0]

    if folder_export_path:

        # Create the folder
        if not os.path.exists(folder_export_path):
            os.mkdir(folder_export_path)

        # Export all the files to the folder
        for i in range(0, main_window.animation_type_value.count()):
            name_file = CPEV.file_character_id + "_" + str(i) + "_" + \
                        main_window.animation_type_value.itemText(i).replace(" ", "_") + properties_text + "." + \
                        IPV.animations_extension
            file_export_path = os.path.join(folder_export_path, name_file)

            animation_array = main_window.animation_type_value.itemData(i)

            IPF.export_animation(animation_array, file_export_path, animation_type_index)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setWindowIcon(main_window.ico_image)
        message = "The animation files weres exported in: <b>" + folder_export_path \
                  + "</b><br><br> Do you wish to open the path?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + folder_export_path.replace("/", "\\"))


def action_import_animation_button_logic(main_window, animation_type_index):
    # Ask to the user from what file wants to open the camera files
    name_file = CPEV.file_character_id + "_" + str(main_window.animation_type_value.currentIndex()) + "_" + \
                main_window.animation_type_value.currentText().replace(" ", "_") + "." + IPV.animations_extension
    file_import_path = QFileDialog.getOpenFileName(main_window, "Import animation",
                                                   os.path.join(main_window.old_path_file, name_file), "")[0]

    if os.path.exists(file_import_path):
        # Import a single animation
        animation_array = main_window.animation_type_value.currentData()
        IPF.import_animation(main_window, file_import_path, animation_array, animation_type_index,
                             main_window.animation_type_value.currentIndex())

        # In the signature animation (72), the array output of the animation could have more files after
        # importing the new files. So, we change it in the combobox updating it
        if main_window.animation_type_value.currentIndex() == 72:
            main_window.animation_type_value.setItemData(main_window.animation_type_value.currentIndex(),
                                                         animation_array)
        # Check if is the file 'transformation in'
        elif main_window.animation_type_value.currentIndex() == 57:
            read_transformation_effect(main_window, animation_array[0][1])

        # Change old path
        main_window.old_path_file = file_import_path


def action_import_all_animation_button_logic(main_window, animation_type_index):
    # Ask to the user from what file wants to open the camera files
    folder_import = QFileDialog.getExistingDirectory(main_window, "Import animations", main_window.old_path_file)

    animations_files_error = []

    if folder_import:

        animation_files = natsorted(os.listdir(folder_import), key=lambda y: y.lower())
        # Get the filename of each animation
        for i in range(0, len(animation_files)):
            # Import every single animation
            animation_array = main_window.animation_type_value.itemData(i)
            IPF.import_animation(main_window, os.path.join(folder_import, animation_files[i]), animation_array,
                                 animation_type_index, i, animation_files[i], animations_files_error)

            # In the signature animation (72), the array output of the animation could have more files after
            # importing the new files. So, we change it in the combobox updating it
            if i == 72:
                main_window.animation_type_value.setItemData(i, animation_array)
            # Check if the combo box is 'animation_properties' and is the file 'transformation in' (57)
            elif i == 57:
                read_transformation_effect(main_window, animation_array[0][1])

        # We show a message with the animations files that couldn't get imported
        if animations_files_error:

            message = ""

            for animations_file_error in animations_files_error:
                message = message + "<li>" + animations_file_error + "</li>"
            message = "The following animations couldn't get imported <ul>" + message + "</ul>"

            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(main_window.ico_image)
            msg.setText(message)
            msg.exec()


def action_export_blast_button_logic(main_window):
    # Ask to the user the file output
    name_file = CPEV.file_character_id + "_" + main_window.blast_key.currentText().replace(" ", "_") + "." + \
                IPV.blast_extension
    file_export_path = QFileDialog.getSaveFileName(main_window, "Export blast",
                                                   os.path.join(main_window.old_path_file, name_file), "")[0]

    if file_export_path:

        blast = main_window.blast_key.currentData()

        IPF.export_blast(file_export_path, blast)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setWindowIcon(main_window.ico_image)
        message = "The blast file was exported in: <b>" + file_export_path \
                  + "</b><br><br> Do you wish to open the path?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + os.path.dirname(file_export_path).replace("/", "\\"))


def action_import_blast_button_logic(main_window):
    # Ask to the user from what file wants to open the camera files
    name_file = CPEV.file_character_id + "_" + main_window.blast_key.currentText().replace(" ", "_") + "." + \
                IPV.blast_extension
    file_export_path = QFileDialog.getOpenFileName(main_window, "Import blast",
                                                   os.path.join(main_window.old_path_file, name_file), "")[0]

    if os.path.exists(file_export_path):

        with open(file_export_path, mode="rb") as file:

            size_file = len(file.read())

            # The file of the blast has to be 100 bytes length
            if size_file == IPV.size_between_blast:
                file.seek(0)
            else:
                # Wrong camera file
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setWindowIcon(main_window.ico_image)
                msg.setText("Invalid blast file.")
                msg.exec()
                return

            # Get the instance of the combo box
            blast = main_window.blast_key.currentData()

            # Import blast values to memory
            IPF.import_blast(blast, file)

            # Show the imported values in the tool
            IPF.change_blast_values(main_window, blast)

        # Change old path
        main_window.old_path_file = file_export_path


def action_export_all_blast_button_logic(main_window):
    # Ask to the user the folder output
    name_folder = CPEV.file_character_id + "_blasts"
    folder_export_path = QFileDialog.getSaveFileName(main_window, "Export blasts",
                                                     os.path.join(main_window.old_path_file, name_folder), "")[0]

    if folder_export_path:

        # Create the folder
        if not os.path.exists(folder_export_path):
            os.mkdir(folder_export_path)

        # Export all the files to the folder
        for i in range(0, main_window.blast_key.count()):
            name_file = CPEV.file_character_id + "_" + main_window.blast_key.itemText(i).replace(" ", "_") + "." + \
                IPV.blast_extension
            file_export_path = os.path.join(folder_export_path, name_file)

            blast = main_window.blast_key.itemData(i)

            IPF.export_blast(file_export_path, blast)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setWindowIcon(main_window.ico_image)
        message = "The blast files were exported in: <b>" + folder_export_path \
                  + "</b><br><br> Do you wish to open the path?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + folder_export_path.replace("/", "\\"))


def action_import_all_blast_button_logic(main_window):

    # Ask to the user from what file wants to open the blast files
    folder_import = QFileDialog.getExistingDirectory(main_window, "Import blasts", main_window.old_path_file)

    blasts_files_error = []

    if folder_import:

        blasts_files = natsorted(os.listdir(folder_import), key=lambda y: y.lower())
        found_current_blast_key = False

        # Get the filename of each blast
        for i in range(0, len(blasts_files)):

            # Read all the data
            file_export_path = os.path.join(folder_import, blasts_files[i])
            with open(file_export_path, mode="rb") as file:

                size_file = len(file.read())
                file.seek(0)

                # Check if blast values file has the correct size
                if size_file == IPV.size_between_blast:

                    # Create an instance of Blast
                    blast = main_window.blast_key.itemData(i)

                    # Import blast to memory
                    IPF.import_blast(blast, file)

                    if not found_current_blast_key and main_window.blast_key.currentIndex() == i:
                        # We found the index of the blast value that the user has currently selected
                        found_current_blast_key = True

                        # Show the imported values in the tool
                        IPF.change_blast_values(main_window, blast)

                else:
                    blasts_files_error.append(blasts_files[i])

        # We show a message with the cameras files that couldn't get imported
        if blasts_files_error:

            message = ""

            for blasts_file_error in blasts_files_error:
                message = message + "<li>" + blasts_file_error + "</li>"
            message = "The following blasts couldn't get imported <ul>" + message + "</ul>"

            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(main_window.ico_image)
            msg.setText(message)
            msg.exec()


def action_export_signature_ki_blast_button_logic(main_window):

    # Ask to the user the file output
    name_file = CPEV.file_character_id + "_" + "Signature_ki_blast_properties"
    file_export_path = QFileDialog.getSaveFileName(main_window, "Export signature ki blast",
                                                   os.path.join(main_window.old_path_file, name_file), "")[0]

    if file_export_path:

        with open(file_export_path, mode="wb") as outputfile:
            outputfile.write(IPV.signature_ki_blast.data)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setWindowIcon(main_window.ico_image)
        message = "The signature ki blast file was exported in: <b>" + file_export_path \
                  + "</b><br><br> Do you wish to open the path?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + os.path.dirname(file_export_path).replace("/", "\\"))


def action_import_signature_ki_blast_button_logic(main_window):

    # Ask to the user from what file wants to open the signature ki blast file
    name_file = CPEV.file_character_id + "_" + "Signature_ki_blast_properties"
    file_export_path = QFileDialog.getOpenFileName(main_window, "Import signature ki blast",
                                                   os.path.join(main_window.old_path_file, name_file), "")[0]

    if os.path.exists(file_export_path):

        with open(file_export_path, mode="rb") as file:
            IPV.signature_ki_blast.data = file.read()
            IPV.signature_ki_blast.modified = True

        # Change old path
        main_window.old_path_file = file_export_path


def action_change_character(event, main_window):

    blast = main_window.blast_key.currentData()

    # Check if the current partner is the same as the selected in the window, so we can clean the window
    if IPV.old_selected_partner != blast.partner_id:
        # Restore the color of the old selected character
        select_chara_roster_window_label = main_window.selectCharaPartnerUI.frame.findChild(QLabel, "label_" + str(IPV.old_selected_partner))
        select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSlotRosterWindow)

        # Store the current partner
        IPV.old_selected_partner = blast.partner_id

    # Change color for the selected character in chara roster window
    select_chara_roster_window_label = main_window.selectCharaPartnerUI.frame.findChild(QLabel, "label_" + str(blast.partner_id))
    select_chara_roster_window_label.setStyleSheet(CPEV.styleSheetSelectCharaRosterWindow)

    # Show the select chara roster window
    main_window.selectCharaPartnerWindow.show()


def action_modify_character(event, main_window, chara_id):

    # Get current blast
    blast = main_window.blast_key.currentData()

    # Change partner id
    blast.partner_id = chara_id
    blast.modified = True

    # Change partner image
    main_window.partner_character_value.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(blast.partner_id).zfill(3) + ".png")))
    # Close Window
    main_window.selectCharaPartnerWindow.close()


def on_camera_type_key_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        IPF.change_camera_cutscene_values(main_window, main_window.camera_type_key.currentData())


def on_pivot_value_changed(main_window, pivot_index):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        if pivot_index == 0:
            main_window.camera_type_key.currentData().pivots["pivot_1"] = \
                main_window.pivot_value.value()
            main_window.camera_type_key.currentData().modified = True
        elif pivot_index == 1:
            main_window.camera_type_key.currentData().pivots["pivot_2"] = \
                main_window.pivot_value_2.value()
            main_window.camera_type_key.currentData().modified = True
        elif pivot_index == 2:
            main_window.camera_type_key.currentData().pivots["pivot_3"] = \
                main_window.pivot_value_3.value()
            main_window.camera_type_key.currentData().modified = True
        else:
            main_window.camera_type_key.currentData().pivots["pivot_4"] = \
                main_window.pivot_value_4.value()
            main_window.camera_type_key.currentData().modified = True


def on_translations_changed(main_window, y, z):
    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        if y >= 0:
            if y == 0:
                main_window.camera_type_key.currentData().positions["Y_start"] =\
                    main_window.translation_y_start_value.value()
                main_window.camera_type_key.currentData().modified = True
            else:
                main_window.camera_type_key.currentData().positions["Y_end"] = \
                    main_window.translation_y_end_value.value()
                main_window.camera_type_key.currentData().modified = True
        else:
            if z == 0:
                main_window.camera_type_key.currentData().positions["Z_start"] =\
                    main_window.translation_z_start_value.value()
                main_window.camera_type_key.currentData().modified = True
            else:
                main_window.camera_type_key.currentData().positions["Z_end"] = \
                    main_window.translation_z_end_value.value()
                main_window.camera_type_key.currentData().modified = True


def on_rotations_changed(main_window, y, z):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        if y >= 0:
            if y == 0:
                main_window.camera_type_key.currentData().rotations["Y_start"] =\
                    main_window.rotation_y_start_value.value()
                main_window.camera_type_key.currentData().modified = True
            else:
                main_window.camera_type_key.currentData().rotations["Y_end"] = \
                    main_window.rotation_y_end_value.value()
                main_window.camera_type_key.currentData().modified = True
        else:
            if z == 0:
                main_window.camera_type_key.currentData().rotations["Z_start"] =\
                    \
                    main_window.rotation_z_start_value.value()
                main_window.camera_type_key.currentData().modified = True
            else:
                main_window.camera_type_key.currentData().rotations["Z_end"] = \
                    main_window.rotation_z_end_value.value()
                main_window.camera_type_key.currentData().modified = True


def on_speed_camera_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        main_window.camera_type_key.currentData().camera_speed = \
            main_window.speed_camera_value.value()
        main_window.camera_type_key.currentData().modified = True


def on_zoom_start_value_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        main_window.camera_type_key.currentData().zooms["Zoom_start"] = \
            main_window.zoom_start_value.value()
        main_window.camera_type_key.currentData().modified = True


def on_zoom_end_value_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        main_window.camera_type_key.currentData().zooms["Zoom_end"] = \
            main_window.zoom_end_value.value()
        main_window.camera_type_key.currentData().modified = True


def on_background_color_trans_change(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the color of the background when we change the combo box background color transformation
        animation_effect = main_window.animation_type_value.itemData(57)[0][1]
        animation_effect.data = animation_effect.data[:IPV.trans_effect_position_byte] + \
            main_window.background_color_trans_value.\
            currentData().to_bytes(1, "big") + animation_effect.data[IPV.trans_effect_position_byte+1:]
        animation_effect.modified = True


def on_blast_attack_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        IPF.change_blast_values(main_window, main_window.blast_key.currentData())


def on_glow_activation_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the glow activation
        blast = main_window.blast_key.currentData()
        blast.glow = main_window.glow_activation_value.currentData()
        blast.modified = True


def on_stackable_skill_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the skill stackable
        blast = main_window.blast_key.currentData()
        blast.skill_stackable = main_window.stackable_skill_value.currentData()
        blast.modified = True


def on_power_up_changed(main_window, combobox, powerup_type):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the powerup activation
        blast = main_window.blast_key.currentData()
        blast.power_ups[powerup_type] = combobox.currentData()
        blast.modified = True


def on_effect_attack_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the activation skill
        blast = main_window.blast_key.currentData()
        blast.activation_skill = main_window.effect_attack_value.currentData()
        blast.modified = True


def on_chargeable_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the chargeable/boost value
        blast = main_window.blast_key.currentData()
        blast.chargeable_boost = main_window.chargeable_value.currentData()
        blast.modified = True


def on_reach_attack_value_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the reach attack value
        blast = main_window.blast_key.currentData()
        blast.reach_attack = main_window.reach_attack_value.value()
        blast.modified = True


def on_speed_attack_value_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the speed_of_attack
        blast = main_window.blast_key.currentData()
        blast.speed_of_attack = main_window.speed_attack_value.value()
        blast.modified = True


def on_blast_attack_damage_value_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the attack_damage
        blast = main_window.blast_key.currentData()
        blast.attack_damage = main_window.blast_attack_damage_value.value()
        blast.modified = True


def on_cost_blast_attack_value_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the cost_attack
        blast = main_window.blast_key.currentData()
        blast.cost_attack = main_window.cost_blast_attack_value.value()
        blast.modified = True


def on_number_of_hits_value_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the number_of_hits
        blast = main_window.blast_key.currentData()
        blast.number_of_hits = main_window.number_of_hits_value.value()
        blast.modified = True


def on_size_attack_value_changed(main_window):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the size_of_attack
        blast = main_window.blast_key.currentData()
        blast.size_of_attack = main_window.size_attack_value.value()
        blast.modified = True


def on_camera_blast_value_changed(main_window, camera_index, spinbox):

    # Avoid change the values when the program is changing the character from the main panel and starting
    if not CPEV.change_character:
        # Change the camera value
        blast = main_window.blast_key.currentData()
        blast.camera[camera_index] = spinbox.value()
        blast.modified = True
