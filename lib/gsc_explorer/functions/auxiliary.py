from lib.packages import struct

from lib.gsc_explorer.GSCEV import GSCEV
from lib.gsc_explorer.classes.GSAC.PointerData import PointerData
from lib.gsc_explorer.classes.GSAC.PointerDataInfo import PointerDataInfo


def search_data_in_gsdt(gsdt_data_array, gsdt_data_array_size, pointer_data):
    index = None

    # Check if we can find the value with the same instance (integer or float)
    for i in range(0, gsdt_data_array_size):
        if gsdt_data_array[i] == pointer_data.value_GSDT and isinstance(gsdt_data_array[i], type(pointer_data.value_GSDT)):
            index = i
            break

    return index


def read_pointer_data_info(file, number_of_bytes_data_readed, start_data_index, pointers):

    pointer_data_info = PointerDataInfo()
    pointer_data_info.type = file.read(1)
    pointer_data_info.number_of_pointers = int.from_bytes(file.read(1), "little")
    pointer_data_info.secundary_number_of_pointers = int.from_bytes(file.read(1), "little")
    pointer_data_info.unk0x04 = file.read(1)
    number_of_bytes_data_readed += 4

    # Load each pointer_data inside the pointer_data_info (only the ones that are a pointer)
    if pointer_data_info.type != b'\x00':

        # Pointers that are not 08 in their first byte, means the number of pointers_data is in the second byte
        if pointer_data_info.type != b'\x08':
            for i in range(0, pointer_data_info.number_of_pointers):
                # Read value
                aux_pointer = file.tell()
                pointer_data = PointerData()
                pointer_data.type_GSDT = file.read(1)
                block_gstd_index = int.from_bytes(file.read(2), 'little')
                pointer_data.unk0x03 = file.read(1)
                file.seek(start_data_index + (block_gstd_index * 4))
                # Check if the data we're reading is an integer or float
                if pointer_data.type_GSDT == b'\x0A':
                    pointer_data.value_GSDT = int.from_bytes(file.read(GSCEV.bytes2Read), "little")
                else:
                    pointer_data.value_GSDT = struct.unpack('<f', file.read(GSCEV.bytes2Read))[0]
                file.seek(aux_pointer + 4)

                # Increase number of bytes readed inside the gsac_data
                number_of_bytes_data_readed += 4

                # Append each pointer data into the pointer data info
                pointer_data_info.pointers_data.append(pointer_data)

        # Pointers that are 08 in their first byte, means the number of pointers_data is in the third byte
        elif pointer_data_info.type == b'\x08':
            for i in range(0, pointer_data_info.secundary_number_of_pointers):
                # Read value
                aux_pointer = file.tell()
                pointer_data = PointerData()
                pointer_data.type_GSDT = file.read(1)
                block_gstd_index = int.from_bytes(file.read(2), 'little')
                pointer_data.unk0x03 = file.read(1)
                file.seek(start_data_index + (block_gstd_index * 4))
                # Check if the data we're reading is an integer or float
                if pointer_data.type_GSDT == b'\x0A':
                    pointer_data.value_GSDT = int.from_bytes(file.read(GSCEV.bytes2Read), "little")
                else:
                    pointer_data.value_GSDT = struct.unpack('<f', file.read(GSCEV.bytes2Read))[0]
                file.seek(aux_pointer + 4)

                # Increase number of bytes readed inside the gsac_data
                number_of_bytes_data_readed += 4

                # Append each pointer data into the pointer data info
                pointer_data_info.pointers_data.append(pointer_data)

        # Append each pointer data info into the entry (gshd or gsac)
        pointers.append(pointer_data_info)

    return number_of_bytes_data_readed


