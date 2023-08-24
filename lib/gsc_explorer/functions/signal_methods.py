from lib.packages import os

from PyQt5.QtGui import QPixmap

from lib.gsc_explorer.GSCEV import GSCEV


def store_parameters_gsc_explorer(main_window):

    # Stage properties (GSAC3)
    gsac_3 = GSCEV.gsc_file.gscf_header.gscd_header.gsac_array[3]
    # Map value
    main_window.map_name_value.setCurrentIndex(gsac_3.data.pointers[0].pointers_data[0].value_GSDT)
    # Music value
    main_window.music_value.setValue(gsac_3.data.pointers[0].pointers_data[1].value_GSDT)

    # Number of characters value
    main_window.num_characters_value.setValue(gsac_3.data.pointers[1].pointers_data[7].value_GSDT)

    # Character id (select only the first one)
    main_window.character_value.setValue(1)
    # Skin (store in gui, only the first one)
    main_window.skin_value.setValue(gsac_3.data.pointers[5].pointers_data[3].value_GSDT)
    # Battle damaged (store in gui, only the first one)
    main_window.damaged_costume.setChecked(gsac_3.data.pointers[5].pointers_data[4].value_GSDT)
    # Health (store in gui, only the first one)
    main_window.gsc_health_value.setValue(gsac_3.data.pointers[5].pointers_data[7].value_GSDT)
    # Character (store in gui, only the first one)
    main_window.char_id_value.setPixmap(QPixmap(os.path.join(GSCEV.path_slot_small_images, "sc_chara_s_" + str(gsac_3.data.pointers[5].pointers_data[2].value_GSDT).zfill(3) + ".png")))

    # Open the tab (gsc explorer)
    if main_window.tabWidget.currentIndex() != 3:
        main_window.tabWidget.setCurrentIndex(3)
