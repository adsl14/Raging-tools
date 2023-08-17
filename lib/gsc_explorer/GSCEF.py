import struct

from lib.functions import show_progress_value, check_entry_module
from lib.gsc_explorer.classes.GSAC.GSACData import GsacData
from lib.gsc_explorer.classes.GSAC.GSACHeader import GsacHeader
from lib.gsc_explorer.classes.GSAC.PointerData import PointerData
from lib.gsc_explorer.classes.GSAC.PointerDataInfo import PointerDataInfo
from lib.gsc_explorer.classes.GSCD.GSCDHeader import GscdHeader
from lib.gsc_explorer.classes.GSCF.GSCFHeader import GscfHeader
from lib.gsc_explorer.classes.GSDT.GSDTHeader import GsdtHeader
from lib.gsc_explorer.classes.GSHD.GSHDHeader import GshdHeader
from lib.gsc_explorer.functions.auxiliary import search_data_in_gsdt
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

        # Save gsc file
        save_gsc_file(self.gsc_file_path)

        # Finish the thread
        self.finished.emit()


def open_gsc_file(worker_gscef, end_progress, gsc_path):

    # Clean vars
    gscf_header = GscfHeader()
    gshd_header = GshdHeader()
    gscd_header = GscdHeader()
    gsdt_header = GsdtHeader()

    # Four tasks
    sub_end_progress = end_progress / 4

    with open(gsc_path, mode="rb") as file:

        # Load gscf header
        # Report progress
        worker_gscef.progressText.emit("Loading GSCF")
        show_progress_value(worker_gscef, sub_end_progress)
        file.seek(4, os.SEEK_CUR)
        gscf_header.unk0x04 = file.read(GSCEV.bytes2Read)
        file.seek(4, os.SEEK_CUR)
        gscf_header.unk0x0c = file.read(GSCEV.bytes2Read)

        # Load gshd header
        # Report progress
        worker_gscef.progressText.emit("Loading GSHD")
        show_progress_value(worker_gscef, sub_end_progress)
        file.seek(4, os.SEEK_CUR)
        gshd_header.unk0x04 = file.read(GSCEV.bytes2Read)
        gshd_header_size = int.from_bytes(file.read(GSCEV.bytes2Read), "little")
        gshd_header.unk0x0c = file.read(GSCEV.bytes2Read)
        gshd_header.data = file.read(gshd_header_size)
        # Avoid eofc tag
        file.seek(16, os.SEEK_CUR)

        # Load gscd header
        # Report progress
        worker_gscef.progressText.emit("Loading GSCD")
        show_progress_value(worker_gscef, sub_end_progress)
        file.seek(4, os.SEEK_CUR)
        gscd_header.unk0x04 = file.read(GSCEV.bytes2Read)
        gscd_header_size = int.from_bytes(file.read(GSCEV.bytes2Read), "little")
        gscd_header.unk0x0c = file.read(GSCEV.bytes2Read)
        gstd_start_data_index = file.tell() + gscd_header_size + 16 + 16

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
                pointer_data_info = PointerDataInfo()
                pointer_data_info.type = file.read(1)
                pointer_data_info.number_of_pointers = int.from_bytes(file.read(1), "little")
                pointer_data_info.secundary_number_of_pointers = int.from_bytes(file.read(1), "little")
                pointer_data_info.unk0x04 = file.read(1)
                number_of_bytes_gsac_data_readed += 4

                # Load each pointer_data inside the pointer_data_info (only the ones that are a pointer)
                if pointer_data_info.type != b'\x00':

                    # Pointers that are not 08 in their first byte, means the number of pointers_data is in the second byte
                    if pointer_data_info.type != b'\x08':
                        for i in range(0, pointer_data_info.number_of_pointers):
                            # Read value
                            aux_pointer = file.tell()
                            pointer_data = PointerData()
                            pointer_data.type_GSDT = file.read(1)
                            block_gstd_index = int.from_bytes(file.read(2), 'little')
                            pointer_data.unk0x03 = file.read(1)
                            file.seek(gstd_start_data_index + (block_gstd_index * 4))
                            # Check if the data we're reading is an integer or float
                            if pointer_data.type_GSDT == b'\x0A':
                                pointer_data.value_GSDT = int.from_bytes(file.read(GSCEV.bytes2Read), "little")
                            else:
                                pointer_data.value_GSDT = struct.unpack('>f', file.read(GSCEV.bytes2Read))[0]
                            file.seek(aux_pointer + 4)

                            # Increase number of bytes readed inside the gsac_data
                            number_of_bytes_gsac_data_readed += 4

                            # Append each pointer data into the pointer data info
                            pointer_data_info.pointers_data.append(pointer_data)

                    # Pointers that are 08 in their first byte, means the number of pointers_data is in the third byte
                    elif pointer_data_info.type == b'\x08':
                        for i in range(0, pointer_data_info.secundary_number_of_pointers):
                            # Read value
                            aux_pointer = file.tell()
                            pointer_data = PointerData()
                            pointer_data.type_GSDT = file.read(1)
                            block_gstd_index = int.from_bytes(file.read(2), 'little')
                            pointer_data.unk0x03 = file.read(1)
                            file.seek(gstd_start_data_index + (block_gstd_index * 4))
                            # Check if the data we're reading is an integer or float
                            if pointer_data.type_GSDT == b'\x0A':
                                pointer_data.value_GSDT = int.from_bytes(file.read(GSCEV.bytes2Read), "little")
                            else:
                                pointer_data.value_GSDT = struct.unpack('>f', file.read(GSCEV.bytes2Read))[0]
                            file.seek(aux_pointer + 4)

                            # Increase number of bytes readed inside the gsac_data
                            number_of_bytes_gsac_data_readed += 4

                            # Append each pointer data into the pointer data info
                            pointer_data_info.pointers_data.append(pointer_data)

                    # Append each pointer data info into the gsac data
                    gsac_data.pointers.append(pointer_data_info)

            # Avoid the EOFC tag
            file.seek(16, os.SEEK_CUR)
            number_of_bytes_gsac_header_readed += number_of_bytes_gsac_data_readed + 16

            # Append each gsac header into the gscd header
            gsac_header.data = gsac_data
            gscd_header.gsac_array.append(gsac_header)

        # Avoid eofc tag
        file.seek(16, os.SEEK_CUR)
        # Load gsdt header
        # Report progress
        worker_gscef.progressText.emit("Loading GSDT")
        show_progress_value(worker_gscef, sub_end_progress)
        file.seek(4, os.SEEK_CUR)
        gsdt_header.unk0x04 = file.read(GSCEV.bytes2Read)
        gsdt_header_size = int.from_bytes(file.read(GSCEV.bytes2Read), "little")
        gsdt_header.unk0x0c = file.read(GSCEV.bytes2Read)

    # Create the class where we will store all the data
    gscf_header.gshd_header = gshd_header
    gscf_header.gscd_header = gscd_header
    gscf_header.gsdt_header = gsdt_header
    GSCEV.gsc_file.gscf_header = gscf_header


