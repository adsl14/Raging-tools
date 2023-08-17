class GscdHeader:

    def __init__(self):
        self.unk0x04 = b'\x10\x00\x00\x00'
        self.unk0x0c = b'\x01\x00\x00\x00'
        self.gsac_array = []  # array of gsac headers
