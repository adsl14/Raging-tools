# Swizzle Xbox 360 algorithm code taken from https://github.com/ascomods/game-assets-converter
# Credits to Banz99 and Ascomods

def xg_address_2d_tiled(axis, offset, width, texel_pitch):
    aligned_width = (width + 31) & ~31

    log_bpp = (texel_pitch >> 2) + ((texel_pitch >> 1) >> (texel_pitch >> 2))
    offset_b = offset << log_bpp
    offset_t = ((offset_b & ~4095) >> 3) + ((offset_b & 1792) >> 2) + (offset_b & 63)
    offset_m = offset_t >> (7 + log_bpp)

    if axis == 'x':
        macro_x = ((offset_m % (aligned_width >> 5)) << 2)
        tile = ((((offset_t >> (5 + log_bpp)) & 2) + (offset_b >> 6)) & 3)
        macro = (macro_x + tile) << 3
        micro = ((((offset_t >> 1) & ~15) + (offset_t & 15)) &
                 ((texel_pitch << 3) - 1)) >> log_bpp

        return macro + micro
    elif axis == 'y':
        macro_y = (int(offset_m / (aligned_width >> 5)) << 2)
        tile = ((offset_t >> (6 + log_bpp)) & 1) + (((offset_b & 2048) >> 10))
        macro = (macro_y + tile) << 3
        micro = ((((offset_t & (((texel_pitch << 6) - 1) & ~31)) +
                   ((offset_t & 15) << 1)) >> (3 + log_bpp)) & ~1)

        return macro + micro + ((offset_t & 16) >> 4)


def convert_linear_texture(data, direction, height, width, texture_type):
    # DXT1
    if texture_type == 8 or texture_type == 15:
        block_size = 4
        texel_pitch = 8
    # DXT3, DXT5 or ATI2
    elif texture_type == 24 or texture_type == 31 or texture_type == 32:
        block_size = 4
        texel_pitch = 16
    else:
        raise Exception('Unknown DXT type')

    block_width = int(width / block_size)
    block_height = int(height / block_size)

    new_data = bytearray(len(data))
    for j in range(block_height):
        for i in range(block_width):
            block_offset = j * block_width + i

            x = xg_address_2d_tiled('x', block_offset, block_width, texel_pitch)
            y = xg_address_2d_tiled('y', block_offset, block_width, texel_pitch)

            src_offset = j * block_width * texel_pitch + i * texel_pitch
            dest_offset = y * block_width * texel_pitch + x * texel_pitch

            if dest_offset < len(data):
                if direction == 'to':
                    new_data[dest_offset:dest_offset + texel_pitch] = \
                        data[src_offset:src_offset + texel_pitch]
                elif direction == 'from':
                    new_data[src_offset:src_offset + texel_pitch] = \
                        data[dest_offset:dest_offset + texel_pitch]

    return new_data


def handle_data(data, width, height, texture_type, action):
    direction = 'from' if (action == 'swizzle') else 'to'
    data = convert_linear_texture(data, direction, height, width, texture_type)

    for i in range(0, len(data), 4):
        # Swapping bytes
        a = data[i]
        data[i] = data[i + 1]
        data[i + 1] = a

        a = data[i + 2]
        data[i + 2] = data[i + 3]
        data[i + 3] = a

    return data


def process(data, width, height, mipmap_count, texture_type, action='unswizzle'):
    new_data = bytearray()
    current_width = width
    current_height = height
    current_mipmap_count = mipmap_count

    while current_mipmap_count > 0:
        if action == 'unswizzle' and current_width <= 64 and current_height <= 64:
            break
        # DXT1
        if texture_type == 8 or texture_type == 15:
            limit = len(new_data) + int(current_width * current_height / 2)
        else:
            limit = len(new_data) + (current_width * current_height)
        new_data.extend(handle_data(
            data[len(new_data):limit], current_width, current_height, texture_type, action))
        current_width = int(current_width / 2)
        current_height = int(current_height / 2)
        current_mipmap_count -= 1
    mipmap_count -= current_mipmap_count

    return mipmap_count, new_data