def save_gsc_file(gsc_path):

    # Create eofc header
    eofc_header = b'EOFC' + b'\x10\x00\x00\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00'

    # Create gshd header
    gshd_data = GSCEV.gsc_file.gscf_header.gshd_header.data
    gshd_data_size = len(GSCEV.gsc_file.gscf_header.gshd_header.data)
    gshd_header = b'GSHD' + GSCEV.gsc_file.gscf_header.gshd_header.unk0x04 + gshd_data_size.to_bytes(4, 'little') + GSCEV.gsc_file.gscf_header.gshd_header.unk0x0c
    gshd = gshd_header + gshd_data + eofc_header

    # Create gscd and gsdt header
    gscd_data = b''
    gscd_data_size = 0
    gsdt_data = b''
    gsdt_data_size = 0
    gsdt_data_array = []
    gsdt_data_array_size = 0
    # Create gsac header
    for gsac in GSCEV.gsc_file.gscf_header.gscd_header.gsac_array:
        gsac_data = b''
        gsac_data_size = 0
        for pointer_data_info in gsac.data.pointers:

            # Store the pointer_data_info
            if pointer_data_info.type != b'\x00':
                # Store the pointer data info in the gsac_data byte
                gsac_data += pointer_data_info.type + pointer_data_info.number_of_pointers.to_bytes(1, 'little') + pointer_data_info.secundary_number_of_pointers.to_bytes(1, 'little') + \
                             pointer_data_info.unk0x04
                gsac_data_size += 4

            # Store the pointer_data
            for pointer_data in pointer_data_info.pointers_data:

                # Search if the value is in the gsdt array
                index = search_data_in_gsdt(gsdt_data_array, gsdt_data_array_size, pointer_data)

                # We didn't find the value in the gsdt array
                if index is None:
                    gsdt_data_array.append(pointer_data.value_GSDT)
                    index = gsdt_data_array_size
                    gsdt_data_array_size += 1

                    # Store the gsdt data value
                    # Integer value
                    if pointer_data.type_GSDT == b'\x0A':
                        value_gsdt = pointer_data.value_GSDT.to_bytes(4, 'little')
                    else:
                        value_gsdt = struct.pack('>f', pointer_data.value_GSDT)
                    gsdt_data += value_gsdt
                    gsdt_data_size += 4

                # Store the pointer data in the gsac_data byte
                gsac_data += pointer_data.type_GSDT + index.to_bytes(2, 'little') + pointer_data.unk0x03
                gsac_data_size += 4

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
    # Check if the data, the module of 16 is 0 before writing
    gsdt_data, gsdt_data_size, _ = check_entry_module(gsdt_data, gsdt_data_size, 16)
    gsdt_header = b'GSDT' + GSCEV.gsc_file.gscf_header.gsdt_header.unk0x04 + gsdt_data_size.to_bytes(4, 'little') + GSCEV.gsc_file.gscf_header.gsdt_header.unk0x0c
    gsdt = gsdt_header + gsdt_data + eofc_header

    # Create gscf
    gscf_data = gshd + gscd + gsdt
    gscf_data_size = 16 + gshd_data_size + 16 + 16 + gscd_data_size + 16 + 16 + gsdt_data_size + 16
    gscf_header = b'GSCF' + GSCEV.gsc_file.gscf_header.unk0x04 + gscf_data_size.to_bytes(4, 'little') + GSCEV.gsc_file.gscf_header.unk0x0c
    gscf = gscf_header + gscf_data + eofc_header

    with open(gsc_path, mode="wb") as output_file:
        output_file.write(gscf)


