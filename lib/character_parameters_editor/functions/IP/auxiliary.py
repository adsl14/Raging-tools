from lib.character_parameters_editor.IPV import IPV


def read_transformation_effect(main_window, animation):

    # Get each four bytes
    for i in range(0, animation.size, 4):
        data = animation.data[i:i+4]

        # If we found the bytes that identify if is a proper trans effect file, we store where is located
        # the background color
        if data == IPV.trans_effect_identification_file:
            # Enable combo box
            main_window.background_color_trans_value.setEnabled(True)
            # Store the data
            IPV.trans_effect_position_byte = i-1
            main_window.background_color_trans_value.setCurrentIndex(main_window.background_color_trans_value.findData
                                                                     (animation.data[i-1]))
            return

    # If we didn't find the bytes that identify if is a proper trans effect file, we disable the combo box
    main_window.background_color_trans_value.setEnabled(False)
