from lib.packages import os


class PEV:

    # types of spr file
    # STPZ and STPK file
    STPZ = b'STPZ'
    STPK = b'STPK'
    stpz_file = False

    # Separator that will be used in pak files (between header and data)
    separator = b''
    for i in range(0, 64):
        separator = separator + bytes.fromhex("00")

    # Temp folder name
    temp_folder = "temp"
    # Path files
    pak_file_path_original = ""
    pak_file_path = ""

    # resources path
    dbrb_compressor_path = os.path.join("lib", "resources", "dbrb_compressor.exe")

    current_selected_subpak_file = 0
