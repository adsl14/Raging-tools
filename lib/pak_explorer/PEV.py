from lib.packages import os


class PEV:

    # types of spr file
    # STPZ and STPK file
    STPZ = b'STPZ'
    STPK = b'STPK'
    stpz_file = False

    # dummy data
    DUMMY = b'DUMM'
    dummy_extension = ".dum"

    # type pak file
    TYPE = b'TYPE'
    type_extension = ".typ"

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

    # List of the Raging Blast series games that we will use it to ask the user for the compression structure
    endianess_structure = ["Raging Blast 1 & 2", "Ultimate Tenkaichi"]

    # Asking base message when we need to ask the user from differents options
    message_endianess_structure = "Choose the compression structure:"
    endianess_structure_result = []
