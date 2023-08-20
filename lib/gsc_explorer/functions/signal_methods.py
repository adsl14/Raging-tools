from lib.gsc_explorer.GSCEV import GSCEV


def store_parameters_gsc_explorer(main_window):

    # Stage properties
    gsac_3 = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3]
    # Map value
    main_window.map_name_value.setCurrentIndex(gsac_3.data.pointers[0].pointers_data[0].value_GSDT)

    # Open the tab (gsc explorer)
    if main_window.tabWidget.currentIndex() != 3:
        main_window.tabWidget.setCurrentIndex(3)
