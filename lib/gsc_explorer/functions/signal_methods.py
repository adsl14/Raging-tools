def enable_gsc_explorer_tab(main_window):

    # Open the tab (pak explorer)
    if main_window.tabWidget.currentIndex() != 3:
        main_window.tabWidget.setCurrentIndex(3)
