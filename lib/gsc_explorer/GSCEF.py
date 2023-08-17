from lib.functions import show_progress_value, check_entry_module
from lib.gsc_explorer.classes.GSAC.GSACData import GsacData
from lib.gsc_explorer.classes.GSAC.GSACHeader import GsacHeader
from lib.gsc_explorer.classes.GSCD.GSCDHeader import GscdHeader
from lib.gsc_explorer.classes.GSCF.GSCFHeader import GscfHeader
from lib.gsc_explorer.classes.GSDT.GSDTHeader import GsdtHeader
from lib.gsc_explorer.classes.GSHD.GSHDHeader import GshdHeader
from lib.gsc_explorer.functions.auxiliary import read_pointer_data_info, write_pointer_data_info
from lib.packages import os

from PyQt5.QtCore import QObject, pyqtSignal

from lib.gsc_explorer.GSCEV import GSCEV


class WorkerGscef(QObject):

    finished = pyqtSignal()
    progressValue = pyqtSignal(float)
    progressText = pyqtSignal(str)

    main_window = None
    start_progress = 0.0
    end_progress = 100.0
    gsc_file_path = ""

    def load_gsc_file(self):

        # Open gsc file (1 task)
        step_progress = self.end_progress
        open_gsc_file(self, step_progress, self.gsc_file_path)

        # Finish the thread
        self.finished.emit()

    def save_gsc_file(self):

        # Save gsc file (1 task)
        step_progress = self.end_progress
        save_gsc_file(self, step_progress, self.gsc_file_path)

        # Finish the thread
        self.finished.emit()


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
        worker_gscef.progressText.emit("Loading GSCF header")
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
            gsac_header.id = file.read(GSCEV.bytes2Read)
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
        gsac_header = b'GSAC' + gsac.unk0x04 + gsac_data_size.to_bytes(4, 'little') + gsac.id
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
