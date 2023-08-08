from lib.vram_explorer.VEV import VEV


def change_endian(data):

    data = data.hex()
    new_data = ""
    for i in range(0, len(data), 8):
        new_data = new_data + data[i+6:i+8] + data[i+4:i+6] + data[i+2:i+4] + data[i:i+2]

    return bytes.fromhex(new_data)


def write_separator_vram(output_vram_file, data_entry):

    extra = output_vram_file.tell() % 16
    if extra > 0:
        for _ in range(0, extra):
            output_vram_file.write(b'\x00')

    # The texture is a square
    if data_entry.data_info.data.width == data_entry.data_info.data.height:
        if data_entry.data_info.data.dxt_encoding == 8:
            output_vram_file.write(VEV.vram_separator_80)
        # We check if the Mipmaps are greater than 1. If that's so, we write a separator
        elif data_entry.data_info.data.mip_maps > 1:
            output_vram_file.write(VEV.vram_separator_48)
    # The texture is not a square.
    # We check if the Mipmaps are greater than 1. If that's so, we write a separator
    elif data_entry.data_info.data.mip_maps > 1:
        # If the encoding is dxt1, we write a separator of 32 bytes
        if data_entry.data_info.data.dxt_encoding == 8:
            output_vram_file.write(VEV.vram_separator_32)
        # If the mipmaps are not 9 or height is not 256, we write a separator of 80 bytes
        elif data_entry.data_info.data.mip_maps != 9 or data_entry.data_info.data.height != 256:
            output_vram_file.write(VEV.vram_separator_80)
        else:
            output_vram_file.write(VEV.vram_separator_16)


def create_header(value):

    # 0x00 RGBA, 0x08 and 0x15 DXT1, 0x24, 0x31 and 0x39 (Zenkai Battle) as DXT5, 0x32 as ATI2 for XBOX or DXT5 for PS3
    if value == 8 or value == 15:
        return bytes.fromhex("04000000"), "DXT1".encode(), bytes.fromhex(
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
            "00 00 00 00 00 00 ".strip())
    elif value == 24 or value == 31 or value == 39:
        return bytes.fromhex("04000000"), "DXT5".encode(), bytes.fromhex(
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 10 00 00 00 00 00 00 00 00 00 00 00 00 "
            "00 00 00 00 00 00 ".strip())
    elif value == 32:
        # If is an XBOX SPR, we return the ATI2 encoding
        if VEV.header_type_spr_file == b'SPR3':
            return bytes.fromhex("04000000"), "ATI2".encode(), bytes.fromhex(
                "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 10 00 00 00 00 00 00 00 00 00 00 00 00 "
                "00 00 00 00 00 00 ".strip())
        # Means is a PS3 SPR, so we return DXT5
        else:
            return bytes.fromhex("04000000"), "DXT5".encode(), bytes.fromhex(
                "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 10 00 00 00 00 00 00 00 00 00 00 00 00 "
                "00 00 00 00 00 00 ".strip())


def get_encoding_name(value):

    # 0x00 RGBA, 0x08 and 0x15 DXT1, 0x24, 0x31 and 0x39 (Zenkai Battle) as DXT5, 0x32 as ATI2 for XBOX or DXT5 for PS3
    if value == 8 or value == 15:
        return "DXT1"
    elif value == 24 or value == 31 or value == 39:
        return "DXT5"
    elif value == 32:
        # If is an XBOX SPR, we return the ATI2 encoding
        if VEV.header_type_spr_file == b'SPR3':
            return "ATI2"
        # Means is a PS3 SP3, so we return DXT5
        else:
            return "DXT5"
    elif value == 0:
        return "RGBA"
    else:
        return "UNKNOWN"


def get_dxt_value(encoding_name):

    # 0x00 RGBA, 0x08 and 0x15 DXT1, 0x24 and 0x31 as DXT5, 0x32 as ATI2 for XBOX or DXT5 for PS3
    if encoding_name == "DXT1":
        return 8
    elif encoding_name == "DXT5":
        return 24
    elif encoding_name == "ATI2":
        return 32


def fix_bmp_header_data(header, data_extra, data_texture):

    # Check if the number of bytes of the data, the mod of 4 is 0, so always will have
    # blocks of four bytes. Doing this, we avoid to corrupt the file
    len_data = len(data_texture)
    mod_4 = len_data % 4
    if mod_4 != 0:
        len_data = len_data - mod_4
        data_texture = data_texture[:-mod_4]

    # Check if we have to modify the header due to some tools export some extra data
    if data_extra:
        header = header[:2] + (len_data + 54).to_bytes(4, byteorder="little") + header[6:10] + \
                 (54).to_bytes(4, byteorder="little") + (40).to_bytes(4, byteorder="little") + header[18:30] + \
                 (0).to_bytes(4, byteorder="little") + header[34:54]

    return len_data, header, data_texture


def check_name_is_string_table(current_index, scne_model, data_info_parent):

    found = False
    name_offset = 0
    data_info_child_2 = None
    for j in range(0, data_info_parent.child_count):
        # Avoid comparing the current child
        if current_index != j:
            # Get the child
            data_info_child_2 = data_info_parent.child_info[j]

            # Check if the parent name value of the current child, is already written
            # in the main name from other child
            if scne_model.parent_offset == data_info_child_2.name_offset:
                if data_info_child_2.name_offset_calculated:
                    found = True
                    name_offset = data_info_child_2.new_name_offset
                break

    return found, name_offset, data_info_child_2


# Get the new name offset of the texture by searching the original texture offset name
def search_texture(self, data, source_name_offset, num_textures):

    for i in range(0, num_textures):
        tx2d_data_entry = self.listView.model().item(i, 0).data()
        if tx2d_data_entry.data_info.name_offset == source_name_offset:
            data += tx2d_data_entry.data_info.new_name_offset.to_bytes(4, 'big')
            return True, data

    return False, data
