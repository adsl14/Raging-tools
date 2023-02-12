from lib.packages import os, copyfile, copytree, QFileDialog, QMessageBox, QColor
from lib.pak_explorer.PEV import PEV


def action_open_temp_folder_button_logic():

    # Show the path folder to the user
    os.system('explorer.exe ' + PEV.temp_folder.replace("/", "\\"))


def action_export_all_2_logic(main_window):

    # Ask to the user in what folder wants to save the files
    name_folder = os.path.basename(os.path.splitext(PEV.pak_file_path_original)[0])
    folder_export_path = QFileDialog.getSaveFileName(main_window, "Export files",
                                                     os.path.join(main_window.old_path_file, name_folder), "")[0]

    # Check if the user has selected the path
    if folder_export_path:

        # Copy all the files to the folder
        copytree(PEV.temp_folder, folder_export_path)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setWindowIcon(main_window.ico_image)
        message = "All the files were exported in: <b>" + folder_export_path \
                  + "</b><br><br> Do you wish to open the folder?"
        message_open_exported_files = msg.question(main_window, '', message, msg.Yes | msg.No)

        # If the users click on 'Yes', it will open the path where the files were saved
        if message_open_exported_files == msg.Yes:
            # Show the path folder to the user
            os.system('explorer.exe ' + folder_export_path.replace("/", "\\"))


def action_export_2_logic(main_window):

    # Ask to the user where to save the file
    item = main_window.listView_2.model().item(main_window.listView_2.selectionModel().currentIndex().row(), 0)
    path_original_file = item.text()
    path_copy_file = QFileDialog.getSaveFileName(main_window, "Export file",
                                                 os.path.join(main_window.old_path_file, item.data()), "")[0]

    if path_copy_file:
        copyfile(path_original_file, path_copy_file)


def action_import_2_logic(main_window):

    # Ask to the user what file wants to import
    item = main_window.listView_2.model().item(main_window.listView_2.selectionModel().currentIndex().row(), 0)
    path_original_file = item.text()
    path_new_file = QFileDialog.getOpenFileName(main_window, "Import file",
                                                os.path.join(main_window.old_path_file, item.data()))[0]

    if os.path.exists(path_new_file):
        # Copy the new file
        copyfile(path_new_file, path_original_file)

        # Changed background color in order to show that file has been changed
        item.setBackground(QColor('#7fc97f'))

        # Change old path
        main_window.old_path_file = path_new_file
