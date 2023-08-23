from PyQt5.QtWidgets import QMainWindow

from lib.functions import show_progress_value, check_entry_module
from lib.gsc_explorer.classes.GSAC.GSACData import GsacData
from lib.gsc_explorer.classes.GSAC.GSACHeader import GsacHeader
from lib.gsc_explorer.classes.GSCD.GSCDHeader import GscdHeader
from lib.gsc_explorer.classes.GSCF.GSCFHeader import GscfHeader
from lib.gsc_explorer.classes.GSDT.GSDTHeader import GsdtHeader
from lib.gsc_explorer.classes.GSHD.GSHDData import GshdData
from lib.gsc_explorer.classes.GSHD.GSHDHeader import GshdHeader
from lib.gsc_explorer.functions.action_logic import on_map_changed, on_music_changed, on_num_characters_changed
from lib.gsc_explorer.functions.auxiliary import read_pointer_data_info, write_pointer_data_info, create_pointer_data_info
from lib.packages import os

from PyQt5.QtCore import QObject, pyqtSignal

from lib.gsc_explorer.GSCEV import GSCEV


class WorkerGscef(QObject):

    # Signals
    finished = pyqtSignal()
    progressValue = pyqtSignal(float)
    progressText = pyqtSignal(str)
    store_parameters_gsc_explorer = pyqtSignal(QMainWindow)

    # Vars
    main_window = None
    start_progress = 0.0
    end_progress = 100.0
    gsc_file_path = ""

    def load_gsc_file(self):

        # Open gsc file (1 task)
        step_progress = self.end_progress
        open_gsc_file(self, step_progress, self.gsc_file_path)

        # Store parameters loaded in gsc tab
        self.store_parameters_gsc_explorer.emit(self.main_window)

        # Finish the thread
        self.finished.emit()

    def save_gsc_file(self):

        # Save gsc file (1 task)
        step_progress = self.end_progress
        save_gsc_file(self, step_progress, self.gsc_file_path)

        # Finish the thread
        self.finished.emit()


