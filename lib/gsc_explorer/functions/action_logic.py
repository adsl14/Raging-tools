from lib.gsc_explorer.GSCEV import GSCEV


def on_map_changed(main_window):

    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[0].pointers_data[0].value_GSDT = main_window.map_name_value.currentIndex()

def on_music_changed(main_window):

    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[0].pointers_data[1].value_GSDT = main_window.music_value.value()

def on_num_characters_changed(main_window):

    # Store the value from ui into the class
    GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3].data.pointers[1].pointers_data[7].value_GSDT = main_window.num_characters_value.value()
