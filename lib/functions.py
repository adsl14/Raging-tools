from PyQt5.QtWidgets import QMessageBox

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


def check_entry_module(entry, entry_size, module):

    rest = module - (entry_size % module)
    if rest != module:
        for i in range(rest):
            entry += b'\00'
            entry_size += 1
    else:
        rest = 0

    return entry, entry_size, rest


def get_name_from_file(file, offset):

    file.seek(offset)
    name = ""

    # Read the file until we find the '00' byte value
    while True:

        # Read one char
        data = file.read(1)

        # If the value is not 00, we store the char
        if data != b'\x00':

            try:
                data_decoded = data.decode('utf-8')
            except UnicodeDecodeError:
                # Some bytes can't be decoded directly, so we will add the string directly instead
                if data == b'\x82':
                    data_decoded = ","
                elif data == b'\x8c':
                    data_decoded = "Œ"
                elif data == b'\xf3':
                    data_decoded = "ó"
                else:
                    data_decoded = "?"

            name += data_decoded

        # The texture name is already stored. We clean it
        else:
            # Get the name splitted by '.'
            name_splitted = name.split(".")
            tam_name_splitted = len(name_splitted)
            name = ""

            # Get the name and extension separatelly
            if tam_name_splitted > 1:
                for i in range(0, tam_name_splitted - 1):
                    name += name_splitted[i] + ("." if i < tam_name_splitted - 2 else "")
                extension = name_splitted[-1]
            else:
                name = name_splitted[0]
                extension = ""

            # The max number of char for the name is 250
            name_size = len(name)
            if name_size > 250:
                name = name[name_size - 250:]

            # Finish the reading of the file
            break

    return name, extension
