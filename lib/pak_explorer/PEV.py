from lib.packages import os


class PEV:

    # types of spr file
    # STPZ and STPK file
    STPZ = b'STPZ'
    STPK = b'STPK'
    stpz_file = False

    # Separator that will be used in pak files (between header block and data)
    separator_size_64 = 64
    separator_64 = b''
    separator_size_4032 = 4032
    separator_4032 = b''
    for i in range(0, separator_size_4032):
        if i < 64:
            separator_64 = separator_64 + bytes.fromhex("00")
        separator_4032 = separator_4032 + bytes.fromhex("00")

    # Temp folder name
    temp_folder = "temp"
    # Path files
    pak_file_path_original = ""
    pak_file_path = ""

    # resources path
    dbrb_compressor_path = os.path.join("lib", "resources", "dbrb_compressor.exe")

    # Index of the current selected file
    current_selected_subpak_file = 0
    # Total number of files in pak_explorer
    number_files = 0
