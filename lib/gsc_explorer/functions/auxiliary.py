def search_data_in_gsdt(gsdt_data_array, gsdt_data_array_size, pointer_data):
    index = None

    for i in range(0, gsdt_data_array_size):
        if gsdt_data_array[i] == pointer_data.value_GSDT:
            index = i
            break

    return index
