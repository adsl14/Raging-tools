#ifndef LZ_COMPRESSION_H
#define LZ_COMPRESSION_H

class compression_settings
{
	public:
		int min_size, max_size, window_size, start_size;

		compression_settings(std::initializer_list<int> settings)
		{
			min_size = settings.begin()[0];
			max_size = settings.begin()[1];
			window_size = settings.begin()[2];
			start_size = settings.begin()[3];
		}
};

auto decompress_data(std::vector<uint8_t>& decomp, std::vector<uint8_t>& comp) -> void;
auto compress_data(std::vector<uint8_t>& comp, std::vector<uint8_t>& data, compression_settings& settings) -> void;
auto compress_data_full(std::vector<uint8_t>& comp, std::vector<uint8_t>& data, compression_settings& settings) -> void;
auto compress_dbrb_data(std::vector<uint8_t>& comp, std::vector<uint8_t>& data) -> void;

#endif