def initialize_gsce(main_window):

    # Initialize the gscfile class
    # gscf
    gscf_header = GscfHeader()
    gscf_header.unk0x04 = b'\x10\x00\x00\x00'
    gscf_header.unk0x0c = b'\x01\x00\x00\x00'

    # gshd
    gshd_header = GshdHeader()
    gshd_header.unk0x04 = b'\x10\x00\x00\x00'
    gshd_header.unk0x0c = b'\x00\x00\x00\x00'
    gshd_data = GshdData()
    gshd_data.pointers.append(create_pointer_data_info(b'\x03', 0, 0, b'\x00', []))
    gshd_data.pointers.append(create_pointer_data_info(b'\x03', 0, 0, b'\x00', []))
    gshd_header.data = gshd_data

    # gscd
    gscd_header = GscdHeader()
    gscd_header.unk0x04 = b'\x10\x00\x00\x00'
    gscd_header.unk0x0c = b'\x01\x00\x00\x00'
    # GSAC 0
    gsac_header = GsacHeader()
    gsac_header.unk0x04 = b'\x10\x00\x00\x00'
    gsac_header.id = 4294967295
    gsac_data = GsacData()
    gsac_data.pointers.append(create_pointer_data_info(b'\x02', 0, 16, b'\x27', []))
    gsac_header.data = gsac_data
    gscd_header.gsac_array.append(gsac_header)
    # GSAC 1
    gsac_header = GsacHeader()
    gsac_header.unk0x04 = b'\x10\x00\x00\x00'
    gsac_header.id = 1000
    gsac_data = GsacData()
    gsac_data.pointers.append(create_pointer_data_info(b'\x02', 0, 254, b'\xFF', []))
    gsac_data.pointers.append(create_pointer_data_info(b'\x02', 0, 253, b'\xFF', []))
    gsac_data.pointers.append(create_pointer_data_info(b'\x02', 0, 252, b'\xFF', []))
    gsac_header.data = gsac_data
    gscd_header.gsac_array.append(gsac_header)
    # GSAC 2
    gsac_header = GsacHeader()
    gsac_header.unk0x04 = b'\x10\x00\x00\x00'
    gsac_header.id = 4294967294
    gsac_data = GsacData()
    gsac_data.pointers.append(create_pointer_data_info(b'\x01', 1, 0, b'\x00', [[b'\x0A', 32, b'\x00']]))
    gsac_data.pointers.append(create_pointer_data_info(b'\x01', 3, 15, b'\x00', [[b'\x0A', 1000, b'\x00'], [b'\x0A', 1500, b'\x00'], [b'\x0A', 2000, b'\x00']]))
    gsac_data.pointers.append(create_pointer_data_info(b'\x01', 3, 16, b'\x00', [[b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00']]))
    gsac_data.pointers.append(create_pointer_data_info(b'\x01', 3, 17, b'\x00', [[b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00']]))
    gsac_data.pointers.append(create_pointer_data_info(b'\x01', 3, 18, b'\x00', [[b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00']]))
    gsac_data.pointers.append(create_pointer_data_info(b'\x01', 3, 19, b'\x00', [[b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00']]))
    gsac_data.pointers.append(create_pointer_data_info(b'\x01', 0, 20, b'\x00', []))
    gsac_data.pointers.append(create_pointer_data_info(b'\x08', 111, 2, b'\x00', [[b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00']]))
    gsac_data.pointers.append(create_pointer_data_info(b'\x08', 111, 2, b'\x00', [[b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00']]))
    gsac_data.pointers.append(create_pointer_data_info(b'\x08', 111, 2, b'\x00', [[b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00']]))
    gsac_data.pointers.append(create_pointer_data_info(b'\x01', 3, 21, b'\x00', [[b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00']]))
    gsac_header.data = gsac_data
    gscd_header.gsac_array.append(gsac_header)
    # GSAC 3
    gsac_header = GsacHeader()
    gsac_header.unk0x04 = b'\x10\x00\x00\x00'
    gsac_header.id = 4294967293
    gsac_data = GsacData()
    gsac_data.pointers.append(create_pointer_data_info(b'\x01', 3, 8, b'\x00', [[b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00']]))
    gsac_data.pointers.append(create_pointer_data_info(b'\x01', 12, 9, b'\x00', [[b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00'],
                                                                                 [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00'],
                                                                                 [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00']]))
    gsac_data.pointers.append(create_pointer_data_info(b'\x01', 0, 10, b'\x00', []))
    gsac_data.pointers.append(create_pointer_data_info(b'\x08', 101, 3, b'\x00', [[b'\x0A', 4294967295, b'\x00'], [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00']]))
    gsac_data.pointers.append(create_pointer_data_info(b'\x08', 101, 3, b'\x00', [[b'\x0A', 4294967295, b'\x00'], [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00']]))
    for i in range(1, 21):
        gsac_data.pointers.append(create_pointer_data_info(b'\x01', 15, 11, b'\x00', [[b'\x0A', i, b'\x00'], [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00'], [b'\x0A', 0, b'\x00'],
                                                                                     [b'\x0A', 0, b'\x00'], [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 100, b'\x00'], [b'\x0A', 4294967295, b'\x00'],
                                                                                      [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00'],
                                                                                      [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00']]))
        gsac_data.pointers.append(create_pointer_data_info(b'\x01', 6, 12, b'\x00', [[b'\x0A', i, b'\x00'], [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00'],
                                                                                     [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00'], [b'\x0A', 4294967295, b'\x00']]))
    gsac_header.data = gsac_data
    gscd_header.gsac_array.append(gsac_header)
    # GSAC 4 (WIP)

    # gsdt
    gsdt_header = GsdtHeader()
    gsdt_header.unk0x04 = b'\x10\x00\x00\x00'
    gsdt_header.unk0x0c = b'\x00\x00\x00\x00'

    gscf_header.gshd_header = gshd_header
    gscf_header.gscd_header = gscd_header
    gscf_header.gsdt_header = gsdt_header

    # Store everything in the global class
    GSCEV.gsc_file.gscf_header = gscf_header

    # Enable all signals
    listen_events_logic(main_window, True)


def listen_events_logic(main_window, flag):

    if flag:
        # GSAC 3
        # Set the map value
        main_window.map_name_value.currentIndexChanged.connect(lambda: on_map_changed(main_window))
        # Set the music value
        main_window.music_value.valueChanged.connect(lambda: on_music_changed(main_window))

        # Set the number of characters value
        main_window.num_characters_value.valueChanged.connect(lambda: on_num_characters_changed(main_window))
    else:

        try:
            # GSAC 3
            # Set the map value
            main_window.map_name_value.disconnect()
            # Set the music value
            main_window.music_value.disconnect()

            # Set the number of characters value
            main_window.num_characters_value.disconnect()
        except TypeError:
            pass


def open_gsc_file(worker_gscef, end_progress, gsc_path):

    # Clean vars
    gscf_header = GscfHeader()
    gshd_header = GshdHeader()
    gscd_header = GscdHeader()
    gsdt_header = GsdtHeader()

    # Six tasks
    sub_end_progress = end_progress / 6

    with open(gsc_path, mode="rb") as file:

        # Load gscf header
        # Report progress
        worker_gscef.progressText.emit("Loading GSCF header")
        show_progress_value(worker_gscef, sub_end_progress)
        file.seek(4, os.SEEK_CUR)
        gscf_header.unk0x04 = file.read(GSCEV.bytes2Read)
        file.seek(4, os.SEEK_CUR)
        gscf_header.unk0x0c = file.read(GSCEV.bytes2Read)

        # Load gshd header
        worker_gscef.progressText.emit("Loading GSHD header")
        show_progress_value(worker_gscef, sub_end_progress)
        file.seek(4, os.SEEK_CUR)
        gshd_header.unk0x04 = file.read(GSCEV.bytes2Read)
        gshd_header_size = int.from_bytes(file.read(GSCEV.bytes2Read), "little")
        gshd_header.unk0x0c = file.read(GSCEV.bytes2Read)
        gshd_data_index = file.tell()
        file.seek(gshd_header_size + 16, os.SEEK_CUR)

        # Load gscd header
        worker_gscef.progressText.emit("Loading GSCD header")
        show_progress_value(worker_gscef, sub_end_progress)
        file.seek(4, os.SEEK_CUR)
        gscd_header.unk0x04 = file.read(GSCEV.bytes2Read)
        gscd_header_size = int.from_bytes(file.read(GSCEV.bytes2Read), "little")
        gscd_header.unk0x0c = file.read(GSCEV.bytes2Read)
        gscd_data_index = file.tell()
        file.seek(gscd_header_size + 16, os.SEEK_CUR)

        # Load gsdt header
        worker_gscef.progressText.emit("Loading GSDT header")
        show_progress_value(worker_gscef, sub_end_progress)
        file.seek(4, os.SEEK_CUR)
        gsdt_header.unk0x04 = file.read(GSCEV.bytes2Read)
        file.seek(4, os.SEEK_CUR)
        gsdt_header.unk0x0c = file.read(GSCEV.bytes2Read)
        gstd_data_index = file.tell()

        # Load gshd data
        worker_gscef.progressText.emit("Loading GSHD data")
        show_progress_value(worker_gscef, sub_end_progress)
        file.seek(gshd_data_index)
        number_of_bytes_gshd_header_readed = 0
        while number_of_bytes_gshd_header_readed < gshd_header_size:
            number_of_bytes_gshd_header_readed = read_pointer_data_info(file, number_of_bytes_gshd_header_readed, gstd_data_index, gshd_header.data.pointers)

        # Load gscd data
        worker_gscef.progressText.emit("Loading GSCD data")
        show_progress_value(worker_gscef, sub_end_progress)
        file.seek(gscd_data_index)
        number_of_bytes_gsac_header_readed = 0
        while number_of_bytes_gsac_header_readed < gscd_header_size:
            # Load each gsac header inside the gscd header
            gsac_header = GsacHeader()

            file.seek(4, os.SEEK_CUR)
            gsac_header.unk0x04 = file.read(GSCEV.bytes2Read)
            gsac_header_size = int.from_bytes(file.read(GSCEV.bytes2Read), "little")
            gsac_header.id = int.from_bytes(file.read(GSCEV.bytes2Read), "little")
            number_of_bytes_gsac_header_readed += 16

            # Load each pointer inside the gsac header
            gsac_data = GsacData()
            number_of_bytes_gsac_data_readed = 0
            while number_of_bytes_gsac_data_readed < gsac_header_size:
                number_of_bytes_gsac_data_readed = read_pointer_data_info(file, number_of_bytes_gsac_data_readed, gstd_data_index, gsac_data.pointers)

            # Avoid the EOFC tag
            file.seek(16, os.SEEK_CUR)
            number_of_bytes_gsac_header_readed += number_of_bytes_gsac_data_readed + 16

            # Append each gsac header into the gscd header
            gsac_header.data = gsac_data
            gscd_header.gsac_array.append(gsac_header)

    # Create the class where we will store all the data
    gscf_header.gshd_header = gshd_header
    gscf_header.gscd_header = gscd_header
    gscf_header.gsdt_header = gsdt_header
    GSCEV.gsc_file.gscf_header = gscf_header


def save_gsc_file(worker_gscef, end_progress, gsc_path):

    # Four tasks
    sub_end_progress = end_progress / 4

    # Create eofc header
    eofc_header = b'EOFC' + b'\x10\x00\x00\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00'

    # Prepare gstd header vars. We will store the gstd data by writting the gshd and gsac data entries
    gsdt_data = b''
    gsdt_data_size = 0
    gsdt_data_array = []
    gsdt_data_array_size = 0

    # Create gshd header
    worker_gscef.progressText.emit("Writing GSHD header")
    show_progress_value(worker_gscef, sub_end_progress)
    gshd_data = b''
    gshd_data_size = 0
    # Write each pointer_data_info from gshd header
    for pointer_data_info in GSCEV.gsc_file.gscf_header.gshd_header.data.pointers:
        gshd_data, gshd_data_size, gsdt_data, gsdt_data_size, gsdt_data_array_size = write_pointer_data_info(pointer_data_info, gshd_data, gshd_data_size, gsdt_data, gsdt_data_size,
                                                                                                             gsdt_data_array, gsdt_data_array_size)
    # Check if the data, the module of 16 is 0 before writing
    gshd_data, gshd_data_size, _ = check_entry_module(gshd_data, gshd_data_size, 16)
    gshd_header = b'GSHD' + GSCEV.gsc_file.gscf_header.gshd_header.unk0x04 + gshd_data_size.to_bytes(4, 'little') + GSCEV.gsc_file.gscf_header.gshd_header.unk0x0c
    gshd = gshd_header + gshd_data + eofc_header

    # Create gscd header
    worker_gscef.progressText.emit("Writing GSCD header")
    show_progress_value(worker_gscef, sub_end_progress)
    gscd_data = b''
    gscd_data_size = 0
    # Create gsac header
    for gsac in GSCEV.gsc_file.gscf_header.gscd_header.gsac_array:
        gsac_data = b''
        gsac_data_size = 0
        for pointer_data_info in gsac.data.pointers:
            gsac_data, gsac_data_size, gsdt_data, gsdt_data_size, gsdt_data_array_size = write_pointer_data_info(pointer_data_info, gsac_data, gsac_data_size, gsdt_data, gsdt_data_size,
                                                                                                                 gsdt_data_array, gsdt_data_array_size)

        # Check if the data, the module of 16 is 0 before writing
        gsac_data, gsac_data_size, _ = check_entry_module(gsac_data, gsac_data_size, 16)

        # Store the gsac
        gsac_header = b'GSAC' + gsac.unk0x04 + gsac_data_size.to_bytes(4, 'little') + gsac.id.to_bytes(4, 'little')
        gsac = gsac_header + gsac_data + eofc_header

        # Store each gsac inside the gscd
        gscd_data += gsac
        gscd_data_size += 16 + gsac_data_size + 16
    # Store the gscd
    gscd_header = b'GSCD' + GSCEV.gsc_file.gscf_header.gscd_header.unk0x04 + gscd_data_size.to_bytes(4, 'little') + GSCEV.gsc_file.gscf_header.gscd_header.unk0x0c
    gscd = gscd_header + gscd_data + eofc_header

    # Store the gsdt
    worker_gscef.progressText.emit("Writing GSDT header")
    show_progress_value(worker_gscef, sub_end_progress)
    # Check if the data, the module of 16 is 0 before writing
    gsdt_data, gsdt_data_size, _ = check_entry_module(gsdt_data, gsdt_data_size, 16)
    gsdt_header = b'GSDT' + GSCEV.gsc_file.gscf_header.gsdt_header.unk0x04 + gsdt_data_size.to_bytes(4, 'little') + GSCEV.gsc_file.gscf_header.gsdt_header.unk0x0c
    gsdt = gsdt_header + gsdt_data + eofc_header

    # Create gscf
    worker_gscef.progressText.emit("Writing GSCF header")
    show_progress_value(worker_gscef, sub_end_progress)
    gscf_data = gshd + gscd + gsdt
    gscf_data_size = 16 + gshd_data_size + 16 + 16 + gscd_data_size + 16 + 16 + gsdt_data_size + 16
    gscf_header = b'GSCF' + GSCEV.gsc_file.gscf_header.unk0x04 + gscf_data_size.to_bytes(4, 'little') + GSCEV.gsc_file.gscf_header.unk0x0c
    gscf = gscf_header + gscf_data + eofc_header

    with open(gsc_path, mode="wb") as output_file:
        output_file.write(gscf)
