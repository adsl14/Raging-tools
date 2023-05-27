import json
import struct

from lib.character_parameters_editor.classes.BONE.BoneEntry import BoneEntry
from lib.character_parameters_editor.classes.CAMERA.CameraEntry import CameraEntry
from lib.character_parameters_editor.classes.SCNE.ScneEntry import ScneEntry
from lib.character_parameters_editor.classes.SPA.SPAFile import SPAFile

from lib.packages import os, stat
from lib.pak_explorer.PEV import PEV


def del_rw(name_method, path, error):
    os.chmod(path, stat.S_IWRITE)
    os.remove(path)

    return name_method, error


def ask_pack_structure(main_window):

    # Ask the user the packing format (separator between header and data)
    PEV.accept_button_pushed_pack_format_window = False
    main_window.packFormatUI.console_version.setCurrentIndex(0)
    main_window.packFormatUI.type_format_pack.setCurrentIndex(0)
    main_window.packFormatWindow.activateWindow()
    main_window.packFormatWindow.exec()


def create_stpk_properties(main_window, num_pak_files):

    separator = b''
    separator_size = 0

    # Calculate the separator size
    # PS3
    if main_window.packFormatUI.console_version.currentIndex() == 0:

        # vram/ioram
        if main_window.packFormatUI.type_format_pack.currentIndex() == 0:
            separator_size = 64
            unk0x0c = bytes.fromhex("00 00 00 80")
            if num_pak_files > 1:
                for i in range(1, num_pak_files):
                    if i % 2 != 0:
                        separator_size = separator_size - 48
                    else:
                        separator_size = separator_size + 80
        # Other and spr
        else:
            unk0x0c = bytes.fromhex("00 00 00 10")
    # XBOX 360
    else:

        # vram/ioram
        if main_window.packFormatUI.type_format_pack.currentIndex() == 0:
            separator_size = 4032
            unk0x0c = bytes.fromhex("00 00 10 00")
            if num_pak_files > 1:
                for i in range(1, num_pak_files):
                    separator_size = separator_size - 48
        # Other
        elif main_window.packFormatUI.type_format_pack.currentIndex() == 2:
            separator_size = 1984
            unk0x0c = bytes.fromhex("00 00 08 00")
            if num_pak_files > 1:
                for i in range(1, num_pak_files):
                    separator_size = separator_size - 48

                    # If the separator size is less than 0, we break the loop and assign the size to 0
                    if separator_size < 0:
                        separator_size = 0
                        break
        # spr
        else:
            unk0x0c = bytes.fromhex("00 00 00 10")

    # Create the separator
    for _ in range(separator_size):
        separator = separator + bytes.fromhex("00")

    return separator_size, separator, unk0x0c


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

            # Get the name and extension separately
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


