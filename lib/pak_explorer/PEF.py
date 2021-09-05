from lib.pak_explorer.PEV import PEV
from lib.packages import os
from lib.packages import QFileDialog
from lib.pak_explorer.classes.UNPAK import UNPAK


def initialize_pe(main_window):

    # Buttons
    main_window.exportButton_2.clicked.connect(lambda: action_export_2_logic(main_window))
    main_window.importButton_2.clicked.connect(lambda: action_import_2_logic(main_window))
    main_window.exportButton_2.setVisible(False)
    main_window.importButton_2.setVisible(False)


def action_item_2(q_model_index):

    if PEV.current_selected_unpak_data != q_model_index.row():
        PEV.current_selected_unpak_data = q_model_index.row()


def action_export_2_logic(main_window):

    # Save unpak file
    export_path = QFileDialog.getSaveFileName(main_window, "Save file", os.path.join(os.path.abspath(os.getcwd()),
                                                                                     PEV.unpaks[
                                                                                     PEV.current_selected_unpak_data]
                                                                                     .name))[0]

    data = PEV.unpaks[PEV.current_selected_unpak_data].data

    if export_path:
        file = open(export_path, mode="wb")
        file.write(data)
        file.close()


def action_import_2_logic(main_window):

    # Save unpak file
    import_path = QFileDialog.getOpenFileName(main_window, "Open file", os.path.join(os.path.abspath(os.getcwd()),
                                                                                     PEV.unpaks[
                                                                                         PEV.current_selected_unpak_data]
                                                                                     .name))[0]

    if import_path:
        with open(import_path, mode="rb") as input_file:

            data = input_file.read()
            size = len(data)

            # Save the new unpak data in the memory
            PEV.unpaks[PEV.current_selected_unpak_data].data = data
            PEV.unpaks[PEV.current_selected_unpak_data].difference = \
                size - PEV.unpaks[PEV.current_selected_unpak_data].size_original
            PEV.unpaks[PEV.current_selected_unpak_data].size = size

            print(PEV.unpaks[PEV.current_selected_unpak_data].difference)


def unpack_pak_file(pak_file, folder_path, file_path="", offset=0, size=0):

    data = pak_file.read(4)

    # If the new file has a STPK, means it has more files
    if data == PEV.STPK:

        pak_file.seek(4, 1)
        number_of_paks = int.from_bytes(pak_file.read(4), "big")
        pak_file.seek(4, 1)
        offset_o = 16

        for i in range(0, number_of_paks):

            offset = int.from_bytes(pak_file.read(4), "big")
            size = int.from_bytes(pak_file.read(4), "big")
            pak_file.seek(8, 1)
            name = pak_file.read(32).decode('utf-8').replace("\x00", "")
            basename = name.split(".")[0]

            pak_file.seek(offset)
            data = pak_file.read(size)

            # Check that the name of the folder and the new file doesn't have the same filename
            if name[-1] == ".":
                name = name[:-1]
            if name == basename:
                basename = basename + "_"

            new_folder_path = os.path.join(folder_path, str(i) + "_" + basename)
            new_file_path = os.path.join(folder_path, str(i) + "_" + name)
            os.mkdir(new_folder_path)

            with open(new_file_path, mode="wb") as output_file:
                output_file.write(data)

            with open(new_file_path, mode="rb") as input_file:
                unpack_pak_file(input_file, new_folder_path, new_file_path, offset, size)

            offset_o = offset_o + 48
            pak_file.seek(offset_o)
    else:

        # We remove the folder that was created because is not a pak file
        os.rmdir(folder_path)

        # Store all the data in memory
        pak_file.seek(0)
        data = pak_file.read()

        # Create a instance
        unpak = UNPAK()
        unpak.name = os.path.basename(file_path)
        unpak.offset = offset
        unpak.size_original = size
        unpak.size = size
        unpak.data = data
        # Save in memory all the info
        PEV.unpaks.append(unpak)
