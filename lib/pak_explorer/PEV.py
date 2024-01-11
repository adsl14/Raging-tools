from lib.packages import os


class PEV:

    # types of spr file
    # STPZ and STPK file
    STPZ = b'STPZ'
    STPK = b'STPK'
    stpz_file = False

    # Pack flag accept/cancel
    accept_button_pushed_pack_format_window = False
    ps3_version = False

    # List of number of bytes for padding (PS3 -> vram/ioram)
    separator_sizes_ps3_vram_ioram = [64, 16, 96, 48, 0, 80, 32, 112]

    # Temp folder name
    temp_folder = "temp"
    # Path files
    pak_file_path_original = ""
    pak_file_path = ""

    # resources path
    dbrb_compressor_path = os.path.join("lib", "resources", "dbrb_compressor.exe")

    # Total number of files in pak_explorer
    number_files = 0
