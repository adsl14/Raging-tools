from lib.packages import datetime, os

class PEV:

    # types of spr file
    # STPZ and STPK file
    STPZ = b'STPZ'
    STPK = b'STPK'
    stpz_file = False

    # Temp folder name
    temp_folder = "temp_PE" + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S")
    # Path files
    pak_file_path_original = ""
    pak_file_path = ""

    # resources path
    dbrb_compressor_path = os.path.join("lib", "resources", "dbrb_compressor.exe")

    current_selected_subpak_file = 0
