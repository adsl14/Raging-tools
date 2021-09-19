from PyQt5.QtGui import QStandardItem, QColor
from PyQt5.QtWidgets import QFileDialog

from lib.packages import os, rmtree, copyfile, natsorted, move, QMessageBox
from lib.functions import del_rw
from lib.pak_explorer.PEV import PEV


def initialize_pe(main_window):

    # Export button
    main_window.exportButton_2.clicked.connect(lambda: action_export_2_logic(main_window))

    # Import button
    main_window.importButton_2.clicked.connect(lambda: action_import_2_logic(main_window))

    # Disable pak explorer tab
    main_window.pak_explorer.setEnabled(False)


def unpack(path_file, extension, main_temp_folder, listView_2):

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
                unpack(new_file_path, name_splitted[1], "", listView_2)

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
            listView_2.model().appendRow(item)


def pack(path_folder, filenames, num_filenames, num_pak_files):

    # Create the headers and data vars
    header_0 = b'STPK' + bytes.fromhex("00 00 00 01") + num_pak_files.to_bytes(4, 'big') + bytes.fromhex("00 00 00 10")
    header = b''
    data = b''

    # Store the sizes
    acumulated_sizes = 0
    size_total_block_header_subpak = num_pak_files * 48
    stpk_header_size = 16

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

            # Calculate offset fot the subpak
            offset = stpk_header_size + size_total_block_header_subpak + acumulated_sizes

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
    pak_file = header_0 + header + pak_file + data

    # Write the new pak file in the folder
    with open(path_folder + ".pak", mode="wb") as output_file:
        output_file.write(pak_file)


def action_item_pak_explorer(q_model_index):
    if PEV.current_selected_subpak_file != q_model_index.row():
        PEV.current_selected_subpak_file = q_model_index.row()


def action_export_2_logic(main_window):

    # Ask to the user where to save the file
    item = main_window.listView_2.model().item(PEV.current_selected_subpak_file, 0)
    path_original_file = item.text()
    path_copy_file = QFileDialog.getSaveFileName(main_window, "Save file", item.data(), "")[0]

    if path_copy_file:
        copyfile(path_original_file, path_copy_file)


def action_import_2_logic(main_window):

    # Ask to the user what file wants to import
    item = main_window.listView_2.model().item(PEV.current_selected_subpak_file, 0)
    path_original_file = item.text()
    path_new_file = QFileDialog.getOpenFileName(main_window, "Open file", item.data(), "")[0]

    if path_new_file:
        # Copy the new file
        copyfile(path_new_file, path_original_file)

        # Changed background color in order to show that file has been changed
        item.setBackground(QColor('#7fc97f'))


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