def read_spa_file(spa_path):

    # Create the instance for the spa
    spa_file = SPAFile()

    # Store the path
    spa_file.path = spa_path

    # Read the data of the spa
    with open(spa_path, mode="rb") as file:
        spa_file.spa_header.unk0x00 = file.read(4)
        name_offset = file.read(4)
        spa_file.spa_header.unk0x08 = file.read(4)

        # If there is data in the first 4 bytes which starts with b'\x00\x00\x00\x00
        # and the byte in position 8 to 12 is 5 (ID of is a spa maybe?) we continue reading
        if spa_file.spa_header.unk0x00 == b'\x00\x00\x00\x00' and spa_file.spa_header.unk0x08 == b'\x00\x00\x00\x05':

            # Read the name and restore the pointer to continue reading the following bytes
            aux_pointer = file.tell()
            spa_file.spa_header.name, spa_file.spa_header.extension = get_name_from_file(file, int.from_bytes(name_offset, "big"))
            file.seek(aux_pointer)

            # Read header
            spa_file.spa_header.frame_count = struct.unpack('>f', file.read(4))[0]
            spa_file.spa_header.bone_count = int.from_bytes(file.read(4), "big")
            spa_file.spa_header.bone_nodes_offset = int.from_bytes(file.read(4), "big")
            spa_file.spa_header.scene_nodes_count = int.from_bytes(file.read(4), "big")
            spa_file.spa_header.scene_nodes_offset = int.from_bytes(file.read(4), "big")
            spa_file.spa_header.camera_count = int.from_bytes(file.read(4), "big")
            spa_file.spa_header.camera_offset = int.from_bytes(file.read(4), "big")
            spa_file.spa_header.unk0x28 = file.read(4)
            spa_file.spa_header.unk0x2c = file.read(4)

            # Read bones
            file.seek(spa_file.spa_header.bone_nodes_offset)
            for _ in range(0, spa_file.spa_header.bone_count):
                # Create bone instance
                bone_entry = BoneEntry()

                # Read the name and restore the pointer to continue reading the following bytes
                aux_pointer = file.tell()
                bone_entry.name, _ = get_name_from_file(file, int.from_bytes(file.read(4), "big"))
                file.seek(aux_pointer + 4)

                # Meta data
                bone_entry.unk0x04 = file.read(4)
                bone_entry.translation_block_count = int.from_bytes(file.read(4), "big")
                bone_entry.rotation_block_count = int.from_bytes(file.read(4), "big")
                bone_entry.unknown_block_count = int.from_bytes(file.read(4), "big")
                bone_entry.translation_frame_offset = int.from_bytes(file.read(4), "big")
                bone_entry.rotation_frame_offset = int.from_bytes(file.read(4), "big")
                bone_entry.unknown_frame_offset = int.from_bytes(file.read(4), "big")
                bone_entry.translation_float_offset = int.from_bytes(file.read(4), "big")
                bone_entry.rotation_float_offset = int.from_bytes(file.read(4), "big")
                bone_entry.unknown_float_offset = int.from_bytes(file.read(4), "big")
                bone_entry.unk0x2c = file.read(4)

                # Data
                aux_pointer = file.tell()
                # Read translations
                file.seek(bone_entry.translation_frame_offset)
                for i in range(0, bone_entry.translation_block_count):
                    # Read frame
                    bone_entry.translation_frame_data.append(struct.unpack('>f', file.read(4))[0])

                    # Read float (x, y, z, w)
                    aux_translation_pointer = file.tell()
                    file.seek(bone_entry.translation_float_offset + (i * 16))
                    bone_entry.translation_float_data.append(dict({"x": struct.unpack('>f', file.read(4))[0], "y": struct.unpack('>f', file.read(4))[0], "z": struct.unpack('>f', file.read(4))[0],
                                                                   "w": struct.unpack('>f', file.read(4))[0]}))
                    # Return to the next frame translation
                    file.seek(aux_translation_pointer)

                # Read rotations
                file.seek(bone_entry.rotation_frame_offset)
                for i in range(0, bone_entry.rotation_block_count):
                    # Read frame
                    bone_entry.rot_frame_data.append(struct.unpack('>f', file.read(4))[0])

                    # Read float (the calculation of x, y and z, needs more research. When we create the rot value from x, y and z, we don't get the same result as the input)
                    aux_rotation_pointer = file.tell()
                    file.seek(bone_entry.rotation_float_offset + (i * 8))
                    rot = int.from_bytes(file.read(8), "big")
                    ''''x = ((((rot & 0x0fffffffffffffff) >> 40) / 0x7ffff) * 90) - 90
                    y = ((((rot & 0x000000ffffffffff) >> 20) / 0x7ffff) * 90) - 90
                    z = (((rot & 0x00000000000fffff) / 0x7ffff) * 90) - 90'''
                    bone_entry.rot_float_data.append(dict({"rot": rot, "x": 0, "y": 0, "z": 0}))
                    # Return to the next frame rotation
                    file.seek(aux_rotation_pointer)

                # Read unknown
                file.seek(bone_entry.unknown_frame_offset)
                for i in range(0, bone_entry.unknown_block_count):
                    # Read frame
                    bone_entry.unknown_frame_data.append(struct.unpack('>f', file.read(4))[0])

                    # Read float (x, y, z, w)
                    aux_unknown_pointer = file.tell()
                    file.seek(bone_entry.unknown_float_offset + (i * 16))
                    bone_entry.unknown_float_data.append(dict({"x": struct.unpack('>f', file.read(4))[0], "y": struct.unpack('>f', file.read(4))[0], "z": struct.unpack('>f', file.read(4))[0],
                                                         "w": struct.unpack('>f', file.read(4))[0]}))
                    # Return to the next frame translation
                    file.seek(aux_unknown_pointer)

                # Restore pointer
                file.seek(aux_pointer)

                # Store everything in the dict
                spa_file.bone_entries[bone_entry.name] = bone_entry

            # Read scenes
            file.seek(spa_file.spa_header.scene_nodes_offset)
            for _ in range(0, spa_file.spa_header.scene_nodes_count):
                # Create scne instance
                scne_entry = ScneEntry()

                # Read the name and restore the pointer to continue reading the following bytes
                aux_pointer = file.tell()
                scne_entry.name, _ = get_name_from_file(file, int.from_bytes(file.read(4), "big"))
                file.seek(aux_pointer + 4)

                # Meta data
                scne_entry.frame_count = int.from_bytes(file.read(4), "big")
                scne_entry.frame_offset = int.from_bytes(file.read(4), "big")
                scne_entry.float_offset = int.from_bytes(file.read(4), "big")

                # Data
                aux_pointer = file.tell()

                # Read float and frame data
                file.seek(scne_entry.frame_offset)
                for i in range(0, scne_entry.frame_count):
                    # Read frame
                    scne_entry.frame_data.append(struct.unpack('>f', file.read(4))[0])

                    # Read float
                    aux_unknown_pointer = file.tell()
                    file.seek(scne_entry.float_offset + (i * 4))
                    scne_entry.float_data.append(struct.unpack('>f', file.read(4))[0])

                    # Return to the next frame
                    file.seek(aux_unknown_pointer)

                # Restore pointer
                file.seek(aux_pointer)

                # Store everything in the dict
                spa_file.camera_entries[scne_entry.name] = scne_entry

            # Read cameras
            file.seek(spa_file.spa_header.camera_offset)
            for _ in range(0, spa_file.spa_header.camera_count):
                # Create camera instance
                camera_entry = CameraEntry()

                # Read the name and restore the pointer to continue reading the following bytes
                aux_pointer = file.tell()
                camera_entry.name, _ = get_name_from_file(file, int.from_bytes(file.read(4), "big"))
                file.seek(aux_pointer + 4)

                # Meta data
                camera_entry.frame_count = int.from_bytes(file.read(4), "big")
                camera_entry.frame_offset = int.from_bytes(file.read(4), "big")
                camera_entry.float_offset = int.from_bytes(file.read(4), "big")

                # Data
                aux_pointer = file.tell()

                # Read float and frame data
                file.seek(camera_entry.frame_offset)
                for i in range(0, camera_entry.frame_count):
                    # Read frame
                    camera_entry.frame_data.append(struct.unpack('>f', file.read(4))[0])

                    # Read float
                    aux_unknown_pointer = file.tell()
                    file.seek(camera_entry.float_offset + (i * 4))
                    camera_entry.float_data.append(struct.unpack('>f', file.read(4))[0])

                    # Return to the next frame
                    file.seek(aux_unknown_pointer)

                # Restore pointer
                file.seek(aux_pointer)

                # Store everything in the dict
                spa_file.camera_entries[camera_entry.name] = camera_entry

        # Store the size of the file
        spa_file.size = file.tell()

    return spa_file


