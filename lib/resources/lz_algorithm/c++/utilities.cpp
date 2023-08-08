#include "utilities.h"

void convert_int_to_byte_little_endian(int number, char* byte)
{
	byte[3] = (number >> 24) & 0xFF;
	byte[2] = (number >> 16) & 0xFF;
	byte[1] = (number >> 8) & 0xFF;
	byte[0] = number & 0xFF;
}

void convert_int_to_byte_big_endian(int number, char* byte)
{
	byte[0] = (number >> 24) & 0xFF;
	byte[1] = (number >> 16) & 0xFF;
	byte[2] = (number >> 8) & 0xFF;
	byte[3] = number & 0xFF;
}