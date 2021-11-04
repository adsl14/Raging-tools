from lib.packages import datetime, os


class PEV:

    # types of spr file
    # STPZ and STPK file
    STPZ = b'STPZ'
    STPK = b'STPK'
    stpz_file = False

    # Flag that will tell us if the pak file has only ioram or vram files
    spr_type_pak = True

    # Separator that will be used in pak files (between header and data, only for pak files that holds vram or ioram)
    separator_vram_ioram = b''
    for i in range(0, 64):
        separator_vram_ioram = separator_vram_ioram + bytes.fromhex("00")

    # Temp folder name
    temp_folder = "temp_PE" + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S")
    # Path files
    pak_file_path_original = ""
    pak_file_path = ""

    # resources path
    dbrb_compressor_path = os.path.join("lib", "resources", "dbrb_compressor.exe")

    current_selected_subpak_file = 0