def write_spa_file(spa_file):

    header_data = b''
    header_size = 0

    bone_entry = b''
    bone_entry_offset = 48
    bone_entry_size = 48 * spa_file.spa_header.bone_count
    bone_data = b''
    bone_data_size = 0

    scne_entry = b''
    scne_entry_offset = bone_entry_offset + bone_entry_size
    scne_entry_size = 16 * spa_file.spa_header.scene_nodes_count
    scne_data = b''
    scne_data_size = 0

    camera_entry = b''
    camera_entry_offset = scne_entry_offset + scne_entry_size
    camera_entry_size = 16 * spa_file.spa_header.camera_count
    camera_data = b''
    camera_data_size = 0

    string_table = b''
    string_table_size = 0

    # If there are camera or bones data, we create the spa. Otherwise, will be empty
    if spa_file.bone_entries or spa_file.scne_entries or spa_file.camera_entries:

        # Write first all the data
        # Write bones
        bone_data_start_offset = bone_entry_offset + bone_entry_size + scne_entry_size + camera_entry_size
        for bone_entry_name in spa_file.bone_entries:
            # Get the bone data
            bone_entry_data = spa_file.bone_entries[bone_entry_name]

            # Write frames
            # Translation
            # Update offset (only if there is data)
            if bone_entry_data.translation_block_count > 0:

                # Check if the data, the module of 16 is 0 before writing
                bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

                bone_entry_data.translation_frame_offset = bone_data_start_offset + bone_data_size
                for translation_frame in bone_entry_data.translation_frame_data:
                    bone_data = bone_data + struct.pack('>f', translation_frame)
                    bone_data_size += 4
            else:
                bone_entry_data.translation_frame_offset = 0

            # Rotations
            # Update offset (only if there is data)
            if bone_entry_data.rotation_block_count > 0:

                # Check if the data, the module of 16 is 0 before writing
                bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

                bone_entry_data.rotation_frame_offset = bone_data_start_offset + bone_data_size
                for rotation_frame in bone_entry_data.rot_frame_data:
                    bone_data = bone_data + struct.pack('>f', rotation_frame)
                    bone_data_size += 4
            else:
                bone_entry_data.rotation_frame_offset = 0

            # Unknown
            # Update offset (only if there is data)
            if bone_entry_data.unknown_block_count > 0:

                # Check if the data, the module of 16 is 0 before writing
                bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

                bone_entry_data.unknown_frame_offset = bone_data_start_offset + bone_data_size
                for unknown_frame in bone_entry_data.unknown_frame_data:
                    bone_data = bone_data + struct.pack('>f', unknown_frame)
                    bone_data_size += 4
            else:
                bone_entry_data.unknown_frame_offset = 0

            # Write floats
            # Translation
            # Update offset (only if there is data)
            if bone_entry_data.translation_block_count > 0:

                # Check if the data, the module of 16 is 0 before writing
                bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

                bone_entry_data.translation_float_offset = bone_data_start_offset + bone_data_size
                for translation_float in bone_entry_data.translation_float_data:
                    bone_data = bone_data + struct.pack('>f', translation_float['x'])
                    bone_data = bone_data + struct.pack('>f', translation_float['y'])
                    bone_data = bone_data + struct.pack('>f', translation_float['z'])
                    bone_data = bone_data + struct.pack('>f', translation_float['w'])
                    bone_data_size += 16

            else:
                bone_entry_data.translation_float_offset = 0

            # Rotation
            # Update offset (only if there is data)
            if bone_entry_data.rotation_block_count > 0:

                # Check if the data, the module of 16 is 0 before writing
                bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

                bone_entry_data.rotation_float_offset = bone_data_start_offset + bone_data_size
                for rotation_float in bone_entry_data.rot_float_data:
                    # Convert each axis rotation in order to write the 'rot' value propertly. It needs more research since the rot calculated is not the same from the original
                    '''rot_x = get_rotation(rotation_float['x']) << 40
                    rot_y = get_rotation(rotation_float['y']) << 20
                    rot_z = get_rotation(rotation_float['z'])
                    rot = 0x3000000000000000 | rot_x | rot_y | rot_z
                    bone_data = bone_data + rot.to_bytes(8, 'big')'''
                    bone_data = bone_data + rotation_float['rot'].to_bytes(8, 'big')
                    bone_data_size += 8
            else:
                bone_entry_data.rotation_float_offset = 0

            # Unknown
            # Update offset (only if there is data)
            if bone_entry_data.unknown_block_count > 0:

                # Check if the data, the module of 16 is 0 before writing
                bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

                bone_entry_data.unknown_float_offset = bone_data_start_offset + bone_data_size
                for unknown_float in bone_entry_data.unknown_float_data:
                    bone_data = bone_data + struct.pack('>f', unknown_float['x'])
                    bone_data = bone_data + struct.pack('>f', unknown_float['y'])
                    bone_data = bone_data + struct.pack('>f', unknown_float['z'])
                    bone_data = bone_data + struct.pack('>f', unknown_float['w'])
                    bone_data_size += 16

            else:
                bone_entry_data.unknown_float_offset = 0
        # Prepare for the next data type if the module of 16 is 0 before writing
        bone_data, bone_data_size, _ = check_entry_module(bone_data, bone_data_size, 16)

        # Write scnes
        scne_data_start_offset = bone_data_start_offset + bone_data_size
        for scne_entry_name in spa_file.scne_entries:
            # Get the scne data
            scne_entry_data = spa_file.scne_entries[scne_entry_name]

            # Write data
            # Update offset (only if there is data)
            if scne_entry_data.frame_count > 0:

                # Write frame data
                # Check if the data, the module of 16 is 0 before writing
                scne_data, scne_data_size, _ = check_entry_module(scne_data, scne_data_size, 16)

                scne_entry_data.frame_offset = scne_data_start_offset + scne_data_size
                for frame_data in scne_entry_data.frame_data:
                    scne_data = scne_data + struct.pack('>f', frame_data)
                    scne_data_size += 4

                # Write float data
                # Check if the data, the module of 16 is 0 before writing
                scne_data, scne_data_size, _ = check_entry_module(scne_data, scne_data_size, 16)

                scne_entry_data.float_offset = scne_data_start_offset + scne_data_size
                for float_data in scne_entry_data.float_data:
                    scne_data = scne_data + struct.pack('>f', float_data)
                    scne_data_size += 4
            else:
                scne_entry_data.frame_offset = 0
                scne_entry_data.float_offset = 0
        # Prepare for the next data type if the module of 16 is 0 before writing
        scne_data, scne_data_size, _ = check_entry_module(scne_data, scne_data_size, 16)

        # Write cameras
        camera_data_start_offset = scne_data_start_offset + scne_data_size
        for camera_entry_name in spa_file.camera_entries:
            # Get the camera data
            camera_entry_data = spa_file.camera_entries[camera_entry_name]

            # Write data
            # Update offset (only if there is data)
            if camera_entry_data.frame_count > 0:

                # Write frame data
                # Check if the data, the module of 16 is 0 before writing
                camera_data, camera_data_size, _ = check_entry_module(camera_data, camera_data_size, 16)

                camera_entry_data.frame_offset = camera_data_start_offset + camera_data_size
                for frame_data in camera_entry_data.frame_data:
                    camera_data = camera_data + struct.pack('>f', frame_data)
                    camera_data_size += 4

                # Write float data
                # Check if the data, the module of 16 is 0 before writing
                camera_data, camera_data_size, _ = check_entry_module(camera_data, camera_data_size, 16)

                camera_entry_data.float_offset = camera_data_start_offset + camera_data_size
                for float_data in camera_entry_data.float_data:
                    camera_data = camera_data + struct.pack('>f', float_data)
                    camera_data_size += 4
            else:
                camera_entry_data.frame_offset = 0
                camera_entry_data.float_offset = 0

        # Write string table
        string_table_start_offset = camera_data_start_offset + camera_data_size
        name = spa_file.spa_header.name + "." + spa_file.spa_header.extension
        string_table += name.encode('utf-8') + b'\x00'
        string_table_size += 1 + len(name)

        # Once the data is written, and we know the size of each data, we can create the spa entirely, We have to, again, loop all the bones, scnes and cameras
        # Write bones entries
        for bone_entry_name in spa_file.bone_entries:
            # Get the bone data
            bone_entry_data = spa_file.bone_entries[bone_entry_name]

            # Write each bone entry
            bone_entry += (string_table_start_offset + string_table_size).to_bytes(4, 'big')
            bone_entry += bone_entry_data.unk0x04
            bone_entry += bone_entry_data.translation_block_count.to_bytes(4, 'big')
            bone_entry += bone_entry_data.rotation_block_count.to_bytes(4, 'big')
            bone_entry += bone_entry_data.unknown_block_count.to_bytes(4, 'big')
            bone_entry += bone_entry_data.translation_frame_offset.to_bytes(4, 'big')
            bone_entry += bone_entry_data.rotation_frame_offset.to_bytes(4, 'big')
            bone_entry += bone_entry_data.unknown_frame_offset.to_bytes(4, 'big')
            bone_entry += bone_entry_data.translation_float_offset.to_bytes(4, 'big')
            bone_entry += bone_entry_data.rotation_float_offset.to_bytes(4, 'big')
            bone_entry += bone_entry_data.unknown_float_offset.to_bytes(4, 'big')
            bone_entry += bone_entry_data.unk0x2c

            # Write the name in the string table
            string_table += bone_entry_name.encode('utf-8') + b'\x00'
            string_table_size += len(bone_entry_name) + 1

        # Write scnes entries
        for scne_entry_name in spa_file.scne_entries:
            # Get the scne data
            scne_entry_data = spa_file.scne_entries[scne_entry_name]

            # Write each scne entry
            scne_entry += (string_table_start_offset + string_table_size).to_bytes(4, 'big')
            scne_entry += scne_entry_data.frame_count.to_bytes(4, 'big')
            scne_entry += scne_entry_data.frame_offset.to_bytes(4, 'big')
            scne_entry += scne_entry_data.float_offset.to_bytes(4, 'big')

            # Write the name in the string table
            string_table += scne_entry_name.encode('utf-8') + b'\x00'
            string_table_size += len(scne_entry_name) + 1

        # Write cameras entries
        for camera_entry_name in spa_file.camera_entries:
            # Get the camera data
            camera_entry_data = spa_file.camera_entries[camera_entry_name]

            # Write each scne entry
            camera_entry += (string_table_start_offset + string_table_size).to_bytes(4, 'big')
            camera_entry += camera_entry_data.frame_count.to_bytes(4, 'big')
            camera_entry += camera_entry_data.frame_offset.to_bytes(4, 'big')
            camera_entry += camera_entry_data.float_offset.to_bytes(4, 'big')

            # Write the name in the string table
            string_table += camera_entry_name.encode('utf-8') + b'\x00'
            string_table_size += len(camera_entry_name) + 1

        # Write finally the header
        header_data += spa_file.spa_header.unk0x00
        header_data += string_table_start_offset.to_bytes(4, 'big')
        header_data += spa_file.spa_header.unk0x08
        header_data += struct.pack('>f', spa_file.spa_header.frame_count)
        header_data += spa_file.spa_header.bone_count.to_bytes(4, 'big')
        header_data += bone_entry_offset.to_bytes(4, 'big')
        header_data += spa_file.spa_header.scene_nodes_count.to_bytes(4, 'big')
        header_data += scne_entry_offset.to_bytes(4, 'big')
        header_data += spa_file.spa_header.camera_count.to_bytes(4, 'big')
        header_data += camera_entry_offset.to_bytes(4, 'big')
        header_data += spa_file.spa_header.unk0x28
        header_data += spa_file.spa_header.unk0x2c
        header_size = 48

    return (header_data + bone_entry + scne_entry + camera_entry + bone_data + scne_data + camera_data + string_table), (header_size + bone_entry_size + scne_entry_size + camera_entry_size +
                                                                                                                         bone_data_size + scne_data_size + camera_data_size + string_table_size)


