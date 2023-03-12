import os

from lib.pak_explorer.PEV import PEV


def enable_pack_explorer_assign_title(pak_explorer, file_name_text_2):
    # Enable the pak explorer
    pak_explorer.setEnabled(True)
    # Add the title
    file_name_text_2.setText(os.path.basename(PEV.pak_file_path_original))


def assign_first_entry_file(list_view):
    list_view.setCurrentIndex(list_view.model().index(0, 0))


def enable_pak_explorer_tab(main_window):

    # Open the tab (pak explorer)
    if main_window.tabWidget.currentIndex() != 1:
        main_window.tabWidget.setCurrentIndex(1)

    # Disable completely the tab character parameters editor
    if main_window.character_parameters_editor.isEnabled():
        main_window.character_parameters_editor.setEnabled(False)
