#include <cstdint>
#include <vector>
#include <algorithm>
#include <iterator>

#include "lz_compression.h"

#define PROCESS_FORWARD 0

auto decompress_data(std::vector<uint8_t>& decomp, std::vector<uint8_t>& comp) -> void
{
    auto pos = 0;
    while (pos < comp.size())
    {
        auto value = comp[pos++];
        auto size = value >> 1;

        if (value & 1)
        {
            auto offset = decomp.size() - comp[pos++];
            while (size > 0)
            {
                --size;
                decomp.emplace_back(decomp[offset++]);
            }
        }
        else
        {
            while (size > 0)
            {
                --size;
                decomp.emplace_back(comp[pos++]);
            }
        }
    }
}

auto compress_data(std::vector<uint8_t>& comp, std::vector<uint8_t>& data, compression_settings& settings) -> void
{
    auto min_size = settings.min_size;
    auto max_size = settings.max_size;
    auto window_size = settings.window_size;

    auto length = static_cast<uint32_t>(data.size());
    auto pos = std::min<int>(settings.start_size, length);
    auto start = 0;
    auto size = pos;

    auto markers = std::vector<std::pair<int, int>>();

    while (pos < length)
    {
        auto prev = pos - 1;

        auto prev_max = prev;
        auto size_max = 0;
        while (prev >= 0 && prev >= pos - window_size)
        {
            auto pos_curr = pos;
            auto prev_curr = prev;
            auto size_curr = 0;
            while (pos_curr < length && size_curr < max_size)
            {
                if (data[prev_curr] != data[pos_curr])
                    break;

                pos_curr++;
                prev_curr++;
                size_curr++;
            }

            if (size_curr > size_max)
            {
                prev_max = prev;
                size_max = size_curr;
            }
            if (size_curr >= max_size || pos_curr >= length)
            {
                break;
            }

            --prev;
        }

        if (size_max >= min_size)
        {
            if (size > 0)
            {
                markers.emplace_back(std::pair<int, int>{ start, size });
            }

            auto offset = prev_max - pos;

            markers.emplace_back(std::pair<int, int>{ offset, size_max });

            start = pos += size_max;
            size = 0;
        }
        else
        {
            pos++;
            size++;

            if (size > 0 && size >= max_size)
            {
                markers.emplace_back(std::pair<int, int>{ start, size });
                start = pos;
                size = 0;
            }
        }
    }
    if (size > 0)
    {
        markers.emplace_back(std::pair<int, int>{ start, size });
        size = 0;
    }

    for (auto& marker : markers)
    {
        auto pos = marker.first;
        auto size = marker.second;

        auto value = size << 1;

        if (pos < 0)
        {
            value |= 1;
            comp.emplace_back(value);
            comp.emplace_back(-pos);
        }
        else
        {
            comp.emplace_back(value);
            std::copy_n(data.begin() + pos, size, std::back_inserter(comp));
        }
    }
}

auto compress_data_full(std::vector<uint8_t>& comp, std::vector<uint8_t>& data, compression_settings& settings) -> void
{
    auto min_size = settings.min_size;
    auto max_size = settings.max_size;
    auto window_size = settings.window_size;

    auto length = static_cast<uint32_t>(data.size());
    auto pos = std::min<int>(settings.start_size, length);
    auto start = 0;
    auto size = pos;

    auto markers = std::vector<std::pair<int, int>>();

    while (pos < length)
    {
#if PROCESS_FORWARD
        auto prev = pos - window_size;
        if (prev < 0)
            prev = 0;
#else
        auto prev = pos - 1;
#endif

        /*if (prev >= pos)
        {
            pos++;
            size++;

            if (size > 0 && size >= max_size)
            {
                markers.emplace_back(std::pair<int, int>{ start, size });
                start = pos;
                size = 0;
            }
            continue;
        }*/

        auto prev_max = prev;
        auto size_max = 0;
#if PROCESS_FORWARD
        while (prev < pos && prev < length)
#else
        while (prev >= 0 && prev >= pos - window_size)
#endif
        {
            auto pos_curr = pos;
            auto prev_curr = prev;
            auto size_curr = 0;
            while (pos_curr < length && size_curr < max_size)
            {
                if (data[prev_curr] != data[pos_curr])
                    break;

                pos_curr++;
                prev_curr++;
                size_curr++;
            }

            if (size_curr > size_max)
            {
                prev_max = prev;
                size_max = size_curr;
            }
            if (size_curr >= max_size || pos_curr >= length)
            {
                break;
            }

#if PROCESS_FORWARD
            ++prev;
#else
            --prev;
#endif
        }

        if (size_max > min_size)
        {
            if (size > 0)
            {
                markers.emplace_back(std::pair<int, int>{ start, size });
            }

            auto offset = prev_max - pos;

            markers.emplace_back(std::pair<int, int>{ offset, size_max });

            start = pos += size_max;
            size = 0;
        }
        else
        {
            pos++;
            size++;

            if (size > 0 && size >= max_size)
            {
                markers.emplace_back(std::pair<int, int>{ start, size });
                start = pos;
                size = 0;
            }
        }
    }
    if (size > 0)
    {
        markers.emplace_back(std::pair<int, int>{ start, size });
        size = 0;
    }

    for (auto& marker : markers)
    {
        auto pos = marker.first;
        auto size = marker.second;

        auto value = size << 1;

        if (pos < 0)
        {
            value |= 1;
            comp.emplace_back(value);
            comp.emplace_back(-pos);
        }
        else
        {
            comp.emplace_back(value);
            std::copy_n(data.begin() + pos, size, std::back_inserter(comp));
        }
    }
}

auto compress_dbrb_data(std::vector<uint8_t>& comp, std::vector<uint8_t>& data) -> void
{
    auto min_size = 3;
    auto max_size = 127;
    auto window_size = 255;
    auto start_size = 0;
    auto settings = compression_settings({ min_size, max_size, window_size, start_size });

    compress_data(comp, data, settings);
}