def read_json_bone_file(file_import_path):

    spa_file = SPAFile()
    # Open the json file
    with open(file_import_path, mode='r') as input_file:

        # Check if is a valid json file
        try:
            # return a json object
            data = json.load(input_file)

            # Read header
            spa_file.spa_header.unk0x00 = data['unk0x00'].to_bytes(4, 'big')
            name, extension = data['name'].split(".")
            spa_file.spa_header.name = name
            spa_file.spa_header.extension = extension
            spa_file.spa_header.unk0x08 = data['unk0x08'].to_bytes(4, 'big')
            spa_file.spa_header.frame_count = data['frame_count']
            spa_file.spa_header.unk0x28 = data['unk0x28'].to_bytes(4, 'big')
            spa_file.spa_header.unk0x2c = data['unk0x2c'].to_bytes(4, 'big')

            # Read each bone from json
            for bone_entry_json in data['bones']:

                # Count the number of bones in json file
                spa_file.spa_header.bone_count += 1

                # Create bone instance
                bone_entry = BoneEntry()

                bone_entry.name = bone_entry_json['name']

                # Meta data
                bone_entry.unk0x04 = bone_entry_json['unk0x04'].to_bytes(4, 'big')
                bone_entry.translation_block_count = bone_entry_json['translation_block_count']
                bone_entry.rotation_block_count = bone_entry_json['rotation_block_count']
                bone_entry.unknown_block_count = bone_entry_json['unknown_block_count']
                bone_entry.unk0x2c = bone_entry_json['unk0x2c'].to_bytes(4, 'big')

                # Data
                # Read translations
                for i in range(0, bone_entry.translation_block_count):
                    # Read frame
                    bone_entry.translation_frame_data.append(bone_entry_json['translation_frame_data'][i])

                    # Read float (x, y, z, w)
                    bone_entry.translation_float_data.append(bone_entry_json['translation_float_data'][i])

                # Read rotations
                for i in range(0, bone_entry.rotation_block_count):
                    # Read frame
                    bone_entry.rot_frame_data.append(bone_entry_json['rot_frame_data'][i])

                    # Read float
                    bone_entry.rot_float_data.append(bone_entry_json['rot_float_data'][i])

                # Read unknown
                for i in range(0, bone_entry.unknown_block_count):
                    # Read frame
                    bone_entry.unknown_frame_data.append(bone_entry_json['unknown_frame_data'][i])

                    # Read float (x, y, z, w)
                    bone_entry.unknown_float_data.append(bone_entry_json['unknown_float_data'][i])

                # Store everything in the dict
                spa_file.bone_entries[bone_entry.name] = bone_entry

            # Read each scne from json
            for scne_entry_json in data['scnes']:

                # Count the number of scnes in json file
                spa_file.spa_header.scene_nodes_count += 1

                # Create bone instance
                scne_entry = ScneEntry()

                scne_entry.name = scne_entry_json['name']

                # Meta data
                scne_entry.frame_count = scne_entry_json['frame_count']

                # Read scne data
                for i in range(0, scne_entry.frame_count):
                    # Read frame
                    scne_entry.frame_data.append(scne_entry_json['frame_data'][i])

                    # Read float
                    scne_entry.float_data.append(scne_entry_json['float_data'][i])

                # Store everything in the dict
                spa_file.scne_entries[scne_entry.name] = scne_entry

            # Read each camera from json
            for camera_entry_json in data['cameras']:

                # Count the number of cameras in json file
                spa_file.spa_header.camera_count += 1

                # Create bone instance
                camera_entry = CameraEntry()

                camera_entry.name = camera_entry_json['name']

                # Meta data
                camera_entry.frame_count = camera_entry_json['frame_count']

                # Read scne data
                for i in range(0, camera_entry.frame_count):
                    # Read frame
                    camera_entry.frame_data.append(camera_entry_json['frame_data'][i])

                    # Read float
                    camera_entry.float_data.append(camera_entry_json['float_data'][i])

                # Store everything in the dict
                spa_file.camera_entries[camera_entry.name] = camera_entry

        except UnicodeDecodeError:
            pass
        except json.decoder.JSONDecodeError:
            pass

        return spa_file


