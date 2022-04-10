class Tx2dInfo:

    def __init__(self):
        self.unk0x00 = 0
        self.data_offset = 0
        self.unk0x08 = 0
        self.data_size = 0
        self.width = 0
        self.height = 0
        self.unk0x14 = 1
        self.mip_maps = 0
        self.unk0x18 = 0
        self.unk0x1c = 0
        self.dxt_encoding = 0

        # TX2D_VRAM
        self.tx2d_vram = None
