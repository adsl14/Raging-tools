import threading

from PyQt5.QtWidgets import QMessageBox

from lib.character_parameters_editor.GPF import write_db_font_pad_ps3, write_operate_resident_param
from lib.character_parameters_editor.GPV import GPV
from lib.character_parameters_editor.IPF import write_single_character_parameters
from lib.character_parameters_editor.REF import write_cs_chip_file
from lib.packages import os, stat
from lib.pak_explorer.PEV import PEV


def del_rw(name_method, path, error):
    os.chmod(path, stat.S_IWRITE)
    os.remove(path)

    return name_method, error


def ask_pack_structure(main_window):

    # Ask to the user if is packing a vram or ioram file for Xbox. If is for Xbox,
    # we have to change the separator size that is written between header and data. Otherwise
    # will crash or make an output with bugs and errors
    msg = QMessageBox()
    msg.setWindowTitle("Message")
    msg.setWindowIcon(main_window.ico_image)
    message = "Do you wish to pack the file with Xbox compatibility?"
    answer = msg.question(main_window, '', message, msg.Yes | msg.No)

    if answer == msg.Yes:
        # Packing file with Xbox compatibility (this is only when packing .vram or .ioram files, but
        # it looks like it's working for any other files)
        print("Packing the file with Xbox compatibility...")
        separator_size = PEV.separator_size_4032
        separator = PEV.separator_4032
    else:
        print("Packing the file...")
        separator_size = PEV.separator_size_64
        separator = PEV.separator_64

    return separator, separator_size
