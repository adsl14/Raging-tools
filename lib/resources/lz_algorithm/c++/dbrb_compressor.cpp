#include <iostream>
#include <string.h>
#include <fstream>
#include <sstream>
#include <vector>

#include "lz_compression.h"
#include "utilities.h"

int main(int argc, char** argv)
{

	char buffer_tag[5], buffer[5], input_block_size_buffer[4], compressed_byte_size[4], decompressed_byte_size[4];
	char buffer_data, stpk_header_info[3][4];
	int uncompressed_entry_size = 0, accumulated_uncompressed_entry_size = 0, compressed_entry_size = 0, accumulated_compressed_entry_size = 0;
	int uncompressed_sub_entry_size = 0, compressed_sub_entry_size = 0;
	int input_block_size = 0, input_file_size = 0, rest_block_size = 0, output_file_size = 0;
	int number_of_entries = 0;
	std::vector<uint8_t> input_buff_file, output_buff_file, compressed_buff_data;
	std::vector<int> block_sizes;

	// Endianess
	bool big_endian = false;

	// The user has to write the input and output file, the compression output is optional
	if (argc < 3)
	{
		std::cout << "Usage:" << std::endl;
		std::cout << "	dbrb_compressor <input file> <output file> (<output compression format>)" << std::endl << std::endl;
		std::cout << "-----------------------------------------" << std::endl;
		std::cout << "output compression format:" << std::endl;
		std::cout << "	-rb: RB and RB2 compression output (little endian). When compressing, if there is no option written, this one will be the default output format." << std::endl;
		std::cout << "	-ut: UT compression output (big endian). " << std::endl;
	}
	else 
	{
		// Open the input file
		std::ifstream file(argv[1], std::ios::in | std::ios::binary);

		// Read first four bytes
		file.read((char*) &buffer_tag[0], 4);

		// Compressed data
		if (strncmp(buffer_tag, "STPZ", 4) == 0)
		{
			// Open output file
			std::ofstream fileOutput(argv[2], std::ios::out | std::ios::binary);

			// Move to the the following entry
			file.seekg(12, std::ios::cur);

			// Read four bytes
			file.read((char*) &buffer_tag[0], 4);

			// Read each entry
			if (strncmp(buffer_tag, "0DCS", 4) == 0 || strncmp(buffer_tag, "SCD0", 4) == 0) 
			{
				// Read uncompressed size
				file.read((char*) &buffer[0], 4);

				// Bytes order
				if (buffer_tag[0] == '0')
				{
					uncompressed_entry_size = int((unsigned char)(buffer[3]) << 24 | 
						(unsigned char)(buffer[2]) << 16 | 
						(unsigned char)(buffer[1]) << 8 | 
						(unsigned char)(buffer[0]));
				} 
				else
				{
					uncompressed_entry_size = int((unsigned char)(buffer[0]) << 24 | 
						(unsigned char)(buffer[1]) << 16 | 
						(unsigned char)(buffer[2]) << 8 | 
						(unsigned char)(buffer[3]));
				}

				output_file_size += uncompressed_entry_size;
				accumulated_uncompressed_entry_size = 0;

				// Read compressed size
				file.read((char*) &buffer[0], 4);

				// Bytes order
				if (buffer_tag[0] == '0')
				{
					compressed_entry_size = int((unsigned char)(buffer[3]) << 24 | 
						(unsigned char)(buffer[2]) << 16 | 
						(unsigned char)(buffer[1]) << 8 | 
						(unsigned char)(buffer[0]));
				} 
				else
				{
					compressed_entry_size = int((unsigned char)(buffer[0]) << 24 | 
						(unsigned char)(buffer[1]) << 16 | 
						(unsigned char)(buffer[2]) << 8 | 
						(unsigned char)(buffer[3]));
				}

				// Prepare the entry buffer
				std::vector<uint8_t> decomp_buff_entry;
				decomp_buff_entry.reserve(uncompressed_entry_size/sizeof(uint8_t));

				// Move to the the following entry
				file.seekg(4, std::ios::cur);

				// Read each sub entry
				while(accumulated_uncompressed_entry_size < uncompressed_entry_size)
				{

					// Read four bytes
					file.read((char*) &buffer_tag[0], 4);

					// Read each sub entry
					if (strncmp(buffer_tag, "0LCS", 4) == 0 || strncmp(buffer_tag, "SCL0", 4) == 0) 
					{
						// Read uncompressed size
						file.read((char*) &buffer[0], 4);

						// Bytes order
						if (buffer_tag[0] == '0')
						{
							uncompressed_sub_entry_size = int((unsigned char)(buffer[3]) << 24 | 
								(unsigned char)(buffer[2]) << 16 | 
								(unsigned char)(buffer[1]) << 8 | 
								(unsigned char)(buffer[0]));
						} 
						else
						{
							uncompressed_sub_entry_size = int((unsigned char)(buffer[0]) << 24 | 
								(unsigned char)(buffer[1]) << 16 | 
								(unsigned char)(buffer[2]) << 8 | 
								(unsigned char)(buffer[3]));
						}
						accumulated_uncompressed_entry_size += uncompressed_sub_entry_size;

						// Read compressed size
						file.read((char*) &buffer[0], 4);

						// Bytes order
						if (buffer_tag[0] == '0')
						{
							compressed_sub_entry_size = int((unsigned char)(buffer[3]) << 24 | 
								(unsigned char)(buffer[2]) << 16 | 
								(unsigned char)(buffer[1]) << 8 | 
								(unsigned char)(buffer[0]));
						} 
						else
						{
							compressed_sub_entry_size = int((unsigned char)(buffer[0]) << 24 | 
								(unsigned char)(buffer[1]) << 16 | 
								(unsigned char)(buffer[2]) << 8 | 
								(unsigned char)(buffer[3]));
						}

						// Move to the data
						file.seekg(4, std::ios::cur);

						// Prepare the buffers
						std::vector<uint8_t> comp_buff_sub_entry;
						std::vector<uint8_t> decomp_buff_sub_entry;
						comp_buff_sub_entry.resize(compressed_sub_entry_size - 0x10/sizeof(uint8_t));
						decomp_buff_sub_entry.reserve(uncompressed_sub_entry_size/sizeof(uint8_t));

						// Read compressed data
						file.read((char*) comp_buff_sub_entry.data(), compressed_sub_entry_size - 0x10);

						// Decompress data
						decompress_data(decomp_buff_sub_entry, comp_buff_sub_entry);

						//Append to the entry data vector
						decomp_buff_entry.insert(std::end(decomp_buff_entry), std::begin(decomp_buff_sub_entry), std::end(decomp_buff_sub_entry));
					}

				}

				// Append to the main decomp buffer file, the entry
				output_buff_file.reserve(output_file_size/sizeof(uint8_t));
				output_buff_file.insert(std::end(output_buff_file), std::begin(decomp_buff_entry), std::end(decomp_buff_entry));
			}

			// Write output data
			fileOutput.write((char*) output_buff_file.data(), output_file_size);

			fileOutput.close();

		} else if (strncmp(buffer_tag, "STPK", 4) == 0)
		{
			// Check compression options
			if(argc > 3 && strncmp(argv[3], "-ut", 3) == 0)
			{
				big_endian = true;
			}

			// Open output file
			std::ofstream fileOutput(argv[2], std::ios::out | std::ios::binary);

			// Read STPK header data
			file.read((char*) &stpk_header_info[0], 4);
			file.read((char*) &stpk_header_info[1], 4);
			file.read((char*) &stpk_header_info[2], 4);

			// Get the size of the file
			file.seekg(0, std::ios::end);
			input_file_size = file.tellg();

			// Start the pointer at the beggining
			file.seekg(0, std::ios::beg);

			// We will compress the data in batches (RB uses 15360 apparently)
			input_block_size = 15360;

			// prepare the buffer size
			input_buff_file.reserve(input_block_size/sizeof(uint8_t));

			// Get the number of entries and size of each block entry
			number_of_entries = (int) input_file_size / input_block_size;
			rest_block_size = input_file_size - (input_block_size * number_of_entries);
			if (rest_block_size > 0)
			{
				number_of_entries++;
			} 
			else
			{
				rest_block_size = input_block_size;
			}

			// Prepare the array of block sizes
			block_sizes.reserve(number_of_entries/sizeof(int));
			for(int i = 0; i < number_of_entries - 1; ++i)
			{
				block_sizes.push_back(input_block_size);
			}
			block_sizes.push_back(rest_block_size);

			// We create the array where we will store all the data in order to write the output
			std::vector<uint8_t> comp_buff_entry, comp_buff_sub_entry;

			// Read all the file
			for(int block_size : block_sizes)
			{
				// Read decompressed data
				input_buff_file.resize(block_size/sizeof(uint8_t));
				file.read((char*) input_buff_file.data(), block_size);

				// Compress the block of data
				compressed_buff_data.resize(0);
				compress_dbrb_data(compressed_buff_data, input_buff_file);

				// Write the SCL0 (0LCS) header + data
				compressed_entry_size = 16 + compressed_buff_data.size();
				accumulated_compressed_entry_size += compressed_entry_size;
				if (big_endian)
				{
					comp_buff_sub_entry.insert(std::end(comp_buff_sub_entry), {'S','C','L','0'});
					convert_int_to_byte_big_endian(block_size, decompressed_byte_size);
					convert_int_to_byte_big_endian(compressed_entry_size, compressed_byte_size);
				} 
				else 
				{
					comp_buff_sub_entry.insert(std::end(comp_buff_sub_entry), {'0','L','C','S'});
					convert_int_to_byte_little_endian(block_size, decompressed_byte_size);
					convert_int_to_byte_little_endian(compressed_entry_size, compressed_byte_size);
				}

				// Store the size of decompressed data
				comp_buff_sub_entry.insert(std::end(comp_buff_sub_entry), std::begin(decompressed_byte_size), std::end(decompressed_byte_size));
				// Store the size of compressed data
				comp_buff_sub_entry.insert(std::end(comp_buff_sub_entry), std::begin(compressed_byte_size), std::end(compressed_byte_size));
				// Store unknown data (max uncompressed block size?)
				comp_buff_sub_entry.insert(std::end(comp_buff_sub_entry), {0x00, 0x00, 0x00, 0x00});
				// Store the compressed data
				comp_buff_sub_entry.insert(std::end(comp_buff_sub_entry), std::begin(compressed_buff_data), std::end(compressed_buff_data));
			}

			// Write the SCD0 (0DCS) header
			accumulated_compressed_entry_size += 16;
			if (big_endian)
			{
				comp_buff_entry.insert(std::end(comp_buff_entry), {'S','C','D','0'});
				convert_int_to_byte_big_endian(input_file_size, decompressed_byte_size);
				convert_int_to_byte_big_endian(accumulated_compressed_entry_size, compressed_byte_size);
				convert_int_to_byte_big_endian(input_block_size, input_block_size_buffer);
			} 
			else 
			{
				comp_buff_entry.insert(std::end(comp_buff_entry), {'0','D','C','S'});
				convert_int_to_byte_little_endian(input_file_size, decompressed_byte_size);
				convert_int_to_byte_little_endian(accumulated_compressed_entry_size, compressed_byte_size);
				convert_int_to_byte_little_endian(input_block_size, input_block_size_buffer);
			}
			// Store the size of decompressed data
			comp_buff_entry.insert(std::end(comp_buff_entry), std::begin(decompressed_byte_size), std::end(decompressed_byte_size));
			// Store the size of compressed data
			comp_buff_entry.insert(std::end(comp_buff_entry), std::begin(compressed_byte_size), std::end(compressed_byte_size));
			// Store unknown data (max uncompressed block size?)
			comp_buff_entry.insert(std::end(comp_buff_entry), std::begin(input_block_size_buffer), std::end(input_block_size_buffer));

			// Store the sub-entries, inside the main entry
			comp_buff_entry.insert(std::end(comp_buff_entry), std::begin(comp_buff_sub_entry), std::end(comp_buff_sub_entry));

			// Store the STPZ tag in the output buff file
			output_buff_file.insert(std::end(output_buff_file), {'S','T','P','Z'});
			output_buff_file.insert(std::end(output_buff_file), std::begin(stpk_header_info[0]), std::end(stpk_header_info[0]));
			output_buff_file.insert(std::end(output_buff_file), std::begin(stpk_header_info[1]), std::end(stpk_header_info[1]));
			output_buff_file.insert(std::end(output_buff_file), std::begin(stpk_header_info[2]), std::end(stpk_header_info[2]));

			// Store the entry in the output buff file
			output_buff_file.insert(std::end(output_buff_file), std::begin(comp_buff_entry), std::end(comp_buff_entry));

			// Write the output
			fileOutput.write((char*) output_buff_file.data(), output_buff_file.size());

			// Close output
			fileOutput.close();
		}

		// Close file input
		file.close();
	}

	return 0;
}