import sys, os
from lz_compression import decompress_data

def main():

    buffer = b''
    compressed_size = b''
    compressed_size_block = b''
    compressed_data_block = b''
    uncompressed_data = b''

    # The user needs to write the input and output file
    if len(sys.argv) < 3:
        print("Ussage:")
        print("\t dbrb_compressor.exe <input_file> <output_file>")
    else:
        with open(sys.argv[1], mode='rb') as input_file:
            # Read first four bytes
            buffer = input_file.read(4)
            
            # Compressed file
            if buffer == b'STPZ':
                # Move to the next entry
                input_file.seek(12, os.SEEK_CUR)

                # Read four bytes
                buffer = input_file.read(4)

                if buffer == b'0DCS':
                    # Read the size
                    input_file.seek(4, os.SEEK_CUR)
                    compressed_size = int.from_bytes(input_file.read(4), 'little') - 0x10

                    # Move to the next entry
                    input_file.seek(4, os.SEEK_CUR)

                    while input_file.tell() < compressed_size:

                        # Read four bytes
                        buffer = input_file.read(4)

                        uncompressed_data_block = b''
                        if buffer == b'0LCS':
                            # Read compressed size of the entry
                            input_file.seek(4, os.SEEK_CUR)
                            compressed_size_block = int.from_bytes(input_file.read(4), 'little') - 0x10

                            # Read data block
                            input_file.seek(4, os.SEEK_CUR)
                            compressed_data_block = input_file.read(compressed_size_block)

                            # Decompress data
                            uncompressed_data_block = decompress_data(compressed_data_block)

                        elif buffer == b'HLCS':

                            # Move to the sub-entry
                            input_file.seek(12, os.SEEK_CUR)

                            # Read four bytes
                            buffer = input_file.read(4)

                            if buffer == b'0HCS':

                                # Read compressed size of the entry
                                input_file.seek(4, os.SEEK_CUR)
                                compressed_size_block = int.from_bytes(input_file.read(4), 'little') - 0x10

                                # Read data block
                                input_file.seek(4, os.SEEK_CUR)
                                compressed_data_block = input_file.read(compressed_size_block)

                                # Decompress data (NOT WORKING FOR 0HCS entries)
                                uncompressed_data_block = decompress_data(compressed_data_block)

                        # Append the data block to the data we will write in the output
                        uncompressed_data += uncompressed_data_block

        # Write the output
        with open(sys.argv[2], mode="wb") as output_file:
            output_file.write(uncompressed_data)


if __name__ == "__main__":
    main()