class GscdHeader:

    def __init__(self):
        self.unk0x04 = b''
        self.unk0x0c = b''
        self.gsac_array = []  # array of gsac headers
