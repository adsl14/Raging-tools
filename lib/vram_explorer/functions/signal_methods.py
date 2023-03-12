from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.functions.action_logic import action_material_val_changed, action_model_part_val_changed


def prepare_buttons_combobox_vram_explorer(main_window, basename):

    # Set the index of the list view to be always the first row when loading a new spr/vram file
    # We show always the first texture
    main_window.listView.setCurrentIndex(main_window.listView.model().index(0, 0))

    # Enable the buttons
    main_window.exportAllButton.setEnabled(True)
    main_window.importAllButton.setEnabled(True)
    main_window.importButton.setEnabled(True)
    main_window.exportButton.setEnabled(True)
    main_window.removeButton.setEnabled(True)
    main_window.addButton.setEnabled(True)

    # If the spr holds entries like pshd or vshd (used in maps), we won't enable the texture
    # adding, removing and the material edition
    if VEV.enable_spr_scratch:
        main_window.addButton.setEnabled(True)
        main_window.removeButton.setEnabled(True)
    else:
        main_window.addButton.setEnabled(False)
        main_window.removeButton.setEnabled(False)
        VEV.exists_mtrl = False

    # Enable the buttons of material only if the spr holds mtrl section
    if VEV.exists_mtrl:
        main_window.materialVal.setEnabled(True)
        main_window.layerVal.setEnabled(True)
        main_window.typeVal.setEnabled(True)
        main_window.effectVal.setEnabled(True)
        main_window.textureVal.setEnabled(True)
        main_window.exportMaterialButton.setEnabled(True)
        main_window.importMaterialButton.setEnabled(True)
        main_window.exportAllMaterialButton.setEnabled(True)
        main_window.importAllMaterialButton.setEnabled(True)
        main_window.addMaterialButton.setEnabled(True)
        main_window.removeMaterialButton.setEnabled(True)
        main_window.editMaterialChildrenButton.setEnabled(True)

        main_window.modelPartVal.setEnabled(True)
        main_window.materialModelPartVal.setEnabled(True)

        # Enable combo box and set the values for the first layer of the first material
        main_window.materialVal.setCurrentIndex(0)
        main_window.modelPartVal.setCurrentIndex(0)
        action_material_val_changed(main_window)
        action_model_part_val_changed(main_window)

    else:
        main_window.materialVal.setEnabled(False)
        main_window.layerVal.setEnabled(False)
        main_window.typeVal.setEnabled(False)
        main_window.effectVal.setEnabled(False)
        main_window.textureVal.setEnabled(False)
        main_window.exportMaterialButton.setEnabled(False)
        main_window.importMaterialButton.setEnabled(False)
        main_window.exportAllMaterialButton.setEnabled(False)
        main_window.importAllMaterialButton.setEnabled(False)
        main_window.addMaterialButton.setEnabled(False)
        main_window.removeMaterialButton.setEnabled(False)
        main_window.editMaterialChildrenButton.setEnabled(False)

        main_window.modelPartVal.setEnabled(False)
        main_window.materialModelPartVal.setEnabled(False)

    # Show the text labels
    main_window.fileNameText.setText(basename)
    main_window.fileNameText.setVisible(True)
    main_window.encodingImageText.setVisible(True)
    main_window.mipMapsImageText.setVisible(True)
    main_window.sizeImageText.setVisible(True)

    # Open the tab
    if main_window.tabWidget.currentIndex() != 0:
        main_window.tabWidget.setCurrentIndex(0)