def write_json_bone_file(file_export_path, spa_header, bone_entries, scne_entries, camera_entries):

    header_text = ""
    scne_text = ""
    camera_text = ""
    bone_text = ""
    with open(file_export_path, mode='w') as output_file:

        # Header (before scne, camera and bone count)
        header_text += "\t\"unk0x00\": " + str(int.from_bytes(spa_header.unk0x00, "big")) + ",\n"
        header_text += "\t\"name\": \"" + spa_header.name + "." + spa_header.extension + "\",\n"
        header_text += "\t\"unk0x08\": " + str(int.from_bytes(spa_header.unk0x08, "big")) + ",\n"
        header_text += "\t\"frame_count\": " + str(spa_header.frame_count) + ",\n"

        # Bones
        bone_text += "\t\"bones\": \n\t\t\t[\n"
        for bone_entry_name in bone_entries:
            bone_entry_data = bone_entries[bone_entry_name]
            bone_text += "\t\t\t\t{"
            bone_text += "\"name\": " + "\"" + bone_entry_data.name + "\", "
            bone_text += "\"unk0x04\": " + str(int.from_bytes(bone_entry_data.unk0x04, "big")) + ", "
            bone_text += "\"translation_block_count\": " + str(bone_entry_data.translation_block_count) + ", "
            bone_text += "\"rotation_block_count\": " + str(bone_entry_data.rotation_block_count) + ", "
            bone_text += "\"unknown_block_count\": " + str(bone_entry_data.unknown_block_count) + ", "
            bone_text += "\"unk0x2c\": " + str(int.from_bytes(bone_entry_data.unk0x2c, "big")) + ",\n"

            bone_text += "\t\t\t\t\t\"translation_frame_data\": ["
            text_write = ""
            for translation_frame in bone_entry_data.translation_frame_data:
                text_write += str(translation_frame) + ", "
            bone_text += text_write[:-2]
            bone_text += "]" + ",\n"

            bone_text += "\t\t\t\t\t\"translation_float_data\": ["
            text_write = ""
            for translation_float in bone_entry_data.translation_float_data:
                text_write += "{\"x\": " + str(translation_float['x']) + ", " + "\"y\": " + str(translation_float['y']) + ", " + "\"z\": " + str(translation_float['z']) + ", " + \
                              "\"w\": " + str(translation_float['w']) + "}" + ", "
            bone_text += text_write[:-2]
            bone_text += "]" + ",\n"

            bone_text += "\t\t\t\t\t\"rot_frame_data\": ["
            text_write = ""
            for rot_frame in bone_entry_data.rot_frame_data:
                text_write += str(rot_frame) + ", "
            bone_text += text_write[:-2]
            bone_text += "]" + ",\n"

            bone_text += "\t\t\t\t\t\"rot_float_data\": ["
            text_write = ""
            for rot_float in bone_entry_data.rot_float_data:
                text_write += "{\"rot\": " + str(rot_float['rot']) + "}" + ", "
            bone_text += text_write[:-2]
            bone_text += "]" + ",\n"

            bone_text += "\t\t\t\t\t\"unknown_frame_data\": ["
            text_write = ""
            for unknown_frame in bone_entry_data.unknown_frame_data:
                text_write += str(unknown_frame) + ", "
            bone_text += text_write[:-2]
            bone_text += "]" + ",\n"

            bone_text += "\t\t\t\t\t\"unknown_float_data\": ["
            text_write = ""
            for unknown_float in bone_entry_data.unknown_float_data:
                text_write += "{\"x\": " + str(unknown_float['x']) + ", " + "\"y\": " + str(unknown_float['y']) + ", " + "\"z\": " + str(unknown_float['z']) + ", " + \
                              "\"w\": " + str(unknown_float['w']) + "}" + ", "
            bone_text += text_write[:-2]
            bone_text += "]"

            bone_text += "\n\t\t\t\t}" + "," + "\n"

        # If there is bones, we remove the last two chars
        if bone_entries:
            bone_text = bone_text[:-2] + "\n\t\t\t],\n"
        else:
            bone_text = bone_text + "\n\t\t\t],\n"

        # Scnes
        scne_text += "\t\"scnes\": \n\t\t\t[\n"
        for scne_entry_name in scne_entries:
            scne_entry_data = scne_entries[scne_entry_name]
            scne_text += "\t\t\t\t{"
            scne_text += "\"name\": " + "\"" + scne_entry_data.name + "\", "
            scne_text += "\"frame_count\": " + str(scne_entry_data.frame_count) + ",\n"

            scne_text += "\t\t\t\t\t\"frame_data\": ["
            text_write_frame = ""
            text_write_float = ""
            for i in range(0, scne_entry_data.frame_count):
                text_write_frame += str(scne_entry_data.frame_data[i]) + ", "
                text_write_float += str(scne_entry_data.float_data[i]) + ", "
            scne_text += text_write_frame[:-2]
            scne_text += "]" + ",\n"

            scne_text += "\t\t\t\t\t\"float_data\": ["
            scne_text += text_write_float[:-2]
            scne_text += "]"

            scne_text += "\n\t\t\t\t}" + "," + "\n"

        # If there is scnes, we remove the last two chars
        if scne_entries:
            scne_text = scne_text[:-2] + "\n\t\t\t],\n"
        else:
            scne_text = scne_text + "\n\t\t\t],\n"

        # Cameras
        camera_text += "\t\"cameras\": \n\t\t\t[\n"
        for camera_entry_name in camera_entries:
            camera_entry_data = camera_entries[camera_entry_name]
            camera_text += "\t\t\t\t{"
            camera_text += "\"name\": " + "\"" + camera_entry_data.name + "\", "
            camera_text += "\"frame_count\": " + str(camera_entry_data.frame_count) + ",\n"

            camera_text += "\t\t\t\t\t\"frame_data\": ["
            text_write_frame = ""
            text_write_float = ""
            for i in range(0, camera_entry_data.frame_count):
                text_write_frame += str(camera_entry_data.frame_data[i]) + ", "
                text_write_float += str(camera_entry_data.float_data[i]) + ", "
            camera_text += text_write_frame[:-2]
            camera_text += "]" + ",\n"

            camera_text += "\t\t\t\t\t\"float_data\": ["
            camera_text += text_write_float[:-2]
            camera_text += "]"

            camera_text += "\n\t\t\t\t}" + "," + "\n"

        # If there is cameras, we remove the last two chars
        if camera_entries:
            camera_text = camera_text[:-2] + "\n\t\t\t]\n"
        else:
            camera_text = camera_text + "\n\t\t\t]\n"

        # Rest of header (after scne, camera and bone count)
        header_text += "\t\"unk0x28\": " + str(int.from_bytes(spa_header.unk0x28, "big")) + ",\n"
        header_text += "\t\"unk0x2c\": " + str(int.from_bytes(spa_header.unk0x2c, "big")) + ",\n"

        # Write json
        output_file.write("{\n")
        output_file.write(header_text)
        output_file.write(bone_text)
        output_file.write(scne_text)
        output_file.write(camera_text)
        output_file.write("}")


def show_progress_value(worker, step_progress):

    i = worker.start_progress
    end_progress = i + step_progress

    # Calculate each step
    step_loop = (end_progress - i)

    # Show progress
    while i <= end_progress:
        worker.progressValue.emit(i)
        i += step_loop

    # Update start progress
    worker.start_progress = end_progress