def write_pointer_data_info(pointer_data_info, data, data_size, gsdt_data, gsdt_data_size, gsdt_data_array, gsdt_data_array_size):

    # Store the pointer_data_info
    if pointer_data_info.type != b'\x00':
        # Store the pointer data info in the gsac_data byte
        data += pointer_data_info.type + pointer_data_info.number_of_pointers.to_bytes(1, 'little') + pointer_data_info.secundary_number_of_pointers.to_bytes(1, 'little') + \
                     pointer_data_info.unk0x04
        data_size += 4

    # Store the pointer_data
    for pointer_data in pointer_data_info.pointers_data:

        # Search if the value is in the gsdt array
        index = search_data_in_gsdt(gsdt_data_array, gsdt_data_array_size, pointer_data)

        # We didn't find the value in the gsdt array
        if index is None:
            gsdt_data_array.append(pointer_data.value_GSDT)
            index = gsdt_data_array_size
            gsdt_data_array_size += 1

            # Store the gsdt data value
            # Integer value
            if pointer_data.type_GSDT == b'\x0A':
                value_gsdt = pointer_data.value_GSDT.to_bytes(4, 'little')
            else:
                value_gsdt = struct.pack('<f', pointer_data.value_GSDT)
            gsdt_data += value_gsdt
            gsdt_data_size += 4

        # Store the pointer data in the gsac_data byte
        data += pointer_data.type_GSDT + index.to_bytes(2, 'little') + pointer_data.unk0x03
        data_size += 4

    return data, data_size, gsdt_data, gsdt_data_size, gsdt_data_array_size


def create_pointer_data_info(type, number_of_pointers, secundary_number_of_pointers, unk0x04, pointers_data_values):

    pointer_data_info = PointerDataInfo()
    pointer_data_info.type = type
    pointer_data_info.number_of_pointers = number_of_pointers
    pointer_data_info.secundary_number_of_pointers = secundary_number_of_pointers
    pointer_data_info.unk0x04 = unk0x04

    for i in range(0, len(pointers_data_values)):
        pointer_data_info.pointers_data.append(create_pointer_data(pointers_data_values[i][0], pointers_data_values[i][1], pointers_data_values[i][2]))

    return pointer_data_info


def create_pointer_data(type_GSDT, value_GSDT, unk0x03):

    pointer_data = PointerData()
    pointer_data.type_GSDT = type_GSDT
    pointer_data.value_GSDT = value_GSDT
    pointer_data.unk0x03 = unk0x03

    return pointer_data


def assign_pointer_to_ui(pointers_values_ui, pointer_data_info, number_of_pointers):

    for i in range(0, number_of_pointers):
        # Enable the pointer value ui
        if not pointers_values_ui[i].isEnabled():
            pointers_values_ui[i].setEnabled(True)

        # Check if the pointer is an integer, so we change the number of decimals and minimun value
        if pointer_data_info.pointers_data[i].type_GSDT == b'\x0A':
            pointers_values_ui[i].setDecimals(0)
            pointers_values_ui[i].setMinimum(0.0)
        else:
            pointers_values_ui[i].setDecimals(2)
            pointers_values_ui[i].setMinimum(-4294967295.000000)
        pointers_values_ui[i].setValue(pointer_data_info.pointers_data[i].value_GSDT)
    # Disable the rest of pointer values in ui
    for i in range(number_of_pointers, 8):
        # Enable the pointer value
        if pointers_values_ui[i].isEnabled:
            pointers_values_ui[i].setEnabled(False)


def get_pointer_data_info_name(event_instruction):

    name = str(event_instruction.type.hex()) + ' ' + "%02X" % event_instruction.number_of_pointers + ' ' + "%02X" % event_instruction.secundary_number_of_pointers + ' ' + \
           str(event_instruction.unk0x04.hex())

    # Function "0x01"
    if event_instruction.type == b'\x01':
        try:
            name = "F: " + GSCEV.instructions_names[0]["%02X" % event_instruction.secundary_number_of_pointers]
        except KeyError:
            pass
    # Properties "0x08"
    else:
        try:
            name = "P: " + GSCEV.instructions_names[1]["%02X" % event_instruction.number_of_pointers]
        except KeyError:
            pass

    return name

