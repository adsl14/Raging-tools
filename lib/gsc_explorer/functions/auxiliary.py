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
    for i in range(number_of_pointers, len(pointers_values_ui)):
        # Enable the pointer value
        if pointers_values_ui[i].isEnabled:
            pointers_values_ui[i].setEnabled(False)


def get_pointer_data_info_name(event_instruction):

    # Function "0x01"
    if event_instruction.type == b'\x01':
        try:
            name = GSCEV.gsc_breakdown_json[str(event_instruction.secundary_number_of_pointers)]["Name"]
        except KeyError:
            name = "Function " + str(event_instruction.secundary_number_of_pointers)
    # Properties "0x08"
    else:
        '''
        try:
            name = "P: " + GSCEV.gsc_breakdown_json[str(event_instruction.number_of_pointers)]["Name"]
        except KeyError:
            name = "Property " + str(event_instruction.number_of_pointers.to_bytes(1, 'little'))[1:]
        '''
        name = "Property " + str(event_instruction.number_of_pointers.to_bytes(1, 'little'))[1:]

    return name


def write_parameters_in_html(list_of_parameters):

    parameters_html = ""
    for parameter in list_of_parameters:
        parameter_html = "\n" + "\t\t\t\t" + parameter["Name"] + " (" + parameter["Type"] + "). "
        parameter_html = parameter_html + parameter["Description"] + "\n"
        for value in parameter["Values"]:
            parameter_html = parameter_html + "\t\t\t\t<li>" + value["Description"] + " = "
            for one_posible_value in value["Value"]:
                parameter_html = parameter_html + str(one_posible_value) + ", "
            parameter_html = parameter_html[:-2] + "</li>\n"
        parameter_html = parameter_html[:-1] + "\n"
        parameters_html = parameters_html + "\t\t\t<dd>" + parameter_html + "\t\t\t</dd>\n"

    return parameters_html


def create_gsc_rb1_html_web(file_export_path, gsc_breakdown_json):

    functions_html = ""

    with open(file_export_path, mode='w') as outf:
        outf.write("<!DOCTYPE html>\n")
        outf.write("<html>\n")

        outf.write("\t<head>\n")

        outf.write("\t</head>\n")

        outf.write("\t<body>\n")
        outf.write("\t\t<h1 id=#FUNC-PROP>Functions and properties</h1>\n")

        # Function index
        outf.write("\t\t<h1 id=\"#FUNC\">Functions</h1>\n")
        outf.write("\t\t<ul>\n")
        for function_id in gsc_breakdown_json:
            outf.write("\t\t\t<li><a href=\"#FUNC_" + function_id + "\">" + gsc_breakdown_json[function_id]["Name"] + "</a></li>\n")
            functions_html = functions_html + "\t\t<h2 id=\"FUNC_" + function_id + "\">" + gsc_breakdown_json[function_id]["Name"] + "</h2>\n"
            functions_html = functions_html + "\t\t<dl>\n"

            functions_html = functions_html + "\t\t\t<dt>Hex interpretation</dt>\n"
            code_hex = "0x01" + '{:02x}'.format(len(gsc_breakdown_json[function_id]["Parameters"]))
            parameters_html = write_parameters_in_html(gsc_breakdown_json[function_id]["Parameters"])
            code_hex = code_hex + '{:02x}'.format(int(function_id)) + "00"
            functions_html = functions_html + "\t\t\t<dd><code>" + code_hex + "</code></dd>\n"

            functions_html = functions_html + "\t\t\t<dt>Description</dt>\n"
            functions_html = functions_html + "\t\t\t<dd>" + gsc_breakdown_json[function_id]["Description"] + "</dd>\n"

            functions_html = functions_html + "\t\t\t<dt>Parameters</dt>\n"
            if parameters_html == "":
                parameters_html = "\t\t\t<dd>None</dd>\n"
            functions_html = functions_html + parameters_html + "\t\t</dl>\n"

            properties_html = ""
            for properties in gsc_breakdown_json[function_id]["Properties"]:
                properties_html = properties_html + "\t\t\t<dt>" + properties["Name"] + " type (<code>" + "0x08" + properties["Name"].encode("utf-8").hex() + \
                                  '{:02x}'.format(len(properties["Parameters"])) + "00</code>)" + "</dt>\n"
                properties_html = properties_html + "\t\t\t<dd>"
                properties_html = properties_html + properties["Description"] + "</dd>\n"
                parameters_html = write_parameters_in_html(properties["Parameters"])
                properties_html = properties_html + parameters_html + "\t\t\t</dd>\n"
            if properties_html != "":
                functions_html = functions_html + "\t\t\t<h3>Properties</h3>\n"
                functions_html = functions_html + "\t\t<dl>\n"
                functions_html = functions_html + properties_html + "\t\t</dl>\n"
        outf.write("\t\t</ul>\n")

        # Write each function
        outf.write(functions_html)

        outf.write("\t</body>\n")
        outf.write("</html>\n")

